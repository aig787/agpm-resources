---
allowed-tools: "Bash(git diff:*), Bash(git status:*), Bash(git log:*), Task, Grep, Read"
description: Perform comprehensive PR self-review with language-specific checks
argument-hint: "[ --quick | --full | --security | --performance ] - e.g., \"--quick\" for basic checks only"
agpm:
  version: "1.0.0"
  templating: true
dependencies:
  snippets:
    - name: pr-self-review-base
      path: ../../snippets/commands/pr-self-review.md
      install: false
---
{{ agpm.deps.snippets.pr_self_review_base.content }}

## Context

- Current changes: !`git diff HEAD`
- Files changed: !`git status --short`
- Recent commits: !`git log --oneline -5`

## Tool-Specific Notes

- This command is designed for Claude Code
- Use the Task tool to delegate to specialized agents
- You have access to all standard Claude Code tools
- Use allowed-tools from frontmatter for git operations
