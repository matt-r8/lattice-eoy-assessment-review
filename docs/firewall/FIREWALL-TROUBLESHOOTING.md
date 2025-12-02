# Firewall Troubleshooting Guide

This guide helps diagnose and resolve common issues with the firewall sidecar implementation.

## Table of Contents

1. [Quick Diagnostics](#quick-diagnostics)
2. [Common Issues](#common-issues)
3. [Diagnostic Commands](#diagnostic-commands)
4. [Troubleshooting Flowcharts](#troubleshooting-flowcharts)
5. [Log Analysis](#log-analysis)
6. [Advanced Debugging](#advanced-debugging)

## Quick Diagnostics

Run these commands first to get a quick health check:

```bash
# Check container status
cd /workspaces/XPai/.devcontainer
podman-compose ps

# Check firewall logs
podman logs cui-firewall-manager | tail -50

# Check iptables rules
podman exec cui-firewall-manager iptables -L OUTPUT -n

# Run test suite
/workspaces/XPai/tests/test-firewall.sh
```

## Common Issues

### 1. Containers Won't Start

**Symptoms**:
- `podman-compose up` fails
- Firewall container exits immediately
- AI assistant container won't start

**Diagnosis**:

```bash
# Check container logs
podman logs cui-firewall-manager
podman logs cui-ai-assistant

# Check compose configuration
podman-compose config

# Verify files exist
ls -la /workspaces/XPai/firewall/
```

**Common Causes & Solutions**:

| Cause | Solution |
|-------|----------|
| **Whitelist file not found** | Verify `/workspaces/XPai/firewall/whitelist.txt` exists with correct path |
| **init-firewall.sh not executable** | `chmod 555 /workspaces/XPai/firewall/init-firewall.sh` |
| **Volume mount path incorrect** | Check docker-compose.yml volume paths match actual file locations |
| **NET_ADMIN capability missing** | Verify `cap_add: [NET_ADMIN]` in docker-compose.yml firewall service |
| **Port conflict** | Another container using same ports - stop conflicting containers |

### 2. Firewall Container Unhealthy

**Symptoms**:
- `podman-compose ps` shows firewall as "unhealthy"
- AI assistant won't start (waiting for firewall health)
- Health check keeps failing

**Diagnosis**:

```bash
# Check health check manually
podman exec cui-firewall-manager sh -c \
  "iptables -L OUTPUT -n | grep -q 'policy DROP' && iptables -L OUTPUT -n | grep -q 'dpt:53' && echo OK || echo FAIL"

# Check for iptables errors
podman logs cui-firewall-manager | grep -i error

# Verify kernel modules loaded
podman exec cui-firewall-manager lsmod | grep ip_tables
```

**Common Causes & Solutions**:

| Cause | Solution |
|-------|----------|
| **iptables not installed** | Firewall init script installs iptables - check installation logs |
| **Kernel module not loaded** | Host kernel must support iptables - check `lsmod | grep ip_tables` |
| **Rules not applied** | Check init script logs for errors during rule application |
| **Health check too early** | Wait for `start_period: 10s` - firewall needs time to initialize |
| **DNS tools missing** | Init script installs `bind-tools` - check installation logs |

### 3. Whitelisted Endpoints Blocked

**Symptoms**:
- Cannot connect to whitelisted endpoint
- curl times out to known-good endpoint
- Previously working endpoint now fails

**Diagnosis**:

```bash
# Check whitelist file content
cat /workspaces/XPai/firewall/whitelist.txt

# Verify endpoint is whitelisted
grep "your-endpoint.com" /workspaces/XPai/firewall/whitelist.txt

# Check if firewall resolved the domain
podman logs cui-firewall-manager | grep "your-endpoint.com"

# Check iptables rules for the IP
podman exec cui-firewall-manager iptables -L OUTPUT -n | grep "<resolved-ip>"

# Test DNS resolution from firewall
podman exec cui-firewall-manager nslookup your-endpoint.com

# Test connection from AI container
podman exec cui-ai-assistant curl -v https://your-endpoint.com
```

**Common Causes & Solutions**:

| Cause | Solution |
|-------|----------|
| **Domain not in whitelist** | Add to `firewall/whitelist.txt` and restart containers |
| **Whitelist format error** | Fix format to `domain:port` (no spaces) |
| **DNS resolution failed at startup** | Check firewall logs - restart containers to retry DNS |
| **IP address changed** | Restart containers to re-resolve DNS |
| **Port mismatch** | Verify whitelist port matches actual port (e.g., 443 for HTTPS) |
| **Containers not restarted after whitelist change** | `podman-compose restart` |

### 4. All Traffic Blocked

**Symptoms**:
- Cannot connect to any endpoint (including whitelisted)
- No network connectivity at all
- DNS queries fail

**Diagnosis**:

```bash
# Check if DROP policy applied too early
podman logs cui-firewall-manager | grep -A 10 "[RULES]"

# Verify rule order
podman exec cui-firewall-manager iptables -L OUTPUT -n -v --line-numbers

# Check for rule application errors
podman logs cui-firewall-manager | grep -i error

# Test DNS from AI container
podman exec cui-ai-assistant nslookup google.com
```

**Common Causes & Solutions**:

| Cause | Solution |
|-------|----------|
| **DROP policy set before ACCEPT rules** | Bug in init-firewall.sh - rules must be added before policy |
| **DNS rules not applied** | Check firewall logs - fix init script |
| **Stateful rules missing** | Check for `ESTABLISHED,RELATED` rules in `iptables -L` |
| **Firewall script error** | Review full firewall logs for script errors |

### 5. Firewall Logs Missing

**Symptoms**:
- No [INIT], [WHITELIST], or [RULES] log entries
- Cannot see blocked connection attempts
- Logs are empty

**Diagnosis**:

```bash
# Check container is running
podman ps | grep cui-firewall-manager

# Check logs with timestamps
podman logs --timestamps cui-firewall-manager

# Check if script is executed
podman inspect cui-firewall-manager --format='{{.Config.Cmd}}'

# Try running script manually
podman exec cui-firewall-manager /firewall/init-firewall.sh
```

**Common Causes & Solutions**:

| Cause | Solution |
|-------|----------|
| **Script not executed** | Check `command:` in docker-compose.yml |
| **Script has syntax error** | Run `shellcheck /workspaces/XPai/firewall/init-firewall.sh` |
| **Script fails before logging** | Add `set -x` to init script for detailed tracing |
| **Container exits immediately** | Check for early exit errors - script may be crashing |

### 6. DNS Resolution Slow or Failing

**Symptoms**:
- Firewall takes >30 seconds to start
- "DNS resolution failed" warnings in logs
- Some whitelist entries skipped

**Diagnosis**:

```bash
# Check DNS resolution time
time podman exec cui-firewall-manager dig +short bedrock-runtime.us-gov-east-1.amazonaws.com

# Check DNS server configuration
podman exec cui-firewall-manager cat /etc/resolv.conf

# Test each whitelist entry
while read -r line; do
  [[ "$line" =~ ^[[:space:]]*# ]] && continue
  domain=$(echo "$line" | cut -d: -f1)
  echo "Testing $domain..."
  podman exec cui-firewall-manager dig +short "$domain" A
done < /workspaces/XPai/firewall/whitelist.txt
```

**Common Causes & Solutions**:

| Cause | Solution |
|-------|----------|
| **DNS server unreachable** | Check network connectivity, DNS server configuration |
| **Domain does not exist** | Verify domain spelling, check if service is up |
| **Slow DNS server** | Change DNS server in container or use faster DNS (8.8.8.8) |
| **Too many whitelist entries** | Serial DNS resolution - consider reducing entries |

### 7. Network Namespace Issues

**Symptoms**:
- AI container and firewall have different IPs
- AI container can bypass firewall
- Network isolation not working

**Diagnosis**:

```bash
# Get firewall IP
firewall_ip=$(podman exec cui-firewall-manager ip addr show eth0 | grep "inet " | awk '{print $2}')

# Get AI container IP (should be same)
ai_ip=$(podman exec cui-ai-assistant ip addr show eth0 | grep "inet " | awk '{print $2}' || echo "no eth0")

echo "Firewall IP: $firewall_ip"
echo "AI IP: $ai_ip"

# Check network mode
podman inspect cui-ai-assistant --format='{{.HostConfig.NetworkMode}}'

# Check if AI container has independent network
podman exec cui-ai-assistant ip link show
```

**Common Causes & Solutions**:

| Cause | Solution |
|-------|----------|
| **network_mode not set** | Add `network_mode: "service:firewall-manager"` to ai-assistant in docker-compose.yml |
| **Wrong network mode** | Ensure exact string: `service:firewall-manager` |
| **Containers started out of order** | Restart: `podman-compose down && podman-compose up -d` |
| **Podman version incompatibility** | Update Podman to latest version, check compatibility |

### 8. Excessive Blocked Attempts

**Symptoms**:
- Hundreds of FW-BLOCKED-OUT log entries
- Performance degradation
- Log file growing rapidly

**Diagnosis**:

```bash
# Count blocked attempts by destination
podman logs cui-firewall-manager 2>&1 | \              # Get all logs from firewall container
  grep "FW-BLOCKED-OUT" | \                            # Filter for blocked outbound attempts
  awk '{for(i=1;i<=NF;i++) if($i~/^DST=/) print $i}' | \  # Extract DST= (destination IP) field
  sort | uniq -c | sort -rn | head -20                 # Count occurrences, sort by frequency, show top 20

# Count by port
podman logs cui-firewall-manager 2>&1 | \              # Get all logs from firewall container
  grep "FW-BLOCKED-OUT" | \                            # Filter for blocked outbound attempts
  awk '{for(i=1;i<=NF;i++) if($i~/^DPT=/) print $i}' | \  # Extract DPT= (destination port) field
  sort | uniq -c | sort -rn | head -20                 # Count occurrences, sort by frequency, show top 20

# Check for patterns
podman logs cui-firewall-manager 2>&1 | \
  grep "FW-BLOCKED-OUT" | tail -100
```

**Common Causes & Solutions**:

| Cause | Solution |
|-------|----------|
| **Application trying non-whitelisted service** | Add service to whitelist if legitimate |
| **Background process scanning** | Identify and stop the process |
| **Malware/compromised container** | Investigate the AI container for compromise |
| **Application misconfiguration** | Fix application to use correct endpoints |

## Diagnostic Commands

### Container Status

```bash
# List all containers
podman ps -a

# Check specific container
podman inspect cui-firewall-manager

# Container resource usage
podman stats cui-firewall-manager cui-ai-assistant

# Container processes
podman top cui-firewall-manager
```

### Network Configuration

```bash
# List networks
podman network ls

# Inspect network
podman network inspect <network-name>

# Check container network settings
podman inspect cui-firewall-manager --format='{{json .NetworkSettings}}' | jq

# Show all network interfaces in firewall container
podman exec cui-firewall-manager ip link show

# Show routing table
podman exec cui-firewall-manager ip route show
```

### iptables Rules

```bash
# List all rules
podman exec cui-firewall-manager iptables -L -n -v

# List OUTPUT chain specifically
podman exec cui-firewall-manager iptables -L OUTPUT -n -v --line-numbers

# Show rule packet counters
podman exec cui-firewall-manager iptables -L OUTPUT -n -v -x

# Show raw iptables-save format
podman exec cui-firewall-manager iptables-save
```

### Logs

```bash
# Tail firewall logs in real-time
podman logs -f cui-firewall-manager

# Show logs with timestamps
podman logs --timestamps cui-firewall-manager

# Show last 100 lines
podman logs --tail 100 cui-firewall-manager

# Show logs from specific time
podman logs --since 10m cui-firewall-manager

# Search logs for errors
podman logs cui-firewall-manager 2>&1 | grep -i error

# Export logs
podman logs cui-firewall-manager > firewall-$(date +%Y%m%d-%H%M%S).log
```

### DNS and Connectivity

```bash
# Test DNS from firewall
podman exec cui-firewall-manager nslookup bedrock-runtime.us-gov-east-1.amazonaws.com

# Test DNS from AI container
podman exec cui-ai-assistant nslookup bedrock-runtime.us-gov-east-1.amazonaws.com

# Test HTTPS connectivity
podman exec cui-ai-assistant curl -v https://bedrock-runtime.us-gov-east-1.amazonaws.com

# Test with timeout
podman exec cui-ai-assistant curl --max-time 5 https://example.com

# Test specific port
podman exec cui-ai-assistant nc -zv bedrock-runtime.us-gov-east-1.amazonaws.com 443
```

## Troubleshooting Flowcharts

### Flowchart 1: Container Won't Start

```
[Run podman-compose up -d]
           |
           v
    [Check Logs]
           |
    +------+------+
    |             |
[WHITELIST    [INIT
 NOT FOUND]    ERROR]
    |             |
[Check path]  [Check script]
    |             |
[Fix volume]  [Fix syntax]
    |             |
[Restart]     [Restart]
```

### Flowchart 2: Connection Blocked

```
[Connection Times Out]
           |
           v
[Check if whitelisted]
           |
    +------+------+
    |             |
  [YES]         [NO]
    |             |
    v             v
[Check DNS]   [Add to whitelist]
    |             |
[Resolved?]   [Restart containers]
    |
+---+---+
|       |
[YES]   [NO]
|       |
v       v
[Check  [Fix DNS or
rules]   restart]
|
v
[Rule
exists?]
|
+---+---+
|       |
[YES]   [NO]
|       |
v       v
[IP    [Restart
changed] containers]
```

### Flowchart 3: Health Check Failing

```
[Firewall Unhealthy]
           |
           v
[Check Logs for Errors]
           |
    +------+------+
    |             |
[IPTABLES    [DNS
 ERROR]       ERROR]
    |             |
[Check NET_  [Check
 ADMIN cap]   resolv.conf]
    |             |
[Verify      [Fix DNS]
 kernel]          |
    |         [Restart]
[Install
 module]
    |
[Restart]
```

## Log Analysis

### Successful Initialization Logs

```
[INIT] Starting firewall initialization...
[WHITELIST] Loading whitelist from /firewall/whitelist.txt
[WHITELIST] Parsing whitelist entries...
[WHITELIST] Resolving bedrock-runtime.us-gov-east-1.amazonaws.com...
[WHITELIST] Adding rule for bedrock-runtime.us-gov-east-1.amazonaws.com:443 (52.46.145.72:443)
[WHITELIST] Resolving bedrock.us-gov-east-1.amazonaws.com...
[WHITELIST] Adding rule for bedrock.us-gov-east-1.amazonaws.com:443 (52.222.147.69:443)
[RULES] Flushing existing iptables rules...
[RULES] Setting temporary ACCEPT policies...
[RULES] Adding stateful rules for ESTABLISHED,RELATED connections...
[RULES] Adding DNS rules (port 53)...
[RULES] Adding logging rules for blocked traffic...
[RULES] Setting default DROP policy (deny by default)...
[INIT] Firewall initialization complete
```

### Error Patterns

#### DNS Resolution Failure

```
[WHITELIST] Resolving nonexistent.example.com...
[WARN] DNS resolution failed for nonexistent.example.com. Skipping entry.
```

**Action**: Verify domain exists, check DNS connectivity

#### Whitelist File Missing

```
[ERROR] Whitelist file not found at /firewall/whitelist.txt
```

**Action**: Check volume mount path in docker-compose.yml

#### Invalid Whitelist Format

```
[WARN] Invalid port for entry 'example.com:99999': port must be 1-65535. Skipping.
```

**Action**: Fix whitelist entry format

#### Permission Denied

```
iptables: Operation not permitted
```

**Action**: Verify firewall container has NET_ADMIN capability

## Advanced Debugging

### Enable Script Debugging

Add to init-firewall.sh:

```bash
#!/usr/bin/env sh
set -x  # Enable trace mode
set -euo pipefail
```

Restart container to see detailed script execution.

### Packet Tracing

```bash
# Capture packets on OUTPUT chain
podman exec cui-firewall-manager iptables -A OUTPUT -j TRACE

# View trace logs (requires kernel support)
podman exec cui-firewall-manager cat /sys/kernel/debug/tracing/trace

# Disable trace
podman exec cui-firewall-manager iptables -D OUTPUT -j TRACE
```

### Manual Rule Testing

```bash
# Enter firewall container
podman exec -it cui-firewall-manager /bin/sh

# Manually add test rule
iptables -A OUTPUT -d 1.2.3.4 -p tcp --dport 443 -j ACCEPT

# Test rule
iptables -L OUTPUT -n | grep "1.2.3.4"

# Remove test rule
iptables -D OUTPUT -d 1.2.3.4 -p tcp --dport 443 -j ACCEPT
```

### Container Shell Access

```bash
# Firewall container shell
podman exec -it cui-firewall-manager /bin/sh

# AI container shell
podman exec -it cui-ai-assistant /bin/bash

# Run commands interactively
podman exec -it cui-firewall-manager sh -c "iptables -L -n; ip addr; ip route"
```

### Recreate Containers from Scratch

```bash
# Stop and remove everything
podman-compose down -v

# Remove images (optional - forces fresh pull)
podman rmi alpine:latest
podman rmi ghcr.io/rise8-us/xpai/ai-assistant-home:latest

# Start fresh
podman-compose up -d

# Watch logs
podman-compose logs -f
```

## Getting Help

If issues persist after trying these troubleshooting steps:

1. **Collect Diagnostic Information**:
   ```bash
   # Create diagnostic report
   {
     echo "=== Container Status ==="
     podman ps -a
     echo ""
     echo "=== Firewall Logs ==="
     podman logs cui-firewall-manager 2>&1 | tail -100
     echo ""
     echo "=== AI Container Logs ==="
     podman logs cui-ai-assistant 2>&1 | tail -50
     echo ""
     echo "=== iptables Rules ==="
     podman exec cui-firewall-manager iptables -L -n -v || echo "Cannot get rules"
     echo ""
     echo "=== Whitelist Content ==="
     cat /workspaces/XPai/firewall/whitelist.txt
     echo ""
     echo "=== Test Results ==="
     /workspaces/XPai/tests/test-firewall.sh 2>&1 || echo "Tests failed"
   } > firewall-diagnostic-$(date +%Y%m%d-%H%M%S).txt
   ```

2. **Review Documentation**:
   - [Firewall Architecture](./FIREWALL-ARCHITECTURE.md)
   - [Whitelist Management](./WHITELIST-MANAGEMENT.md)
   - [Feature Specification](../specs/001-firewall-sidecar-implementation/spec.md)

3. **Create GitHub Issue**:
   - Include diagnostic report
   - Describe what you were trying to do
   - What you expected to happen
   - What actually happened
   - Steps to reproduce

## References

- [iptables Debugging Guide](https://www.netfilter.org/documentation/HOWTO/packet-filtering-HOWTO-7.html)
- [Podman Troubleshooting](https://github.com/containers/podman/blob/main/troubleshooting.md)
- [Docker Compose Networking](https://docs.docker.com/compose/networking/)
