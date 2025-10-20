---
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

### OpenCode Execution

- Use standard input/output for interactive prompts and confirmations
- Use Task tool for delegating complex change analysis to specialized agents
- Use Bash tool for all git operations and checkpoint management
- Use Read/Edit tools for file operations when needed
- Preserve all content during the split process

### Argument Parsing

Parse arguments from command line using the following rules:
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

Integrate with checkpoint system:
- Create checkpoint before squashing operations
- Use checkpoint restore for undo operations
- Provide clear recovery options to users

### Interactive Prompts

When user confirmation is needed:
- Prompt about wrapper creation using standard input/output
- Ask for confirmation before history-modifying operations
- Present options clearly and wait for user response
- Handle multi-line input appropriately for pasted content

## Implementation Notes

This command follows OpenCode execution patterns:
- Conversational interaction for user input
- Tool-based operations for git commands
- Clear error handling and user feedback
- Integration with existing repository infrastructure