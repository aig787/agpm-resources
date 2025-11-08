---
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*), Read, Edit, MultiEdit, Grep, Task
description: Review changes and update README.md to stay current with implementation
argument-hint: '[ --check-only | --auto-update ] - e.g., "--check-only" to only report needed updates'
agpm:
  version: "1.1.0"
  templating: true
dependencies:
  snippets:
    - name: update-docs-command
      path: ../../snippets/commands/update-docs.md
      install: false
---
{{ agpm.deps.snippets.update_docs_command.content }}

## Context

- Current changes: !`git diff HEAD`
- Files changed: !`git status --short`
- Recent commits: !`git log --oneline -5`

## Tool-Specific Notes

- This command is designed for Claude Code
- Use the Task tool to delegate comprehensive documentation improvements to specialized agents
- Use allowed-tools from frontmatter for git operations and file access
- Example delegation:
  ```
  Task(description="Update project documentation",
       prompt="Review changes and update README.md and docs/ files to match current implementation...",
       subagent_type="<appropriate-agent>")
  ```
