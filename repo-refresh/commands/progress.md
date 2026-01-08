---
description: Add a manual progress note or view recent progress. Use "/progress" to view, or "/progress [note]" to add a note for future sessions.
---

# Progress Notes

This command lets you manually add notes to the progress log. Background tracking happens automatically and invisibly - this is for when YOU want to leave a note for future-you (or future-Claude).

## Viewing Progress

If invoked without arguments (just `/progress`), display:
1. Today's file activity from `.claude/progress/[today's date].md`
2. Recent session summaries from `.claude/progress/summaries.md` (last 5 entries)

Keep output concise - this is a quick status check.

## Adding a Note

If invoked with text (like `/progress Figured out the auth bug - was a race condition`), append that note to `.claude/progress/summaries.md` with the current timestamp.

Format:
```
## [YYYY-MM-DD HH:MM] 📝
[user's note text]

---
```

The 📝 emoji distinguishes manual notes from auto-generated ones.

## Good Uses for Manual Notes

- "Decision: Going with Postgres over SQLite for X reason"
- "BLOCKER: Waiting on API keys from DevOps"  
- "Next session: finish the auth flow, then tackle caching"
- "Note to self: the bug is in the scheduler, not the router"

## If Progress Directory Doesn't Exist

Create it at `.claude/progress/` and confirm tracking is now enabled.

## Behind the Scenes

File edits and session summaries are logged automatically in the background - you won't see that happening. This command is just for when you want to explicitly leave a breadcrumb.
