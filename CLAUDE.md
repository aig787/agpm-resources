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

## Artifact Versioning and Tagging

This repository uses **semantic versioning** and **automated Git tagging** to track artifact versions and enable reproducible installations.

### Version Management Overview

**Key Concepts**:
1. **Individual artifact versioning**: Each artifact (agent, command, snippet) has its own independent version
2. **Semantic versioning**: Version format follows `v{major}.{minor}.{patch}` (e.g., `v1.2.3`)
3. **Git tags**: Each artifact version is tagged in Git for traceability
4. **Automated tagging**: GitHub Actions automatically creates tags when artifacts are updated
5. **Frontmatter tracking**: Version is stored in each artifact's YAML frontmatter

### Tag Naming Convention

**Format**: `{tool}-{category}-{artifact-name}-v{semver}`

**Examples**:
- `snippet-agent-backend-engineer-v1.0.0`
- `claude-code-agent-backend-engineer-v1.2.3`
- `opencode-command-commit-v2.1.0`
- `snippet-best-practices-python-v1.5.2`

**Component Breakdown**:
- `{tool}`: `snippet`, `claude-code`, or `opencode`
- `{category}`: `agent`, `command`, `best-practices`, `styleguide`, `framework`, or `rule`
- `{artifact-name}`: Kebab-case name (e.g., `backend-engineer`, `commit`)
- `{semver}`: Semantic version with `v` prefix (e.g., `v1.2.3`)

### Semantic Versioning Rules

**Major (X.0.0)** - Breaking changes:
- Changed agent/command interface or arguments
- Removed features or capabilities
- Modified dependencies that break compatibility
- Restructured frontmatter in breaking ways

**Minor (x.Y.0)** - New features (backward compatible):
- Added new functionality
- Enhanced existing features
- Added new optional parameters
- Improved documentation significantly

**Patch (x.y.Z)** - Bug fixes:
- Fixed bugs or errors
- Minor documentation updates
- Performance improvements
- Typo corrections

### Version in Frontmatter

**Every artifact should include a version field** in the `agpm` section of its YAML frontmatter:

```yaml
---
name: backend-engineer
description: Python backend development expert
agpm:
  version: "1.0.0"
  templating: true
dependencies:
  snippets:
    - name: backend-engineer-base
      path: ../../../snippets/agents/backend-engineer.md
      tool: agpm
---
```

**Important Notes**:
- Version is stored WITHOUT the `v` prefix (e.g., `"1.0.0"`, not `"v1.0.0"`)
- Version must be quoted as a string
- Version is nested under the `agpm` section
- If no version is present, the bootstrap script will add `"1.0.0"`

### Automated Tagging Workflow

The repository includes a GitHub Actions workflow (`.github/workflows/tag-artifacts.yml`) that automatically:

1. **Detects changed artifacts** when code is pushed to `main`
2. **Analyzes commit messages** to determine version bump type
3. **Updates version** in artifact frontmatter
4. **Creates Git tags** for changed artifacts
5. **Pushes tags** to the repository
6. **Generates summary** of created tags

**Commit Message Conventions**:

To control version bumping, use conventional commit messages:

```bash
# Major version bump (breaking change)
git commit -m "feat!: redesign backend-engineer agent interface"
git commit -m "BREAKING CHANGE: remove deprecated command flags"

# Minor version bump (new feature)
git commit -m "feat: add type checking to lint command"
git commit -m "feat(agent): enhance error handling in backend-engineer"

# Patch version bump (bug fix, default)
git commit -m "fix: correct path reference in commit command"
git commit -m "docs: update backend-engineer usage examples"
git commit -m "chore: improve formatting in lint-config"
```

**Manual Workflow Dispatch**:

You can also trigger tagging manually:

```bash
# Via GitHub UI: Actions → Tag Artifacts → Run workflow
# Choose options:
# - dry_run: true/false (test without creating tags)
# - force_version_bump: auto/major/minor/patch
```

### Dependency Version Constraints

When declaring dependencies, you can specify version constraints using semantic versioning ranges:

```yaml
dependencies:
  snippets:
    - name: backend-engineer-base
      path: ../../../snippets/agents/backend-engineer.md
      version: "^1.0.0"  # Compatible with 1.x.x (>= 1.0.0, < 2.0.0)
      tool: agpm
```

**Version Range Syntax**:
- `"1.0.0"` - Exact version
- `"^1.0.0"` - Compatible with 1.x.x (default for most cases)
- `"~1.2.0"` - Compatible with 1.2.x
- `">=1.0.0"` - Any version >= 1.0.0
- `">=1.0.0 <2.0.0"` - Version range

### Bootstrap Initial Versions

To add initial versions to all existing artifacts, use the bootstrap script:

```bash
# Dry-run (preview changes without modifying files)
python .github/scripts/bootstrap-versions.py --dry-run

# Apply initial versions (default: 1.0.0)
python .github/scripts/bootstrap-versions.py

# Apply with custom default version
python .github/scripts/bootstrap-versions.py --default-version 0.1.0

# Create tags for initial versions
python .github/scripts/bootstrap-versions.py --output initial-tags.txt
bash .github/scripts/create-tags.sh initial-tags.txt
```

**What the bootstrap script does**:
1. Finds all artifact files (*.md) in `snippets/`, `claude-code/`, `opencode/`
2. Parses YAML frontmatter from each file
3. Adds `agpm.version` field if not present (default: `"1.0.0"`)
4. Generates git tag names for all artifacts
5. Outputs tag list to file for tag creation

### Manual Version Management

**Updating a version manually**:

1. Edit the artifact file
2. Update the version in frontmatter:
   ```yaml
   agpm:
     version: "1.2.0"  # Increment as needed
   ```
3. Commit with appropriate conventional commit message
4. Push to trigger automated tagging

**Creating tags manually**:

```bash
# Using the create-tags script
echo "snippet-agent-backend-engineer-v1.2.0" > tags.txt
bash .github/scripts/create-tags.sh tags.txt

# Or directly with git
git tag -a snippet-agent-backend-engineer-v1.2.0 \
  -m "Release snippet/agent/backend-engineer v1.2.0"
git push origin snippet-agent-backend-engineer-v1.2.0
```

### Version Tracking Tools

**Scripts in `.github/scripts/`**:

1. **`bump-version.py`** - Analyzes changed files, increments versions, updates frontmatter
   ```bash
   python .github/scripts/bump-version.py \
     --changed-files changed.txt \
     --bump-type minor \
     --output tags.txt
   ```

2. **`create-tags.sh`** - Creates annotated Git tags and pushes to repository
   ```bash
   bash .github/scripts/create-tags.sh tags.txt
   ```

3. **`bootstrap-versions.py`** - Adds initial versions to all artifacts
   ```bash
   python .github/scripts/bootstrap-versions.py --dry-run
   ```

### Using Versioned Artifacts

**In AGPM configuration** (`agpm.toml`):

```toml
[snippets]
backend-engineer = {
  source = "github",
  repo = "your-org/agpm-resources",
  path = "snippets/agents/backend-engineer.md",
  version = "^1.0.0",  # Use version constraint
  tag = "snippet-agent-backend-engineer-v1.0.0"  # Or specific tag
}
```

**Benefits of versioned artifacts**:
1. **Reproducible installations**: Pin to specific versions for stability
2. **Safe upgrades**: Test new versions before upgrading
3. **Rollback capability**: Revert to previous versions if needed
4. **Dependency tracking**: Ensure compatible versions across artifacts
5. **Change history**: Track evolution of artifacts over time

### Version Compatibility Matrix

When upgrading artifacts, consider compatibility between:

| Artifact Type | Depends On | Compatibility Notes |
|--------------|------------|---------------------|
| Claude Code Agent | Snippet Agent | Should match major version |
| OpenCode Agent | Snippet Agent | Should match major version |
| Claude Code Command | Snippet Command | Should match major version |
| OpenCode Command | Snippet Command | Should match major version |
| Agent | Best Practices | Minor versions acceptable |
| Agent | Style Guide | Minor versions acceptable |
| Command | Configuration | Must be compatible |

**Example Compatibility**:
- `snippet-agent-backend-engineer-v2.0.0` with `claude-code-agent-backend-engineer-v2.1.0` ✅
- `snippet-agent-backend-engineer-v2.0.0` with `claude-code-agent-backend-engineer-v1.9.0` ❌

### Best Practices for Versioning

1. **Always increment versions** when making changes to artifacts
2. **Use conventional commits** to trigger appropriate version bumps
3. **Test before merging** to ensure changes don't break dependents
4. **Document breaking changes** in commit messages and release notes
5. **Pin versions** for production use, use ranges for development
6. **Review dependency versions** when upgrading artifacts
7. **Keep wrappers in sync** with snippet versions (same major version)
8. **Tag releases** before announcing new features
9. **Maintain changelog** for significant version changes
10. **Use semantic versioning strictly** for predictability

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
