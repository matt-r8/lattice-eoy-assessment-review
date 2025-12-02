# Firewall Compliance Documentation

## CMMC Level 2 Compliance

This firewall implementation helps satisfy the following CMMC Level 2 requirements for CUI projects:

### Requirements Mapping

| Requirement | Control | Implementation |
|-------------|---------|----------------|
| **SC.L2-3.13.6** | Deny by default, allow by exception | iptables DROP policy with whitelist |
| **SC.L2-3.13.1** | Boundary protection | Firewall at container network boundary |
| **AC.L2-3.1.20** | Least privilege | AI container: cap_drop: ALL |

### Control Details

#### SC.L2-3.13.6: Deny by Default, Allow by Exception

**Requirement**: "Deny network communications traffic by default and allow network communications traffic by exception (i.e., deny all, permit by exception)."

**Implementation**:
- iptables default OUTPUT policy set to DROP
- Only explicitly whitelisted endpoints are ACCEPT rules
- All non-whitelisted traffic is logged and dropped

**Verification**:
```bash
# View iptables rules showing DROP policy
podman exec cui-firewall-manager iptables -L OUTPUT -v -n

# Test that non-whitelisted domains are blocked
podman exec cui-ai-assistant curl --max-time 5 https://example.com
# Expected: Connection timeout
```

#### SC.L2-3.13.1: Boundary Protection

**Requirement**: "Monitor, control, and protect organizational communications (i.e., information transmitted or received by organizational information systems) at the external boundaries and key internal boundaries of the information systems."

**Implementation**:
- Network namespace boundary between AI container and external networks
- All outbound traffic passes through firewall container
- Firewall logs all blocked connection attempts
- Container cannot bypass firewall due to shared network namespace

**Verification**:
```bash
# Verify AI container uses firewall's network namespace
podman inspect cui-ai-assistant --format='{{.HostConfig.NetworkMode}}'
# Expected: container:cui-firewall-manager

# View blocked connection logs
podman logs cui-firewall-manager 2>&1 | grep "FW-BLOCKED-OUT"
```

#### AC.L2-3.1.20: Least Privilege

**Requirement**: "Authorize access to security functions and security-relevant information."

**Implementation**:
- AI container has ALL capabilities dropped (cap_drop: ALL)
- AI container cannot modify network rules
- Only firewall container has CAP_NET_ADMIN (minimum required for iptables)
- No privileged containers

**Verification**:
```bash
# Verify AI container has no capabilities
podman inspect cui-ai-assistant --format='{{.HostConfig.CapDrop}}'
# Expected: [ALL]

# Verify firewall has only NET_ADMIN
podman inspect cui-firewall-manager --format='{{.HostConfig.CapAdd}}'
# Expected: [NET_ADMIN]
```

## Audit Evidence

Compliance auditors can verify the following:

### 1. Configuration Files (Version Controlled)

**Location**: `firewall/` directory

**Files**:
- `whitelist.txt` - Approved network destinations (read-only, chmod 444)
- `init-firewall.sh` - Firewall initialization script (read-only, chmod 555)

**Audit Trail**:
- All changes tracked in Git
- Pull request review required (see `.github/CODEOWNERS.example`)
- Change history available via `git log firewall/`

### 2. Container Configuration

**Location**: `.devcontainer/docker-compose.firewall.yml`

**Security Controls**:
```yaml
# Firewall container
cap_add:
  - NET_ADMIN  # Only capability needed for iptables
security_opt:
  - no-new-privileges:true

# AI assistant container
cap_drop:
  - ALL  # Zero capabilities
network_mode: "service:firewall"  # Uses firewall's network
security_opt:
  - no-new-privileges:true
```

### 3. Runtime Verification

**Firewall Logs**:
```bash
# View blocked connection attempts
podman logs cui-firewall-manager 2>&1 | grep "FW-BLOCKED-OUT"
```

**Test Results**:
```bash
# Run security validation suite
./tests/test-firewall.sh
```

All tests must pass to demonstrate:
- Deny-by-default enforcement
- Whitelist-only access
- Zero capabilities on AI container
- Proper network isolation

### 4. Documentation

**Evidence Package**:
- Security architecture: `docs/firewall/FIREWALL-ARCHITECTURE.md`
- Implementation details: `docs/firewall/README-FIREWALL.md`
- Troubleshooting procedures: `docs/firewall/FIREWALL-TROUBLESHOOTING.md`
- Whitelist management process: `docs/firewall/WHITELIST-MANAGEMENT.md`
- Test procedures: `docs/firewall/FIREWALL-TESTING.md`

## Residual Risks

The following limitations are accepted trade-offs:

1. **DNS-based exfiltration**: DNS queries (port 53) are allowed for name resolution. Mitigated by:
   - Using trusted DNS servers only
   - Monitoring DNS query volume
   - Short data exfiltration via DNS is impractical for CUI volumes

2. **HTTPS content inspection**: HTTPS payloads are encrypted and not inspected. Mitigated by:
   - Whitelist controls destination domains
   - AWS Bedrock endpoints are trusted
   - Prompt injection attacks are limited by destination whitelist

3. **IPv6 traffic**: Only IPv4 addresses are whitelisted. Mitigated by:
   - AWS Bedrock uses IPv4
   - IPv6 is not required for CUI operations

## References

- [CMMC Level 2 Requirements](https://www.acq.osd.mil/cmmc/)
- [NIST SP 800-171 Rev 2](https://csrc.nist.gov/publications/detail/sp/800-171/rev-2/final)
- [iptables Documentation](https://www.netfilter.org/documentation/)
- [Linux Capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html)
