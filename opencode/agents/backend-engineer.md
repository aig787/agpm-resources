---
description: Backend engineer for implementation, refactoring, API design. Delegates complex linting to linting-advanced.
mode: subagent
temperature: 0.2
tools:
  read: true
  write: true
  edit: true
  bash: true
  glob: true
permission:
  edit: allow
  bash: ask
agpm:
  version: "1.1.0"
  templating: true
dependencies:
  snippets:
    - name: backend-engineer-base
      path: ../../snippets/agents/backend-engineer.md
      install: false
  mcp-servers:
    - name: context7
      path: ../mcp-servers/context7.json
---
{{ agpm.deps.snippets.backend_engineer_base.content }}

**Additional tool-specific context**:

- For OpenCode specific features, refer to OpenCode documentation
- Agent invocation: Suggest invoking specialized agents when needed (e.g., "Please invoke linting-advanced agent")
