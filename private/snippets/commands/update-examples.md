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

1. **Read the first 20 lines** to extract frontmatter (dependencies are always in the frontmatter at the top of the file)
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

### 4. Discover Available Template Variants

Dynamically discover available template variants by inspecting the snippets directory:

1. **Find template variable patterns**: Search for all `{{ agpm.project.* }}` patterns in artifacts
2. **Discover available values**: For each template variable, find available options:
   - `{{ agpm.project.language }}`: Scan `snippets/best-practices/*-best-practices.md` and `snippets/styleguides/*-styleguide.md`
   - `{{ agpm.project.framework }}`: Scan `snippets/frameworks/*-framework.md` (if exists)
   - `{{ agpm.project.* }}`: Generic pattern matching for future variables

**Example discovery process**:
```bash
# For language variants
find snippets/best-practices/ -name "*-best-practices.md" | sed 's/.*\/\(.*\)-best-practices.md/\1/'
# Returns: javascript, python, rust

# For framework variants  
find snippets/frameworks/ -name "*-framework.md" | sed 's/.*\/\(.*\)-framework.md/\1/'
# Returns: react, vue, angular (if available)
```

Store discovered variants as:
```json
{
  "language": ["javascript", "python", "rust"],
  "framework": ["react", "vue", "angular"],
  "other_template_var": ["value1", "value2"]
}
```

### 5. Identify Template-Using Artifacts

Identify artifacts that use template variables by checking:
1. **Direct template usage**: Artifact content contains any `{{ agpm.project.* }}` pattern
2. **Dependency template usage**: Any dependency contains `{{ agpm.project.* }}` in its path
3. **Build template map**: Map each artifact to the template variables it uses

**Template detection patterns**:
- `{{ agpm.project.language }}`
- `{{ agpm.project.framework }}`
- `{{ agpm.project.* }}` (catch-all for future variables)

Store artifacts with their template variable requirements for variant generation.

### 6. Identify Top-Level Artifacts

**Top-level artifacts** = All Artifacts - Referenced Artifacts

These are artifacts that exist but are not referenced as dependencies by any other artifact.

### 7. Categorize Top-Level Artifacts

Group the top-level artifacts by:

**Tool**:
- Claude Code: paths starting with `claude-code/`
- OpenCode: paths starting with `opencode/`
- Skip: paths starting with `snippets/` (these are library code, not user-facing)

**Type**:
- Agents: paths containing `/agents/`
- Commands: paths containing `/commands/`
- Other: any other paths (hooks, mcp-servers, etc.)

### 7. Generate TOML Entries

For each top-level artifact, generate TOML entries:

**Base Entry Formats**:
```toml
# Claude Code agents
artifact-name = { path = "../claude-code/agents/artifact-name.md" }

# Claude Code commands  
artifact-name = { path = "../claude-code/commands/artifact-name.md" }

# OpenCode agents
opencode-artifact-name = { path = "../opencode/agents/artifact-name.md", tool = "opencode" }

# OpenCode commands
opencode-artifact-name = { path = "../opencode/commands/artifact-name.md", tool = "opencode" }
```

**Template Variant Format**:
```toml
# Single template variable
artifact-name-variant = { path = "../claude-code/agents/artifact-name.md", filename = "artifact-name-variant", template_vars = { project = { variable = "value" } } }

# Multiple template variables
artifact-name-variant1-variant2 = { path = "../claude-code/agents/artifact-name.md", filename = "artifact-name-variant1-variant2", template_vars = { project = { variable1 = "value1", variable2 = "value2" } } }

# OpenCode template variants
opencode-artifact-name-variant = { path = "../opencode/agents/artifact-name.md", filename = "opencode-artifact-name-variant", template_vars = { project = { variable = "value" } }, tool = "opencode" }
```

**Naming rules**:
- For Claude Code: use the base filename without extension (e.g., `backend-engineer.md` → `backend-engineer`)
- For OpenCode: prefix with `opencode-` (e.g., `backend-engineer.md` → `opencode-backend-engineer`)
- For template variants: append variant values in order (e.g., `backend-engineer-rust`, `backend-engineer-rust-react`)
- Maintain alphabetical ordering within each section

**Template Variant Generation Algorithm**:

For each top-level artifact:
1. **Check template usage**: Determine which template variables the artifact uses
2. **Determine if variants will be generated**: Check if the artifact uses template variables that will result in meaningful variants
3. **Conditionally generate entries**:
   - **If template variants will be generated**: ONLY generate template variant entries (skip the base entry)
   - **If no template variants will be generated**: Generate only the base entry
4. **Generate intelligent variant entries**: Use judgment to create only meaningful combinations:
   - If artifact uses 1 template variable (e.g., `language`): Generate N variants where N = number of available values
   - If artifact uses 2+ template variables: Generate only compatible combinations using language-framework mapping
   - Use `filename` parameter to create unique variant names
   - Use `template_vars.project` to override template variables

**Language-Framework Compatibility Mapping**:

```javascript
const compatibility = {
  // Frontend languages (compatible with frontend frameworks)
  javascript: ["react", "vue", "angular"],
  typescript: ["react", "vue", "angular"],
  
  // Backend languages (typically not used with frontend frameworks)
  python: [],
  golang: [],
  java: [],
  rust: [],
  
  // Full-stack languages (limited framework compatibility)
  // Note: These can be used with frameworks in specific contexts (e.g., server-side rendering)
  // but for agent variants, we focus on the primary use case
}
```

**Agent-Specific Logic**:

- **Frontend Engineers**: Only generate language-framework combinations for frontend languages (javascript, typescript)
- **Backend Engineers**: Generate language variants only (no framework combinations)
- **Linting Agents**: Generate language variants only (frameworks don't affect linting)
- **Commands**: Generate language variants only (commands are typically language-agnostic or framework-agnostic)

**Example Generation**:
```javascript
// Discovered variants: { language: ["javascript", "python", "golang"], framework: ["react", "vue", "angular"] }
// Artifact uses: {{ agpm.project.language }} and {{ agpm.project.framework }}

// For backend-engineer (backend agent):
// Generated entries: language variants only (no frameworks) - NO BASE ENTRY since language variants exist
backend-engineer-javascript = { path = "../claude-code/agents/backend-engineer.md", filename = "backend-engineer-javascript", template_vars = { project = { language = "javascript" } } }
backend-engineer-python = { path = "../claude-code/agents/backend-engineer.md", filename = "backend-engineer-python", template_vars = { project = { language = "python" } } }
backend-engineer-golang = { path = "../claude-code/agents/backend-engineer.md", filename = "backend-engineer-golang", template_vars = { project = { language = "golang" } } }
// Note: NO base backend-engineer entry since language variants are available

// For frontend-engineer (frontend agent):
// Generated entries: language variants + compatible language-framework combinations - NO BASE ENTRY
frontend-engineer-javascript = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-javascript", template_vars = { project = { language = "javascript" } } }
frontend-engineer-javascript-react = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-javascript-react", template_vars = { project = { language = "javascript", framework = "react" } } }
frontend-engineer-javascript-vue = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-javascript-vue", template_vars = { project = { language = "javascript", framework = "vue" } } }
frontend-engineer-javascript-angular = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-javascript-angular", template_vars = { project = { language = "javascript", framework = "angular" } } }
// Note: No frontend-engineer-python-react generated (incompatible combination)
// Note: NO base frontend-engineer entry since language variants are available

// For general-purpose (no template usage):
// Generated entries: base entry only (no template variants)
general-purpose = { path = "../claude-code/agents/general-purpose.md" }
```

**Variant Naming Convention**:
- Single variable: `{artifact-name}-{value}` (e.g., `backend-engineer-rust`)
- Multiple variables: `{artifact-name}-{value1}-{value2}-{...}` in variable order
- OpenCode variants: `opencode-{artifact-name}-{value(s)}`
- Maintain consistent ordering: language first, then framework, then alphabetical by variable name

**Intelligent Filtering Rules**:

1. **Frontend Agents** (agents with "frontend" in name):
   - Generate language variants ONLY for frontend-compatible languages (javascript, typescript)
   - Generate language-framework variants for frontend-compatible languages (javascript, typescript)
   - Do NOT generate any variants for backend languages (python, golang, java, rust)

2. **Backend Agents** (agents with "backend" in name):
   - Generate language variants for all languages
   - Do NOT generate any framework variants (backend agents don't use frontend frameworks)

3. **Linting Agents** (agents with "linting" in name):
   - Generate language variants for all languages
   - Do NOT generate framework variants (linting is language-specific, not framework-specific)

4. **Commands**:
   - Generate language variants only if the command is language-specific
   - Do NOT generate framework variants (commands are typically framework-agnostic)

5. **Other Agents** (general-purpose, git-expert, etc.):
   - Generate base entry only (no variants needed)
   - These agents are typically language and framework agnostic

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
3. **YAML Parsing**: Handle YAML frontmatter correctly (only need first 20 lines - dependencies are always in frontmatter)
  may contain template syntax like
  ```literal
  {{ agpm.project.language }}
  ```

4. **Template Variables**: Skip dependencies with template variables in paths e.g.
```literal
{{ agpm.project.language }}-best-practices.md
```
as these are dynamic
5. **File Reading Optimization**: Always use `limit: 20` when reading files for dependency parsing - frontmatter is always at the top
6. **Preserve Order**: Keep sections in the same order as the original TOML
7. **Alphabetical Sorting**: Sort entries within each section alphabetically
8. **Comments**: Preserve section comments in the TOML file

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
- Use Read tool with `limit: 20` to parse frontmatter from each file (dependencies are always in the first 20 lines)
- Use Edit or Write tool to update examples/agpm.toml
- Follow allowed-tools restrictions from frontmatter
- Use Bash tool only for getting current working directory if needed

### OpenCode Execution
- Use Glob tool to find all .md files efficiently
- Use Read tool with `limit: 20` to parse frontmatter from each file (dependencies are always in the first 20 lines)
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
# Template variants for backend-engineer (language: golang, java, javascript, python, rust)
# Note: No base backend-engineer entry since language variants are available
backend-engineer-golang = { path = "../claude-code/agents/backend-engineer.md", filename = "backend-engineer-golang", template_vars = { project = { language = "golang" } } }
backend-engineer-java = { path = "../claude-code/agents/backend-engineer.md", filename = "backend-engineer-java", template_vars = { project = { language = "java" } } }
backend-engineer-javascript = { path = "../claude-code/agents/backend-engineer.md", filename = "backend-engineer-javascript", template_vars = { project = { language = "javascript" } } }
backend-engineer-python = { path = "../claude-code/agents/backend-engineer.md", filename = "backend-engineer-python", template_vars = { project = { language = "python" } } }
backend-engineer-rust = { path = "../claude-code/agents/backend-engineer.md", filename = "backend-engineer-rust", template_vars = { project = { language = "rust" } } }
# Template variants for backend-engineer-advanced (language: golang, java, javascript, python, rust)
# Note: No base backend-engineer-advanced entry since language variants are available
backend-engineer-advanced-golang = { path = "../claude-code/agents/backend-engineer-advanced.md", filename = "backend-engineer-advanced-golang", template_vars = { project = { language = "golang" } } }
backend-engineer-advanced-java = { path = "../claude-code/agents/backend-engineer-advanced.md", filename = "backend-engineer-advanced-java", template_vars = { project = { language = "java" } } }
backend-engineer-advanced-javascript = { path = "../claude-code/agents/backend-engineer-advanced.md", filename = "backend-engineer-advanced-javascript", template_vars = { project = { language = "javascript" } } }
backend-engineer-advanced-python = { path = "../claude-code/agents/backend-engineer-advanced.md", filename = "backend-engineer-advanced-python", template_vars = { project = { language = "python" } } }
backend-engineer-advanced-rust = { path = "../claude-code/agents/backend-engineer-advanced.md", filename = "backend-engineer-advanced-rust", template_vars = { project = { language = "rust" } } }
# Template variants for frontend-engineer (language: javascript, typescript; framework: angular, react, vue)
# Note: No base frontend-engineer entry since language variants are available
frontend-engineer-javascript = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-javascript", template_vars = { project = { language = "javascript" } } }
frontend-engineer-javascript-angular = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-javascript-angular", template_vars = { project = { language = "javascript", framework = "angular" } } }
frontend-engineer-javascript-react = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-javascript-react", template_vars = { project = { language = "javascript", framework = "react" } } }
frontend-engineer-javascript-vue = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-javascript-vue", template_vars = { project = { language = "javascript", framework = "vue" } } }
frontend-engineer-typescript = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-typescript", template_vars = { project = { language = "typescript" } } }
frontend-engineer-typescript-angular = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-typescript-angular", template_vars = { project = { language = "typescript", framework = "angular" } } }
frontend-engineer-typescript-react = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-typescript-react", template_vars = { project = { language = "typescript", framework = "react" } } }
frontend-engineer-typescript-vue = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-typescript-vue", template_vars = { project = { language = "typescript", framework = "vue" } } }
# Note: Frontend engineers only support frontend languages (javascript, typescript)
general-purpose = { path = "../claude-code/agents/general-purpose.md" }
git-expert = { path = "../claude-code/agents/git-expert.md" }
github-actions-expert = { path = "../claude-code/agents/github-actions-expert.md" }
k8s-expert = { path = "../claude-code/agents/k8s-expert.md" }
# Template variants for linting-advanced (language: golang, java, javascript, python, rust)
# Note: No base linting-advanced entry since language variants are available
linting-advanced-golang = { path = "../claude-code/agents/linting-advanced.md", filename = "linting-advanced-golang", template_vars = { project = { language = "golang" } } }
linting-advanced-java = { path = "../claude-code/agents/linting-advanced.md", filename = "linting-advanced-java", template_vars = { project = { language = "java" } } }
linting-advanced-javascript = { path = "../claude-code/agents/linting-advanced.md", filename = "linting-advanced-javascript", template_vars = { project = { language = "javascript" } } }
linting-advanced-python = { path = "../claude-code/agents/linting-advanced.md", filename = "linting-advanced-python", template_vars = { project = { language = "python" } } }
linting-advanced-rust = { path = "../claude-code/agents/linting-advanced.md", filename = "linting-advanced-rust", template_vars = { project = { language = "rust" } } }
# Template variants for linting-standard (language: golang, java, javascript, python, rust)
# Note: No base linting-standard entry since language variants are available
linting-standard-golang = { path = "../claude-code/agents/linting-standard.md", filename = "linting-standard-golang", template_vars = { project = { language = "golang" } } }
linting-standard-java = { path = "../claude-code/agents/linting-standard.md", filename = "linting-standard-java", template_vars = { project = { language = "java" } } }
linting-standard-javascript = { path = "../claude-code/agents/linting-standard.md", filename = "linting-standard-javascript", template_vars = { project = { language = "javascript" } } }
linting-standard-python = { path = "../claude-code/agents/linting-standard.md", filename = "linting-standard-python", template_vars = { project = { language = "python" } } }
linting-standard-rust = { path = "../claude-code/agents/linting-standard.md", filename = "linting-standard-rust", template_vars = { project = { language = "rust" } } }
# Note: No framework variants for linting agents (linting is language-specific, not framework-specific)
# OpenCode Agents
# Template variants for opencode-backend-engineer (language: golang, java, javascript, python, rust)
# Note: No base opencode-backend-engineer entry since language variants are available
opencode-backend-engineer-golang = { path = "../opencode/agents/backend-engineer.md", filename = "opencode-backend-engineer-golang", template_vars = { project = { language = "golang" } }, tool = "opencode" }
opencode-backend-engineer-java = { path = "../opencode/agents/backend-engineer.md", filename = "opencode-backend-engineer-java", template_vars = { project = { language = "java" } }, tool = "opencode" }
opencode-backend-engineer-javascript = { path = "../opencode/agents/backend-engineer.md", filename = "opencode-backend-engineer-javascript", template_vars = { project = { language = "javascript" } }, tool = "opencode" }
opencode-backend-engineer-python = { path = "../opencode/agents/backend-engineer.md", filename = "opencode-backend-engineer-python", template_vars = { project = { language = "python" } }, tool = "opencode" }
opencode-backend-engineer-rust = { path = "../opencode/agents/backend-engineer.md", filename = "opencode-backend-engineer-rust", template_vars = { project = { language = "rust" } }, tool = "opencode" }
# Template variants for opencode-backend-engineer-advanced (language: golang, java, javascript, python, rust)
# Note: No base opencode-backend-engineer-advanced entry since language variants are available
opencode-backend-engineer-advanced-golang = { path = "../opencode/agents/backend-engineer-advanced.md", filename = "opencode-backend-engineer-advanced-golang", template_vars = { project = { language = "golang" } }, tool = "opencode" }
opencode-backend-engineer-advanced-java = { path = "../opencode/agents/backend-engineer-advanced.md", filename = "opencode-backend-engineer-advanced-java", template_vars = { project = { language = "java" } }, tool = "opencode" }
opencode-backend-engineer-advanced-javascript = { path = "../opencode/agents/backend-engineer-advanced.md", filename = "opencode-backend-engineer-advanced-javascript", template_vars = { project = { language = "javascript" } }, tool = "opencode" }
opencode-backend-engineer-advanced-python = { path = "../opencode/agents/backend-engineer-advanced.md", filename = "opencode-backend-engineer-advanced-python", template_vars = { project = { language = "python" } }, tool = "opencode" }
opencode-backend-engineer-advanced-rust = { path = "../opencode/agents/backend-engineer-advanced.md", filename = "opencode-backend-engineer-advanced-rust", template_vars = { project = { language = "rust" } }, tool = "opencode" }
# Template variants for opencode-backend-pair-programmer (language: golang, java, javascript, python, rust)
# Note: No base opencode-backend-pair-programmer entry since language variants are available
opencode-backend-pair-programmer-golang = { path = "../opencode/agents/backend-pair-programmer.md", filename = "opencode-backend-pair-programmer-golang", template_vars = { project = { language = "golang" } }, tool = "opencode" }
opencode-backend-pair-programmer-java = { path = "../opencode/agents/backend-pair-programmer.md", filename = "opencode-backend-pair-programmer-java", template_vars = { project = { language = "java" } }, tool = "opencode" }
opencode-backend-pair-programmer-javascript = { path = "../opencode/agents/backend-pair-programmer.md", filename = "opencode-backend-pair-programmer-javascript", template_vars = { project = { language = "javascript" } }, tool = "opencode" }
opencode-backend-pair-programmer-python = { path = "../opencode/agents/backend-pair-programmer.md", filename = "opencode-backend-pair-programmer-python", template_vars = { project = { language = "python" } }, tool = "opencode" }
opencode-backend-pair-programmer-rust = { path = "../opencode/agents/backend-pair-programmer.md", filename = "opencode-backend-pair-programmer-rust", template_vars = { project = { language = "rust" } }, tool = "opencode" }
# Template variants for opencode-frontend-engineer (language: javascript, typescript; framework: angular, react, vue)
# Note: No base opencode-frontend-engineer entry since language variants are available
opencode-frontend-engineer-javascript = { path = "../opencode/agents/frontend-engineer.md", filename = "opencode-frontend-engineer-javascript", template_vars = { project = { language = "javascript" } }, tool = "opencode" }
opencode-frontend-engineer-javascript-angular = { path = "../opencode/agents/frontend-engineer.md", filename = "opencode-frontend-engineer-javascript-angular", template_vars = { project = { language = "javascript", framework = "angular" } }, tool = "opencode" }
opencode-frontend-engineer-javascript-react = { path = "../opencode/agents/frontend-engineer.md", filename = "opencode-frontend-engineer-javascript-react", template_vars = { project = { language = "javascript", framework = "react" } }, tool = "opencode" }
opencode-frontend-engineer-javascript-vue = { path = "../opencode/agents/frontend-engineer.md", filename = "opencode-frontend-engineer-javascript-vue", template_vars = { project = { language = "javascript", framework = "vue" } }, tool = "opencode" }
opencode-frontend-engineer-typescript = { path = "../opencode/agents/frontend-engineer.md", filename = "opencode-frontend-engineer-typescript", template_vars = { project = { language = "typescript" } }, tool = "opencode" }
opencode-frontend-engineer-typescript-angular = { path = "../opencode/agents/frontend-engineer.md", filename = "opencode-frontend-engineer-typescript-angular", template_vars = { project = { language = "typescript", framework = "angular" } }, tool = "opencode" }
opencode-frontend-engineer-typescript-react = { path = "../opencode/agents/frontend-engineer.md", filename = "opencode-frontend-engineer-typescript-react", template_vars = { project = { language = "typescript", framework = "react" } }, tool = "opencode" }
opencode-frontend-engineer-typescript-vue = { path = "../opencode/agents/frontend-engineer.md", filename = "opencode-frontend-engineer-typescript-vue", template_vars = { project = { language = "typescript", framework = "vue" } }, tool = "opencode" }
# Note: Frontend engineers only support frontend languages (javascript, typescript)
opencode-general-purpose = { path = "../opencode/agents/general-purpose.md", tool = "opencode" }
opencode-git-expert = { path = "../opencode/agents/git-expert.md", tool = "opencode" }
opencode-github-actions-expert = { path = "../opencode/agents/github-actions-expert.md", tool = "opencode" }
opencode-k8s-expert = { path = "../opencode/agents/k8s-expert.md", tool = "opencode" }
# Template variants for opencode-linting-advanced (language: golang, java, javascript, python, rust)
# Note: No base opencode-linting-advanced entry since language variants are available
opencode-linting-advanced-golang = { path = "../opencode/agents/linting-advanced.md", filename = "opencode-linting-advanced-golang", template_vars = { project = { language = "golang" } }, tool = "opencode" }
opencode-linting-advanced-java = { path = "../opencode/agents/linting-advanced.md", filename = "opencode-linting-advanced-java", template_vars = { project = { language = "java" } }, tool = "opencode" }
opencode-linting-advanced-javascript = { path = "../opencode/agents/linting-advanced.md", filename = "opencode-linting-advanced-javascript", template_vars = { project = { language = "javascript" } }, tool = "opencode" }
opencode-linting-advanced-python = { path = "../opencode/agents/linting-advanced.md", filename = "opencode-linting-advanced-python", template_vars = { project = { language = "python" } }, tool = "opencode" }
opencode-linting-advanced-rust = { path = "../opencode/agents/linting-advanced.md", filename = "opencode-linting-advanced-rust", template_vars = { project = { language = "rust" } }, tool = "opencode" }
# Template variants for opencode-linting-standard (language: golang, java, javascript, python, rust)
# Note: No base opencode-linting-standard entry since language variants are available
opencode-linting-standard-golang = { path = "../opencode/agents/linting-standard.md", filename = "opencode-linting-standard-golang", template_vars = { project = { language = "golang" } }, tool = "opencode" }
opencode-linting-standard-java = { path = "../opencode/agents/linting-standard.md", filename = "opencode-linting-standard-java", template_vars = { project = { language = "java" } }, tool = "opencode" }
opencode-linting-standard-javascript = { path = "../opencode/agents/linting-standard.md", filename = "opencode-linting-standard-javascript", template_vars = { project = { language = "javascript" } }, tool = "opencode" }
opencode-linting-standard-python = { path = "../opencode/agents/linting-standard.md", filename = "opencode-linting-standard-python", template_vars = { project = { language = "python" } }, tool = "opencode" }
opencode-linting-standard-rust = { path = "../opencode/agents/linting-standard.md", filename = "opencode-linting-standard-rust", template_vars = { project = { language = "rust" } }, tool = "opencode" }
# Note: No framework variants for linting agents (linting is language-specific, not framework-specific)

[commands]
# Claude Code Commands
checkpoint = { path = "../claude-code/commands/checkpoint.md" }
commit = { path = "../claude-code/commands/commit.md" }
gh-pr-create = { path = "../claude-code/commands/gh-pr-create.md" }
# Template variants for lint (language: golang, java, javascript, python, rust)
# Note: No base lint entry since language variants are available
lint-golang = { path = "../claude-code/commands/lint.md", filename = "lint-golang", template_vars = { project = { language = "golang" } } }
lint-java = { path = "../claude-code/commands/lint.md", filename = "lint-java", template_vars = { project = { language = "java" } } }
lint-javascript = { path = "../claude-code/commands/lint.md", filename = "lint-javascript", template_vars = { project = { language = "javascript" } } }
lint-python = { path = "../claude-code/commands/lint.md", filename = "lint-python", template_vars = { project = { language = "python" } } }
lint-rust = { path = "../claude-code/commands/lint.md", filename = "lint-rust", template_vars = { project = { language = "rust" } } }
# Template variants for pr-self-review (language: golang, java, javascript, python, rust)
# Note: No base pr-self-review entry since language variants are available
pr-self-review-golang = { path = "../claude-code/commands/pr-self-review.md", filename = "pr-self-review-golang", template_vars = { project = { language = "golang" } } }
pr-self-review-java = { path = "../claude-code/commands/pr-self-review.md", filename = "pr-self-review-java", template_vars = { project = { language = "java" } } }
pr-self-review-javascript = { path = "../claude-code/commands/pr-self-review.md", filename = "pr-self-review-javascript", template_vars = { project = { language = "javascript" } } }
pr-self-review-python = { path = "../claude-code/commands/pr-self-review.md", filename = "pr-self-review-python", template_vars = { project = { language = "python" } } }
pr-self-review-rust = { path = "../claude-code/commands/pr-self-review.md", filename = "pr-self-review-rust", template_vars = { project = { language = "rust" } } }
# Note: No framework variants for commands (commands are typically framework-agnostic)
review-docs = { path = "../claude-code/commands/review-docs.md" }
squash = { path = "../claude-code/commands/squash.md" }
update-agentic-context = { path = "../claude-code/commands/update-agentic-context.md" }
update-docs = { path = "../claude-code/commands/update-docs.md" }
update-docstrings = { path = "../claude-code/commands/update-docstrings.md" }
# OpenCode Commands
opencode-checkpoint = { path = "../opencode/commands/checkpoint.md", tool = "opencode" }
opencode-commit = { path = "../opencode/commands/commit.md", tool = "opencode" }
opencode-gh-pr-create = { path = "../opencode/commands/gh-pr-create.md", tool = "opencode" }
# Template variants for opencode-lint (language: golang, java, javascript, python, rust)
# Note: No base opencode-lint entry since language variants are available
opencode-lint-golang = { path = "../opencode/commands/lint.md", filename = "opencode-lint-golang", template_vars = { project = { language = "golang" } }, tool = "opencode" }
opencode-lint-java = { path = "../opencode/commands/lint.md", filename = "opencode-lint-java", template_vars = { project = { language = "java" } }, tool = "opencode" }
opencode-lint-javascript = { path = "../opencode/commands/lint.md", filename = "opencode-lint-javascript", template_vars = { project = { language = "javascript" } }, tool = "opencode" }
opencode-lint-python = { path = "../opencode/commands/lint.md", filename = "opencode-lint-python", template_vars = { project = { language = "python" } }, tool = "opencode" }
opencode-lint-rust = { path = "../opencode/commands/lint.md", filename = "opencode-lint-rust", template_vars = { project = { language = "rust" } }, tool = "opencode" }
# Template variants for opencode-pr-self-review (language: golang, java, javascript, python, rust)
# Note: No base opencode-pr-self-review entry since language variants are available
opencode-pr-self-review-golang = { path = "../opencode/commands/pr-self-review.md", filename = "opencode-pr-self-review-golang", template_vars = { project = { language = "golang" } }, tool = "opencode" }
opencode-pr-self-review-java = { path = "../opencode/commands/pr-self-review.md", filename = "opencode-pr-self-review-java", template_vars = { project = { language = "java" } }, tool = "opencode" }
opencode-pr-self-review-javascript = { path = "../opencode/commands/pr-self-review.md", filename = "opencode-pr-self-review-javascript", template_vars = { project = { language = "javascript" } }, tool = "opencode" }
opencode-pr-self-review-python = { path = "../opencode/commands/pr-self-review.md", filename = "opencode-pr-self-review-python", template_vars = { project = { language = "python" } }, tool = "opencode" }
opencode-pr-self-review-rust = { path = "../opencode/commands/pr-self-review.md", filename = "opencode-pr-self-review-rust", template_vars = { project = { language = "rust" } }, tool = "opencode" }
# Note: No framework variants for commands (commands are typically framework-agnostic)
opencode-review-docs = { path = "../opencode/commands/review-docs.md", tool = "opencode" }
opencode-squash = { path = "../opencode/commands/squash.md", tool = "opencode" }
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

**Note**: The actual output will vary based on:
1. **Discovered template variants**: What languages, frameworks, and other variables are found in the snippets directory
2. **Template-using artifacts**: Which artifacts actually use template variables
3. **Intelligent filtering**: Only compatible language-framework combinations are generated based on agent type

**Key Filtering Principles**:
- **Frontend agents**: Generate framework variants only for frontend-compatible languages (javascript, typescript)
- **Backend agents**: Generate language variants only (no frameworks)
- **Linting agents**: Generate language variants only (frameworks don't affect linting)
- **Commands**: Generate language variants only (typically framework-agnostic)
- **General agents**: Generate base entry only (language/framework agnostic)

**Example with intelligent filtering**:
```toml
# Frontend agent with framework support (only for javascript and typescript)
# Note: NO base frontend-engineer entry since language variants are available
frontend-engineer-javascript = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-javascript", template_vars = { project = { language = "javascript" } } }
frontend-engineer-javascript-react = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-javascript-react", template_vars = { project = { language = "javascript", framework = "react" } } }
frontend-engineer-typescript = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-typescript", template_vars = { project = { language = "typescript" } } }
frontend-engineer-typescript-react = { path = "../claude-code/agents/frontend-engineer.md", filename = "frontend-engineer-typescript-react", template_vars = { project = { language = "typescript", framework = "react" } } }
# Note: NO frontend-engineer-python or frontend-engineer-rust generated (backend languages, not frontend)

# Backend agent (no framework variants)
# Note: NO base backend-engineer entry since language variants are available
backend-engineer-python = { path = "../claude-code/agents/backend-engineer.md", filename = "backend-engineer-python", template_vars = { project = { language = "python" } } }
# Note: NO backend-engineer-python-react generated (incompatible combination)
```
