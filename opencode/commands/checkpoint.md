---
description: Git-based checkpoint system for preserving development state without polluting branch history
agpm:
  version: "1.1.1"
  templating: true
dependencies:
  snippets:
    - name: checkpoint-base
      path: ../../snippets/commands/checkpoint.md
      version: "snippet-command-checkpoint-^v1.1.0"
      tool: agpm
      install: false
---
{{ agpm.deps.snippets.checkpoint_base.content }}

## Tool-Specific Notes

### OpenCode Integration

This command integrates seamlessly with OpenCode's TUI interface:

```bash
# Create checkpoint before major changes
/checkpoint create --message "Before implementing user authentication"

# Use with OpenCode's plan/build modes
/checkpoint create
# Switch to plan mode for architecture design
# Switch to build mode for implementation
/checkpoint restore latest  # If something goes wrong
```

### Visual Feedback

OpenCode provides enhanced visual feedback for checkpoint operations:

- Checkpoint creation shows progress in the TUI
- Restore operations display diff previews
- List command uses formatted tables for better readability
- Clean operations show space reclaimed

### Multi-Provider Support

The checkpoint system works across different AI providers:

- Provider-agnostic Git operations
- Consistent behavior regardless of underlying model
- Preserves state when switching between providers

### Keyboard Shortcuts

Recommended OpenCode keyboard shortcuts for checkpoint workflow:

- `Ctrl+C` then `/checkpoint create` - Quick checkpoint before changes
- `Ctrl+L` then `/checkpoint list` - View available checkpoints
- `Ctrl+R` then `/checkpoint restore latest` - Quick restore

## Project-Specific Context

### Repository Structure

This checkpoint system is designed for the agpm-resources repository structure:

- Works with both public and private artifact directories
- Preserves state across different tool-specific implementations
- Maintains compatibility with AGPM dependency management

### Development Environment

OpenCode-specific considerations:

- Terminal-based workflow benefits from quick checkpoint creation
- No GUI distractions during checkpoint operations
- Fast keyboard-driven interaction
- Consistent with CLI-first development philosophy

### Integration with Build Systems

Checkpoints work well with OpenCode's build system integration:

- Preserve build state between sessions
- Quick restoration of working builds
- Safe experimentation with build configurations
- Maintain dependency state across checkpoint cycles

### Performance Optimization

For OpenCode's terminal environment:

- Minimal output for checkpoint operations
- Fast execution to avoid workflow interruption
- Efficient Git operations for large repositories
- Background cleanup operations to maintain responsiveness