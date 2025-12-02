#!/bin/bash

# Task Dependency Checker
# Validates task dependencies and identifies potential issues

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

echo -e "${BLUE}🔗 Task Dependency Analysis${NC}"
echo "Project: $PROJECT_ROOT"
echo

# Initialize counters
ISSUES=0
WARNINGS=0
ANALYZED=0

# Function to report issue
issue() {
    echo -e "${RED}🔴 ISSUE: $1${NC}"
    ((ISSUES++))
}

# Function to report warning
warning() {
    echo -e "${YELLOW}🟡 WARNING: $1${NC}"
    ((WARNINGS++))
}

# Function to report info
info() {
    echo -e "${GREEN}🟢 $1${NC}"
}

echo "1. Analyzing Active Tasks..."

# Find all active task files
active_task_files=($(find "$PROJECT_ROOT$CLAUDE_DIR/2_active" -name "tasks-prd-*.md" 2>/dev/null || true))

if [ ${#active_task_files[@]} -eq 0 ]; then
    info "No active tasks found"
    echo
else
    for task_file in "${active_task_files[@]}"; do
        ((ANALYZED++))
        task_name=$(basename "$task_file" .md | sed 's/tasks-prd-//')

        echo "📋 Analyzing: $task_name"

        # Check for incomplete parent tasks with completed subtasks
        if [ -f "$task_file" ]; then
            # Extract task structure and check for inconsistencies
            awk '
            /^- \[ \] [0-9]+\.[0-9]+ / {
                parent_line = $0
                parent_complete = 0
                parent_task = $0
                subtask_count = 0
                completed_subtasks = 0
                getline
                while (getline && match($0, /^  - \[/)) {
                    subtask_count++
                    if (match($0, /^  - \[x\]/)) {
                        completed_subtasks++
                    }
                }
                if (subtask_count > 0 && completed_subtasks == subtask_count && parent_complete == 0) {
                    print "INCONSISTENCY: Parent task incomplete but all subtasks complete: " parent_task
                }
                if (subtask_count > 8) {
                    print "WARNING: Parent task has too many subtasks (" subtask_count "): " parent_task
                }
            }
            /^- \[x\] [0-9]+\.[0-9]+ / {
                parent_line = $0
                parent_complete = 1
                parent_task = $0
                subtask_count = 0
                completed_subtasks = 0
                getline
                while (getline && match($0, /^  - \[/)) {
                    subtask_count++
                    if (match($0, /^  - \[ \]/)) {
                        print "INCONSISTENCY: Parent task complete but has incomplete subtasks: " parent_task
                    }
                }
            }
            ' "$task_file" | while read line; do
                if [[ $line == INCONSISTENCY:* ]]; then
                    issue "${line#INCONSISTENCY: }"
                elif [[ $line == WARNING:* ]]; then
                    warning "${line#WARNING: }"
                fi
            done

            # Check for missing agent assignments
            if ! grep -q "Assigned Agent:" "$task_file" 2>/dev/null; then
                warning "No agent assignments found in $task_name"
            fi

            # Check for orphaned subtasks (subtasks without parent tasks)
            orphaned_subtasks=$(grep -n "^  - \[" "$task_file" | head -1)
            if [ -n "$orphaned_subtasks" ] && ! grep -B1 "^  - \[" "$task_file" | grep -q "^- \["; then
                warning "Potential orphaned subtasks found in $task_name"
            fi
        fi

        echo
    done
fi

echo "2. Checking for Task Conflicts..."

# Check for duplicate task names across active and backlog
all_task_files=($(find "$PROJECT_ROOT$CLAUDE_DIR/2_active" "$PROJECT_ROOT$CLAUDE_DIR/1_backlog" -name "tasks-prd-*.md" 2>/dev/null || true))
declare -A task_names

for task_file in "${all_task_files[@]}"; do
    task_name=$(basename "$task_file" .md | sed 's/tasks-prd-//')
    if [ -n "${task_names[$task_name]}" ]; then
        issue "Duplicate task name found: $task_name"
        echo "       Locations: ${task_names[$task_name]} and $task_file"
    else
        task_names[$task_name]="$task_file"
    fi
done

echo

echo "3. Analyzing Agent Workload..."

# Extract agent assignments and check for overloading
declare -A agent_workload

for task_file in "${active_task_files[@]}"; do
    if [ -f "$task_file" ]; then
        # Count tasks per agent
        while IFS= read -r line; do
            if [[ $line =~ Assigned\ Agent.*:\ ([a-zA-Z-]+) ]]; then
                agent="${BASH_REMATCH[1]}"
                ((agent_workload[$agent]++))
            fi
        done < "$task_file"
    fi
done

if [ ${#agent_workload[@]} -gt 0 ]; then
    echo "Agent Task Distribution:"
    for agent in "${!agent_workload[@]}"; do
        count=${agent_workload[$agent]}
        if [ $count -gt 10 ]; then
            warning "$agent has high task load: $count tasks"
        else
            info "$agent: $count tasks"
        fi
    done
else
    warning "No agent assignments found in active tasks"
fi

echo

echo "4. Checking Task Complexity..."

for task_file in "${active_task_files[@]}"; do
    if [ -f "$task_file" ]; then
        task_name=$(basename "$task_file" .md | sed 's/tasks-prd-//')

        # Count total tasks and subtasks
        parent_count=$(grep -c "^- \[" "$task_file" 2>/dev/null || echo 0)
        subtask_count=$(grep -c "^  - \[" "$task_file" 2>/dev/null || echo 0)
        total_tasks=$((parent_count + subtask_count))

        if [ $total_tasks -gt 30 ]; then
            warning "$task_name has high complexity: $total_tasks total tasks"
        elif [ $total_tasks -gt 20 ]; then
            info "$task_name has moderate complexity: $total_tasks total tasks"
        else
            info "$task_name has manageable complexity: $total_tasks total tasks"
        fi
    fi
done

echo

echo "5. Validating Agent Availability..."

# Check if assigned agents exist in the agents directory
agents_dir="$PROJECT_ROOT/.claude/agents"
if [ -d "$agents_dir" ]; then
    available_agents=($(find "$agents_dir" -name "*.md" -exec basename {} .md \; 2>/dev/null || true))

    for task_file in "${active_task_files[@]}"; do
        if [ -f "$task_file" ]; then
            # Extract unique agent assignments
            assigned_agents=($(grep "Assigned Agent:" "$task_file" | awk -F: '{print $2}' | tr -d ' ' | sort -u))

            for agent in "${assigned_agents[@]}"; do
                if [[ " ${available_agents[@]} " =~ " ${agent} " ]]; then
                    info "Agent available: $agent"
                else
                    issue "Assigned agent not found: $agent"
                    echo "       Available agents: ${available_agents[*]}"
                fi
            done
        fi
    done
else
    warning "No agents directory found at $agents_dir"
fi

echo

# Summary
echo "📊 Dependency Analysis Summary:"
echo "   Tasks analyzed: $ANALYZED"
echo -e "   ${GREEN}Valid configurations: $((ANALYZED - ISSUES - WARNINGS))${NC}"
if [ $WARNINGS -gt 0 ]; then
    echo -e "   ${YELLOW}Warnings: $WARNINGS${NC}"
fi
if [ $ISSUES -gt 0 ]; then
    echo -e "   ${RED}Issues: $ISSUES${NC}"
fi

echo

if [ $ISSUES -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}🎉 All task dependencies are valid!${NC}"
        exit 0
    else
        echo -e "${YELLOW}✅ Dependency analysis completed with warnings${NC}"
        exit 0
    fi
else
    echo -e "${RED}❌ Dependency analysis found $ISSUES critical issues${NC}"
    exit 1
fi