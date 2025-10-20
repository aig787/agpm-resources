---
name: squash
description: Squash commits between specified range into a single commit, with optional intelligent regrouping, or restore from a previous squash operation
agpm:
  templating: true
dependencies:
  snippets:
    - name: squash-base
      path: ../../snippets/commands/squash.md
      install: false
---

{{ agpm.deps.snippets.squash_base.content }}

## Tool-Specific Notes

### Claude Code Execution

- Use Task tool for delegating complex change analysis to specialized agents
- Use Bash tool for all git operations and checkpoint management
- Use AskUserQuestion tool for interactive confirmations when needed
- Follow allowed-tools restrictions from frontmatter
- All file operations should preserve proper formatting and structure

### Argument Parsing

Parse arguments from `$ARGUMENTS` using the following rules:
- `<from>`: First positional argument that doesn't start with `--` (optional if --restore used)
- `<to>`: Second positional argument (optional if --restore used)
- `--restore`: Flag to enable restore mode
- `--regroup`: Flag to enable intelligent regrouping
- `--reflog <entry>`: Specific reflog entry for restore mode

### Agent Delegation

For complex changes (>10 files or >500 lines), use Task tool:
```
Task(description="Analyze for regrouping",
     prompt="Analyze these changes and suggest logical groupings for separate commits...",
     subagent_type="general-purpose")
```

### Checkpoint Integration

Load and execute checkpoint commands:
- Create: Use checkpoint create command before squashing
- Restore: Use checkpoint restore latest for undo operations

## Project-Specific Context

This command is designed for repositories using:
- Conventional commit format
- Attribution analysis for AI-generated content
- Checkpoint system for safety
- AGPM for dependency management

The command integrates with the existing commit and checkpoint infrastructure in the repository.