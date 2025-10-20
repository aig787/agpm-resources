# Update Examples Command

## Purpose

This command scans all artifacts in `opencode/`, `claude-code/`, and `snippets/` directories, builds a dependency graph, identifies top-level dependencies (artifacts that nothing depends on), and updates `examples/agpm.toml` with these top-level artifacts.

## Definition: Top-Level Dependencies

**Top-level dependencies** are artifacts that:
- Are NOT listed as dependencies in any other artifact's frontmatter
- Represent user-facing agents and commands that users would directly install
- Include wrappers from `claude-code/` and `opencode/` directories
- Exclude snippets that are only dependencies of wrappers

## Core Algorithm

### 1. Scan All Artifacts

Find all `.md` files in these directories:
- `opencode/agents/**/*.md`
- `opencode/commands/**/*.md`
- `claude-code/agents/**/*.md`
- `claude-code/commands/**/*.md`
- `snippets/**/*.md`

Store the list of all artifact file paths.

### 2. Parse Dependencies from All Artifacts

For each artifact file:

1. **Read the file** to extract frontmatter
2. **Parse YAML frontmatter** (between `---` markers)
3. **Extract dependencies** from the `dependencies` section
4. **Record each dependency path**:
   - Dependencies are listed under `dependencies.snippets[]`, `dependencies.agents[]`, `dependencies.commands[]`, etc.
   - Each dependency has a `path` field (relative to the declaring file)
   - Convert relative paths to absolute paths for comparison

**Example frontmatter parsing**:
```yaml
---
agpm:
  templating: true
dependencies:
  snippets:
    - name: backend-engineer-base
      path: ../../snippets/agents/backend-engineer.md
      tool: agpm
  agents:
    - name: linting-standard
      path: ../agents/linting-standard.md
      tool: claude-code
---
```

From this, record:
- `snippets/agents/backend-engineer.md` (as a dependency)
- `claude-code/agents/linting-standard.md` (as a dependency)

### 3. Build Dependency Graph

Create two sets:

1. **All Artifacts**: Set of all artifact file paths found in step 1
2. **Referenced Artifacts**: Set of all artifact file paths that appear as dependencies in step 2

**Important**: When resolving relative paths, calculate from the declaring file to get the absolute repository path.

### 4. Identify Top-Level Artifacts

**Top-level artifacts** = All Artifacts - Referenced Artifacts

These are artifacts that exist but are not referenced as dependencies by any other artifact.

### 5. Categorize Top-Level Artifacts

Group the top-level artifacts by:

**Tool**:
- Claude Code: paths starting with `claude-code/`
- OpenCode: paths starting with `opencode/`
- Skip: paths starting with `snippets/` (these are library code, not user-facing)

**Type**:
- Agents: paths containing `/agents/`
- Commands: paths containing `/commands/`
- Other: any other paths (hooks, mcp-servers, etc.)

### 6. Generate TOML Entries

For each top-level artifact, generate a TOML entry:

**Format for Claude Code agents**:
```toml
artifact-name = { path = "../claude-code/agents/artifact-name.md" }
```

**Format for Claude Code commands**:
```toml
artifact-name = { path = "../claude-code/commands/artifact-name.md" }
```

**Format for OpenCode agents**:
```toml
opencode-artifact-name = { path = "../opencode/agents/artifact-name.md", tool = "opencode" }
```

**Format for OpenCode commands**:
```toml
opencode-artifact-name = { path = "../opencode/commands/artifact-name.md", tool = "opencode" }
```

**Naming rules**:
- For Claude Code: use the base filename without extension (e.g., `backend-engineer.md` → `backend-engineer`)
- For OpenCode: prefix with `opencode-` (e.g., `backend-engineer.md` → `opencode-backend-engineer`)
- Maintain alphabetical ordering within each section

### 7. Update examples/agpm.toml

Read the current `examples/agpm.toml` file and:

1. **Preserve the header and project section**:
   - Keep lines from start until `[agents]` section
   - Keep the `[project]` and `[sources]` sections unchanged

2. **Replace the [agents] section**:
   - Add comment: `# Claude Code Agents`
   - Add all Claude Code agents (alphabetically sorted)
   - Add comment: `# OpenCode Agents`
   - Add all OpenCode agents (alphabetically sorted)

3. **Replace the [commands] section**:
   - Add comment: `# Claude Code Commands`
   - Add all Claude Code commands (alphabetically sorted)
   - Add comment: `# OpenCode Commands`
   - Add all OpenCode commands (alphabetically sorted)

4. **Preserve other sections**:
   - Keep `[hooks]`, `[mcp-servers]`, and any other sections unchanged

### 8. Write Updated TOML

Write the updated content back to `examples/agpm.toml`.

### 9. Report Results

Provide a summary using the tool-appropriate format:
```
✓ Analysis complete

Scanned: {total} artifacts
- Claude Code: {count} agents, {count} commands
- OpenCode: {count} agents, {count} commands
- Snippets: {count} (skipped as library code)

Dependencies found: {count} unique referenced artifacts

Top-level artifacts: {count}
- Claude Code Agents: [list]
- Claude Code Commands: [list]
- OpenCode Agents: [list]
- OpenCode Commands: [list]

✓ Updated examples/agpm.toml with {count} entries
```

## Implementation Guidelines

1. **Path Normalization**: Convert all paths to absolute repository paths for comparison
2. **Relative Path Calculation**: When a dependency has `path: ../../snippets/foo.md`, resolve it relative to the declaring file
3. **YAML Parsing**: Handle YAML frontmatter correctly
  may contain template syntax like
  ```literal
  {{ agpm.project.language }}
  ```

4. **Template Variables**: Skip dependencies with template variables in paths e.g.
```literal
{{ agpm.project.language }}-best-practices.md
```
as these are dynamic
5. **Preserve Order**: Keep sections in the same order as the original TOML
6. **Alphabetical Sorting**: Sort entries within each section alphabetically
7. **Comments**: Preserve section comments in the TOML file

## Edge Cases

1. **No frontmatter**: Some files may not have frontmatter - treat as having no dependencies
2. **Invalid YAML**: Handle malformed frontmatter gracefully
3. **Circular dependencies**: Not possible to have top-level artifacts if all artifacts reference each other (unlikely but possible)
4. **Template paths**: Skip dependencies with template variables - these are resolved at install time
5. **Non-existent dependencies**: If a dependency path doesn't exist, record it anyway (may be a template path)
6. **Multiple dependency types**: An artifact can have dependencies in multiple sections (snippets, agents, commands, mcp-servers, etc.)

## Example Dependency Resolution

**Declaring file**: `claude-code/commands/lint.md`

**Dependency in frontmatter**:
```yaml
dependencies:
  snippets:
    - name: lint-command
      path: ../../snippets/commands/lint.md
      tool: agpm
```

**Resolution**:
- Start at: `claude-code/commands/lint.md`
- Navigate: `../../` goes up to repository root
- Target: `snippets/commands/lint.md`
- Record: `snippets/commands/lint.md` as referenced

## Tool-Specific Execution Patterns

### Claude Code Execution
- Use Glob tool to find all .md files in repository
- Use Read tool to parse frontmatter from each file
- Use Edit or Write tool to update examples/agpm.toml
- Follow allowed-tools restrictions from frontmatter
- Use Bash tool only for getting current working directory if needed

### OpenCode Execution
- Use Glob tool to find all .md files efficiently
- Use Read tool to parse frontmatter from each file
- Use Edit or Write tool to update examples/agpm.toml
- All file operations should preserve formatting
- Execute analysis and update automatically without asking for permission

## Expected Output Structure

**examples/agpm.toml** after update:

```toml
# AGPM Manifest
# This file defines your Claude Code resource dependencies
# Only contains top-level resources - dependencies are pulled in automatically

[project]
language = "python"
best_practices = "best_practices.md"
styleguide = "styleguide.md"

[sources]
# Add your Git repository sources here
# Example: official = "https://github.com/aig787/agpm-community.git"

[agents]
# Claude Code Agents
backend-engineer = { path = "../claude-code/agents/backend-engineer.md" }
backend-engineer-advanced = { path = "../claude-code/agents/backend-engineer-advanced.md" }
general-purpose = { path = "../claude-code/agents/general-purpose.md" }
linting-advanced = { path = "../claude-code/agents/linting-advanced.md" }
linting-standard = { path = "../claude-code/agents/linting-standard.md" }
# OpenCode Agents
opencode-backend-engineer = { path = "../opencode/agents/backend-engineer.md", tool = "opencode" }
opencode-backend-engineer-advanced = { path = "../opencode/agents/backend-engineer-advanced.md", tool = "opencode" }
opencode-backend-pair-programmer = { path = "../opencode/agents/backend-pair-programmer.md", tool = "opencode" }
opencode-general-purpose = { path = "../opencode/agents/general-purpose.md", tool = "opencode" }
opencode-linting-advanced = { path = "../opencode/agents/linting-advanced.md", tool = "opencode" }
opencode-linting-standard = { path = "../opencode/agents/linting-standard.md", tool = "opencode" }

[commands]
# Claude Code Commands
commit = { path = "../claude-code/commands/commit.md" }
lint = { path = "../claude-code/commands/lint.md" }
pr-self-review = { path = "../claude-code/commands/pr-self-review.md" }
review-docs = { path = "../claude-code/commands/review-docs.md" }
update-agentic-context = { path = "../claude-code/commands/update-agentic-context.md" }
update-docs = { path = "../claude-code/commands/update-docs.md" }
update-docstrings = { path = "../claude-code/commands/update-docstrings.md" }
# OpenCode Commands
opencode-commit = { path = "../opencode/commands/commit.md", tool = "opencode" }
opencode-lint = { path = "../opencode/commands/lint.md", tool = "opencode" }
opencode-pr-self-review = { path = "../opencode/commands/pr-self-review.md", tool = "opencode" }
opencode-review-docs = { path = "../opencode/commands/review-docs.md", tool = "opencode" }
opencode-update-agentic-context = { path = "../opencode/commands/update-agentic-context.md", tool = "opencode" }
opencode-update-docs = { path = "../opencode/commands/update-docs.md", tool = "opencode" }
opencode-update-docstrings = { path = "../opencode/commands/update-docstrings.md", tool = "opencode" }

[hooks]
# Add your hook dependencies here
# Example: pre-commit = { source = "official", path = "hooks/pre-commit.json" }
agpm-update = { path = "../claude-code/hooks/agpm-update.json" }

[mcp-servers]
# Add your MCP server dependencies here
# Example: filesystem = { source = "official", path = "mcp-servers/filesystem.json" }
```
