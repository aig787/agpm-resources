# Import Artifact to Split Architecture

## Purpose

This command automates converting a single artifact (agent or command) into the split architecture pattern with AGPM templating.

It supports two modes:
1. **Direct Import Mode**: Provide artifact path and type to convert an existing file
2. **Interactive Creation Mode**: No arguments triggers interactive prompts to create a new artifact from scratch

## Mode Selection

**Check if a file path is provided:**

- **If `<artifact-path>` is provided**: Continue to "Direct Import Mode" (file-based import)
- **If no `<artifact-path>` is provided**: Enter "Interactive Creation Mode" (see section below)

**Important**: Multi-line input pasted after the command should NOT be treated as direct artifact content. Instead, it should be handled through the Interactive Creation Mode flow where users are explicitly asked if they want to paste existing artifact content.

**Pre-served Arguments**: In Interactive Mode, any arguments provided (like `--name`, `--type`, `--target`) will be preserved and used as defaults, so users won't be asked for information they've already specified.

## Interactive Creation Mode

When no arguments are provided, guide the user through creating a new artifact interactively:

### Step 1: Ask About Existing Artifact

Prompt the user:
- **Question**: "Do you have an existing artifact that you want to paste in for conversion?"
- **Options**: Yes / No

- **If YES**: 
  - **Question**: "Please paste the complete artifact content below (including frontmatter if it has any):"
  - **Input**: Multi-line text input with the full artifact content
  - **Action**: Store the content and proceed to Step 2 (treat as if we read from a file)
  - **Skip**: Skip to Step 3 (Ask for Name) since we already have the content
  - **Note**: Accept any markdown content - the system will parse it regardless of format

- **If NO**: Continue to Step 2 (Ask About Artifact Type)

### Step 2: Ask About Artifact Type (if not provided)

**Check if `--type` was provided in arguments**:
- If yes: Use the provided type and skip this step
- If no: Prompt the user:
  - **Question**: "What type of artifact do you want to create?"
  - **Options**:
    - Agent
    - Command
    - Snippet

### Step 2: Ask for Description/Purpose (if not pasting content)

**If user pasted existing artifact content in Step 1**:
- Skip this step - the description is already in the pasted content
- Extract description from the content if needed for other purposes

**If user is creating new artifact (no pasted content)**:
- Prompt the user:
  - **Question**: "Please describe what this artifact should do. Be specific about its purpose and functionality."
  - **Input**: Free-form text description

### Step 3: Ask for Name (if not provided)

**Check if `--name` was provided in arguments**:
- If yes: Use the provided name and skip this step
- If no: Prompt the user:
  - **Question**: "What should this artifact be named? (Use lowercase-with-hyphens format)"
  - **Input**: Artifact name
  - **Validation**: Must be lowercase with hyphens only (e.g., "backend-engineer", "commit", "best-practices")

**Note**: If user pasted existing artifact content in Step 1, try to extract the name from the content (filename in frontmatter, title in content, etc.) and suggest it as a default (unless `--name` was already provided).

### Step 4: Ask for Target Location (if not provided)

**Check if `--target` was provided in arguments**:
- If yes: Use the provided target path and skip this step
- If no: Prompt the user:
  - **Question**: "Where should this artifact be created?"
  - **Options**:
    - Standard location (snippets/, claude-code/, opencode/)
    - Private location (private/snippets/, private/claude-code/, private/opencode/)
    - Custom path (user provides specific directory)

### Step 5: Additional Questions Based on Type

**For Snippets**:
- **Question**: "Do you want to create Claude Code and OpenCode wrappers for this snippet?"
- **Options**: Yes / No
- If Yes:
  - **Question**: "Any additional content for the wrappers? (optional, leave blank if none)"

**For Agents**:
- **Question**: "What programming language or domain does this agent focus on? (e.g., python, javascript, rust, general)"
- **Input**: Language/domain name

**For Commands**:
- **Question**: "Does this command need arguments?"
- **Options**: Yes / No
- If Yes:
  - **Question**: "Describe the expected arguments format (e.g., '--fix --check', '<file-path> --type <type>')"

### Step 6: Process Content

**If user pasted existing artifact content (from Step 1)**:
- Treat the pasted content as if it was read from a file
- Proceed to "Analyze Content Structure" (Step 6 from Direct Import Mode)
- Extract business logic, tool-specific content, and project-specific content
- Skip template generation and go directly to Step 8 (Create Files)
- **Skip all remaining prompts** - we have all necessary information from the pasted content

**If creating new artifact (no existing content)**:
- Generate appropriate template content based on the collected information:

**For Agents**:
```markdown
# {Name} Agent

## Purpose

{User-provided description}

## Role and Expertise

You are a {domain/language} specialist responsible for...

## Core Responsibilities

1. {Derived from description}
2. {Derived from description}
3. {Derived from description}

## Development Approach

1. Understand requirements thoroughly
2. Design before implementation
3. Write clean, maintainable code
4. Test and validate changes
5. Document decisions

## Best Practices

{Generate relevant best practices based on domain/language}

## Example Usage

{Generate example scenarios based on description}
```

**For Commands**:
```markdown
# {Name} Command

## Purpose

{User-provided description}

## Arguments

{If arguments are needed, describe the argument format}

## Execution Steps

### 1. Parse Arguments

{If arguments specified, add parsing logic}

### 2. Execute Task

{Outline execution steps based on description}

### 3. Report Results

Provide a summary of what was accomplished.

## Implementation Guidelines

1. {Derive from description}
2. {Derive from description}

## Examples

{Generate example commands based on description}
```

**For Snippets**:
```markdown
# {Name}

## Purpose

{User-provided description}

## Content

{Generate template content based on the description}

## Usage

{Explain how this snippet should be used}

## Examples

{Provide example usage patterns}
```

### Step 7: Create Files

**If processing existing artifact content**:
1. Write the snippet file with extracted business logic to the appropriate location
2. If agent or command (or snippet with wrappers):
   - Create Claude Code wrapper with proper frontmatter and AGPM template reference
   - Create OpenCode wrapper with proper frontmatter and AGPM template reference
   - Include tool-specific and project-specific content in the wrappers
3. Calculate relative paths correctly based on target location

**If creating new artifact from template**:
1. Write the snippet file with generated template content to the appropriate location
2. If agent or command (or snippet with wrappers):
   - Create Claude Code wrapper with proper frontmatter and AGPM template reference
   - Create OpenCode wrapper with proper frontmatter and AGPM template reference
3. Calculate relative paths correctly based on target location

### Step 8: Report Interactive Creation Results

Provide a summary:

**For existing artifact conversion**:
```
Converted existing {type} artifact: {name}

Files created:
- Snippet: {path}
- Claude Code wrapper: {path}
- OpenCode wrapper: {path}

Next steps:
1. Review the split architecture and adjust content categorization if needed
2. Test the artifact in both tools
3. Add any additional tool-specific or project-specific context
4. Commit changes
```

**For new artifact creation**:
```
Created new {type} artifact: {name}

Files created:
- Snippet: {path}
- Claude Code wrapper: {path}
- OpenCode wrapper: {path}

Next steps:
1. Review and enhance the generated template content
2. Add specific implementation details
3. Test the artifact in both tools
4. Customize based on your needs
```

## Arguments

Parse the following arguments from `$ARGUMENTS`:

**Argument Parsing Rules**:
- `<artifact-path>`: First positional argument that doesn't start with `--` (optional - if not provided, enters Interactive Mode)
- `--type <value>`: Look for `--type` followed by agent|command|snippet (optional)
- `--target <value>`: Look for `--target` followed by a path (optional)
- `--name <value>`: Look for `--name` followed by a name (optional)

**Examples**:
```
# Direct Import Mode (with file path)
/import path/to/agent.md --type agent
/import path/to/command.md --type command --name commit
/import path/to/best-practices.md --type snippet --target snippets/standards/python
/import existing.md --type agent --target private/claude-code/agents

# Interactive Mode (no file path)
/import --type agent --name my-agent
/import --target private/snippets/commands
/import --name commit
/import
```

**Critical Implementation Note**: When parsing arguments, ensure that:
1. You correctly identify `<artifact-path>` as the first non-`--` argument
2. You properly extract the values following each `--` flag
3. You store these values and use them to skip prompts in Interactive Mode

**Pasted Content Handling**: When user pastes existing artifact content in Interactive Mode Step 1:
- Skip ALL remaining prompts (description, type, name, target, etc.)
- Extract all necessary information from the pasted content itself
- Proceed directly to file creation using the extracted information
- The pasted content contains everything needed - no additional user input required

**Examples**:
```
# Direct Import Mode (with file path)
/import path/to/agent.md --type agent
/import path/to/command.md --type command --name commit
/import path/to/best-practices.md --type snippet --target snippets/standards/python
/import existing.md --type agent --target private/claude-code/agents

# Interactive Mode (no file path)
/import --type agent --name my-agent
/import --target private/snippets/commands
/import --name commit
/import
```

## Execution Steps



### 1. Parse Arguments and Determine Mode

Extract all provided arguments from `$ARGUMENTS`:
- Check if `<artifact-path>` is provided (first positional argument, not starting with --)
- Extract `--type <value>` if provided
- Extract `--target <value>` if provided  
- Extract `--name <value>` if provided
- Store all extracted values for use in both modes

**Determine mode**:
- If `<artifact-path>` is provided: Direct Import Mode
- If no `<artifact-path>`: Interactive Creation Mode

**Important**: In Interactive Creation Mode, use the extracted values as defaults and skip corresponding prompts.

### 2. Direct Import Mode (if path provided)

Validate arguments for file-based import:
- Artifact path must exist
- Type must be "agent", "command", or "snippet" (required for direct import)
- Derive name from filename if not provided (strip .md extension, convert to lowercase-with-hyphens)
- If `--target` is provided, use it as the base directory; otherwise use repository root
- Proceed to Step 3 (Read the Artifact File)

### 3. Interactive Creation Mode (if no path provided)

Follow the Interactive Creation Mode steps, but skip any prompts for information already provided via arguments:

**Before each prompt, check the parsed arguments from Step 1**:
- If `--type` was parsed: Skip "Ask About Artifact Type", use parsed type
- If `--name` was parsed: Skip "Ask for Name", use parsed name  
- If `--target` was parsed: Skip "Ask for Target Location", use parsed target

Proceed with the interactive flow using parsed values as defaults for any skipped prompts.

### 4. Handle Snippet Import Mode

**If type is "snippet"**, prompt the user:

**Question 1**: "Do you want to create Claude Code and OpenCode wrappers for this snippet?"
- If **NO**: Skip to Step 2b (Direct Snippet Import)
- If **YES**: Continue to Question 2

**Question 2**: "Please provide any additional content that should be added to the wrappers (or leave blank):"
- **Claude Code wrapper additions**: (user input)
- **OpenCode wrapper additions**: (user input)

**Step 4a: Split Architecture for Snippet**
- Follow the normal split architecture flow (Steps 5-11)
- Add user-provided additional content to the wrapper files

**Step 4b: Direct Snippet Import**
- Determine target path:
  - If `--target` provided: {% raw %}`{target}/{name}.md`{% endraw %}
  - Otherwise: {% raw %}`snippets/{name}.md`{% endraw %}
- Copy the artifact file to the target location
- Report the created file
- Exit (skip steps 5-11)

### 5. Read the Artifact File

**If using file path (Direct Import Mode)**:
Read the entire contents of the artifact file to analyze.

### 6. Analyze Content Structure

Identify and extract:

**Business Logic (for snippet)**:
- Core instructions and responsibilities
- Algorithm and execution steps
- Best practices and guidelines
- Generic examples
- Everything that is NOT tool-specific or project-specific

**Tool-Specific Content**:
- References to specific tools (Task, Bash, etc.)
- Tool-specific placeholders ($ARGUMENTS, @files, !commands)
- Tool-specific frontmatter fields

**Project-Specific Content**:
- Project names, paths, specific configurations
- Team conventions
- Specific tech stack references

**Frontmatter**:
- Extract existing frontmatter to adapt for wrappers

### 7. Generate Directory Structure

Based on the type and target:

{% raw %}**For Agents**:
- If `--target` provided:
  - Use target path as base
  - Example: `--target private/claude-code/agents` → `private/claude-code/agents/{name}.md`
- Otherwise (default):
  - Snippet: `snippets/agents/{name}.md`
  - Claude Code: `claude-code/agents/{name}.md`
  - OpenCode: `opencode/agents/{name}.md`

**For Commands**:
- If `--target` provided:
  - Use target path as base
  - Example: `--target private/snippets/commands` → `private/snippets/commands/{name}.md`
- Otherwise (default):
  - Snippet: `snippets/commands/{name}.md`
  - Claude Code: `claude-code/commands/{name}.md`
  - OpenCode: `opencode/commands/{name}.md`

**For Snippets** (with wrappers):
- If `--target` provided:
  - Use target path as base for snippet
  - Derive wrapper paths based on target structure
- Otherwise (default):
  - Snippet: `snippets/{name}.md`
  - Claude Code: `claude-code/{name}.md`
  - OpenCode: `opencode/{name}.md`{% endraw %}

### 8. Create Snippet File

Write the snippet file with:
- No frontmatter (or minimal agpm-only frontmatter if it has dependencies)
- Business logic only (tool-agnostic, project-agnostic)
- Generic examples
- Clean, well-structured markdown

### 9. Calculate Relative Paths

**CRITICAL**: Calculate the correct relative path from each wrapper file to the snippet file.

**Path calculation rules**:
- Count directory levels from wrapper to repository root
- Count directory levels from repository root to snippet
- Build relative path with appropriate `../` prefixes

**Examples**:
- From `claude-code/commands/lint.md` to `snippets/commands/lint.md`: `../../snippets/commands/lint.md`
- From `claude-code/agents/python/backend.md` to `snippets/agents/python/backend.md`: `../../../snippets/agents/python/backend.md`
- From `opencode/commands/commit.md` to `snippets/commands/commit.md`: `../../snippets/commands/commit.md`

### 10. Create Claude Code Wrapper

Write the Claude Code wrapper with:

- **Frontmatter**: Include name, description, AGPM templating enabled, and dependency on snippet file
- **Body**: Insert snippet content using AGPM template syntax, then add:
  - Tool-Specific Notes section for Claude Code
  - Project-Specific Context section (if applicable)
  - User-provided additions (for snippet imports)
- **Template syntax**: Convert hyphens in dependency names to underscores (e.g., "import-base" becomes "import_base")

### 11. Create OpenCode Wrapper

Write the OpenCode wrapper with:

- **Frontmatter**: Include description, AGPM templating enabled, and dependency on snippet file
- **Body**: Insert snippet content using AGPM template syntax, then add:
  - Tool-Specific Notes section for OpenCode
  - User-provided additions (for snippet imports)
- **Template syntax**: Convert hyphens in dependency names to underscores (e.g., "import-base" becomes "import_base")

### 12. Report Results

Provide a summary:
{% raw %}```
✓ Created snippet: {path}
✓ Created Claude Code wrapper: {path}
✓ Created OpenCode wrapper: {path}

Next steps:
1. Review generated files and adjust as needed
2. Test in both Claude Code and OpenCode
3. Add any additional tool-specific or project-specific context
4. Commit changes
```{% endraw %}

## Implementation Guidelines

1. **Be Conservative**: When in doubt about whether content is business logic or tool-specific, include it in the snippet
2. **Preserve Structure**: Maintain the original markdown structure and formatting
3. **Calculate Paths Carefully**: Double-check relative paths are correct for AGPM
4. **Use Consistent Naming**: Follow the repository's naming conventions (lowercase-with-hyphens)
5. **Template Syntax**: Always use AGPM template syntax with underscore conversion
6. **Don't Lose Content**: If unsure where content belongs, add a comment in the file for manual review

## Edge Cases

- **Complex Dependencies**: If the artifact already has dependencies, preserve them in the snippet and wrappers
- **Custom Target Paths**: When `--target` is used, adjust all path calculations relative to the custom location
- **Existing Files**: Warn if target files already exist, ask for confirmation to overwrite
- **Invalid Paths**: Validate all paths before writing files
- **Malformed Frontmatter**: Handle artifacts with missing or invalid frontmatter gracefully
- **Snippet-Only Import**: For snippets without wrappers, simply copy the file to the target location
- **Empty Wrapper Additions**: If user provides no additional content for wrappers, that's fine - just use the template reference

## Tool-Specific Execution Patterns

### Claude Code Execution
- Use AskUserQuestion tool for interactive prompts
- Use Read tool to read artifact files
- Use Write tool to create output files
- Use Glob tool to check for existing files
- Use Bash tool only for directory creation (mkdir)
- Follow allowed-tools restrictions from frontmatter
- All file operations should preserve proper formatting and structure


### OpenCode Execution
- Use standard input/output for interactive prompts (conversationally ask the user)
- Use Read tool to read artifact files
- Use Write tool to create output files (or Edit if they exist and user confirms)
- Use Bash tool for directory creation if needed
- Preserve all content during the split process
- Prompt the user about wrapper creation using standard input/output
- When --target is used, adjust all paths accordingly

## Template Syntax Examples

**Example Claude Code wrapper** (for an artifact named "backend-engineer"):
```yaml
---
name: backend-engineer
description: Senior Python backend engineer agent
agpm:
  templating: true
dependencies:
  snippets:
    - name: backend-engineer-base
      path: ../../snippets/agents/backend-engineer.md
      tool: agpm
---
```

**Example OpenCode wrapper** (for an artifact named "backend-engineer"):
```yaml
---
description: Senior Python backend engineer agent
agpm:
  templating: true
dependencies:
  snippets:
    - name: backend-engineer-base
      path: ../../snippets/agents/backend-engineer.md
      tool: agpm
---
```

**Wrapper body example**:
```literal
{{ agpm.deps.snippets.backend_engineer_base.content }}

## Tool-Specific Notes
- Additional tool-specific notes here

## Project-Specific Context
- Project-specific information here (Claude Code only)
```

**Note**: Replace "backend-engineer" with your artifact name, and convert hyphens to underscores in template references (e.g., `backend-engineer-base` → `backend_engineer_base`). Use proper AGPM template syntax for the reference.
