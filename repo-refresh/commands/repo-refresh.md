---
description: Full project recontextualization. Reads CLAUDE.md, recent progress logs, git status, and synthesizes a comprehensive "here's where we left off" briefing. Run this when starting a new session.
---

# Repo Refresh - Complete Recontextualization

When this command runs, perform a comprehensive project recontextualization by gathering and synthesizing the following sources. Present the information as a natural briefing, not a data dump.

## 1. Read Core Project Context

First, check for and read these files if they exist:
- `CLAUDE.md` - Primary project instructions and context
- `.claude/CLAUDE.md` - Alternative location
- `README.md` - Project overview (skim for key points only)

## 2. Read Progress Logs

Check for `.claude/progress/` directory. If it exists:
- Read the most recent progress log files (last 5-10 entries)
- These are timestamped notes from previous sessions documenting what was worked on
- Pay special attention to:
  - Last task being worked on
  - Any blockers or issues noted
  - Decisions made
  - Next steps that were planned

## 3. Gather Current State

Run these commands to understand current project state:
```bash
# Git status - what's changed, what branch
git status --short 2>/dev/null || echo "Not a git repo"

# Recent commits (last 5)
git log --oneline -5 2>/dev/null || echo "No git history"

# Current branch
git branch --show-current 2>/dev/null || echo "Unknown"

# Any uncommitted work
git diff --stat 2>/dev/null | tail -5
```

## 4. Check for Session Artifacts

Look for:
- `.claude/todos.md` - Any outstanding todos
- `.claude/decisions.md` - Architectural decisions log
- `.claude/blockers.md` - Known issues or blockers
- Any recent files modified in the last session

## 5. Synthesize and Present

Present the gathered information as a natural briefing:

**Format your response like this:**

> **Welcome back.** Here's where we stand:
>
> **Last Session:** [What was being worked on, from progress logs]
>
> **Current State:** [Branch, uncommitted changes, recent commits]
>
> **Open Items:** [Any todos, blockers, or planned next steps]
>
> **Ready to continue?** [Suggest logical next action based on context]

## Important Notes

- If progress logs don't exist yet, mention that the progress tracking will start now
- If CLAUDE.md doesn't exist, note that and offer to help create one
- Be conversational, not robotic - you're catching yourself up, not filing a report
- If there's clearly unfinished work, acknowledge it and ask if user wants to continue
