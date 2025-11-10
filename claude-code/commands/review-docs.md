---
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*), Read, Edit, MultiEdit, Grep, Glob, Task
description: Review and update all documentation files in docs/ directory for accuracy
argument-hint: '[ --check-only | --auto-update ] - e.g., "--check-only" to only report needed updates'
agpm:
  version: "1.1.1"
  templating: true
dependencies:
  snippets:
    - name: review-docs-command
      path: ../../snippets/commands/review-docs.md
      version: "snippet-command-review-docs-^v1.1.0"
      tool: agpm
      install: false
---
{{ agpm.deps.snippets.review_docs_command.content }}

## Context

- Current changes: !`git diff HEAD`
- Files changed: !`git status --short`
- Recent commits: !`git log --oneline -5`
- Documentation files: !`ls -la docs/`

## Tool-Specific Notes

- This command is designed for Claude Code
- Use the Task tool to delegate comprehensive documentation improvements to specialized agents
- Use allowed-tools from frontmatter for git operations and file access
- Example delegation:
  ```
  Task(description="Update project documentation",
       prompt="Review and update all documentation files in docs/ directory to match current implementation...",
       subagent_type="<appropriate-agent>")
  ```
