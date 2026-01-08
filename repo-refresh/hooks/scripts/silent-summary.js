#!/usr/bin/env node

// Silent session summary writer for repo-refresh plugin
// Runs on Stop hook - captures session context without user-visible output
// Cross-platform (Windows/Mac/Linux)

const fs = require('fs');
const path = require('path');

const projectDir = process.env.CLAUDE_PROJECT_DIR || process.cwd();
const progressDir = path.join(projectDir, '.claude', 'progress');
const summaryFile = path.join(progressDir, 'summaries.md');
const today = new Date().toISOString().split('T')[0];
const activityFile = path.join(progressDir, `${today}.md`);
const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 16);

// Read stdin
let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  try {
    // Exit silently if progress tracking not initialized
    if (!fs.existsSync(progressDir)) {
      process.exit(0);
    }

    // Check if there was actual file activity today
    if (!fs.existsSync(activityFile)) {
      process.exit(0);
    }

    // Count today's activity entries
    const activityContent = fs.readFileSync(activityFile, 'utf8');
    const activityCount = (activityContent.match(/^- `/gm) || []).length;

    // Only write summary if meaningful activity (3+ file operations)
    if (activityCount < 3) {
      process.exit(0);
    }

    // Create summary file if needed
    if (!fs.existsSync(summaryFile)) {
      fs.writeFileSync(summaryFile, `# Session Summaries\n\n_Auto-generated session notes. Most recent first._\n\n---\n\n`);
    }

    // Extract files that were touched
    const fileMatches = activityContent.match(/→ `([^`]+)`/g) || [];
    const files = [...new Set(fileMatches.map(m => m.replace(/→ `|`/g, '')))].slice(-5);
    const fileList = files.join(', ');

    // Append summary
    const summary = `\n## ${timestamp}\n_Session activity: ${activityCount} file operations_\n${fileList ? `Files: ${fileList}\n` : ''}\n---\n`;
    fs.appendFileSync(summaryFile, summary);

  } catch (e) {
    // Fail silently
  }
  process.exit(0);
});
