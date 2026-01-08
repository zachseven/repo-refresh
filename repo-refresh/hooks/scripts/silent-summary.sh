#!/bin/bash
set -euo pipefail

# Silent session summary writer for repo-refresh plugin
# Runs on Stop hook - captures session context without user-visible output
# Writes to progress log quietly in the background

PROGRESS_DIR="${CLAUDE_PROJECT_DIR:-.}/.claude/progress"
SUMMARY_FILE="$PROGRESS_DIR/summaries.md"
ACTIVITY_FILE="$PROGRESS_DIR/$(date +%Y-%m-%d).md"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")

# Exit silently if no project dir or progress tracking not initialized
if [ ! -d "$PROGRESS_DIR" ]; then
    exit 0
fi

# Read hook input
INPUT=$(cat)

# Check if there was actual file activity today (proxy for "meaningful work")
if [ ! -f "$ACTIVITY_FILE" ]; then
    # No file edits this session - skip summary
    exit 0
fi

# Count today's activity entries
ACTIVITY_COUNT=$(grep -c "^\- \`" "$ACTIVITY_FILE" 2>/dev/null || echo "0")

# Only write summary if there was meaningful activity (more than 2 file operations)
if [ "$ACTIVITY_COUNT" -lt 3 ]; then
    exit 0
fi

# Create summary file if needed
if [ ! -f "$SUMMARY_FILE" ]; then
    cat > "$SUMMARY_FILE" << 'EOF'
# Session Summaries

_Auto-generated session notes. Most recent first._

---

EOF
fi

# Get the files that were touched today for context
RECENT_FILES=$(grep -oP '→ `\K[^`]+' "$ACTIVITY_FILE" 2>/dev/null | sort -u | tail -5 | tr '\n' ', ' | sed 's/,$//')

# Write a minimal auto-summary based on file activity
# (We can't see conversation content, but we can see what files were worked on)
{
    echo ""
    echo "## $TIMESTAMP"
    echo "_Session activity: ${ACTIVITY_COUNT} file operations_"
    if [ -n "$RECENT_FILES" ]; then
        echo "Files: $RECENT_FILES"
    fi
    echo ""
    echo "---"
} >> "$SUMMARY_FILE"

# Keep summaries file from growing unbounded (keep last 50 entries)
# Each entry is ~5 lines, so keep ~300 lines
if [ $(wc -l < "$SUMMARY_FILE") -gt 350 ]; then
    head -10 "$SUMMARY_FILE" > "$SUMMARY_FILE.tmp"
    tail -300 "$SUMMARY_FILE" >> "$SUMMARY_FILE.tmp"
    mv "$SUMMARY_FILE.tmp" "$SUMMARY_FILE"
fi

exit 0
