---
name: gh-pr-create
description: Create GitHub pull requests with automatic title and description generation
agpm:
  version: "1.1.1"
  templating: true
dependencies:
  snippets:
    - name: gh-pr-create-base
      path: ../../snippets/commands/gh-pr-create.md
      version: "snippet-command-gh-pr-create-^v1.1.0"
      tool: agpm
      install: false
---
{{ agpm.deps.snippets.gh_pr_create_base.content }}

## Tool-Specific Notes

### Claude Code Integration
- Use the Task tool for complex git operations
- Leverage AskUserQuestion for interactive confirmation when needed
- Utilize Bash tool for git and gh CLI commands
- Parse arguments from the command context using available tools

### Execution Pattern
1. Use Bash tool to run git commands for prerequisite checks
2. Use Task tool to analyze changes and generate PR content
3. Use Bash tool to create the PR with gh CLI
4. Return the PR URL to the user

## Project-Specific Context

### Argument Parsing
- Access command arguments through the tool's argument parsing capabilities
- Handle flags like `--draft`, `--base <branch>`, and custom titles appropriately
- Provide clear error messages for invalid argument combinations

### Error Handling
- Provide actionable error messages for common issues:
  - Uncommitted changes present
  - Branch not pushed to remote
  - gh CLI not installed or authenticated
  - Invalid base branch specified