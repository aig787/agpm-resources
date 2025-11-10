---
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

### OpenCode Integration
- Use standard bash commands for git operations
- Parse arguments from $ARGUMENTS variable
- Utilize gh CLI directly through bash commands
- Provide clear output formatting for terminal display

### Execution Pattern
1. Run prerequisite checks using bash commands
2. Analyze changes and generate PR content
3. Create PR using gh CLI with proper formatting
4. Display PR URL and summary to user

### Argument Handling
- Parse $ARGUMENTS for flags and parameters
- Support `--draft`, `--base <branch>`, and custom title arguments
- Provide help text for invalid usage

### Output Formatting
- Use clear, concise terminal output
- Show progress indicators for long-running operations
- Display PR URL prominently when created
- Provide helpful error messages with suggested fixes