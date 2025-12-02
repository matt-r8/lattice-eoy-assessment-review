# Firewall Sidecar Implementation for CUI Compliance

## Overview

**This firewall protection is mandatory for all CUI projects** to meet CMMC Level 2 compliance requirements.

This implementation provides a deny-by-default network firewall for AI assistants operating in Controlled Unclassified Information (CUI) environments. It uses a privileged firewall container with iptables to enforce whitelist-based network access, protecting against data exfiltration via prompt injection attacks.

**Key Security Properties**:
- ✅ **Deny by Default**: Only explicitly whitelisted endpoints are accessible
- ✅ **Zero Capabilities**: AI container has no network privileges (cap_drop: ALL)
- ✅ **Fail-Secure**: Network unavailable if firewall fails
- ✅ **Audit Trail**: All blocked attempts are logged
- ✅ **CMMC Level 2 Compliant**: Meets boundary protection requirements

## Quick Start

### Prerequisites

- **Container Runtime**: Docker or Podman installed
- **Platform**: Linux or macOS (with Podman machine)
- **VSCode**: With Remote-Containers extension (for devcontainer integration)
- **Network Access**: Ability to reach AWS Bedrock endpoints

### Step 1: Navigate to Project

```bash
# Navigate to your project directory
cd /path/to/your/project
```

### Step 2: Review Whitelist

The whitelist contains approved network destinations:

```bash
cat firewall/whitelist.txt
```

Default entries:
- `bedrock-runtime.us-gov-east-1.amazonaws.com:443`
- `bedrock.us-gov-east-1.amazonaws.com:443`

### Step 3: Start Containers

```bash
cd .devcontainer
podman-compose up -d

# Wait for firewall to become healthy (~30 seconds)
watch podman-compose ps
```

Expected output:
```
NAME                    STATUS
cui-firewall-manager    Up (healthy)
cui-ai-assistant        Up
```

### Step 4: Verify Security Properties

Run the automated test suite:

```bash
# Run all security tests
./tests/test-firewall.sh
```

Expected result: All tests pass ✅

### Step 5: Connect with VSCode

1. Open VSCode in project directory
2. Click green "Remote" button (bottom-left)
3. Select "Reopen in Container"
4. Choose `devcontainer.cui.json` configuration (automatically includes firewall protection)
5. VSCode connects to firewall-protected AI assistant

## Architecture

This firewall uses a sidecar container pattern with network namespace sharing to enforce deny-by-default network access control.

For detailed architecture documentation including container design, network flow, iptables rules, and threat model, see [Firewall Architecture](FIREWALL-ARCHITECTURE.md).

## Usage

### Adding a New Whitelist Entry

1. **Edit whitelist locally**:
   ```bash
   cd firewall
   chmod 644 whitelist.txt
   echo "api.newservice.com:443" >> whitelist.txt
   chmod 444 whitelist.txt
   ```

2. **Restart containers**:
   ```bash
   cd .devcontainer
   podman-compose down && podman-compose up -d
   ```

3. **Test connectivity**:
   ```bash
   podman exec cui-ai-assistant curl -v https://api.newservice.com
   ```

4. **Verify firewall security**:
   ```bash
   ./tests/test-firewall.sh
   ```

5. **Promote via pull request** (see [Whitelist Management](WHITELIST-MANAGEMENT.md))

### Viewing Firewall Logs

```bash
# Real-time logs
podman logs -f cui-firewall-manager

# Search for blocked attempts
podman logs cui-firewall-manager 2>&1 | grep "FW-BLOCKED-OUT"

# View iptables rules
podman exec cui-firewall-manager iptables -L OUTPUT -n -v
```

### Troubleshooting

If you encounter issues:

1. **Check container status**: `podman-compose ps`
2. **View logs**: `podman logs cui-firewall-manager`
3. **Run tests**: `./tests/test-firewall.sh`
4. **Consult guide**: [Troubleshooting Guide](FIREWALL-TROUBLESHOOTING.md)

## Testing

To verify the firewall is working correctly:

```bash
./tests/test-firewall.sh
```

Expected result: All tests pass ✅

For detailed testing documentation, see [Firewall Testing Guide](FIREWALL-TESTING.md).

## Security Checklist

After setup, verify these properties:

- [ ] Firewall container has NET_ADMIN capability only
- [ ] AI container has cap_drop: ALL
- [ ] AI container shares firewall's network namespace
- [ ] iptables default policy is DROP
- [ ] Whitelisted endpoints are accessible
- [ ] Non-whitelisted endpoints are blocked
- [ ] Blocked attempts are logged
- [ ] whitelist.txt is read-only (chmod 444)
- [ ] init-firewall.sh is read-only (chmod 555)
- [ ] All tests pass

## Compliance

This firewall implementation meets CMMC Level 2 requirements for CUI projects.

For detailed compliance documentation, audit evidence, and control mappings, see [Firewall Compliance Guide](FIREWALL-COMPLIANCE.md).

## Documentation

- **[Firewall Architecture](FIREWALL-ARCHITECTURE.md)**: Detailed security design
- **[Firewall Compliance](FIREWALL-COMPLIANCE.md)**: CMMC Level 2 requirements and audit evidence
- **[Firewall Testing](FIREWALL-TESTING.md)**: Test suites and validation procedures
- **[Whitelist Management](WHITELIST-MANAGEMENT.md)**: How to manage whitelist entries
- **[Troubleshooting Guide](FIREWALL-TROUBLESHOOTING.md)**: Common issues and solutions

## Known Limitations

1. **DNS-based exfiltration**: DNS queries are allowed (residual risk)
2. **IP address changes**: Requires container restart to re-resolve DNS
3. **No IPv6 support**: Only IPv4 addresses whitelisted
4. **No wildcard domains**: Each domain must be explicitly listed
5. **No content filtering**: HTTPS payload is encrypted (not inspected)

For detailed risk analysis, see [Firewall Compliance Guide](FIREWALL-COMPLIANCE.md).
