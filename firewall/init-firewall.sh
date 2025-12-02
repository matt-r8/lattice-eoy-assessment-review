#!/usr/bin/env sh
# Firewall Initialization Script
# Configures iptables rules for network isolation with whitelist-based access

set -euo pipefail

# Configuration
# RFC-compliant IPv4 address pattern: validates each octet is 0-255
# Pattern breakdown: (25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9]) matches:
#   - 250-255: 25[0-5]
#   - 200-249: 2[0-4][0-9]
#   - 100-199: 1[0-9]{2}
#   - 0-99: [1-9]?[0-9]
IPV4_REGEX='^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$'

WHITELIST_FILE="${WHITELIST_FILE:-/firewall/whitelist.txt}"
LOG_PREFIX_IN="FW-BLOCKED-IN: "
LOG_PREFIX_OUT="FW-BLOCKED-OUT: "
LOG_PREFIX_FWD="FW-BLOCKED-FWD: "

# Logging functions
log_init() {
    echo "[INIT] $*"
}

log_whitelist() {
    echo "[WHITELIST] $*"
}

log_rules() {
    echo "[RULES] $*"
}

log_error() {
    echo "[ERROR] $*" >&2
}

log_warn() {
    echo "[WARN] $*" >&2
}

# Error handling
die() {
    log_error "$*"
    exit 1
}

# Main initialization
main() {
    log_init "Starting firewall initialization..."

    # Check if whitelist file exists
    if [ ! -f "$WHITELIST_FILE" ]; then
        die "Whitelist file not found at $WHITELIST_FILE"
    fi

    log_whitelist "Loading whitelist from $WHITELIST_FILE"

    # Flush existing rules
    log_rules "Flushing existing iptables rules..."
    iptables -F INPUT || true
    iptables -F OUTPUT || true
    iptables -F FORWARD || true

    # Set default policies to ACCEPT temporarily (will change to DROP later)
    log_rules "Setting temporary ACCEPT policies..."
    iptables -P INPUT ACCEPT
    iptables -P OUTPUT ACCEPT
    iptables -P FORWARD ACCEPT

    # Step 1: Add stateful rules (ESTABLISHED,RELATED connections)
    log_rules "Adding stateful rules for ESTABLISHED,RELATED connections..."
    iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
    iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

    # Step 2: Allow localhost/loopback connections (required for VS Code Server)
    log_rules "Adding loopback rules (localhost connections)..."
    iptables -A INPUT -i lo -j ACCEPT
    iptables -A OUTPUT -o lo -j ACCEPT

    # Step 3: Add DNS rules (UDP and TCP port 53)
    log_rules "Adding DNS rules (port 53)..."
    iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
    iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT

    # Step 4: Parse whitelist and add rules for each entry
    log_whitelist "Parsing whitelist entries..."
    while IFS= read -r line || [ -n "$line" ]; do
        # Skip empty lines
        [ -z "$line" ] && continue

        # Skip comments (lines starting with #)
        case "$line" in
            \#*|\ *\#*|"	"*\#*) continue ;;
        esac

        # Parse domain:port
        domain=$(echo "$line" | cut -d: -f1 | tr -d '[:space:]')
        port=$(echo "$line" | cut -d: -f2 | tr -d '[:space:]')

        # Validate port range (1-65535)
        if ! echo "$port" | grep -qE '^[0-9]+$' || [ "$port" -lt 1 ] || [ "$port" -gt 65535 ]; then
            log_warn "Invalid port for entry '$line': port must be 1-65535. Skipping."
            continue
        fi

        # Validate domain format (basic check)
        if ! echo "$domain" | grep -qE '^[a-zA-Z0-9.-]+$'; then
            log_warn "Invalid domain format for entry '$line'. Skipping."
            continue
        fi

        # Resolve domain to IP(s)
        log_whitelist "Resolving $domain..."
        ips=$(dig +short "$domain" A | grep -E "$IPV4_REGEX" || true)

        if [ -z "$ips" ]; then
            log_warn "DNS resolution failed for $domain. Skipping entry."
            continue
        fi

        # Add iptables rule for each resolved IP
        for ip in $ips; do
            log_whitelist "Adding rule for $domain:$port ($ip:$port)"
            iptables -A OUTPUT -d "$ip" -p tcp --dport "$port" -j ACCEPT
        done

    done < "$WHITELIST_FILE"

    # Step 5: Add logging rules (before DROP policy)
    log_rules "Adding logging rules for blocked traffic..."
    iptables -A INPUT -j LOG --log-prefix "$LOG_PREFIX_IN" --log-level 4
    iptables -A OUTPUT -j LOG --log-prefix "$LOG_PREFIX_OUT" --log-level 4
    iptables -A FORWARD -j LOG --log-prefix "$LOG_PREFIX_FWD" --log-level 4

    # Step 6: Set default DROP policy (deny by default)
    log_rules "Setting default DROP policy (deny by default)..."
    iptables -P INPUT DROP
    iptables -P OUTPUT DROP
    iptables -P FORWARD DROP

    log_init "Firewall initialization complete"

    # Display final rules for verification
    log_init "Current iptables rules:"
    iptables -L -n -v
}

# Run main function
main "$@"
