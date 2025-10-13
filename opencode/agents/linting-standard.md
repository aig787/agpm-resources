---
description: Fast linting and formatting (optimized for speed with quick model)
mode: subagent
temperature: 0.0
tools:
  read: true
  write: false
  edit: true
  bash: true
  glob: true
permission:
  edit: allow
  bash: allow
agpm:
  templating: true
dependencies:
  snippets:
    - name: linting-standard-base
      path: ../../snippets/agents/linting-standard.md
      tool: agpm
---

**IMPORTANT**: This agent extends the shared base prompt. Read the complete prompt from:

- `{{ agpm.deps.snippets.linting_standard_base.install_path }}`

**Additional tool-specific context**:

- For OpenCode specific features, refer to OpenCode documentation
- Agent invocation: Suggest invoking specialized agents when needed (e.g., "Please invoke linting-advanced agent")
