#!/bin/bash
################################################################################
# AI Assistant Container - Onboarding Script
# Target: ARM macOS (Apple Silicon) only
# Scope: Non-CUI projects (Anthropic API)
#
# This script automates the setup of the AI assistant development environment
# for new team members, handling everything from Homebrew installation to
# tool setup and configuration.
#
# SECURITY: All downloads over HTTPS, minimal sudo usage, secure credential storage
# IDEMPOTENCY: Safe to re-run, detects existing installations
################################################################################

set -euo pipefail  # Exit on error, undefined variables, pipe failures

################################################################################
# CONSTANTS & CONFIGURATION
################################################################################

readonly SCRIPT_VERSION="1.0.0"
readonly LOG_FILE="./ai-assistant-onboard.log"
readonly HOMEBREW_URL="https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"
readonly REQUIRED_ARCH="arm64"
readonly REQUIRED_OS="Darwin"

# Podman machine configuration
readonly PODMAN_CPUS=6
readonly PODMAN_MEMORY=16384

# Color codes for output
readonly COLOR_RESET='\033[0m'
readonly COLOR_GREEN='\033[0;32m'
readonly COLOR_YELLOW='\033[1;33m'
readonly COLOR_RED='\033[0;31m'
readonly COLOR_CYAN='\033[0;36m'

# Emoji for visual feedback
readonly EMOJI_CHECK="✅"
readonly EMOJI_CROSS="❌"
readonly EMOJI_ARROW="→"
readonly EMOJI_GEAR="⚙️"
readonly EMOJI_INFO="📝"
readonly EMOJI_QUESTION="❓"
readonly EMOJI_PACKAGE="📦"

################################################################################
# LOGGING FUNCTIONS
################################################################################

# Initialize log file with timestamp separator and system info
init_log() {
    echo "========== NEW RUN: $(date -u +"%Y-%m-%dT%H:%M:%SZ") ==========" >> "${LOG_FILE}"
    log_info "Script version: ${SCRIPT_VERSION}"
    log_info "Platform: $(uname -s) $(uname -m)"
    log_info "macOS version: $(sw_vers -productVersion 2>/dev/null || echo 'unknown')"
    log_info "Kernel: $(uname -r)"
    log_info "Shell: ${SHELL}"
    log_info "User: $(whoami)"
    log_info "Home: ${HOME}"
    log_info "PATH: ${PATH}"

    # Log system resources
    log_info "System memory: $(sysctl -n hw.memsize 2>/dev/null | awk '{print int($1/1024/1024/1024)"GB"}' || echo 'unknown')"
    log_info "CPU cores: $(sysctl -n hw.ncpu 2>/dev/null || echo 'unknown')"
    log_info "Available disk space: $(df -h . | tail -1 | awk '{print $4}' || echo 'unknown')"
}

# Log message with level and timestamp
log_message() {
    local level=$1
    shift
    local message="$*"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "${timestamp} [${level}] ${message}" >> "${LOG_FILE}"
}

log_info() { log_message "INFO" "$@"; }
log_warn() { log_message "WARN" "$@"; }
log_error() { log_message "ERROR" "$@"; }
log_metric() { log_message "METRIC" "$@"; }

################################################################################
# OUTPUT FUNCTIONS
################################################################################

print_header() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║  AI Assistant Container - Onboarding Script               ║"
    echo "║  Non-CUI Projects (Anthropic API)                         ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
}

print_success() {
    echo -e "${COLOR_GREEN}${EMOJI_CHECK} $*${COLOR_RESET}"
}

print_error() {
    echo -e "${COLOR_RED}${EMOJI_CROSS} $*${COLOR_RESET}"
}

print_info() {
    echo -e "${COLOR_CYAN}${EMOJI_INFO} $*${COLOR_RESET}"
}

print_step() {
    echo ""
    echo "---"
    echo -e "${COLOR_CYAN}${EMOJI_ARROW} $*${COLOR_RESET}"
    echo ""
}

print_helpdesk_instructions() {
    echo ""
    echo "NEXT STEPS:"
    echo "  1. Check the log file: ${LOG_FILE}"
    echo "  2. File a #helpdesk ticket"
    echo "  3. Attach the log file to your ticket"
    echo "  4. Include this error: 'AI assistant onboard script failed'"
    echo ""
}

################################################################################
# PHASE 0: PREREQUISITE VALIDATION
################################################################################

# Detect and validate platform architecture
validate_architecture() {
    local arch
    arch=$(uname -m)

    log_info "Detected architecture: ${arch}"

    if [[ "${arch}" != "${REQUIRED_ARCH}" ]]; then
        print_error "Incompatible architecture detected: ${arch}"
        echo ""
        echo "REQUIREMENT: This script requires ARM64 architecture (Apple Silicon)"
        echo ""
        echo "Your system: ${arch}"
        echo "Required: ${REQUIRED_ARCH}"
        echo ""
        echo "This script only supports:"
        echo "  - Apple Silicon Macs (M1, M2, M3, M4)"
        echo ""
        echo "Intel Macs and other architectures are not currently supported."
        log_error "Platform validation failed: incompatible architecture ${arch}"
        exit 1
    fi

    print_success "Architecture validated: ${arch}"
    return 0
}

# Detect and validate operating system
validate_os() {
    local os
    os=$(uname -s)

    log_info "Detected OS: ${os}"

    if [[ "${os}" != "${REQUIRED_OS}" ]]; then
        print_error "Incompatible operating system detected: ${os}"
        echo ""
        echo "REQUIREMENT: This script requires macOS (Darwin)"
        echo ""
        echo "Your system: ${os}"
        echo "Required: ${REQUIRED_OS}"
        echo ""
        echo "This script only supports:"
        echo "  - macOS (Apple's operating system)"
        echo ""
        echo "Linux and Windows are not currently supported."
        log_error "Platform validation failed: incompatible OS ${os}"
        exit 1
    fi

    print_success "Operating system validated: macOS"
    return 0
}

# Check if Xcode Command Line Tools are installed
check_xcode_cli_tools() {
    if xcode-select -p &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Install Xcode Command Line Tools with automatic dialog handling
install_xcode_cli_tools() {
    print_info "Xcode Command Line Tools not found - installing automatically..."
    echo ""
    echo "${EMOJI_QUESTION} What are Xcode Command Line Tools?"
    echo "   Essential developer utilities (git, make, compilers) required by Homebrew"
    echo "   and other development tools. These are provided by Apple."
    echo ""
    echo "${EMOJI_INFO} Installation process:"
    echo "   • A system dialog will appear automatically"
    echo "   • Click 'Install' when prompted"
    echo "   • Installation takes 5-15 minutes depending on your connection"
    echo "   • This script will wait and continue automatically when done"
    echo ""

    log_info "Starting Xcode CLI Tools installation"

    # Trigger the installation dialog
    # NOTE: macOS requires GUI dialog for security - no silent install method
    print_info "Launching installation dialog..."

    # Launch xcode-select --install
    # Capture output to detect if already installed or other issues
    local install_output
    install_output=$(xcode-select --install 2>&1)
    local install_exit_code=$?

    log_info "xcode-select --install output: ${install_output}"
    log_info "xcode-select --install exit code: ${install_exit_code}"

    # Check if installation dialog was triggered
    if echo "${install_output}" | grep -qi "install requested"; then
        print_success "Installation dialog launched"
        echo ""
        echo "${EMOJI_GEAR} Please complete the installation:"
        echo "   1. Look for the 'Software Update' dialog"
        echo "   2. Click 'Install' to begin"
        echo "   3. Wait for download and installation to complete"
        echo "   4. This script will detect completion automatically"
        echo ""
    elif echo "${install_output}" | grep -qi "already installed"; then
        print_success "Xcode Command Line Tools already installed"
        log_info "Xcode CLI Tools already present"
        return 0
    else
        # Installation may have been triggered silently
        print_info "Installation initiated"
    fi

    # Wait for installation to complete
    print_info "Waiting for installation to complete..."
    echo "   (This may take 5-15 minutes - please be patient)"
    echo ""

    local max_wait=2700  # 45 minutes max (generous timeout)
    local elapsed=0
    local check_interval=15  # Check every 15 seconds
    local last_dot_time=0

    while [ ${elapsed} -lt ${max_wait} ]; do
        # Check if tools are now installed
        if check_xcode_cli_tools; then
            echo ""
            print_success "Xcode Command Line Tools detected!"
            local xcode_path
            xcode_path=$(xcode-select -p)
            echo "   Location: ${xcode_path}"
            log_info "Xcode CLI Tools installation detected at: ${xcode_path}"

            # Wait for installation to fully complete and dialog to close
            print_info "Verifying tools are fully operational..."
            echo "   (Waiting for system finalization...)"
            sleep 5

            # Verify git is available and functional (critical for Homebrew)
            print_info "Testing git command..."
            local git_test_attempts=0
            local git_test_max=6  # 30 seconds total (5 second intervals)

            while [ ${git_test_attempts} -lt ${git_test_max} ]; do
                if command -v git &> /dev/null && git --version &> /dev/null; then
                    local git_version
                    git_version=$(git --version)
                    print_success "Git verified and operational: ${git_version}"
                    log_info "Git available and functional: ${git_version}"

                    # Additional verification: test that git can actually run a command
                    if git config --global --list &> /dev/null || true; then
                        print_success "Xcode Command Line Tools fully operational!"
                        log_info "Xcode CLI Tools verification complete - all tools functional"

                        # Final message before continuing
                        echo ""
                        echo "   ${EMOJI_INFO} Installation dialog may still be visible - safe to close"
                        sleep 2

                        return 0
                    fi
                fi

                # Git not ready yet - wait and retry
                echo -n "."
                sleep 5
                git_test_attempts=$((git_test_attempts + 1))
            done

            # Git didn't become available - this is unusual
            print_error "Git command not available after installation"
            log_error "Xcode CLI Tools installed but git not functional"
            return 1
        fi

        # Show progress dots every 15 seconds
        if [ $((elapsed - last_dot_time)) -ge ${check_interval} ]; then
            echo -n "."
            # Every 60 seconds, show a status message
            if [ $((elapsed % 60)) -eq 0 ] && [ ${elapsed} -gt 0 ]; then
                local minutes=$((elapsed / 60))
                echo ""
                echo "   Still installing... ${minutes} minute(s) elapsed (this is normal)"
                echo -n "   "
            fi
            last_dot_time=${elapsed}
        fi

        sleep 5
        elapsed=$((elapsed + 5))
    done

    # Installation timed out
    echo ""
    print_error "Installation timed out after ${max_wait} seconds"
    echo ""
    echo "TROUBLESHOOTING:"
    echo "  • Check if the installation dialog appeared"
    echo "  • Verify you clicked 'Install' (not 'Cancel')"
    echo "  • Check your internet connection"
    echo "  • Check available disk space (requires ~5GB)"
    echo ""
    echo "MANUAL INSTALLATION:"
    echo "  1. Run: xcode-select --install"
    echo "  2. Complete the installation"
    echo "  3. Verify: xcode-select -p"
    echo "  4. Re-run this script"
    echo ""
    log_error "Xcode CLI Tools installation timed out"
    log_error "Available disk space: $(df -h / | tail -1 || echo 'unknown')"
    return 1
}

# Validate or install Xcode Command Line Tools
validate_xcode_cli_tools() {
    log_info "Checking for Xcode Command Line Tools..."

    if check_xcode_cli_tools; then
        local xcode_path
        xcode_path=$(xcode-select -p)
        print_success "Xcode Command Line Tools found: ${xcode_path}"
        log_info "Xcode CLI Tools verified at: ${xcode_path}"
        return 0
    else
        # Not installed - trigger automatic installation
        if ! install_xcode_cli_tools; then
            print_error "Xcode Command Line Tools installation failed"
            echo ""
            print_helpdesk_instructions
            log_error "Xcode CLI Tools installation failed"
            exit 1
        fi
        return 0
    fi
}

# Verify git is available
validate_git() {
    log_info "Checking for git..."

    if command -v git &> /dev/null; then
        local git_version
        git_version=$(git --version)
        print_success "Git found: ${git_version}"
        log_info "Git verified: ${git_version}"
        return 0
    else
        print_error "Git not found"
        echo ""
        echo "ERROR: git command not available"
        echo ""
        echo "Git should be installed automatically with Xcode Command Line Tools."
        echo ""
        echo "NEXT STEPS:"
        echo "  1. Check the log file: ${LOG_FILE}"
        echo "  2. File a #helpdesk ticket"
        echo "  3. Attach the log file to your ticket"
        echo "  4. Include this error: 'AI assistant onboard script failed'"
        echo ""
        log_error "Git not found despite Xcode CLI Tools check"
        log_error "Git path check: $(which git 2>&1 || echo 'not found')"
        log_error "Xcode CLI Tools path: $(xcode-select -p 2>&1 || echo 'not found')"
        exit 1
    fi
}

# Validate admin/sudo privileges
validate_admin_privileges() {
    log_info "Checking for admin/sudo privileges..."

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_info "Administrator Password Required"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "This setup requires admin access to install software."
    echo ""
    echo "What you need to know:"
    echo "  • You'll enter your macOS LOGIN PASSWORD (the one you use to login)"
    echo "  • Your typing will be invisible (normal security behavior)"
    echo "  • This password is NOT stored anywhere"
    echo "  • This is safe and standard for software installation"
    echo ""
    echo "If you don't have admin access, see README.md for Rippling instructions."
    echo ""

    # Give users time to read
    sleep 2

    print_info "Please enter your macOS login password below:"
    echo ""

    # Attempt to validate sudo access
    # Using sudo -v which updates cached credentials without running a command
    if sudo -v 2>/dev/null; then
        print_success "Admin privileges confirmed"
        log_info "Admin privileges validated successfully"
        return 0
    else
        print_error "Admin privileges not available"
        echo ""
        echo "PREREQUISITE MISSING: Admin/Sudo Privileges"
        echo ""
        echo "This script requires admin (sudo) access to install software."
        echo ""
        echo "TROUBLESHOOTING:"
        echo ""
        echo "  • Verify you're an administrator (System Settings → Users & Groups)"
        echo "  • Using Rippling? See README.md for admin access steps"
        echo "  • Contact IT support if needed"
        echo ""
        echo "If you're using Rippling for device management:"
        echo "  See README.md for instructions on enabling admin privileges in Rippling."
        echo "  The README includes step-by-step screenshots."
        echo ""
        echo "If you continue to have issues:"
        echo "  - Contact your IT administrator"
        echo "  - Request admin/sudo access for software installation"
        echo ""
        log_error "Admin privileges validation failed - sudo access not available"
        exit 1
    fi
}

# Run all prerequisite validation checks
validate_prerequisites() {
    print_step "Phase 0: Prerequisite Validation"

    print_info "Validating system requirements..."
    echo ""

    validate_architecture
    validate_os
    validate_xcode_cli_tools
    validate_git
    validate_admin_privileges

    echo ""
    print_success "All prerequisites validated!"
    log_info "Phase 0: Prerequisite validation completed successfully"
}

################################################################################
# TERMINAL MANAGEMENT WARNING
################################################################################

# Display warning about closing other terminal windows
display_terminal_warning() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║  ⚠️  Please close all other terminal windows             ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "   For best results, close any other open terminal windows now."
    echo "   You can reopen them after installation completes."
    echo ""
    print_info "Continuing in 5 seconds..."
    sleep 5
    echo ""
}

################################################################################
# PHASE 1: HOMEBREW INSTALLATION
################################################################################

# Check if Homebrew is installed
check_homebrew() {
    if command -v brew &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Verify Homebrew installation URL for security
verify_homebrew_url() {
    local url=$1

    # SECURITY: Verify URL is HTTPS and from official Homebrew repository
    if [[ "${url}" != "${HOMEBREW_URL}" ]]; then
        print_error "Security check failed: Invalid Homebrew URL"
        echo ""
        echo "SECURITY ERROR: Homebrew installation URL does not match expected value"
        echo ""
        echo "Expected: ${HOMEBREW_URL}"
        echo "Got: ${url}"
        echo ""
        echo "This script will only install Homebrew from the official source."
        log_error "Security check failed: invalid Homebrew URL ${url}"
        exit 1
    fi

    log_info "Homebrew URL verified: ${url}"
    return 0
}

# Install Homebrew
install_homebrew() {
    print_step "Phase 1: Homebrew Installation"

    if check_homebrew; then
        local brew_version
        brew_version=$(brew --version | head -n1)
        print_success "Homebrew already installed: ${brew_version}"
        log_info "Homebrew already present: ${brew_version}"
        return 0
    fi

    print_info "Homebrew not found - installing automatically..."
    echo ""
    echo "${EMOJI_QUESTION} What is Homebrew?"
    echo "   Homebrew is the most popular package manager for macOS."
    echo "   It allows easy installation and management of software tools."
    echo "   We'll use it to install Podman, gh CLI, VSCode, and other tools."
    echo ""
    echo "${EMOJI_INFO} Installation details:"
    echo "   • Official Homebrew installation script will be executed"
    echo "   • URL: ${HOMEBREW_URL}"
    echo "   • You may be prompted for your password (sudo/admin access required)"
    echo "   • This is safe and standard practice for macOS development"
    echo ""
    echo "${EMOJI_GEAR} Installing Homebrew now..."
    echo ""

    # Verify URL security before installation
    verify_homebrew_url "${HOMEBREW_URL}"

    log_info "Starting Homebrew installation from ${HOMEBREW_URL}"

    # Execute official Homebrew installation script
    # REASON: Use NONINTERACTIVE=1 to skip prompts and proceed automatically
    if NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL ${HOMEBREW_URL})"; then
        log_info "Homebrew installation script completed"

        # Update PATH to include Homebrew
        if [[ -f "/opt/homebrew/bin/brew" ]]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
            log_info "Homebrew PATH updated: /opt/homebrew/bin/brew"
        fi

        # Verify installation
        if check_homebrew; then
            local brew_version
            brew_version=$(brew --version | head -n1)
            echo ""
            print_success "Homebrew installed successfully: ${brew_version}"
            log_info "Homebrew installation verified: ${brew_version}"
            return 0
        else
            print_error "Homebrew installation verification failed"
            echo ""
            echo "ERROR: Homebrew was installed but 'brew' command not found"
            echo ""
            echo "NEXT STEPS:"
            echo "  1. Check the log file: ${LOG_FILE}"
            echo "  2. File a #helpdesk ticket"
            echo "  3. Attach the log file to your ticket"
            echo "  4. Include this error: 'AI assistant onboard script failed'"
            echo ""
            log_error "Homebrew installation completed but brew command not available"
            log_error "Brew path check: $(which brew 2>&1 || echo 'not found')"
            log_error "Homebrew directories: $(ls -la /opt/homebrew/bin/ 2>&1 || echo 'directory not found')"
            log_error "Current PATH: ${PATH}"
            exit 1
        fi
    else
        print_error "Homebrew installation failed"
        echo ""
        echo "ERROR: Homebrew installation script failed"
        echo ""
        echo "NEXT STEPS:"
        echo "  1. Check the log file: ${LOG_FILE}"
        echo "  2. File a #helpdesk ticket"
        echo "  3. Attach the log file to your ticket"
        echo "  4. Include this error: 'AI assistant onboard script failed'"
        echo ""
        log_error "Homebrew installation script failed"
        log_error "Network connectivity test: $(curl -s -o /dev/null -w '%{http_code}' https://brew.sh 2>&1 || echo 'failed')"
        log_error "Disk space: $(df -h / | tail -1 || echo 'unknown')"
        exit 1
    fi
}

################################################################################
# PHASE 2: TOOL INSTALLATION VIA HOMEBREW
################################################################################

# Check if a tool is installed
check_tool() {
    local tool_command=$1
    command -v "${tool_command}" &> /dev/null
}

# Install a tool via Homebrew
install_tool_via_brew() {
    local tool_name=$1
    local brew_package=$2
    local tool_command=$3
    local description=$4
    local is_cask=${5:-false}

    echo ""
    print_info "Checking ${tool_name}..."

    # Check if already installed
    if check_tool "${tool_command}"; then
        local version_output
        version_output=$("${tool_command}" --version 2>&1 | head -n1 || echo "version unknown")
        print_success "${tool_name} already installed: ${version_output}"
        log_info "${tool_name} already present: ${version_output}"
        return 0
    fi

    print_info "${tool_name} not found - installing..."
    echo "   Why needed: ${description}"

    # Build brew install command
    local brew_cmd="brew install"
    if [[ "${is_cask}" == "true" ]]; then
        brew_cmd="brew install --cask"
    fi
    brew_cmd="${brew_cmd} ${brew_package}"

    echo "   Command: ${brew_cmd}"
    log_info "Installing ${tool_name} via: ${brew_cmd}"

    # Execute installation
    if ${brew_cmd}; then
        # Verify installation
        if check_tool "${tool_command}"; then
            local version_output
            version_output=$("${tool_command}" --version 2>&1 | head -n1 || echo "installed")
            print_success "${tool_name} installed successfully: ${version_output}"
            log_info "${tool_name} installation verified: ${version_output}"
            return 0
        else
            print_error "${tool_name} installation verification failed"
            log_error "${tool_name} installed but command '${tool_command}' not available"
            log_error "PATH: ${PATH}"
            log_error "Brew list: $(brew list ${brew_package} 2>&1 || echo 'not found')"
            log_error "Which ${tool_command}: $(which ${tool_command} 2>&1 || echo 'not found')"
            return 1
        fi
    else
        local brew_exit_code=$?
        print_error "${tool_name} installation failed"
        log_error "${tool_name} installation via Homebrew failed with exit code: ${brew_exit_code}"
        log_error "Brew doctor: $(brew doctor 2>&1 | head -20 || echo 'brew doctor failed')"
        log_error "Disk space: $(df -h ~ | tail -1 || echo 'unknown')"
        return 1
    fi
}

# Install and configure Podman
install_podman() {
    if ! install_tool_via_brew "Podman" "podman" "podman" "Container runtime for running the AI assistant" false; then
        return 1
    fi

    # Check if podman machine already exists
    if podman machine list --format "{{.Name}}" 2>/dev/null | grep -q "podman-machine-default"; then
        print_info "Podman machine already exists"
        log_info "Podman machine already configured"

        # Check if machine is running
        if podman machine list --format "{{.Name}}\t{{.Running}}" 2>/dev/null | grep -q "podman-machine-default.*true"; then
            print_success "Podman machine is running"
            log_info "Podman machine already running"
        else
            print_info "Starting Podman machine..."
            if podman machine start; then
                print_success "Podman machine started"
                log_info "Podman machine started successfully"
            else
                print_error "Failed to start Podman machine"
                log_error "Podman machine start failed"
                log_error "Podman machine list: $(podman machine list 2>&1 || echo 'failed')"
                log_error "Podman machine inspect: $(podman machine inspect 2>&1 || echo 'failed')"
                return 1
            fi
        fi
    else
        # Configure Zscaler certificates BEFORE machine creation (Podman will auto-sync them)
        configure_zscaler_certificates_for_podman

        # Initialize podman machine with configured resources
        print_info "Initializing Podman machine (${PODMAN_CPUS} CPUs, ${PODMAN_MEMORY}MB memory)..."
        echo "   This may take 5-10 minutes..."
        log_info "Initializing podman machine: ${PODMAN_CPUS} CPUs, ${PODMAN_MEMORY}MB memory"

        if podman machine init --cpus "${PODMAN_CPUS}" --memory "${PODMAN_MEMORY}"; then
            print_success "Podman machine initialized"
            log_info "Podman machine initialization completed"

            # Start the machine
            print_info "Starting Podman machine..."
            if podman machine start; then
                print_success "Podman machine started"
                log_info "Podman machine started successfully"
            else
                print_error "Failed to start Podman machine"
                log_error "Podman machine start failed after initialization"
                log_error "Podman machine list: $(podman machine list 2>&1 || echo 'failed')"
                log_error "Podman machine inspect: $(podman machine inspect 2>&1 || echo 'failed')"
                return 1
            fi
        else
            print_error "Podman machine initialization failed"
            echo ""
            echo "NEXT STEPS:"
            echo "  1. Check the log file: ${LOG_FILE}"
            echo "  2. File a #helpdesk ticket"
            echo "  3. Attach the log file to your ticket"
            echo "  4. Include this error: 'AI assistant onboard script failed'"
            echo ""
            log_error "Podman machine initialization failed"
            log_error "Podman version: $(podman --version 2>&1 || echo 'unknown')"
            log_error "Podman machine list: $(podman machine list 2>&1 || echo 'failed')"
            log_error "Available disk space: $(df -h ~ | tail -1 || echo 'unknown')"
            log_error "Available memory: $(vm_stat | head -5 || echo 'unknown')"
            return 1
        fi
    fi

    # Verify Podman is working
    if podman info &> /dev/null; then
        print_success "Podman verified and operational"
        log_info "Podman verification successful"
        log_info "Podman info: $(podman info --format json 2>&1 | head -50 || echo 'info failed')"
    else
        print_error "Podman verification failed"
        log_error "Podman installed but 'podman info' failed"
        log_error "Podman version: $(podman --version 2>&1 || echo 'unknown')"
        log_error "Podman machine list: $(podman machine list 2>&1 || echo 'failed')"
        log_error "Podman system connection list: $(podman system connection list 2>&1 || echo 'failed')"
        return 1
    fi

    # Create docker symlink to podman for compatibility
    echo ""
    print_info "Creating docker symlink for compatibility..."
    echo "   Why: Many tools expect 'docker' command - podman is API-compatible"
    log_info "Attempting to create docker -> podman symlink"

    # Check if docker command already exists (not a symlink to podman)
    if command -v docker &> /dev/null; then
        # Check if it's already a symlink to podman
        if [[ -L "$(command -v docker)" ]]; then
            local link_target
            link_target=$(readlink "$(command -v docker)")
            if [[ "${link_target}" == *"podman"* ]] || [[ "$(basename "${link_target}")" == "podman" ]]; then
                print_success "docker symlink already exists"
                log_info "docker command already symlinked to podman"
                return 0
            fi
        fi

        # docker exists but is not a symlink to podman
        print_info "docker command already exists (not a podman symlink)"
        echo "   Skipping symlink creation - using existing docker installation"
        log_info "docker command exists independently - skipping symlink"
        return 0
    fi

    # Ensure /usr/local/bin exists
    if [[ ! -d "/usr/local/bin" ]]; then
        print_info "Creating /usr/local/bin directory..."
        if sudo mkdir -p /usr/local/bin; then
            log_info "Created /usr/local/bin directory"
        else
            print_error "Failed to create /usr/local/bin directory"
            log_error "Could not create /usr/local/bin for docker symlink"
            return 1
        fi
    fi

    # Determine podman location
    local podman_path
    podman_path=$(command -v podman)

    if [[ -z "${podman_path}" ]]; then
        print_error "Cannot locate podman binary"
        log_error "podman command not found in PATH for symlink creation"
        return 1
    fi

    print_info "Podman location: ${podman_path}"
    log_info "Creating symlink: /usr/local/bin/docker -> ${podman_path}"

    # Create symlink (requires sudo)
    if sudo ln -sf "${podman_path}" /usr/local/bin/docker; then
        print_success "docker symlink created: /usr/local/bin/docker -> ${podman_path}"
        log_info "Successfully created docker symlink to podman"

        # Verify symlink was created successfully
        if [[ -L "/usr/local/bin/docker" ]]; then
            print_success "docker command verified"
            log_info "Symlink verification successful"

            # Test docker command
            if docker --version &> /dev/null; then
                local docker_version
                docker_version=$(docker --version 2>&1 | head -n1)
                print_success "docker command works: ${docker_version}"
                log_info "docker command operational: ${docker_version}"
            fi

            return 0
        else
            print_error "Symlink creation failed - file not found at /usr/local/bin/docker"
            log_error "Symlink verification failed"
            return 1
        fi
    else
        print_error "Failed to create docker symlink"
        echo ""
        echo "NOTE: This is not critical - you can use 'podman' command directly"
        echo "      Some tools may require 'docker' command and won't work without the symlink"
        echo ""
        log_error "Could not create docker symlink - sudo failed (non-critical)"
        log_error "Podman path: ${podman_path}"
        log_error "/usr/local/bin permissions: $(ls -la /usr/local/bin 2>&1 || echo 'directory not accessible')"
        # Don't return error - this is non-critical
        return 0
    fi
}

# Configure Podman machine to auto-start on macOS login
configure_podman_auto_start() {
    echo ""
    print_info "Configuring Podman machine to auto-start on login..."
    echo ""
    echo "${EMOJI_QUESTION} Why auto-start Podman machine?"
    echo "   After macOS reboots, the Podman machine needs to be started manually."
    echo "   This LaunchAgent will automatically start Podman when you login,"
    echo "   ensuring your development environment is always ready."
    echo ""
    log_info "Configuring Podman auto-start LaunchAgent"

    # Define LaunchAgent paths
    local launch_agents_dir="${HOME}/Library/LaunchAgents"
    local plist_file="${launch_agents_dir}/com.podman.machine.plist"
    local label="com.podman.machine"

    # Ensure LaunchAgents directory exists
    if [[ ! -d "${launch_agents_dir}" ]]; then
        print_info "Creating LaunchAgents directory..."
        if mkdir -p "${launch_agents_dir}"; then
            print_success "LaunchAgents directory created"
            log_info "Created LaunchAgents directory: ${launch_agents_dir}"
        else
            print_error "Failed to create LaunchAgents directory"
            echo "   This is non-critical - you can manually start Podman after reboots"
            log_error "Could not create LaunchAgents directory (non-critical)"
            return 0
        fi
    fi

    # Check if LaunchAgent already exists
    if [[ -f "${plist_file}" ]]; then
        print_success "Podman auto-start already configured"
        log_info "LaunchAgent plist already exists: ${plist_file}"

        # Verify if LaunchAgent is loaded
        if launchctl list | grep -q "${label}"; then
            print_success "LaunchAgent is active"
            log_info "LaunchAgent ${label} is loaded and active"
        else
            print_info "LaunchAgent exists but not loaded - loading now..."
            if launchctl load -w "${plist_file}" 2>/dev/null; then
                print_success "LaunchAgent loaded successfully"
                log_info "Loaded existing LaunchAgent: ${label}"
            else
                print_info "LaunchAgent load skipped (may already be running)"
                log_warn "LaunchAgent load command returned non-zero (may be benign)"
            fi
        fi

        echo ""
        print_success "Podman machine will automatically start after reboots"
        return 0
    fi

    # Determine podman binary path
    local podman_path
    podman_path=$(command -v podman)

    if [[ -z "${podman_path}" ]]; then
        print_error "Cannot locate podman binary"
        echo "   This is non-critical - you can manually start Podman after reboots"
        log_error "podman command not found in PATH for LaunchAgent configuration (non-critical)"
        return 0
    fi

    print_info "Podman location: ${podman_path}"
    log_info "Using podman binary: ${podman_path}"

    # Create LaunchAgent plist file
    print_info "Creating LaunchAgent configuration..."
    log_info "Creating plist file: ${plist_file}"

    # Write plist content
    # NOTE: Using heredoc for clean multi-line XML
    # NOTE: AbandonProcessGroup=true prevents launchd from killing the VM when start command exits
    cat > "${plist_file}" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${label}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${podman_path}</string>
        <string>machine</string>
        <string>start</string>
        <string>podman-machine-default</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${HOME}/Library/Logs/podman-machine-start.log</string>
    <key>StandardErrorPath</key>
    <string>${HOME}/Library/Logs/podman-machine-start-error.log</string>
    <key>AbandonProcessGroup</key>
    <true/>
</dict>
</plist>
EOF

    local plist_exit_code=$?

    if [[ ${plist_exit_code} -ne 0 ]] || [[ ! -f "${plist_file}" ]]; then
        print_error "Failed to create LaunchAgent plist file"
        echo "   This is non-critical - you can manually start Podman after reboots"
        log_error "Could not create plist file (non-critical)"
        return 0
    fi

    print_success "LaunchAgent plist file created"
    log_info "Successfully created plist file: ${plist_file}"

    # Set correct permissions (644 - owner read/write, group/others read)
    print_info "Setting file permissions..."
    if chmod 644 "${plist_file}"; then
        print_success "Permissions set to 644"
        log_info "Set plist permissions to 644"
    else
        print_info "Could not set permissions (non-critical)"
        log_warn "chmod 644 failed on plist file (non-critical)"
    fi

    # Load LaunchAgent
    print_info "Loading LaunchAgent..."
    log_info "Attempting to load LaunchAgent: ${label}"

    if launchctl load -w "${plist_file}" 2>/dev/null; then
        print_success "LaunchAgent loaded successfully"
        log_info "Successfully loaded LaunchAgent: ${label}"
    else
        local launchctl_exit_code=$?
        print_info "LaunchAgent installation completed (load status unclear)"
        echo "   The LaunchAgent will activate on next login"
        log_warn "launchctl load returned exit code ${launchctl_exit_code} (may be benign)"
    fi

    # Verify LaunchAgent is loaded
    echo ""
    print_info "Verifying LaunchAgent status..."
    if launchctl list | grep -q "${label}"; then
        print_success "LaunchAgent is active and will run at login"
        log_info "LaunchAgent verification successful: ${label} is loaded"
    else
        print_info "LaunchAgent installed - will activate on next login"
        log_info "LaunchAgent not immediately visible in launchctl list (will activate on next login)"
    fi

    echo ""
    echo "---"
    print_info "Auto-Start Configuration Summary:"
    echo ""
    echo "   LaunchAgent: ${label}"
    echo "   Location: ${plist_file}"
    echo "   Command: ${podman_path} machine start"
    echo "   Logs: ${HOME}/Library/Logs/podman-machine-start*.log"
    echo ""
    echo "   ${EMOJI_CHECK} Podman machine will automatically start after reboots"
    echo "   ${EMOJI_INFO} Logs available if troubleshooting needed"
    echo ""

    log_info "Podman auto-start configuration completed successfully"
    return 0
}

# Install GitHub CLI
install_gh_cli() {
    install_tool_via_brew "GitHub CLI" "gh" "gh" "GitHub authentication and container registry access" false
}

# Install VSCode and handle PATH issues
install_vscode() {
    if ! install_tool_via_brew "VSCode" "visual-studio-code" "code" "Code editor for development" true; then
        # If installation succeeded but 'code' command not available, try to fix PATH
        if [[ -d "/Applications/Visual Studio Code.app" ]]; then
            print_info "VSCode installed but 'code' command not in PATH"
            print_info "Creating symlink to make 'code' command available..."

            # Ensure /usr/local/bin exists
            if [[ ! -d "/usr/local/bin" ]]; then
                print_info "Creating /usr/local/bin directory..."
                if sudo mkdir -p /usr/local/bin; then
                    log_info "Created /usr/local/bin directory"
                else
                    print_error "Failed to create /usr/local/bin directory"
                    log_error "Could not create /usr/local/bin"
                    return 1
                fi
            fi

            # Create symlink (requires sudo)
            if sudo ln -sf "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" /usr/local/bin/code; then
                print_success "Added 'code' command to PATH"
                log_info "Created symlink for 'code' command at /usr/local/bin/code"

                # Verify symlink was created successfully
                if [[ -L "/usr/local/bin/code" ]]; then
                    print_success "VSCode CLI symlink verified at /usr/local/bin/code"
                    log_info "Symlink verification successful"

                    # Note: 'code' command may not be available in current shell session
                    # but will work in new terminal sessions
                    print_info "Note: 'code' command will be available in new terminal sessions"
                    log_info "VSCode CLI command configured - new terminal sessions required to use 'code'"
                    return 0
                else
                    print_error "Symlink creation failed - file not found at /usr/local/bin/code"
                    log_error "Symlink verification failed"
                    return 1
                fi
            else
                print_error "Failed to create 'code' symlink"
                echo ""
                echo "NEXT STEPS:"
                echo "  1. Check the log file: ${LOG_FILE}"
                echo "  2. File a #helpdesk ticket"
                echo "  3. Attach the log file to your ticket"
                echo "  4. Include this error: 'AI assistant onboard script failed'"
                echo ""
                log_error "Could not create 'code' symlink - sudo failed"
                log_error "VSCode app path: $(ls -la '/Applications/Visual Studio Code.app' 2>&1 || echo 'not found')"
                log_error "/usr/local/bin permissions: $(ls -la /usr/local/bin 2>&1 || echo 'directory not accessible')"
                return 1
            fi
        else
            log_error "VSCode installation failed - application not found"
            return 1
        fi
    fi

    # If VSCode was already installed or install_tool_via_brew succeeded,
    # verify the 'code' command is accessible
    if check_tool "code"; then
        print_success "VSCode CLI command verified and accessible"
        log_info "VSCode 'code' command available in current PATH"
        return 0
    else
        # 'code' not in PATH - may need symlink or PATH update
        if [[ -d "/Applications/Visual Studio Code.app" ]]; then
            print_info "'code' command not in current PATH - checking for symlink..."

            # Check if symlink exists
            if [[ -L "/usr/local/bin/code" ]]; then
                print_success "VSCode CLI symlink exists"
                print_info "Note: 'code' command will be available in new terminal sessions"
                log_info "Symlink exists but not in current shell PATH - new terminal required"
                return 0
            else
                print_info "Creating symlink for 'code' command..."
                log_info "Attempting to create symlink for existing VSCode installation"

                # Ensure /usr/local/bin exists
                if [[ ! -d "/usr/local/bin" ]]; then
                    sudo mkdir -p /usr/local/bin
                fi

                # Create symlink
                if sudo ln -sf "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" /usr/local/bin/code; then
                    print_success "VSCode CLI symlink created"
                    print_info "Note: 'code' command will be available in new terminal sessions"
                    log_info "Successfully created symlink for existing VSCode installation"
                    return 0
                else
                    print_error "Failed to create VSCode CLI symlink"
                    log_error "Could not create symlink for existing VSCode installation"
                    return 1
                fi
            fi
        else
            log_error "VSCode not found - neither command nor application exists"
            return 1
        fi
    fi

    return 0
}

# NOTE: Dev Containers extension installation removed
# The extension will be automatically installed by VSCode when it detects
# the devcontainer configuration file on first open

# Install all required tools
install_tools() {
    print_step "Phase 2: Tool Installation"

    print_info "Automatically installing required tools via Homebrew..."
    echo ""
    echo "${EMOJI_PACKAGE} Tools that will be installed automatically:"
    echo "   • Podman - Container runtime"
    echo "   • GitHub CLI - GitHub authentication"
    echo "   • VSCode - Code editor"
    echo ""
    echo "This process is fully automated. Progress will be shown for each tool."
    echo ""
    echo "${EMOJI_INFO} Note: Dev Containers extension will be installed automatically"
    echo "   by VSCode when you open the project for the first time."
    echo ""

    log_info "Phase 2: Tool installation started"

    # Track installation results
    local failed_tools=()

    # Install Podman
    if ! install_podman; then
        failed_tools+=("Podman")
    fi

    # Configure Podman auto-start (non-critical - always returns 0)
    configure_podman_auto_start

    # Install GitHub CLI
    if ! install_gh_cli; then
        failed_tools+=("GitHub CLI")
    fi

    # Install VSCode
    if ! install_vscode; then
        failed_tools+=("VSCode")
    fi

    # Report results
    echo ""
    echo "---"
    print_info "Installation Summary:"

    if [[ ${#failed_tools[@]} -eq 0 ]]; then
        print_success "All tools installed successfully!"
        log_info "Phase 2: All tools installed successfully"
        return 0
    else
        print_error "Some tools failed to install:"
        for tool in "${failed_tools[@]}"; do
            echo "   ${EMOJI_CROSS} ${tool}"
        done
        echo ""
        echo "NEXT STEPS:"
        echo "  1. Check the log file for details: ${LOG_FILE}"
        echo "  2. Try installing failed tools manually"
        echo "  3. Re-run this script (it will skip successful installations)"
        echo ""
        log_error "Phase 2: Tool installation completed with failures: ${failed_tools[*]}"
        exit 1
    fi
}

################################################################################
# PHASE 3: FILE STRUCTURE CLEANUP
################################################################################

# Remove CUI-related files that are not needed for non-CUI projects
cleanup_cui_files() {
    print_step "Phase 3: File Structure Cleanup"

    print_info "Cleaning up CUI-related files..."
    echo ""
    echo "${EMOJI_QUESTION} What is CUI?"
    echo "   CUI (Controlled Unclassified Information) is a designation for sensitive"
    echo "   government data that requires special security controls and network isolation."
    echo ""
    echo "   This repository supports two deployment paths:"
    echo "   1. Standard cloud deployment (AWS Bedrock, Anthropic API)"
    echo "   2. CUI-compliant deployment (isolated networks, firewall rules)"
    echo ""
    echo "   Since you're setting up a non-CUI project, we'll remove CUI-specific files"
    echo "   to simplify your environment and avoid confusion."
    echo ""
    echo "${EMOJI_INFO} Files to be removed (if present):"
    echo "   • firewall/ - Network firewall configuration for CUI environments"
    echo "   • docs/firewall/ - Firewall documentation"
    echo "   • .devcontainer/devcontainer.cui.json - CUI-specific container config"
    echo "   • .devcontainer/docker-compose.firewall.yml - Firewall container setup"
    echo ""

    log_info "Phase 3: File structure cleanup started"

    # Track cleanup results
    local removed_count=0
    local skipped_count=0
    local failed_count=0

    # Define CUI files/directories to remove
    declare -a cui_files=(
        "firewall"
        "docs/firewall"
        ".devcontainer/devcontainer.cui.json"
        ".devcontainer/docker-compose.firewall.yml"
    )

    # Process each CUI file/directory
    for file_path in "${cui_files[@]}"; do
        # Use absolute path from repository root
        local full_path="${file_path}"

        # Check if file or directory exists
        if [[ -e "${full_path}" ]]; then
            print_info "Removing: ${file_path}"
            log_info "Attempting to remove: ${full_path}"

            # Determine if it's a directory or file
            if [[ -d "${full_path}" ]]; then
                # Remove directory recursively
                if rm -rf "${full_path}"; then
                    print_success "Removed directory: ${file_path}"
                    log_info "Successfully removed directory: ${full_path}"
                    ((removed_count++))
                else
                    print_error "Failed to remove directory: ${file_path}"
                    log_error "Failed to remove directory: ${full_path}"
                    log_error "Directory permissions: $(ls -ld "${full_path}" 2>&1 || echo 'cannot stat')"
                    ((failed_count++))
                fi
            else
                # Remove file
                if rm -f "${full_path}"; then
                    print_success "Removed file: ${file_path}"
                    log_info "Successfully removed file: ${full_path}"
                    ((removed_count++))
                else
                    print_error "Failed to remove file: ${file_path}"
                    log_error "Failed to remove file: ${full_path}"
                    log_error "File permissions: $(ls -l "${full_path}" 2>&1 || echo 'cannot stat')"
                    ((failed_count++))
                fi
            fi
        else
            # File/directory doesn't exist - this is fine (idempotent)
            print_info "Already removed or not present: ${file_path}"
            log_info "File/directory not found (already removed or never existed): ${full_path}"
            ((skipped_count++))
        fi
    done

    # Report results
    echo ""
    echo "---"
    print_info "Cleanup Summary:"
    echo "   ${EMOJI_CHECK} Files/directories removed: ${removed_count}"
    echo "   ${EMOJI_INFO} Already cleaned: ${skipped_count}"

    if [[ ${failed_count} -gt 0 ]]; then
        echo "   ${EMOJI_CROSS} Failed removals: ${failed_count}"
        print_error "Some files could not be removed"
        echo ""
        echo "NEXT STEPS:"
        echo "  1. Check the log file: ${LOG_FILE}"
        echo "  2. Try removing failed files manually"
        echo "  3. Re-run this script (it will skip successful removals)"
        echo ""
        log_error "Phase 3: File cleanup completed with failures (${failed_count} failed)"
        return 1
    fi

    echo ""
    print_success "File structure cleanup completed!"
    log_info "Phase 3: File structure cleanup completed successfully"
    log_metric "cleanup_removed=${removed_count}"
    log_metric "cleanup_skipped=${skipped_count}"
    log_metric "cleanup_failed=${failed_count}"
    return 0
}

################################################################################
# PHASE 4: DEVCONTAINER CONFIGURATION
################################################################################

# Configure devcontainer for non-CUI development
configure_devcontainer() {
    print_step "Phase 4: DevContainer Configuration"

    print_info "Configuring devcontainer for non-CUI development..."
    echo ""
    echo "${EMOJI_QUESTION} What is a devcontainer?"
    echo "   A devcontainer (development container) provides a consistent development"
    echo "   environment using Docker/Podman containers. This ensures all team members"
    echo "   work with identical tools, dependencies, and configurations."
    echo ""
    echo "   This repository includes different devcontainer configurations:"
    echo "   • devcontainer.no-cui.json - For standard cloud projects (Anthropic API)"
    echo "   • devcontainer.cui.json - For CUI-compliant projects (isolated networks)"
    echo ""
    echo "   We'll configure the standard (non-CUI) devcontainer for your environment."
    echo ""

    log_info "Phase 4: DevContainer configuration started"

    # Define source and target paths
    local source_file=".devcontainer/devcontainer.no-cui.json"
    local target_file=".devcontainer/devcontainer.json"

    # Check if source file exists
    if [[ ! -f "${source_file}" ]]; then
        print_error "Source file not found: ${source_file}"
        echo ""
        echo "ERROR: Cannot configure devcontainer - source file missing"
        echo ""
        echo "Expected file: ${source_file}"
        echo ""
        echo "NEXT STEPS:"
        echo "  1. Check the log file: ${LOG_FILE}"
        echo "  2. Verify repository integrity"
        echo "  3. File a #helpdesk ticket if issue persists"
        echo ""
        log_error "DevContainer source file not found: ${source_file}"
        log_error "Directory contents: $(ls -la .devcontainer/ 2>&1 || echo 'directory not accessible')"
        return 1
    fi

    print_success "Source file found: ${source_file}"
    log_info "Source file verified: ${source_file}"

    # Perform the rename/copy operation
    print_info "Configuring devcontainer.json..."
    log_info "Copying ${source_file} to ${target_file}"

    if cp "${source_file}" "${target_file}"; then
        print_success "DevContainer configuration file created: ${target_file}"
        log_info "Successfully created/updated devcontainer.json"
    else
        print_error "Failed to create devcontainer configuration"
        echo ""
        echo "ERROR: Could not copy devcontainer configuration"
        echo ""
        echo "NEXT STEPS:"
        echo "  1. Check the log file: ${LOG_FILE}"
        echo "  2. Verify file permissions"
        echo "  3. Try copying manually or file a #helpdesk ticket"
        echo ""
        log_error "Failed to copy ${source_file} to ${target_file}"
        log_error "Source file permissions: $(ls -l "${source_file}" 2>&1 || echo 'cannot stat')"
        log_error "Target directory permissions: $(ls -ld .devcontainer/ 2>&1 || echo 'cannot stat')"
        return 1
    fi

    # Remove the source file after successful configuration
    print_info "Cleaning up source file..."
    log_info "Removing source file: ${source_file}"

    if rm -f "${source_file}"; then
        print_success "Source file removed: ${source_file}"
        log_info "Successfully removed source file"
    else
        print_info "Could not remove source file (non-critical)"
        echo "   You can manually remove: ${source_file}"
        log_warn "Failed to remove source file (non-critical): ${source_file}"
    fi

    echo ""
    print_success "DevContainer configuration completed!"
    log_info "Phase 4: DevContainer configuration completed successfully"
    return 0
}

################################################################################
# ZSCALER CERTIFICATE CONFIGURATION (for Podman)
################################################################################

# Configure Zscaler certificates for Podman
# This is called BEFORE podman machine init so certificates are auto-synced
configure_zscaler_certificates_for_podman() {
    echo ""
    print_info "Checking for Zscaler certificates..."
    log_info "Zscaler certificate configuration started"

    # Check if Zscaler is running
    if ! ps aux | grep -i "[Z]scaler" &> /dev/null; then
        print_info "Zscaler not detected - skipping"
        log_info "Zscaler not running - skipping certificate configuration"
        return 0
    fi

    print_info "Zscaler detected - configuring certificates for Podman..."
    log_info "Zscaler process detected"

    # Create certificate directory
    local cert_dir="${HOME}/.config/containers/certs.d/ghcr.io"
    local cert_file="${cert_dir}/ca.crt"

    mkdir -p "${cert_dir}" || {
        print_error "Failed to create certificate directory"
        log_error "Could not create ${cert_dir}"
        return 1
    }

    # Always extract fresh certificates from macOS keychain (single source of truth)
    if security find-certificate -c "Zscaler" -a -p /Library/Keychains/System.keychain > "${cert_file}" 2>/dev/null; then
        print_success "Zscaler certificates installed from keychain"
        echo "   ${EMOJI_INFO} Certificates will auto-sync to Podman machine during init"
        log_info "Zscaler certificates extracted and installed to ${cert_file}"
    else
        print_error "Failed to extract Zscaler certificates"
        echo ""
        echo "   TROUBLESHOOTING: Verify Zscaler certificates are in System keychain"
        echo "   Test: security find-certificate -c 'Zscaler' /Library/Keychains/System.keychain"
        echo ""
        log_error "Failed to extract Zscaler certificates from keychain"
        return 1
    fi

    echo ""
    return 0
}

################################################################################
# PHASE 6: GITHUB AUTHENTICATION
################################################################################

# Check if user is authenticated to GitHub CLI
check_gh_auth() {
    log_info "Checking GitHub CLI authentication status..."

    # Run gh auth status and capture both stdout and stderr
    # gh auth status returns 0 if authenticated, non-zero if not
    if gh auth status &> /dev/null; then
        # Authenticated - get details
        local gh_user
        gh_user=$(gh api user --jq .login 2>/dev/null || echo "unknown")
        log_info "GitHub CLI authenticated as: ${gh_user}"
        return 0
    else
        log_info "GitHub CLI not authenticated"
        return 1
    fi
}

# Verify GitHub authentication has read:packages scope
check_gh_packages_scope() {
    log_info "Verifying read:packages scope..."

    # Get current token scopes
    # gh auth token returns the token, we can test it against the API
    local token
    token=$(gh auth token 2>/dev/null)

    if [[ -z "${token}" ]]; then
        log_warn "Could not retrieve GitHub token"
        return 1
    fi

    # Test if token has read:packages scope by attempting to list packages
    # This is a lightweight check that validates the scope exists
    if gh api user/packages?package_type=container &> /dev/null; then
        log_info "Token has read:packages scope"
        return 0
    else
        log_warn "Token may be missing read:packages scope"
        return 1
    fi
}

# Perform GitHub CLI authentication with read:packages scope
perform_gh_auth() {
    print_info "Initiating GitHub authentication..."
    echo ""
    echo "${EMOJI_INFO} Authentication Details:"
    echo "   • Method: OAuth via web browser"
    echo "   • Scope: read:packages (required for container registry access)"
    echo "   • Security: Token stored securely by gh CLI"
    echo ""

    log_info "Starting gh auth login with read:packages scope"

    # Initiate gh auth login with read:packages scope
    if gh auth login -s read:packages -w; then
        print_success "GitHub authentication completed"
        log_info "GitHub authentication successful"
        return 0
    else
        local auth_exit_code=$?
        print_error "GitHub authentication failed"
        log_error "gh auth login failed with exit code: ${auth_exit_code}"
        return 1
    fi
}

# Handle stale or invalid GitHub authentication
handle_stale_auth() {
    print_info "Detected stale or invalid authentication"
    echo ""
    echo "${EMOJI_INFO} The current GitHub authentication is invalid or missing required permissions."
    echo "   This can happen if:"
    echo "   • The token has expired"
    echo "   • The token lacks read:packages scope"
    echo "   • Authentication was interrupted previously"
    echo ""
    echo "We'll logout and re-authenticate to fix this."
    echo ""

    log_info "Attempting to fix stale authentication"

    # Logout from GitHub CLI
    print_info "Logging out from GitHub CLI..."
    if gh auth logout --hostname github.com 2>/dev/null; then
        print_success "Logged out successfully"
        log_info "GitHub logout successful"
    else
        print_info "Logout skipped (may not have been logged in)"
        log_warn "GitHub logout failed or was unnecessary"
    fi

    # Perform fresh authentication
    return 0  # Return success - perform_gh_auth will be called next
}

# Configure GitHub authentication
configure_github_auth() {
    print_step "Phase 6: GitHub Authentication"

    print_info "Configuring GitHub authentication for container registry access..."
    echo ""
    echo "${EMOJI_QUESTION} What is GitHub CLI (gh) authentication?"
    echo "   GitHub CLI provides secure authentication to GitHub services using OAuth."
    echo "   This enables access to GitHub Container Registry (ghcr.io) where the"
    echo "   AI assistant container image is stored."
    echo ""
    echo "${EMOJI_INFO} Why is read:packages scope needed?"
    echo "   • Allows downloading container images from ghcr.io"
    echo "   • Required to access: ghcr.io/rise8-us/xpai/ai-assistant-home"
    echo "   • Uses OAuth for security (no passwords stored locally)"
    echo "   • Token stored securely by GitHub CLI"
    echo ""

    log_info "Phase 6: GitHub authentication started"

    # Check if gh CLI is installed
    if ! command -v gh &> /dev/null; then
        print_error "GitHub CLI (gh) not found"
        echo ""
        echo "ERROR: gh command not available"
        echo ""
        echo "GitHub CLI should have been installed in Phase 2."
        echo ""
        print_helpdesk_instructions
        log_error "GitHub CLI not found - prerequisite missing"
        log_error "PATH: ${PATH}"
        log_error "Which gh: $(which gh 2>&1 || echo 'not found')"
        return 1
    fi

    print_success "GitHub CLI found: $(gh --version | head -n1)"
    log_info "GitHub CLI verified: $(gh --version | head -n1)"

    # Check current authentication status
    echo ""
    print_info "Checking GitHub authentication status..."

    local needs_auth=false
    local needs_scope=false

    if check_gh_auth; then
        local gh_user
        gh_user=$(gh api user --jq .login 2>/dev/null || echo "unknown")
        print_success "Already authenticated to GitHub as: ${gh_user}"
        log_info "GitHub authenticated as: ${gh_user}"

        # Check if token has read:packages scope
        if check_gh_packages_scope; then
            print_success "Token has read:packages scope"
            echo ""
            print_success "GitHub authentication already configured correctly!"
            log_info "Phase 6: GitHub authentication completed (already configured)"
            return 0
        else
            print_info "Token may be missing read:packages scope"
            log_warn "Token authentication valid but scope verification unclear"
            needs_scope=true
        fi
    else
        print_info "Not authenticated to GitHub"
        needs_auth=true
    fi

    # Handle authentication based on current state
    if [[ "${needs_auth}" == "true" ]] || [[ "${needs_scope}" == "true" ]]; then
        echo ""

        if [[ "${needs_scope}" == "true" ]]; then
            # Stale or missing scope - automatically re-authenticate
            print_info "Re-authentication required to ensure read:packages scope"
            echo ""
            echo "${EMOJI_INFO} The current GitHub authentication may be missing required permissions."
            echo "   Automatically re-authenticating to ensure correct scope..."
            echo ""
            log_info "Automatically re-authenticating for correct scope"

            # Handle stale auth
            if ! handle_stale_auth; then
                print_error "Failed to logout for re-authentication"
                print_helpdesk_instructions
                log_error "Could not logout for re-authentication"
                return 1
            fi
        fi

        # Perform authentication
        echo ""
        print_info "Starting GitHub authentication flow..."
        echo ""
        echo "${EMOJI_GEAR} What will happen next:"
        echo "   1. Your web browser will open automatically"
        echo "   2. You'll be prompted to login to GitHub (if not already logged in)"
        echo "   3. You'll be asked to authorize GitHub CLI"
        echo "   4. The authorization includes 'read:packages' permission"
        echo "   5. After authorizing, return to this terminal"
        echo ""

        if ! perform_gh_auth; then
            print_error "GitHub authentication failed"
            echo ""
            echo "TROUBLESHOOTING STEPS:"
            echo ""
            echo "Common Issues:"
            echo "  • Browser did not open: Check that you have a default browser set"
            echo "  • Authorization was cancelled: Re-run script and complete authorization"
            echo "  • Network issues: Check your internet connection and GitHub status"
            echo ""
            echo "Manual Authentication:"
            echo "  If automatic authentication fails, try manually:"
            echo "  1. Run: gh auth login -s read:packages"
            echo "  2. Follow the prompts to complete authentication"
            echo "  3. Re-run this script to continue"
            echo ""
            print_helpdesk_instructions
            log_error "GitHub authentication failed"
            return 1
        fi

        # Verify authentication after login
        echo ""
        print_info "Verifying authentication..."

        if check_gh_auth; then
            local gh_user
            gh_user=$(gh api user --jq .login 2>/dev/null || echo "unknown")
            print_success "Successfully authenticated as: ${gh_user}"
            log_info "Authentication verification successful: ${gh_user}"
        else
            print_error "Authentication verification failed"
            echo ""
            echo "Authentication appeared to succeed but verification failed."
            echo ""
            echo "TROUBLESHOOTING:"
            echo "  • Try running: gh auth status"
            echo "  • If that fails, try: gh auth login -s read:packages"
            echo "  • Re-run this script after manual authentication"
            echo ""
            print_helpdesk_instructions
            log_error "Authentication succeeded but verification failed"
            return 1
        fi
    fi

    echo ""
    echo "---"
    print_info "GitHub Authentication Summary:"
    local gh_user
    gh_user=$(gh api user --jq .login 2>/dev/null || echo "unknown")
    echo ""
    echo "   GitHub User: ${gh_user}"
    echo "   Scope: read:packages"
    echo "   Token Storage: Managed securely by gh CLI"
    echo ""

    echo ""
    print_success "GitHub authentication completed!"
    log_info "Phase 6: GitHub authentication completed successfully"
    log_metric "github_user=${gh_user}"
    log_metric "github_auth_completed=true"
    return 0
}

################################################################################
# PHASE 5: ENVIRONMENT CONFIGURATION
################################################################################

# Validate Anthropic API key format
validate_api_key() {
    local api_key=$1

    # Check if empty
    if [[ -z "${api_key}" ]]; then
        return 1
    fi

    # Check format: must start with sk-ant-api03-
    if [[ ! "${api_key}" =~ ^sk-ant-api03- ]]; then
        return 1
    fi

    # Check minimum length (key should be substantial)
    if [[ ${#api_key} -lt 50 ]]; then
        return 1
    fi

    return 0
}

# Mask API key for display (show first 15 chars + asterisks)
mask_api_key() {
    local api_key=$1
    local visible_part="${api_key:0:15}"
    echo "${visible_part}***********************************"
}

# Remove CUI-related sections from .env file
remove_cui_sections_from_env() {
    local env_file=$1

    log_info "Removing CUI-related sections from ${env_file}"

    # Create temporary file
    local temp_file="${env_file}.tmp"

    # Use sed to remove CUI section (from "# CUI Projects" line to line before "# Non-CUI Projects")
    # This is more reliable than awk for this specific task
    sed -n '
        # If we see the CUI Projects header, skip until we see Non-CUI Projects
        /^# CUI Projects/,/^# Non-CUI Projects/ {
            # Print the Non-CUI Projects line when we reach it
            /^# Non-CUI Projects/ p
            # Skip everything else in this range
            d
        }
        # Print all other lines
        p
    ' "${env_file}" > "${temp_file}"

    # Replace original file with modified version
    if mv "${temp_file}" "${env_file}"; then
        log_info "Successfully removed CUI sections from ${env_file}"
        return 0
    else
        log_error "Failed to update ${env_file}"
        rm -f "${temp_file}"
        return 1
    fi
}

# Configure environment variables in .env file
configure_environment() {
    print_step "Phase 5: Environment Configuration"

    log_info "Phase 5: Environment configuration started"

    # Define source and target paths
    local source_file=".env.example"
    local target_file=".env"

    # Check if .env already exists FIRST (before any messaging about API key prompts)
    if [[ -f "${target_file}" ]]; then
        print_info "Existing .env file found - validating configuration..."
        log_info "Existing .env file detected - skipping configuration (idempotent)"

        # Verify permissions are secure
        local current_perms
        current_perms=$(stat -f "%Lp" "${target_file}" 2>/dev/null || stat -c "%a" "${target_file}" 2>/dev/null)

        if [[ "${current_perms}" != "600" ]]; then
            print_info "Fixing .env file permissions..."
            if chmod 600 "${target_file}"; then
                print_success "Permissions updated to 600 (owner read/write only)"
                log_info "Fixed .env permissions: 600"
            else
                print_error "Failed to update permissions"
                log_error "Could not update .env permissions"
            fi
        else
            print_success "File permissions are secure (600)"
            log_info ".env permissions verified: 600"
        fi

        echo ""
        print_success "Environment configuration validated!"
        log_info "Phase 5: Environment configuration completed (existing file kept)"
        return 0
    fi

    # Only show these messages if we need to create .env
    print_info "Configuring environment variables..."
    echo ""
    echo "${EMOJI_QUESTION} What is the .env file?"
    echo "   The .env file stores environment-specific configuration like your"
    echo "   API credentials. This file is never committed to git for security reasons."
    echo ""
    echo "${EMOJI_INFO} This process will:"
    echo "   • Create .env from .env.example template"
    echo "   • Securely prompt for your Anthropic API key (input will be hidden)"
    echo "   • Remove CUI-related configuration (not needed for non-CUI projects)"
    echo "   • Set restrictive permissions (600 - owner read/write only)"
    echo ""

    # Check if source file exists
    if [[ ! -f "${source_file}" ]]; then
        print_error "Source file not found: ${source_file}"
        echo ""
        echo "ERROR: Cannot configure environment - template file missing"
        echo ""
        echo "Expected file: ${source_file}"
        echo ""
        print_helpdesk_instructions
        log_error "Environment configuration source file not found: ${source_file}"
        log_error "Current directory: $(pwd)"
        log_error "Directory contents: $(ls -la . 2>&1 || echo 'cannot list')"
        return 1
    fi

    print_success "Template file found: ${source_file}"
    log_info "Source file verified: ${source_file}"

    # Copy template to .env
    print_info "Creating .env from template..."
    if cp "${source_file}" "${target_file}"; then
        print_success ".env file created"
        log_info "Copied ${source_file} to ${target_file}"
    else
        print_error "Failed to create .env file"
        echo ""
        print_helpdesk_instructions
        log_error "Failed to copy ${source_file} to ${target_file}"
        log_error "Source file permissions: $(ls -l "${source_file}" 2>&1 || echo 'cannot stat')"
        log_error "Target directory permissions: $(ls -ld . 2>&1 || echo 'cannot stat')"
        return 1
    fi

    echo ""
    echo "---"
    print_info "Configuration Input Required"
    echo ""

    # Prompt for ANTHROPIC_API_KEY
    local api_key=""

    echo "${EMOJI_GEAR} ANTHROPIC_API_KEY"
    echo "   Your personal Anthropic API key for accessing Claude."
    echo "   Format: sk-ant-api03-..."
    echo "   Security: Your input will be hidden (not displayed on screen)"
    echo ""
    echo "   ${EMOJI_INFO} If you don't have an API key yet:"
    echo "   File a #helpdesk ticket requesting an Anthropic API key"
    echo ""

    # Loop until valid API key is provided
    while true; do
        read -r -s -p "Anthropic API key: " api_key
        echo ""  # New line after hidden input

        # Check if empty
        if [[ -z "${api_key}" ]]; then
            print_error "API key cannot be empty"
            echo ""
            continue
        fi

        # Validate API key
        if validate_api_key "${api_key}"; then
            print_success "Valid API key format"
            log_info "API key format validated (key not logged for security)"
            break
        else
            print_error "Invalid API key format"
            echo "   Requirements:"
            echo "   • Must start with: sk-ant-api03-"
            echo "   • Must be at least 50 characters long"
            echo "   • Check for typos or request a new key from #helpdesk"
            echo ""
        fi
    done

    echo ""
    echo "---"
    print_info "Writing configuration to .env file..."

    # Update ANTHROPIC_API_KEY in .env file
    # Replace empty ANTHROPIC_API_KEY= with the actual key
    if sed -i.bak "s/^ANTHROPIC_API_KEY=$/ANTHROPIC_API_KEY=${api_key}/" "${target_file}"; then
        log_info "Updated ANTHROPIC_API_KEY in .env (value not logged)"
    else
        print_error "Failed to update ANTHROPIC_API_KEY"
        log_error "sed command failed for ANTHROPIC_API_KEY"
        # Continue anyway
    fi

    # Remove backup files created by sed
    rm -f "${target_file}.bak"

    # Remove CUI-related sections from .env
    print_info "Removing CUI-related sections..."
    if remove_cui_sections_from_env "${target_file}"; then
        print_success "CUI sections removed"
    else
        print_error "Failed to remove CUI sections (non-critical)"
        log_warn "Could not remove CUI sections from .env (non-critical)"
    fi

    # Set restrictive permissions (600 - owner read/write only)
    print_info "Setting secure file permissions..."
    if chmod 600 "${target_file}"; then
        print_success "Permissions set to 600 (owner read/write only)"
        log_info "Set .env permissions to 600"
    else
        print_error "Failed to set secure permissions"
        echo ""
        echo "SECURITY WARNING: Could not set restrictive permissions on .env file"
        echo ""
        echo "Please manually run: chmod 600 ${target_file}"
        echo ""
        log_error "Failed to chmod 600 on .env file"
    fi

    # Verify .env is in .gitignore
    print_info "Verifying .env is excluded from git..."
    if [[ -f ".gitignore" ]]; then
        if grep -q "^\.env$" .gitignore; then
            print_success ".env is in .gitignore (secure)"
            log_info ".env verified in .gitignore"
        else
            print_error ".env not found in .gitignore"
            echo ""
            echo "SECURITY WARNING: .env should be in .gitignore to prevent accidental commits"
            echo ""
            echo "This is unusual - check your .gitignore file"
            echo ""
            log_error ".env not found in .gitignore - security risk"
        fi
    else
        print_error ".gitignore file not found"
        log_warn ".gitignore file not present in project"
    fi

    # Clear API key from memory (security best practice)
    unset api_key
    log_info "Cleared API key from memory"

    # Display configuration summary (with masked key)
    echo ""
    echo "---"
    print_info "Configuration Summary:"
    echo ""
    echo "   ANTHROPIC_API_KEY: $(mask_api_key "$(grep '^ANTHROPIC_API_KEY=' "${target_file}" | cut -d'=' -f2)")"
    echo ""
    echo "   File: ${target_file}"
    echo "   Permissions: 600 (owner read/write only)"
    echo ""

    echo ""
    print_success "Environment configuration completed!"
    log_info "Phase 5: Environment configuration completed successfully"
    log_metric "env_file_created=true"
    return 0
}

################################################################################
# PHASE 7: CONTAINER REGISTRY AUTHENTICATION
################################################################################

# Check if already authenticated to container registry
check_registry_auth() {
    local registry=$1
    log_info "Checking authentication status for ${registry}..."

    # Check if logged in by inspecting podman auth file
    # This is more reliable than trying to pull, which could fail for other reasons
    if podman login --get-login "${registry}" &> /dev/null; then
        local username
        username=$(podman login --get-login "${registry}" 2>/dev/null || echo "")
        if [[ -n "${username}" ]]; then
            log_info "Already authenticated to ${registry} as: ${username}"
            return 0
        fi
    fi

    log_info "Not authenticated to ${registry}"
    return 1
}

# Authenticate to GitHub Container Registry
configure_container_registry_auth() {
    print_step "Phase 7: Container Registry Authentication"

    print_info "Configuring GitHub Container Registry (ghcr.io) authentication..."
    echo ""
    echo "${EMOJI_QUESTION} What is GitHub Container Registry (ghcr.io)?"
    echo "   GitHub Container Registry (ghcr.io) is a service for hosting and"
    echo "   distributing container images. It's where the AI assistant container"
    echo "   images are stored and version-controlled."
    echo ""
    echo "${EMOJI_INFO} Why is authentication needed?"
    echo "   • Access to organization images: ghcr.io/rise8-us/xpai/ai-assistant-home"
    echo "   • Uses your GitHub credentials (already configured in Phase 6)"
    echo "   • Enables pulling container images for development"
    echo "   • Required for DevContainer and Podman operations"
    echo ""

    log_info "Phase 7: Container registry authentication started"

    # Verify prerequisites
    if ! command -v podman &> /dev/null; then
        print_error "Podman not found"
        echo ""
        echo "ERROR: podman command not available"
        echo ""
        echo "Podman should have been installed in Phase 2."
        echo ""
        print_helpdesk_instructions
        log_error "Podman not found - prerequisite missing"
        log_error "PATH: ${PATH}"
        log_error "Which podman: $(which podman 2>&1 || echo 'not found')"
        return 1
    fi

    print_success "Podman found: $(podman --version | head -n1)"
    log_info "Podman verified: $(podman --version | head -n1)"

    if ! command -v gh &> /dev/null; then
        print_error "GitHub CLI (gh) not found"
        echo ""
        echo "ERROR: gh command not available"
        echo ""
        echo "GitHub CLI should have been installed in Phase 2."
        echo ""
        print_helpdesk_instructions
        log_error "GitHub CLI not found - prerequisite missing"
        log_error "PATH: ${PATH}"
        log_error "Which gh: $(which gh 2>&1 || echo 'not found')"
        return 1
    fi

    print_success "GitHub CLI found: $(gh --version | head -n1)"
    log_info "GitHub CLI verified: $(gh --version | head -n1)"

    # Check if already authenticated
    echo ""
    print_info "Checking registry authentication status..."

    local registry="ghcr.io"

    if check_registry_auth "${registry}"; then
        local username
        username=$(podman login --get-login "${registry}" 2>/dev/null || echo "unknown")
        print_success "Already authenticated to ${registry} as: ${username}"
        echo ""
        print_success "Container registry authentication already configured!"
        log_info "Phase 7: Container registry authentication completed (already configured)"
        return 0
    fi

    print_info "Not authenticated to ${registry} - authenticating now..."

    # Get GitHub username for login
    local gh_user
    if ! gh_user=$(gh api user --jq .login 2>/dev/null); then
        print_error "Failed to get GitHub username"
        echo ""
        echo "ERROR: Could not retrieve GitHub username from gh CLI"
        echo ""
        echo "TROUBLESHOOTING:"
        echo "  • Check that GitHub authentication is working: gh auth status"
        echo "  • If authentication expired, re-run Phase 6 or run: gh auth login -s read:packages"
        echo "  • Verify network connectivity to GitHub"
        echo ""
        print_helpdesk_instructions
        log_error "Failed to retrieve GitHub username via gh CLI"
        log_error "gh auth status: $(gh auth status 2>&1 || echo 'failed')"
        return 1
    fi

    print_success "GitHub username: ${gh_user}"
    log_info "Retrieved GitHub username: ${gh_user}"

    # Authenticate to container registry using gh CLI token
    echo ""
    print_info "Authenticating to ${registry}..."
    echo "   Username: ${gh_user}"
    echo "   Authentication: Using gh CLI token (secure)"
    echo ""
    log_info "Attempting podman login to ${registry} as ${gh_user}"

    # Execute podman login with gh token
    local login_output
    local login_exit_code

    if login_output=$(gh auth token 2>/dev/null | podman login "${registry}" -u "${gh_user}" --password-stdin 2>&1); then
        login_exit_code=0
    else
        login_exit_code=$?
    fi

    if [[ ${login_exit_code} -eq 0 ]]; then
        print_success "Successfully authenticated to ${registry}"
        log_info "Container registry authentication successful"
        log_info "Registry: ${registry}, User: ${gh_user}"

        # Verify authentication worked
        if check_registry_auth "${registry}"; then
            print_success "Authentication verified"
            log_info "Registry authentication verification successful"
        else
            print_error "Authentication verification failed"
            log_error "podman login succeeded but verification check failed"
            log_error "This may be a transient issue - proceeding anyway"
        fi
    else
        # Authentication failed - check for specific errors
        print_error "Failed to authenticate to ${registry}"
        log_error "podman login failed with exit code: ${login_exit_code}"
        log_error "Login output: ${login_output}"

        echo ""

        # Check for organization access denied error
        if echo "${login_output}" | grep -qi "unauthorized.*access denied"; then
            echo "ERROR: Organization Access Denied"
            echo ""
            echo "You are authenticated to GitHub but do not have access to the"
            echo "rise8-us/XPai organization container registry."
            echo ""
            echo "REMEDIATION STEPS:"
            echo ""
            echo "  1. Contact your administrator or team lead"
            echo "  2. Request access to the rise8-us/XPai organization on GitHub"
            echo "  3. Verify your GitHub account (${gh_user}) has been added to the organization"
            echo "  4. Wait for the organization invite and accept it"
            echo "  5. Re-run this script after access is granted"
            echo ""
            echo "HOW TO CHECK:"
            echo "  • Visit: https://github.com/rise8-us"
            echo "  • If you see the organization, you have access"
            echo "  • If prompted to request access, do so and wait for approval"
            echo ""
            log_error "Organization access denied for user: ${gh_user}"
            log_error "User needs to be added to rise8-us/XPai organization"
        else
            echo "ERROR: Container registry authentication failed"
            echo ""
            echo "TROUBLESHOOTING:"
            echo ""
            echo "Common Issues:"
            echo "  • GitHub token expired: Re-run Phase 6 or: gh auth login -s read:packages"
            echo "  • Network connectivity: Check internet connection and GitHub status"
            echo "  • Podman not running: Verify Podman machine is running: podman machine list"
            echo ""
        fi

        print_helpdesk_instructions
        log_error "Container registry authentication failed"
        log_error "GitHub user: ${gh_user}"
        log_error "Registry: ${registry}"
        log_error "Podman machine status: $(podman machine list 2>&1 || echo 'failed')"
        log_error "gh auth status: $(gh auth status 2>&1 || echo 'failed')"
        return 1
    fi

    echo ""
    echo "---"
    print_info "Container Registry Authentication Summary:"
    echo ""
    echo "   Registry: ${registry}"
    echo "   GitHub User: ${gh_user}"
    echo "   Status: Authenticated"
    echo "   Access: Can pull container images from rise8-us/XPai"
    echo ""

    echo ""
    print_success "Container registry authentication completed!"
    log_info "Phase 7: Container registry authentication completed successfully"
    log_metric "registry=${registry}"
    log_metric "registry_user=${gh_user}"
    log_metric "registry_auth_completed=true"
    return 0
}

################################################################################
# PHASE 8: SETUP VERIFICATION
################################################################################

# Verify setup is complete and functional
verify_setup() {
    print_step "Phase 8: Setup Verification"

    print_info "Verifying your development environment is ready..."
    echo ""
    echo "${EMOJI_QUESTION} What does verification check?"
    echo "   This phase ensures all components are properly configured and"
    echo "   can communicate with each other. It validates that you have a"
    echo "   fully functional development environment."
    echo ""
    echo "${EMOJI_INFO} Verification checks:"
    echo "   • Podman daemon communication"
    echo "   • Configuration files exist and are valid"
    echo "   • File permissions are secure"
    echo ""

    log_info "Phase 8: Setup verification started"

    # Track verification results
    local verification_failed=false
    local warning_count=0

    # Check 1: Podman daemon communication
    echo ""
    print_info "Checking Podman daemon communication..."

    if ! command -v podman &> /dev/null; then
        print_error "Podman command not found"
        log_error "Verification failed: podman command not available"
        verification_failed=true
    else
        # Check if podman machine is running
        if podman machine list --format "{{.Name}}\t{{.Running}}" 2>/dev/null | grep -q "podman-machine-default.*true"; then
            print_success "Podman machine is running"
            log_info "Verification: Podman machine running"

            # Try podman info to verify daemon communication
            if podman info &> /dev/null; then
                print_success "Podman daemon communication verified"
                log_info "Verification: Podman daemon communication successful"
            else
                print_error "Podman daemon not responding"
                echo "   Podman is installed but cannot communicate with the daemon"
                log_error "Verification failed: podman info command failed"
                verification_failed=true
            fi
        else
            print_error "Podman machine is not running"
            echo ""
            echo "REMEDIATION:"
            echo "   Start the Podman machine with:"
            echo "   podman machine start"
            echo ""
            log_error "Verification failed: Podman machine not running"
            verification_failed=true
        fi
    fi

    # Check 2: Configuration files exist
    echo ""
    print_info "Checking configuration files..."

    # Check .env file
    if [[ ! -f ".env" ]]; then
        print_error ".env file not found"
        echo "   Expected location: $(pwd)/.env"
        log_error "Verification failed: .env file not found"
        verification_failed=true
    else
        print_success ".env file exists"
        log_info "Verification: .env file found"
    fi

    # Check .devcontainer/devcontainer.json
    if [[ ! -f ".devcontainer/devcontainer.json" ]]; then
        print_error ".devcontainer/devcontainer.json not found"
        echo "   Expected location: $(pwd)/.devcontainer/devcontainer.json"
        log_error "Verification failed: devcontainer.json not found"
        verification_failed=true
    else
        print_success ".devcontainer/devcontainer.json exists"
        log_info "Verification: devcontainer.json file found"
    fi

    # Check 3: File permissions
    echo ""
    print_info "Checking file permissions..."

    if [[ -f ".env" ]]; then
        local env_perms
        env_perms=$(stat -f "%Lp" ".env" 2>/dev/null || stat -c "%a" ".env" 2>/dev/null)

        if [[ "${env_perms}" == "600" ]]; then
            print_success ".env file has secure permissions (600)"
            log_info "Verification: .env permissions correct (600)"
        else
            print_error ".env file has incorrect permissions: ${env_perms}"
            echo ""
            echo "REMEDIATION:"
            echo "   Fix permissions with:"
            echo "   chmod 600 .env"
            echo ""
            echo "   This ensures your API keys are only readable by you."
            echo ""
            log_error "Verification failed: .env permissions incorrect (${env_perms}, expected 600)"
            verification_failed=true
        fi
    fi

    # Check 4: Validate .env contents
    echo ""
    print_info "Validating .env configuration..."

    if [[ -f ".env" ]]; then
        # Check ANTHROPIC_API_KEY is set (and not placeholder or commented)
        if grep -q "^ANTHROPIC_API_KEY=sk-ant-api03-" ".env"; then
            print_success "ANTHROPIC_API_KEY is configured"
            log_info "Verification: ANTHROPIC_API_KEY is set"
        elif grep -q "^#ANTHROPIC_API_KEY=" ".env" || ! grep -q "^ANTHROPIC_API_KEY=" ".env"; then
            print_error "ANTHROPIC_API_KEY not configured (commented or missing)"
            echo ""
            echo "REMEDIATION:"
            echo "   1. Edit the .env file: nano .env"
            echo "   2. Uncomment or add the line: ANTHROPIC_API_KEY=sk-ant-api03-..."
            echo "   3. Replace with your actual API key"
            echo "   4. Save and re-run verification"
            echo ""
            echo "   If you don't have an API key:"
            echo "   File a #helpdesk ticket requesting an Anthropic API key"
            echo ""
            log_error "Verification failed: ANTHROPIC_API_KEY not configured (commented or missing)"
            verification_failed=true
        else
            print_error "ANTHROPIC_API_KEY has placeholder or invalid value"
            echo "   Make sure .env contains:"
            echo "   ANTHROPIC_API_KEY=sk-ant-api03-..."
            echo "   (not a placeholder like 'your-key-here' or 'sk-ant-api03-PLACEHOLDER')"
            log_error "Verification failed: ANTHROPIC_API_KEY not properly configured"
            verification_failed=true
        fi
    fi

    # Summary of verification results
    echo ""
    echo "---"
    print_info "Verification Summary:"
    echo ""

    if [[ "${verification_failed}" == "true" ]]; then
        print_error "Setup verification failed - some checks did not pass"
        echo ""
        echo "NEXT STEPS:"
        echo "   1. Review the errors above"
        echo "   2. Follow the remediation steps provided"
        echo "   3. Re-run this script to verify fixes: ./scripts/onboard.sh"
        echo "   4. If issues persist, check the log file: ${LOG_FILE}"
        echo ""
        echo "   Need help? File a #helpdesk ticket with:"
        echo "   • This error message"
        echo "   • The log file: ${LOG_FILE}"
        echo ""
        log_error "Phase 8: Setup verification completed with failures"
        return 1
    else
        print_success "All verification checks passed!"
        echo ""
        log_info "Phase 8: Setup verification completed successfully"
        return 0
    fi
}

################################################################################
# MAIN EXECUTION
################################################################################

main() {
    local start_time
    start_time=$(date +%s)

    # Initialize logging
    init_log

    log_info "Onboarding process started"

    # Phase 0: Validate prerequisites
    validate_prerequisites

    # Display terminal warning
    display_terminal_warning

    # Phase 1: Install Homebrew
    install_homebrew

    # Phase 2: Install tools (includes Zscaler cert config for Podman)
    install_tools

    # Phase 3: Cleanup CUI files
    cleanup_cui_files

    # Phase 4: Configure DevContainer
    configure_devcontainer

    # Phase 5: Environment Configuration
    configure_environment

    # Phase 6: GitHub Authentication
    configure_github_auth

    # Phase 7: Container Registry Authentication
    configure_container_registry_auth

    # Phase 8: Setup Verification
    if ! verify_setup; then
        echo ""
        print_error "Setup verification failed"
        echo ""
        echo "The onboarding process completed, but verification found issues."
        echo "Please review the errors above and follow the remediation steps."
        echo ""
        log_error "Onboarding completed but verification failed"
        exit 1
    fi

    # Calculate elapsed time
    local end_time
    end_time=$(date +%s)
    local elapsed=$((end_time - start_time))
    local elapsed_minutes=$((elapsed / 60))

    # Final summary
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║  Setup Complete! ${EMOJI_CHECK}                                       ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    print_success "Onboarding completed successfully!"
    echo ""
    echo "${EMOJI_INFO} What was accomplished:"
    echo "   ${EMOJI_CHECK} Platform validated (ARM64 macOS)"
    echo "   ${EMOJI_CHECK} Prerequisites verified (Xcode CLI Tools, git)"
    echo "   ${EMOJI_CHECK} Homebrew installed and configured"
    echo "   ${EMOJI_CHECK} Podman installed and machine initialized"
    echo "   ${EMOJI_CHECK} Podman auto-start configured (starts on login)"
    echo "   ${EMOJI_CHECK} Docker symlink created (docker -> podman)"
    echo "   ${EMOJI_CHECK} Zscaler certificates configured (if Zscaler detected)"
    echo "   ${EMOJI_CHECK} GitHub CLI installed"
    echo "   ${EMOJI_CHECK} VSCode installed"
    echo "   ${EMOJI_CHECK} CUI files cleaned up (non-CUI project setup)"
    echo "   ${EMOJI_CHECK} DevContainer configured for non-CUI projects"
    echo "   ${EMOJI_CHECK} Environment variables configured (.env file created)"
    echo "   ${EMOJI_CHECK} GitHub authenticated with read:packages scope"
    echo "   ${EMOJI_CHECK} Container registry authenticated (ghcr.io)"
    echo "   ${EMOJI_CHECK} Setup verification passed"
    echo ""
    echo "⏱️  Setup time: ${elapsed_minutes} minutes"
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║  NEXT STEPS                                               ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "${EMOJI_GEAR} Open Your Development Environment:"
    echo ""

    # Simple, clear instruction
    echo "   1. Close this terminal window"
    echo "   2. Open a new terminal window"
    echo "   3. Navigate to your project:"
    echo -e "      ${COLOR_CYAN}cd $(pwd)${COLOR_RESET}"
    echo "   4. Open in VS Code:"
    echo -e "      ${COLOR_CYAN}code .${COLOR_RESET}"
    echo ""

    echo ""
    echo "   When VSCode opens, you'll see a notification:"
    echo "      \"Folder contains a Dev Container configuration file.\""
    echo ""
    echo "   Click \"Reopen in Container\" to start the development environment"
    echo "      (First time will download the container image - may take 5-15 minutes)"
    echo ""
    echo "   Alternative: Use the Command Palette"
    echo "      • Press: Cmd+Shift+P (macOS)"
    echo "      • Type: \"Dev Containers: Reopen in Container\""
    echo "      • Press Enter"
    echo ""
    echo "${EMOJI_INFO} What happens next?"
    echo "   • VSCode will rebuild the devcontainer (automatic)"
    echo "   • Your project will be ready inside the container"
    echo "   • All AI assistants and tools will be pre-installed"
    echo "   • You can start developing immediately!"
    echo ""
    echo "${EMOJI_INFO} Troubleshooting:"
    echo "   If you encounter issues:"
    echo "   • VSCode should auto-install the \"Dev Containers\" extension on first open"
    echo "   • Verify Podman is running: podman machine list"
    echo "   • Review the log file: ${LOG_FILE}"
    echo "   • File a #helpdesk ticket if problems persist"
    echo ""
    echo "📝 Log file: ${LOG_FILE}"
    echo ""

    log_metric "setup_time_seconds=${elapsed}"
    log_metric "status=success"
    log_info "Onboarding script completed successfully"
}

# Execute main function
main "$@"
