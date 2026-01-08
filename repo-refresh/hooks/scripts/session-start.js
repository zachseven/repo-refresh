#!/usr/bin/env node

// Session start hook for repo-refresh plugin
// Shows reminder if progress tracking is active
// Cross-platform (Windows/Mac/Linux)

const fs = require('fs');
const path = require('path');

const projectDir = process.env.CLAUDE_PROJECT_DIR || process.cwd();
const progressDir = path.join(projectDir, '.claude', 'progress');

if (fs.existsSync(progressDir)) {
  console.log('💡 Run /repo-refresh to catch up on where you left off');
}
