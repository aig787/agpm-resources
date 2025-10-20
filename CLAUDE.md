# Agent and Command Architecture

This repository uses a **split architecture** pattern for organizing agents and commands across Claude Code and OpenCode. This approach enables code reuse while maintaining tool-specific customizations.

## Installation with AGPM

**IMPORTANT**: These agents, commands, and snippets are designed to be installed using [AGPM (AI Generated Prompt Manager)](https://github.com/aig787/agpm).

AGPM is a Git-based package manager for AI coding assistant resources. Instead of manually copying files, AGPM:

1. **Installs artifacts** from this repository into your projects
2. **Manages dependencies** between snippets, commands, and agents automatically
3. **Supports multiple tools** (Claude Code, OpenCode) simultaneously
4. **Handles version control** for reproducible environments

### Installing AGPM

Choose one of the following methods:

**Homebrew (macOS/Linux)**:
```bash
brew install aig787/agpm/agpm
```

**Installer Script (Unix/Linux/macOS)**:
```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/aig787/agpm/releases/latest/download/agpm-installer.sh | sh
```

**Windows PowerShell**:
```powershell
irm https://github.com/aig787/agpm/releases/latest/download/agpm-installer.ps1 | iex
```

**Cargo**:
```bash
cargo install agpm-cli
```

### Using AGPM

1. **Initialize your project**:
   ```bash
   agpm init
   ```

2. **Configure dependencies** in `agpm.toml`:
   Add the artifacts you want from this repository

3. **Install dependencies**:
   ```bash
   agpm install
   ```

For detailed documentation, see the [AGPM repository](https://github.com/aig787/agpm).

## Architecture Overview

### The Split Approach

```
agpm-resources/
├── snippets/                    # Shared business logic (tool-agnostic)
│   ├── agents/
│   │   └── python/
│   │       ├── backend-engineer.md
│   │       ├── linting-standard.md
│   │       └── linting-advanced.md
│   ├── commands/
│   │   ├── commit.md
│   │   └── lint.md             # Generic lint command
│   └── standards/              # Example configurations
│       └── python/
│           └── lint-config.md
├── claude-code/                 # Claude Code specific wrappers
│   ├── agents/
│   │   └── python/
│   │       └── backend-engineer.md
│   └── commands/
│       ├── commit.md
│       └── lint.md
└── opencode/                    # OpenCode specific wrappers
    ├── agents/
    │   └── python/
    │       └── backend-engineer.md
    └── commands/
        ├── commit.md
        └── lint.md
```

### Benefits

1. **Single Source of Truth**: Core logic lives in `snippets/`, eliminating duplication
2. **Tool-Specific Customization**: Wrappers can add tool-specific context, frontmatter, and tooling
3. **Maintainability**: Updates to core logic only need to happen once
4. **Consistency**: Agents and commands behave consistently across tools

## Important: Path References

**When referencing files within agents and commands, always use the installed path where the tools expect to find them, not the repository path.**

### Repository Structure vs. Installed Paths

The repository uses these directories for organization:
- `claude-code/` - Claude Code wrappers (repository path)
- `opencode/` - OpenCode wrappers (repository path)
- `snippets/` - Shared business logic (repository path)

However, when these files are installed/symlinked into a project, they exist at different locations:

**Claude Code Installed Paths:**
- Agents: `.claude/agents/`
- Commands: `.claude/commands/`

**OpenCode Installed Paths:**
- Agents: `.opencode/agent/`
- Commands: `.opencode/command/`

**Snippets Installed Path:**
- All snippets: `.agpm/snippets/`

### Path Reference Examples

**❌ Incorrect (hardcoded paths or repository-root-relative paths):**
```markdown
Read the complete agent instructions from:
- `snippets/agents/python/backend-engineer.md`
```

```yaml
dependencies:
  snippets:
    - name: backend-engineer-base
      path: snippets/agents/python/backend-engineer.md  # WRONG: relative to repo root, not to file
      tool: agpm
```

**✅ Correct (using relative paths and AGPM template syntax):**

**For Claude Code** (file at `claude-code/agents/python/backend-engineer.md`):
```yaml
agpm:
  templating: true
dependencies:
  snippets:
    - name: backend-engineer-base
      path: ../../../snippets/agents/python/backend-engineer.md  # Relative to this file
      tool: agpm
---
```
```markdown
{{ agpm.deps.snippets.backend_engineer_base.content }}
```

**For OpenCode** (file at `opencode/agents/python/backend-engineer.md`):
```yaml
agpm:
  templating: true
dependencies:
  snippets:
    - name: backend-engineer-base
      path: ../../../snippets/agents/python/backend-engineer.md  # Relative to this file
      tool: agpm
---
```
```markdown
{{ agpm.deps.snippets.backend_engineer_base.content }}
```

### Why This Matters

1. **Runtime Resolution**: Tools look for files at their installed locations, not repository paths
2. **Consistency**: Using installed paths makes documentation accurate for end users
3. **Portability**: Files can be moved in the repository without breaking references
4. **Clarity**: Clear distinction between repository organization and runtime structure

## AGPM Template Syntax for Dependencies

**IMPORTANT**: Always use AGPM's template syntax to reference dependencies. This ensures paths are resolved dynamically at install time and never hardcoded.

### Required Frontmatter for Templating

**Any artifact that uses AGPM template syntax must include this in the frontmatter:**

```yaml
agpm:
  templating: true
```

This enables AGPM to process template variables before the artifact is used.

### Declaring Named Dependencies

Every dependency in the frontmatter **must** have a `name` field:

```yaml
agpm:
  templating: true
dependencies:
  snippets:
    - name: commit-logic
      path: ../../snippets/commands/commit.md
      tool: agpm
    - name: backend-engineer-base
      path: ../../snippets/agents/python/backend-engineer.md
      tool: agpm
```

**CRITICAL: Dependency Paths Must Be Relative to the Declaring File**

Dependency paths are **always relative to the file declaring them**, NOT relative to the repository root.

**Path Calculation Examples**:

| Declaring File | Dependency File | Correct Path |
|----------------|-----------------|--------------|
| `claude-code/commands/lint.md` | `snippets/commands/lint.md` | `../../snippets/commands/lint.md` |
| `opencode/commands/commit.md` | `snippets/commands/commit.md` | `../../snippets/commands/commit.md` |
| `claude-code/agents/python/backend-engineer.md` | `snippets/agents/python/backend-engineer.md` | `../../../snippets/agents/python/backend-engineer.md` |
| `snippets/commands/lint.md` | `snippets/standards/python/lint-config.md` | `../standards/python/lint-config.md` |

**Why Relative Paths Matter**:
1. **Repository Independence**: Works regardless of where the repository is cloned
2. **AGPM Requirement**: AGPM processes dependencies relative to the declaring file's location
3. **Portability**: Files can be moved within the repository structure
4. **No Hardcoding**: Avoids assumptions about repository root location

### Template Reference Syntax

Reference dependencies using the template syntax:

```
{{ agpm.deps.snippets.<name>.content }}
```

**Naming Rules**:
- Hyphens (`-`) in the dependency name become underscores (`_`) in the template
- Example: `commit-logic` → `commit_logic`
- Example: `backend-engineer-base` → `backend_engineer_base`

### Complete Example

**Frontmatter** (for a file at `claude-code/commands/commit.md`):
```yaml
---
name: commit
description: Create conventional commits with validation
agpm:
  templating: true
dependencies:
  snippets:
    - name: commit-logic
      path: ../../snippets/commands/commit.md
      tool: agpm
---
```

**Body**:
```markdown
{{ agpm.deps.snippets.commit_logic.content }}

## Tool-Specific Notes

- This command is designed for Claude Code
- Use the Task tool and allowed-tools from frontmatter
```

### Benefits of Template Syntax

1. **Dynamic Resolution**: AGPM resolves paths at install time, no hardcoding needed
2. **Installation Agnostic**: Works regardless of where files are installed
3. **Refactoring Safe**: Repository reorganization doesn't break references
4. **Type Safe**: AGPM validates that referenced dependencies exist
5. **Maintainable**: Single source of truth for dependency locations

### Common Patterns

**Inserting Command Logic** (from `claude-code/commands/lint.md`):
```yaml
agpm:
  templating: true
dependencies:
  snippets:
    - name: lint-command
      path: ../../snippets/commands/lint.md
      tool: agpm
```
```markdown
## Command Execution

{{ agpm.deps.snippets.lint_command.content }}
```

**Inserting Agent Content** (from `claude-code/agents/python/backend-engineer.md`):
```yaml
agpm:
  templating: true
dependencies:
  snippets:
    - name: python-backend-base
      path: ../../../snippets/agents/python/backend-engineer.md
      tool: agpm
```
```markdown
{{ agpm.deps.snippets.python_backend_base.content }}

## Tool-Specific Notes

- This agent is designed for Claude Code
- Use the Task tool to delegate complex tasks
```

**Inserting Configuration Content** (from `snippets/agents/backend-engineer.md`):
```yaml
agpm:
  templating: true
dependencies:
  snippets:
    - name: best-practices
      path: ../best-practices/python-best-practices.md
      tool: agpm
    - name: styleguide
      path: ../styleguides/python-styleguide.md
      tool: agpm
```
```markdown
## Best Practices

{{ agpm.deps.snippets.best_practices.content }}

## Style Guide

{{ agpm.deps.snippets.styleguide.content }}
```

## Creating Agents

### Snippet Structure (Tool-Agnostic)

**Location**: `snippets/agents/{language}/{agent-name}.md` (e.g., `snippets/agents/python/backend-engineer.md`)

The snippet contains the core agent instructions:
- Agent persona and role
- Responsibilities and capabilities
- Development approach
- Best practices
- Context7 integration (if applicable)
- **No tool-specific references**
- **No project-specific context**

Example:
```markdown
You are a Senior Python Backend Engineer with deep expertise in modern Python development...

Your core responsibilities:
- Design and implement robust backend architectures
- Write clean, modular, well-documented Python code
- ...

Your development approach:
1. Always start by understanding requirements
2. Design the system architecture before coding
...
```

### Claude Code Agent Wrapper

**Location**: `.claude/agents/{agent-name}.md` or `claude-code/agents/{agent-name}.md`

**Required Frontmatter**:
- `name`: Unique identifier (lowercase letters and hyphens only)
- `description`: Natural language explanation with usage examples

**Optional Frontmatter**:
- `tools`: Comma-separated list of allowed tools (e.g., `Read, Write, Bash`)
- `model`: AI model (`sonnet`, `opus`, `haiku`, `inherit`)
- `color`: Visual identifier for the agent
- `dependencies`: Reference to snippet files

**Structure** (for a file at `claude-code/agents/python/backend-engineer.md`):
```markdown
---
name: backend-engineer
description: Use this agent when you need to develop, refactor, or optimize Python backend systems. Examples: <example>Context: User needs FastAPI app. user: 'Build REST API' assistant: 'I'll use backend-engineer' <commentary>Backend development task</commentary></example>
color: green
model: sonnet
agpm:
  templating: true
dependencies:
  snippets:
    - name: backend-engineer-base
      path: ../../../snippets/agents/python/backend-engineer.md
      tool: agpm
---

{{ agpm.deps.snippets.backend_engineer_base.content }}

## Project-Specific Context

- Project: Shore (Security Content Orchestration API)
- Tech stack: Sanic, PostgreSQL, Redis
- Main directory: `shore/`

## Tool-Specific Notes

- This agent is designed for Claude Code
- Use the Task tool to delegate complex tasks
- You have access to all standard Claude Code tools
```

### OpenCode Agent Wrapper

**Location**: `.opencode/agent/{agent-name}.md` or `opencode/agents/{agent-name}.md`

**Required Frontmatter**:
- `description`: Brief explanation of agent's purpose

**Optional Frontmatter**:
- `mode`: `primary`, `subagent`, or `all` (default: `all`)
- `model`: AI model specification (e.g., `anthropic/claude-sonnet-4-20250514`)
- `temperature`: Control AI response creativity (0.0-1.0)
- `tools`: Object with tool enable/disable flags
  - `read`, `write`, `edit`, `bash`, `glob`, etc.
- `permission`: Object with approval settings
  - `edit: allow`, `bash: ask`, etc.
- `dependencies`: Reference to snippet files

**Structure** (for a file at `opencode/agents/python/backend-engineer.md`):
```markdown
---
description: Python backend engineer for implementation, refactoring, API design. Delegates complex linting to linting-advanced.
mode: subagent
model: anthropic/claude-sonnet-4-20250514
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
  templating: true
dependencies:
  snippets:
    - name: backend-engineer-base
      path: ../../../snippets/agents/python/backend-engineer.md
      tool: agpm
---

{{ agpm.deps.snippets.backend_engineer_base.content }}

**Additional tool-specific context**:

- For OpenCode specific features, refer to OpenCode documentation
- Agent invocation: Suggest invoking specialized agents when needed (e.g., "Please invoke linting-advanced agent")
```

## Creating Commands

### Snippet Structure (Tool-Agnostic)

**Location**: `snippets/commands/{command-name}.md`

The snippet contains the core command logic:
- Argument parsing logic
- Execution steps
- Business logic
- Examples of usage
- **No tool-specific references**
- **No project-specific paths or names**

Example:
```markdown
## Your task

Run code quality checks for the Python project:

1. Parse the arguments:
   - `--fix`: Apply automatic fixes
   - `--check`: Run in CI mode
   - Arguments: $ARGUMENTS

2. Based on the arguments, perform the appropriate actions:
   - For `--fix`: Run `./build.sh lint-fix`
   - For `--check`: Run `./build.sh lint` in strict mode
...
```

### Claude Code Command Wrapper

**Location**: `.claude/commands/{command-name}.md` or `claude-code/commands/{command-name}.md`

**Optional Frontmatter**:
- `allowed-tools`: Specify permitted tools (e.g., `Task, Bash(git:*), Read`)
- `argument-hint`: Describe expected arguments
- `description`: Brief command explanation
- `model`: Specify AI model
- `disable-model-invocation`: Prevent automatic execution
- `dependencies`: Reference to snippet files

**Structure** (for a file at `claude-code/commands/lint.md`):
```markdown
---
allowed-tools: Task, Bash(./build.sh lint:*), Bash(uv run ruff:*), Read
description: |
  Run code quality checks (formatting, linting, type checking) with test verification
argument-hint: [ --fix | --check ] [ --all ] - e.g., "--fix --all"
agpm:
  templating: true
dependencies:
  snippets:
    - name: lint-command
      path: ../../snippets/commands/lint.md
      tool: agpm
---

{{ agpm.deps.snippets.lint_command.content }}

## Context

- Project name: Shore (Security Content Orchestration API)
- Current working directory: !`pwd`
- Python version: !`python --version 2>&1 | head -n 1`

## Tool-Specific Notes

- This command is designed for Claude Code
- Use the Task tool and allowed-tools from frontmatter
- The project uses uv for package management and build.sh for task automation
```

### OpenCode Command Wrapper

**Location**: `.opencode/command/{command-name}.md` or `opencode/commands/{command-name}.md`

**Optional Frontmatter**:
- `description`: Brief command description
- `agent`: Specify which agent should execute
- `model`: Override default model
- `subtask`: Boolean to force subagent invocation
- `dependencies`: Reference to snippet files

**Structure** (for a file at `opencode/commands/lint.md`):
```markdown
---
description: Run code quality checks (formatting, linting, type checking) with test verification
agpm:
  templating: true
dependencies:
  snippets:
    - name: lint-command
      path: ../../snippets/commands/lint.md
      tool: agpm
---

## Your task

Run code quality checks for the Python project.

**IMPORTANT**: You are being asked to directly perform code quality checks - run the appropriate commands, apply fixes if requested, and report the results. Do NOT ask for permission or confirmation.

{{ agpm.deps.snippets.lint_command.content }}

## Argument Parsing

Parse the arguments from the command invocation:

- Arguments received: $ARGUMENTS
- Parse for flags: `--fix`, `--check`, `--all`, `--doc`, `--test`
- Pass parsed arguments to the sub-logic referenced above

**Flag Examples**:
```
/lint                    # run standard checks
/lint --fix              # apply automatic fixes
/lint --fix --test       # apply fixes and run tests
/lint --check            # CI mode with strict validation
/lint --all              # all checks including type checking
```

## Execution

Based on the parsed arguments, execute the appropriate logic from the sub-command file:

- If `--fix`: Apply automatic fixes using specialized agents for complex issues
- If `--check`: Run in strict CI mode with fail-on-warnings
- If `--all`: Run comprehensive checks including type checking and tests
- If `--doc`: Improve documentation using specialized agents
- If `--test`: Run tests to verify code changes
- If no arguments: Run standard formatting and linting checks

## Tool-Specific Notes

- This command is designed for OpenCode
- Adjust any tool-specific syntax as needed
- Use the Bash tool to run linting commands directly
- Report any issues found and suggest fixes
```

## Project-Specific Configuration Patterns

Some commands require project-specific configuration to be language-agnostic. This section documents standard configuration patterns.

### Lint Configuration Pattern

The `/lint` command is designed to be language-agnostic and project-configurable. It works by reading project-specific configuration from a required snippet file.

#### Configuration File

**Location**: `.agpm/snippets/lint-config.md` (installed path in project)

**Purpose**: Defines how to run code quality checks for the specific project/language

**Required Sections**:

1. **Linting Tools**: What tools to use (e.g., ruff, eslint, golangci-lint)
2. **Commands**: Shell commands to run for different scenarios
3. **Agent Delegation Strategy**: Which agents to use for complex issues
4. **Best Practices**: Language/project-specific guidelines

#### Example: Python Lint Configuration

See `snippets/standards/python/lint-config.md` for a complete example. Here's the structure:

```markdown
# Python Linting Configuration

## Linting Tools
- **Formatter**: ruff format
- **Linter**: ruff check
- **Type Checkers**: mypy, ty

## Commands

### Standard Check
./build.sh lint

### Auto-fix
./build.sh lint-fix

## Agent Delegation Strategy

### Basic Fixes
- **Agent**: python-linting-basic
- **Purpose**: Mechanical fixes

### Complex Fixes
- **Agent**: python-linting-specialist
- **Purpose**: Refactoring, security

## Best Practices
- Use async libraries
- Keep mock signatures matching APIs
...
```

#### Generic Command Structure

**Snippet**: `snippets/commands/lint.md`
- Reads `.agpm/snippets/lint-config.md`
- Parses standard flags: `--fix`, `--check`, `--all`, `--doc`, `--test`
- Executes commands and delegates to agents per configuration

**Claude Code Wrapper**: `claude-code/commands/lint.md`
- Minimal wrapper with frontmatter
- References generic command
- Adds tool-specific context

**OpenCode Wrapper**: `opencode/commands/lint.md`
- Minimal wrapper with frontmatter
- References generic command
- Adds tool-specific notes

#### Creating a Lint Config for Your Project

1. **Copy example configuration**:
   ```bash
   cp snippets/standards/python/lint-config.md .agpm/snippets/lint-config.md
   # Or create your own for other languages
   ```

2. **Customize for your project**:
   - Update linting tools and commands
   - Configure agent delegation strategy
   - Add language-specific best practices

3. **Use the `/lint` command**:
   ```bash
   /lint                 # standard checks
   /lint --fix           # apply fixes
   /lint --fix --test    # fix and test
   /lint --check         # CI mode
   ```

#### Benefits of This Pattern

1. **Language-Agnostic**: Same command works for Python, JavaScript, Go, etc.
2. **Project-Specific**: Each project defines its own linting workflow
3. **Reusable**: Generic command logic shared across all projects
4. **Maintainable**: Configuration separate from command implementation
5. **Discoverable**: Examples in `snippets/standards/` for reference

#### Creating New Configuration Patterns

Follow this pattern for other project-specific commands:

1. Create generic command in `snippets/commands/{name}.md`
2. Require configuration at `.agpm/snippets/{name}-config.md`
3. Provide example in `snippets/standards/{language}-{name}-config.md`
4. Document the pattern in this file

## Special Placeholders

### Claude Code
- `$ARGUMENTS`: Capture all arguments
- `$1`, `$2`, etc.: Individual argument access
- `!command`: Execute bash command and inject output
- `@filename`: Reference file contents

### OpenCode
- `$ARGUMENTS`: Capture all arguments
- `$NAME`: Named argument placeholders
- `!command`: Execute bash command and inject output
- `@filename`: Include file contents

## Tool Access Control

### Claude Code
Use the `allowed-tools` frontmatter to restrict tool access:

```yaml
allowed-tools: Task, Bash(git:*), Read, Write, Edit, Glob, Grep
```

Pattern matching:
- `Bash(git:*)`: Allow all git commands
- `Bash(npm install:*)`: Allow npm install variants
- `Read, Write`: Allow specific tools

### OpenCode
Use the `tools` frontmatter to enable/disable tools:

```yaml
tools:
  write: false
  edit: false
  bash: true
```

Or use the `permissions` field for approval control:
```yaml
permissions:
  bash: approve
  write: approve
```

## Best Practices

1. **Keep Snippets Generic**: No project names, specific paths, or tool references
2. **Add Context in Wrappers**: Project-specific details belong in Claude Code/OpenCode wrappers
3. **Use Dependencies**: Always reference snippets using the `dependencies` frontmatter
4. **Document Examples**: Include clear usage examples in agent descriptions
5. **Use Template Syntax**: Always reference dependencies using AGPM template syntax (`{{ agpm.deps.snippets.<name>.content }}`), never hardcoded paths
6. **Name All Dependencies**: Every dependency must have a `name` field in the frontmatter
7. **Enable Templating**: Any artifact using template syntax must have `agpm: templating: true` in the frontmatter
8. **Version Control**: Keep all three directories in sync when updating logic
9. **Test Both Tools**: Verify agents/commands work in both Claude Code and OpenCode
10. **Tool-Specific Features**: Use wrapper sections for tool-specific notes and requirements
11. **All AGPM Artifacts**: **ALL artifacts that will be installed via AGPM (including private/project-specific commands) must follow the split architecture pattern** - no exceptions

## Directory Structure Requirements

**Note**: These are the **installed paths** where tools expect to find files. These differ from the repository organization paths (`claude-code/`, `opencode/`, `snippets/`).

### Claude Code
- Project agents: `.claude/agents/`
- User agents: `~/.claude/agents/`
- Project commands: `.claude/commands/`
- User commands: `~/.claude/commands/`

### OpenCode
- Project agents: `.opencode/agent/`
- Global agents: `~/.config/opencode/agent/`
- Project commands: `.opencode/command/`
- Global commands: `~/.config/opencode/command/`

### Snippets (AGPM)
- All snippets: `.agpm/snippets/`
- This is where snippet files are installed/symlinked when used in a project

## Migration Guide

To migrate existing agents/commands to the split architecture:

1. **Extract Business Logic**:
   ```bash
   # Remove project-specific references
   # Remove tool-specific syntax
   # Move to snippets/agents/ or snippets/commands/
   ```

2. **Create Claude Code Wrapper**:
   ```bash
   # Add Claude Code frontmatter
   # Add project-specific context section
   # Add tool-specific notes
   # Reference snippet with dependencies
   ```

3. **Create OpenCode Wrapper**:
   ```bash
   # Add OpenCode frontmatter
   # Add tool-specific notes (generic, not project-specific)
   # Reference snippet with dependencies
   ```

4. **Test Both**:
   ```bash
   # Verify in Claude Code: Load agent/command and test
   # Verify in OpenCode: Load agent/command and test
   # Ensure shared logic works correctly
   ```

## Examples

See the following files for complete examples (repository paths shown):

**Agents**:
- `snippets/agents/python/backend-engineer.md` (shared logic)
- `claude-code/agents/python/backend-engineer.md` (Claude Code wrapper)
- `opencode/agents/python/backend-engineer.md` (OpenCode wrapper)

**Commands**:
- `snippets/commands/commit.md` (shared logic)
- `claude-code/commands/commit.md` (Claude Code wrapper)
- `opencode/commands/commit.md` (OpenCode wrapper)

**Commands with Configuration Pattern**:
- `snippets/commands/lint.md` (generic command that reads configuration)
- `snippets/standards/python/lint-config.md` (example Python configuration)
- `claude-code/commands/lint.md` (Claude Code wrapper)
- `opencode/commands/lint.md` (OpenCode wrapper)
- Project-specific: `.agpm/snippets/lint-config.md` (installed in each project)

**Note**: When these files reference each other, they use AGPM template syntax like `{{ agpm.deps.snippets.<name>.content }}` rather than hardcoded paths.
