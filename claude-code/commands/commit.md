---
allowed-tools: "Task, Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git commit:*), Bash(git log:*), Bash(git show:*), Read, Glob, Grep, TodoWrite"
description: |
  Create well-formatted git commits following project conventions - supports single or multiple logically grouped commits
argument-hint: "[ --multi[=N] | --co-authored | --contributed | --no-attribution | --include-untracked ] [ paths... ] [ message ] - e.g., \"--multi\" or \"--multi=3\" for multiple commits or \"tests/\" for specific paths"
agpm:
  version: "1.1.0"
  templating: true
dependencies:
  snippets:
    - name: commit-base
      path: ../../snippets/commands/commit.md
      version: "snippet-command-commit-^v1.1.0"
      tool: agpm
      install: false
---
{{ agpm.deps.snippets.commit_base.content }}

## Context

- Current git status: !`git status --short`
- Current git diff: !`git diff HEAD`
- Recent commits for style reference: !`git log --oneline -5`

## Tool-Specific Notes

- This command is designed for Claude Code
- Use the Task tool and allowed-tools from frontmatter
