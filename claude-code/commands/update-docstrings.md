---
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*), Read, Edit, MultiEdit, Grep, Task
description: Review code changes and ensure all related documentation is accurate and up-to-date
argument-hint: '[ --check-only | --auto-update | --focus=<module> ] - e.g., "--focus=cli" to review specific module docs'
agpm:
  templating: true
dependencies:
  snippets:
    - name: update-docstrings-logic
      path: ../../snippets/commands/update-docstrings.md
      install: false
---

{{ agpm.deps.snippets.update_docstrings_logic.content }}

## Context

- Current changes: !`git diff HEAD`
- Files changed: !`git status --short`
- Recent commits: !`git log --oneline -5`

## Tool-Specific Notes

- This command is designed for Claude Code
- Use the Task tool to delegate complex documentation updates to specialized agents
- The `allowed-tools` frontmatter restricts which tools can be used
- Git commands are permitted for analyzing changes
- Use Edit/MultiEdit for documentation updates, or delegate to agents using Task

## Project-Specific Context

Add your project-specific context here if needed:
- Project name and description
- Documentation conventions used
- Specific modules or components to prioritize
- Language-specific documentation tools
- Links to style guides or documentation standards
