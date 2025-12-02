#!/bin/bash

# Workflow Validation Script
# Validates the integrity of the Claude task workflow system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Base directory
CLAUDE_DIR="/.claude/tasks"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo -e "${BLUE}🔍 Claude Workflow Validation${NC}"
echo "Project: $PROJECT_ROOT"
echo "Validating: $PROJECT_ROOT$CLAUDE_DIR"
echo

# Check if .claude directory exists
if [ ! -d "$PROJECT_ROOT$CLAUDE_DIR" ]; then
    echo -e "${RED}❌ ERROR: .claude/tasks directory not found${NC}"
    echo "Expected: $PROJECT_ROOT$CLAUDE_DIR"
    exit 1
fi

# Initialize counters
ERRORS=0
WARNINGS=0
CHECKS=0

# Function to report error
error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
    ((ERRORS++))
}

# Function to report warning
warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
    ((WARNINGS++))
}

# Function to report success
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to increment check counter
check() {
    ((CHECKS++))
}

echo "1. Validating Directory Structure..."

# Check required directories
for dir in "1_backlog" "2_active" "3_completed" "templates"; do
    check
    if [ -d "$PROJECT_ROOT$CLAUDE_DIR/$dir" ]; then
        success "Directory exists: $dir/"
    else
        error "Missing required directory: $dir/"
    fi
done

echo

echo "2. Validating File Naming Conventions..."

# Check backlog files
check
backlog_prds=($(find "$PROJECT_ROOT$CLAUDE_DIR/1_backlog" -name "prd-*.md" 2>/dev/null || true))
backlog_tasks=($(find "$PROJECT_ROOT$CLAUDE_DIR/1_backlog" -name "tasks-prd-*.md" 2>/dev/null || true))

for prd_file in "${backlog_prds[@]}"; do
    prd_name=$(basename "$prd_file" .md)
    expected_task_file="$PROJECT_ROOT$CLAUDE_DIR/1_backlog/tasks-$prd_name.md"

    check
    if [ -f "$expected_task_file" ]; then
        success "Matching task file found: $(basename "$expected_task_file")"
    else
        error "Missing task file for PRD: $(basename "$prd_file")"
        echo "       Expected: tasks-$prd_name.md"
    fi
done

# Check active files
check
active_prds=($(find "$PROJECT_ROOT$CLAUDE_DIR/2_active" -name "prd-*.md" 2>/dev/null || true))
active_tasks=($(find "$PROJECT_ROOT$CLAUDE_DIR/2_active" -name "tasks-prd-*.md" 2>/dev/null || true))

for prd_file in "${active_prds[@]}"; do
    prd_name=$(basename "$prd_file" .md)
    expected_task_file="$PROJECT_ROOT$CLAUDE_DIR/2_active/tasks-$prd_name.md"

    check
    if [ -f "$expected_task_file" ]; then
        success "Matching task file found: $(basename "$expected_task_file")"
    else
        error "Missing task file for PRD: $(basename "$prd_file")"
        echo "       Expected: tasks-$prd_name.md"
    fi
done

echo

echo "3. Validating Completed Features..."

# Check completed folders
check
completed_dirs=($(find "$PROJECT_ROOT$CLAUDE_DIR/3_completed" -maxdepth 1 -type d -name "[0-9][0-9][0-9]-*" 2>/dev/null || true))

for completed_dir in "${completed_dirs[@]}"; do
    dir_name=$(basename "$completed_dir")

    # Check for required files in completed directory
    prd_files=($(find "$completed_dir" -name "prd-*.md" 2>/dev/null || true))
    task_files=($(find "$completed_dir" -name "tasks-prd-*.md" 2>/dev/null || true))

    check
    if [ ${#prd_files[@]} -eq 1 ] && [ ${#task_files[@]} -eq 1 ]; then
        success "Completed feature has required files: $dir_name"
    else
        error "Completed feature missing files: $dir_name"
        echo "       Found PRD files: ${#prd_files[@]}"
        echo "       Found task files: ${#task_files[@]}"
        echo "       Expected: 1 PRD file and 1 task file"
    fi

    # Check for implementation notes
    check
    if [ -f "$completed_dir/implementation-notes.md" ]; then
        success "Implementation notes found: $dir_name"
    else
        warning "Missing implementation notes: $dir_name"
    fi
done

echo

echo "4. Validating Project Status..."

# Check project-status.md exists and is up to date
check
status_file="$PROJECT_ROOT$CLAUDE_DIR/project-status.md"
if [ -f "$status_file" ]; then
    success "Project status file exists"

    # Count actual vs reported features
    actual_completed=${#completed_dirs[@]}
    actual_active=${#active_prds[@]}
    actual_backlog=${#backlog_prds[@]}

    # Extract numbers from status file (basic check)
    if grep -q "Completed Features.*: $actual_completed" "$status_file" 2>/dev/null; then
        success "Completed features count matches: $actual_completed"
    else
        warning "Completed features count may be out of sync in project-status.md"
    fi

    check
    if grep -q "Active Features.*: $actual_active" "$status_file" 2>/dev/null; then
        success "Active features count matches: $actual_active"
    else
        warning "Active features count may be out of sync in project-status.md"
    fi

    check
    if grep -q "Backlog Features.*: $actual_backlog" "$status_file" 2>/dev/null; then
        success "Backlog features count matches: $actual_backlog"
    else
        warning "Backlog features count may be out of sync in project-status.md"
    fi
else
    error "Missing project-status.md file"
fi

echo

echo "5. Validating Template Files..."

# Check template files exist
for template in "prd-template.md" "tasks-template.md" "implementation-notes-template.md"; do
    check
    if [ -f "$PROJECT_ROOT$CLAUDE_DIR/templates/$template" ]; then
        success "Template exists: $template"
    else
        warning "Missing template: $template"
    fi
done

echo

# Summary
echo "📋 Validation Summary:"
echo "   Checks performed: $CHECKS"
echo -e "   ${GREEN}Successes: $((CHECKS - ERRORS - WARNINGS))${NC}"
if [ $WARNINGS -gt 0 ]; then
    echo -e "   ${YELLOW}Warnings: $WARNINGS${NC}"
fi
if [ $ERRORS -gt 0 ]; then
    echo -e "   ${RED}Errors: $ERRORS${NC}"
fi

echo

if [ $ERRORS -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}🎉 All workflow validations passed!${NC}"
        exit 0
    else
        echo -e "${YELLOW}✅ Workflow validation completed with warnings${NC}"
        exit 0
    fi
else
    echo -e "${RED}❌ Workflow validation failed with $ERRORS errors${NC}"
    exit 1
fi