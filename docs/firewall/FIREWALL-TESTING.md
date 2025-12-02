# Firewall Testing Documentation

## Overview

This document describes the test suites available for validating the firewall implementation.

## Quick Test

To run all tests:

```bash
# Test with default "test" project name
./tests/test-firewall.sh

# Test a specific project
./tests/test-firewall.sh my-project-name
```

Expected result: All tests pass ✅

## Test Suite

### Integration Tests (Self-Managing)

**Purpose**: Validates actual firewall behavior with running containers

**Prerequisites**:
- Docker or Podman installed and running
- `podman-compose` or `docker-compose` installed

**Command**:
```bash
./tests/test-firewall.sh
```

**How it works**: The test script automatically:
1. Starts containers using `docker-compose.firewall.yml` with specified PROJECT_NAME
2. Runs all integration tests
3. Cleans up containers on exit (even if tests fail)

This ensures tests validate the exact same configuration as production deployment.

**Multi-Project Testing:**
```bash
# Test default "test" project (containers: test-firewall-manager, test-ai-assistant)
./tests/test-firewall.sh

# Test specific project (containers: alpha-firewall-manager, alpha-ai-assistant)
./tests/test-firewall.sh alpha
```

**Note**: If containers with the specified PROJECT_NAME already exist, tests will use them. To test with fresh containers:
```bash
cd .devcontainer && PROJECT_NAME=test podman-compose down && cd .. && ./tests/test-firewall.sh
```

**Validates**:
- Containers are running
- Firewall container is healthy
- Whitelisted endpoints are accessible
- Non-whitelisted endpoints are blocked
- AI container has zero capabilities
- Blocked attempts are logged
- Network namespace is shared

**Example Output**:
```
✅ Firewall container is running and healthy
✅ AI container is running
✅ Whitelisted endpoint accessible (bedrock-runtime.us-gov-east-1.amazonaws.com)
✅ Non-whitelisted endpoint blocked (example.com)
✅ AI container has no capabilities (cap_drop: ALL)
✅ Blocked attempts are logged
✅ Network namespace properly shared
```

## Manual Testing

### Test Whitelisted Access

Verify that whitelisted endpoints are accessible:

```bash
podman exec cui-ai-assistant curl -v https://bedrock-runtime.us-gov-east-1.amazonaws.com
```

**Expected**: Connection succeeds, HTTP response received

### Test Blocked Access

Verify that non-whitelisted endpoints are blocked:

```bash
podman exec cui-ai-assistant curl --max-time 5 https://example.com
```

**Expected**: Connection times out or fails immediately

### Verify Zero Capabilities

Verify the AI container has no Linux capabilities:

```bash
podman inspect cui-ai-assistant --format='{{.HostConfig.CapDrop}}'
```

**Expected**: `[ALL]`

### Verify Firewall Capabilities

Verify the firewall has only NET_ADMIN:

```bash
podman inspect cui-firewall-manager --format='{{.HostConfig.CapAdd}}'
```

**Expected**: `[NET_ADMIN]`

### View Blocked Attempts

Check firewall logs for blocked connection attempts:

```bash
podman logs cui-firewall-manager 2>&1 | grep "FW-BLOCKED-OUT"
```

**Expected**: Log entries showing blocked destinations (if any attempts were made)

### View iptables Rules

Inspect the actual firewall rules:

```bash
podman exec cui-firewall-manager iptables -L OUTPUT -v -n
```

**Expected**:
- Default policy: DROP
- ACCEPT rules for DNS (port 53)
- ACCEPT rules for ESTABLISHED/RELATED connections
- ACCEPT rules for whitelisted IPs
- LOG and DROP rule at the end

## Continuous Integration

### Running Tests in CI

Integration tests can be run in CI/CD pipelines. The test script is self-contained:

```bash
# Simple - test script handles container lifecycle
./tests/test-firewall.sh
```

The test script automatically:
- Starts containers using `docker-compose.firewall.yml` with PROJECT_NAME
- Waits for firewall initialization
- Runs all tests
- Cleans up containers (even on failure)

**Note**: Specify PROJECT_NAME to test specific projects or use default "test" for isolated testing.

### Test Exit Codes

The test script follows standard exit codes:
- `0` - All tests passed
- `1` - One or more tests failed

## Troubleshooting Test Failures

### Integration Test Fails

**Common causes**:
- Containers not running
- Firewall not healthy yet
- Network connectivity issues

**Fix**:
```bash
# Check container status
podman-compose ps

# Check firewall logs
podman logs cui-firewall-manager

# Wait longer for health check
sleep 30
```

### Blocked Access Test Fails (Non-whitelisted site accessible)

**Common causes**:
- Firewall rules not applied
- Container using wrong network
- DNS resolution bypassing firewall

**Fix**:
```bash
# Verify network configuration
podman inspect cui-ai-assistant --format='{{.HostConfig.NetworkMode}}'
# Should be: container:cui-firewall-manager

# Restart containers
podman-compose down && podman-compose up -d
```

## Adding New Tests

When adding new firewall features, follow TDD:

1. **Write test first** (RED phase)
   - Add test case to appropriate test script
   - Run test - it should fail

2. **Implement feature** (GREEN phase)
   - Implement the feature
   - Run test - it should pass

3. **Refactor** (REFACTOR phase)
   - Improve code quality
   - Ensure test still passes

**Example**: Adding test for new whitelist entry

```bash
# Add to test-firewall.sh
test_new_endpoint() {
  echo "Testing new endpoint..."
  if podman exec cui-ai-assistant curl --max-time 5 -s https://new-service.com; then
    echo "✅ New endpoint accessible"
  else
    echo "❌ New endpoint blocked"
    return 1
  fi
}
```

## Performance Benchmarks

Expected test execution time:

- **test-firewall.sh**: 10-30 seconds (depends on network and container startup)
