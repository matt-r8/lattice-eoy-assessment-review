#!/bin/bash

# Workflow Metrics Generator
# Auto-updates project-status.md with current statistics

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

echo -e "${BLUE}📊 Generating Workflow Metrics${NC}"
echo "Project: $PROJECT_ROOT"
echo

# Count features in each status
completed_count=$(find "$PROJECT_ROOT$CLAUDE_DIR/completed" -maxdepth 1 -type d -name "[0-9][0-9][0-9]-*" 2>/dev/null | wc -l)
active_count=$(find "$PROJECT_ROOT$CLAUDE_DIR/2_active" -name "prd-*.md" 2>/dev/null | wc -l)
backlog_count=$(find "$PROJECT_ROOT$CLAUDE_DIR/1_backlog" -name "prd-*.md" 2>/dev/null | wc -l)
total_count=$((completed_count + active_count + backlog_count))

echo "Current Status:"
echo "  Completed: $completed_count"
echo "  Active: $active_count"
echo "  Backlog: $backlog_count"
echo "  Total: $total_count"
echo

# Generate next sequential number
if [ $completed_count -gt 0 ]; then
    # Get the highest numbered completion folder
    latest_number=$(find "$PROJECT_ROOT$CLAUDE_DIR/completed" -maxdepth 1 -type d -name "[0-9][0-9][0-9]-*" | \
                   sed 's/.*\/\([0-9][0-9][0-9]\)-.*/\1/' | \
                   sort -n | \
                   tail -1)
    next_number=$(printf "%03d" $((10#$latest_number + 1)))
else
    next_number="001"
fi

echo "Next sequential number: $next_number"
echo

# Calculate this week/month/quarter counts (simplified - based on modification time)
current_date=$(date +%s)
week_ago=$((current_date - 604800))  # 7 days
month_ago=$((current_date - 2592000)) # 30 days
quarter_ago=$((current_date - 7776000)) # 90 days

week_count=0
month_count=0
quarter_count=0

if [ $completed_count -gt 0 ]; then
    for completed_dir in $(find "$PROJECT_ROOT$CLAUDE_DIR/3_completed" -maxdepth 1 -type d -name "[0-9][0-9][0-9]-*" 2>/dev/null); do
        dir_time=$(stat -c %Y "$completed_dir" 2>/dev/null || echo 0)

        if [ $dir_time -gt $week_ago ]; then
            ((week_count++))
        fi
        if [ $dir_time -gt $month_ago ]; then
            ((month_count++))
        fi
        if [ $dir_time -gt $quarter_ago ]; then
            ((quarter_count++))
        fi
    done
fi

# Calculate average duration (simplified - based on directory timestamps)
if [ $completed_count -gt 0 ]; then
    total_duration=0
    duration_count=0

    for completed_dir in $(find "$PROJECT_ROOT$CLAUDE_DIR/3_completed" -maxdepth 1 -type d -name "[0-9][0-9][0-9]-*" 2>/dev/null); do
        # Look for PRD file creation time vs completion time
        prd_file=$(find "$completed_dir" -name "prd-*.md" | head -1)
        if [ -n "$prd_file" ]; then
            prd_time=$(stat -c %Y "$prd_file" 2>/dev/null || echo 0)
            completion_time=$(stat -c %Y "$completed_dir" 2>/dev/null || echo 0)

            if [ $prd_time -gt 0 ] && [ $completion_time -gt 0 ]; then
                duration=$((completion_time - prd_time))
                total_duration=$((total_duration + duration))
                ((duration_count++))
            fi
        fi
    done

    if [ $duration_count -gt 0 ]; then
        avg_duration_seconds=$((total_duration / duration_count))
        avg_duration_days=$((avg_duration_seconds / 86400))
        if [ $avg_duration_days -eq 0 ]; then
            avg_duration_text="Same day"
        elif [ $avg_duration_days -eq 1 ]; then
            avg_duration_text="1 day"
        else
            avg_duration_text="$avg_duration_days days"
        fi
    else
        avg_duration_text="N/A"
    fi
else
    avg_duration_text="N/A"
fi

echo "Calculated metrics:"
echo "  This week: $week_count features"
echo "  This month: $month_count features"
echo "  This quarter: $quarter_count features"
echo "  Average duration: $avg_duration_text"
echo

# Update project-status.md
status_file="$PROJECT_ROOT$CLAUDE_DIR/project-status.md"
current_date_formatted=$(date +%Y-%m-%d)

if [ -f "$status_file" ]; then
    echo "Updating project-status.md..."

    # Create temporary file with updated content
    temp_file=$(mktemp)

    # Process the file line by line, updating specific sections
    in_stats_section=false
    in_completion_rate=false
    in_development_velocity=false

    while IFS= read -r line; do
        case "$line" in
            "## 📊 Current Statistics")
                echo "$line"
                in_stats_section=true
                ;;
            "- **Completed Features**: "*)
                if [ "$in_stats_section" = true ]; then
                    echo "- **Completed Features**: $completed_count"
                else
                    echo "$line"
                fi
                ;;
            "- **Active Features**: "*)
                if [ "$in_stats_section" = true ]; then
                    echo "- **Active Features**: $active_count"
                else
                    echo "$line"
                fi
                ;;
            "- **Backlog Features**: "*)
                if [ "$in_stats_section" = true ]; then
                    echo "- **Backlog Features**: $backlog_count"
                else
                    echo "$line"
                fi
                ;;
            "- **Total Features**: "*)
                if [ "$in_stats_section" = true ]; then
                    echo "- **Total Features**: $total_count"
                    in_stats_section=false
                else
                    echo "$line"
                fi
                ;;
            "### Completion Rate")
                echo "$line"
                in_completion_rate=true
                ;;
            "- **This Week**: "*)
                if [ "$in_completion_rate" = true ]; then
                    echo "- **This Week**: $week_count features"
                else
                    echo "$line"
                fi
                ;;
            "- **This Month**: "*)
                if [ "$in_completion_rate" = true ]; then
                    echo "- **This Month**: $month_count features"
                else
                    echo "$line"
                fi
                ;;
            "- **This Quarter**: "*)
                if [ "$in_completion_rate" = true ]; then
                    echo "- **This Quarter**: $quarter_count features"
                    in_completion_rate=false
                else
                    echo "$line"
                fi
                ;;
            "### Development Velocity")
                echo "$line"
                in_development_velocity=true
                ;;
            "- **Average Feature Duration**: "*)
                if [ "$in_development_velocity" = true ]; then
                    echo "- **Average Feature Duration**: $avg_duration_text"
                else
                    echo "$line"
                fi
                ;;
            "- **Active Feature Capacity**: "*)
                if [ "$in_development_velocity" = true ]; then
                    echo "- **Active Feature Capacity**: Multiple concurrent features supported"
                    in_development_velocity=false
                else
                    echo "$line"
                fi
                ;;
            "*Last Updated: "*)
                echo "*Last Updated: $current_date_formatted*"
                ;;
            "*Next Sequential Number: "*)
                echo "*Next Sequential Number: $next_number*"
                ;;
            *)
                echo "$line"
                ;;
        esac
    done < "$status_file" > "$temp_file"

    # Replace original with updated content
    mv "$temp_file" "$status_file"

    echo -e "${GREEN}✅ Successfully updated project-status.md${NC}"
else
    echo -e "${RED}❌ project-status.md not found at $status_file${NC}"
    exit 1
fi

echo
echo -e "${GREEN}📊 Metrics generation complete!${NC}"