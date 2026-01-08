# repo-refresh

**Claude Code plugin that makes Claude remember where you left off.**

Ever start a Claude Code session and spend the first 5 minutes re-explaining what you were working on? This fixes that.

## What it does

1. **Silently tracks progress** as you work (file edits, session summaries)
2. **`/repo-refresh`** command catches Claude up instantly on next session
3. Claude picks up mid-thought instead of starting cold

## The Experience

**Without repo-refresh:**
> You: "So yesterday we were working on the auth system..."
> Claude: "I don't have context from previous sessions. Could you explain..."

**With repo-refresh:**
> You: `/repo-refresh`
> Claude: "Welcome back. Last session you refactored the auth middleware - got JWT validation working but hit a snag with refresh tokens. Branch is `feature/auth` with 3 uncommitted files. Want to pick up on the refresh token logic?"

## Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/repo-refresh.git

# Install in Claude Code
claude /plugin install ./repo-refresh
```

Or install directly:
```bash
claude /plugin install github:YOUR_USERNAME/repo-refresh
```

## Commands

| Command | Description |
|---------|-------------|
| `/repo-refresh` | Full project recontextualization - reads CLAUDE.md, progress logs, git status |
| `/progress` | View recent activity or add manual notes |
| `/progress [note]` | Leave a breadcrumb for future sessions |

## How It Works

**Invisible background tracking:**
- `PostToolUse` hook logs every file edit silently
- `Stop` hook writes session summary when meaningful work happened
- All stored in `.claude/progress/` (gitignored by default)

**On-demand catchup:**
- `/repo-refresh` reads the logs + git state + CLAUDE.md
- Synthesizes a natural briefing
- Suggests logical next action

## Example Progress Logs

**`.claude/progress/2025-01-08.md`** (auto-generated):
```markdown
- `14:23:15` **Write** → `auth-middleware.ts`
- `14:25:02` **Edit** → `auth-middleware.ts`
- `14:31:18` **Write** → `jwt-utils.ts`
- `14:45:33` **Edit** → `routes/login.ts`
```

**`.claude/progress/summaries.md`** (auto-generated):
```markdown
## 2025-01-08 15:30
_Session activity: 12 file operations_
Files: auth-middleware.ts, jwt-utils.ts, login.ts, user-model.ts

---
```

**Manual note via `/progress`:**
```markdown
## 2025-01-08 15:45 📝
Decision: Using short-lived JWTs (15min) + refresh tokens instead of long-lived tokens

---
```

## Philosophy

Claude Code sessions are ephemeral. Your project context shouldn't be.

This plugin creates a "memory layer" that persists across sessions - not by storing conversations, but by tracking *what actually happened* (files touched, work completed) and letting Claude reconstruct context from artifacts.

## Requirements

- Claude Code
- Bash (for hook scripts)
- `jq` (for JSON parsing in hooks)

## License

MIT
