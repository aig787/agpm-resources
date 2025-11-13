---
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*), Read, Edit, MultiEdit, Grep, Task
description: Review code changes and ensure all related documentation is accurate and up-to-date
argument-hint: '[ --check-only | --auto-update ] [ --focus=<module> ] [ commit-range ] - e.g., "--focus=cli HEAD~5..HEAD" to review specific module docs for last 5 commits'
agpm:
  version: "1.2.0"
  templating: true
dependencies:
  snippets:
    - name: update-docstrings-logic
      path: ../../snippets/commands/update-docstrings.md
      version: "snippet-command-update-docstrings-^v1.2.0"
      tool: agpm
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
- **Range Support**: Can analyze historical changes using positional commit range arguments
- **Position-based parsing**: First non-flag argument is treated as commit range

## Claude Code Examples

### Current Changes
```
/update-docstrings                                # analyze current changes
/update-docstrings --check-only                   # check-only current changes
/update-docstrings --focus=api                    # focus on api module
```

### Positional Range Examples
```
/update-docstrings HEAD~5..HEAD                   # last 5 commits
/update-docstrings --check-only origin/main..HEAD # check-only since divergence
/update-docstrings --focus=cli abc123..def456     # cli module for specific range
```

## Project-Specific Context

Add your project-specific context here if needed:
- Project name and description
- Documentation conventions used
- Specific modules or components to prioritize
- Language-specific documentation tools
- Links to style guides or documentation standards
