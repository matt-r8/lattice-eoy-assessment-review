# Firewall Whitelist Management

This document describes how to manage the firewall whitelist for the AI assistant firewall sidecar implementation.

## Overview

The firewall whitelist (`firewall/whitelist.txt`) controls which external endpoints the AI assistant can access. It uses a deny-by-default security model where only explicitly whitelisted domains are accessible.

## Whitelist Format

### Entry Format

Each whitelist entry follows the format:
```
domain:port
```

**Example**:
```
bedrock-runtime.us-gov-east-1.amazonaws.com:443
```

### Rules

1. **One entry per line**: Each domain:port combination must be on its own line
2. **Comments**: Lines starting with `#` are treated as comments
3. **Empty lines**: Empty lines are ignored
4. **No spaces**: Do not include spaces in entries (except in comments)
5. **Valid ports**: Ports must be between 1-65535
6. **Valid domains**: Domains must be valid FQDNs (alphanumeric, hyphens, dots)

### Valid Examples

```
# AWS Bedrock endpoints (us-gov-east-1)
bedrock-runtime.us-gov-east-1.amazonaws.com:443
bedrock.us-gov-east-1.amazonaws.com:443

# Additional services
api.example.com:8443
service.company.com:443
```

### Invalid Examples

```
# These will be rejected or skipped:
example.com                          # Missing port
example.com:443:extra               # Multiple colons
example.com: 443                    # Space after colon
example.com:99999                   # Invalid port range
-example.com:443                    # Invalid domain (starts with hyphen)
```

## Local Testing Workflow

When you need to test a new service that requires network access:

### Step 1: Edit Whitelist Locally

```bash
# Navigate to firewall directory
cd /workspaces/XPai/firewall

# Edit whitelist.txt (requires changing permissions temporarily)
chmod 644 whitelist.txt

# Add your new entry
echo "api.newservice.com:443" >> whitelist.txt

# Restore read-only permissions
chmod 444 whitelist.txt
```

### Step 2: Restart Containers

The firewall resolves domains to IPs at startup, so you must restart the containers for changes to take effect:

```bash
# Navigate to devcontainer directory
cd /workspaces/XPai/.devcontainer

# Stop containers
podman-compose down

# Start containers (firewall will reload whitelist)
podman-compose up -d

# Wait for firewall to become healthy (10-30 seconds)
podman-compose ps
```

### Step 3: Test Connectivity

```bash
# Enter the AI assistant container
podman exec -it cui-ai-assistant /bin/bash

# Test the newly whitelisted endpoint
curl -v https://api.newservice.com

# Expected: Connection succeeds (HTTP response received)
```

### Step 4: Verify Firewall Logs

```bash
# Check firewall logs to confirm the new rule was added
podman logs cui-firewall-manager | grep "api.newservice.com"
```

Expected output:
```
[WHITELIST] Resolving api.newservice.com...
[WHITELIST] Adding rule for api.newservice.com:443 (93.184.216.34:443)
```

### Step 5: Run Integration Tests

```bash
# Run full firewall test suite
./tests/test-firewall.sh
```

## Git PR Workflow (Promoting Changes)

Once you've tested the whitelist changes locally and verified they work, promote them to the team via pull request:

### Step 1: Create Feature Branch

```bash
# Create a branch for your whitelist change
git checkout -b feature/whitelist-add-newservice

# Stage whitelist changes
git add firewall/whitelist.txt
```

### Step 2: Commit with Descriptive Message

```bash
git commit -m "firewall: add api.newservice.com to whitelist

Adds api.newservice.com:443 to firewall whitelist to enable
integration with NewService API.

Tested locally:
- Whitelist format validation passed
- Container restart successful
- Connectivity to api.newservice.com verified
- Integration tests passed

Rationale: Required for [FEATURE-123] NewService integration"
```

### Step 3: Push and Create Pull Request

```bash
# Push to remote
git push origin feature/whitelist-add-newservice

# Create pull request using GitHub CLI
gh pr create \
  --title "firewall: add api.newservice.com to whitelist" \
  --body "Adds api.newservice.com:443 to enable NewService integration.

## Testing
- ✅ Local whitelist validation passed
- ✅ Container restart successful
- ✅ Connectivity verified
- ✅ Integration tests passed

## Security Review
Required for CMMC compliance - security team review needed.

Closes #123"
```

### Step 4: Security Team Review

The `.github/CODEOWNERS` file designates the security team as required reviewers for `firewall/whitelist.txt` changes. Your PR will automatically request their review.

**Security team will verify**:
1. Business justification for the new endpoint
2. Endpoint is HTTPS (port 443) when possible
3. Domain belongs to trusted service
4. No overly broad wildcards (not supported, but good to check for attempts)
5. Test evidence provided

### Step 5: Merge and Deploy

Once approved:

```bash
# Merge via GitHub UI or CLI
gh pr merge --squash

# Other team members pull changes
git pull origin main

# Restart their containers to apply new whitelist
cd .devcontainer && podman-compose restart
```

## Removing Whitelist Entries

To remove an endpoint from the whitelist:

### Step 1: Edit Whitelist

```bash
# Edit whitelist.txt
chmod 644 firewall/whitelist.txt

# Remove or comment out the entry
# Before:
# api.oldservice.com:443

# After:
# Removed 2025-10-15: Service decommissioned
# api.oldservice.com:443

chmod 444 firewall/whitelist.txt
```

### Step 2: Test and Verify Blocking

```bash
# Restart containers
cd .devcontainer && podman-compose down && podman-compose up -d

# Verify the endpoint is now blocked
podman exec cui-ai-assistant curl --max-time 5 https://api.oldservice.com

# Expected: Connection timeout or refused
```

### Step 3: Follow Git PR Workflow

Same as adding entries - create branch, commit, PR, get security review, merge.

## Troubleshooting

### Problem: Whitelist changes not taking effect

**Symptoms**: Added endpoint still blocked after edit

**Diagnosis**:
```bash
# Check if firewall loaded the new entry
podman logs cui-firewall-manager | grep "newservice"

# Check iptables rules
podman exec cui-firewall-manager iptables -L OUTPUT -n | grep "newservice_ip"
```

**Solution**:
```bash
# Ensure you restarted containers
podman-compose down && podman-compose up -d

# Wait for health check
watch podman-compose ps
```

### Problem: DNS resolution fails for whitelist entry

**Symptoms**: Firewall logs show "DNS resolution failed"

**Diagnosis**:
```bash
# Check firewall logs
podman logs cui-firewall-manager | grep "DNS resolution failed"

# Test DNS from firewall container
podman exec cui-firewall-manager nslookup problematic-domain.com
```

**Solution**:
1. Verify domain is correct (no typos)
2. Check network connectivity
3. If domain has no A records, contact service provider
4. Remove entry from whitelist if domain is invalid

### Problem: Whitelist format issues

**Symptoms**: Firewall logs show warnings about invalid entries

**Diagnosis**:
```bash
# Check firewall logs for warnings
podman logs cui-firewall-manager | grep WARN
```

**Common issues**:
- **Invalid port**: Port must be 1-65535
- **Invalid format**: Must be `domain:port` (no spaces)
- **Duplicate entries**: Remove duplicates
- **Invalid domain**: Check for typos, invalid characters

**Solution**: Fix the reported issues in whitelist.txt and restart containers

### Problem: Firewall container fails health check

**Symptoms**: `podman-compose ps` shows firewall as "unhealthy"

**Diagnosis**:
```bash
# Check health check logs
podman logs cui-firewall-manager 2>&1 | tail -50

# Manually run health check command
podman exec cui-firewall-manager sh -c \
  "iptables -L OUTPUT -n | grep -q 'policy DROP' && echo OK || echo FAIL"
```

**Solution**:
1. Check for errors in firewall initialization logs
2. Verify whitelist.txt is accessible (`podman exec cui-firewall-manager cat /firewall/whitelist.txt`)
3. Verify iptables rules were applied (`podman exec cui-firewall-manager iptables -L -n`)

## Performance Considerations

### Restart Time

- **Expected**: Container restart takes <1 minute
- **DNS resolution**: ~1-2 seconds per entry
- **iptables rules**: ~100ms per entry
- **Total for 10 entries**: ~30-45 seconds

### Large Whitelists

If you have more than 50 entries:
1. Consider grouping by service (comments for organization)
2. Be aware of DNS lookup time during initialization
3. Monitor firewall initialization logs for slow DNS queries

### IP Address Changes

Whitelisted domains are resolved to IPs at firewall startup. If a service's IP changes:

1. **Symptoms**: Previously working endpoint now blocked
2. **Diagnosis**: Check firewall logs for resolved IP vs actual IP
3. **Solution**: Restart containers to re-resolve DNS

```bash
# Quick restart
cd .devcontainer && podman-compose restart firewall-manager
```

## CODEOWNERS Configuration

Create `.github/CODEOWNERS` to enforce security team review:

```
# Firewall whitelist requires security team approval
/firewall/whitelist.txt @your-org/security-team
```

This ensures all whitelist changes are reviewed by security before merging.

## Best Practices

1. **Test locally first**: Always test changes in your local environment before creating a PR
2. **Run integration tests**: Use `./tests/test-firewall.sh` to verify security properties
3. **Descriptive commits**: Explain why the endpoint is needed
4. **Security justification**: Include business reason for whitelisting
5. **Monitor logs**: Check firewall logs after changes
6. **Document removals**: Comment out removed entries with date and reason
7. **Review regularly**: Periodically audit whitelist for unused entries
8. **Use HTTPS**: Prefer port 443 (HTTPS) over HTTP for security
9. **Minimize entries**: Only whitelist what's necessary
10. **Group related entries**: Use comments to organize by service or purpose

## Examples

### Example 1: Adding AWS Service Endpoint

```bash
# Add to whitelist.txt
echo "# S3 endpoint for artifact storage" >> firewall/whitelist.txt
echo "s3.us-gov-east-1.amazonaws.com:443" >> firewall/whitelist.txt
```

### Example 2: Adding Multiple Related Endpoints

```bash
# Add to whitelist.txt
cat >> firewall/whitelist.txt <<EOF

# GitHub API for repository access
api.github.com:443
github.com:443
EOF
```

### Example 3: Temporarily Disabling an Entry

```bash
# Comment out instead of deleting
# old-api.service.com:443  # Disabled 2025-10-15: Migrating to new-api.service.com
new-api.service.com:443
```

## Security Considerations

### Threat Model

The whitelist protects against:
- **Prompt injection → data exfiltration**: Attacker cannot exfiltrate data to non-whitelisted endpoints
- **Compromised AI model**: Even if model is compromised, network access is restricted
- **Accidental data leaks**: Only approved endpoints can receive data

### What the Whitelist Does NOT Protect Against

- **Content of requests**: Firewall inspects destination only, not payload
- **Malicious responses**: Whitelisted endpoints could return malicious content
- **Application-layer attacks**: Firewall works at network layer only

### Compliance

This whitelist-based firewall helps satisfy:
- **CMMC Level 2 SC.L2-3.13.6**: Deny network communications traffic by default; allow network communications traffic by exception
- **CMMC Level 2 SC.L2-3.13.1**: Monitor and control communications at external system boundaries and key internal boundaries

## References

- [Firewall Architecture Documentation](./FIREWALL-ARCHITECTURE.md)
- [Firewall Troubleshooting Guide](./FIREWALL-TROUBLESHOOTING.md)
- [Feature Specification](../specs/001-firewall-sidecar-implementation/spec.md)
- [Test Scripts](../tests/)
