---
name: checkpoint
description: Git-based checkpoint system for preserving development state without polluting branch history
agpm:
  templating: true
dependencies:
  snippets:
    - name: checkpoint-base
      path: ../../snippets/commands/checkpoint.md
      install: false
---

{{ agpm.deps.snippets.checkpoint_base.content }}

## Tool-Specific Notes

### Claude Code Integration

This command integrates seamlessly with Claude Code's workflow:

```bash
# Create checkpoint before major changes
/checkpoint create --message "Before implementing user authentication"

# Use with other Claude Code commands
/checkpoint create
/lint --fix
/commit "feat: add user authentication"
/checkpoint restore latest  # If something goes wrong
```

### Task Tool Integration

When working with the Task tool, checkpoints are automatically created before major operations:

```bash
# Before delegating to Task tool
/checkpoint create --message "Before Task: refactor database layer"

# After Task completion
/checkpoint create --message "After Task: database refactor completed"
```

### Working with Branch Protection

Checkpoints work around branch protection rules since they create detached commits:

- No need to bypass protection for temporary saves
- Clean branch history for PR reviews
- Safe experimentation without affecting main branch

### Integration with Git Hooks

The checkpoint system respects existing Git hooks:

- Pre-commit hooks are bypassed for checkpoint creation
- Post-checkout hooks work normally during restore
- Custom hooks can be added to enhance checkpoint functionality

## Project-Specific Context

### Repository Structure

This checkpoint system is designed for the agpm-resources repository structure:

- Works with both public and private artifact directories
- Preserves state across different tool-specific implementations
- Maintains compatibility with AGPM dependency management

### Team Workflow

For team collaboration:

- Checkpoints are local-only and never pushed
- Each developer maintains their own checkpoint history
- No conflicts with remote repository state
- Safe for experimental features and debugging

### Development Patterns

Common development patterns with checkpoints:

1. **Before major refactoring**: Create checkpoint to preserve working state
2. **During debugging**: Checkpoint after each significant discovery
3. **Before commits**: Ensure clean working directory for proper commits
4. **After testing**: Save successful test states for quick restoration

### Performance Considerations

- Checkpoints include all files (including build artifacts)
- Consider `.gitignore` configuration to exclude unnecessary files
- Use `checkpoint clean` regularly to prevent repository bloat
- Large binary files may impact checkpoint creation speed