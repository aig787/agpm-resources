---
agpm:
  version: "1.0.0"
---

# Update Agentic Context Command

## Overview

This command reviews code changes and updates AI context files (CLAUDE.md, AGENTS.md) to reflect current architecture and implementation. It ensures AI assistants have accurate, up-to-date information about the codebase.

## Context Files Supported

- **CLAUDE.md**: Claude Code context file with architecture, implementation details, and guidelines
- **AGENTS.md**: Agent-specific context with delegation patterns and specializations

Both files are optional. The command only updates files that exist.

## Your Task

Review recent changes and ensure context files accurately reflect the project's architecture, implementation, and guidelines.

### 1. Parse Update Mode

Arguments: $ARGUMENTS

Modes:
- `--check-only`: Report needed updates without making changes
- `--auto-update`: Make necessary updates (default)

### 2. Analyze Changes

Examine git diff and status to understand architectural and implementation changes:

**Code Structure Changes**:
- New modules or restructured directories
- Renamed or moved components
- Changed project organization

**Dependency Changes**:
- New or removed dependencies
- Version updates
- Build tool configuration changes

**API/Interface Changes**:
- New or modified endpoints/interfaces
- Changed request/response formats
- Updated protocols or contracts

**Architecture Decisions**:
- Design pattern changes
- Component interaction updates
- System architecture evolution

**Testing Strategy**:
- New test types or frameworks
- Coverage requirements
- Testing pattern changes

**Security Updates**:
- Authentication/authorization changes
- Security validation rules
- Credential handling updates

**Build/Deployment**:
- CI/CD workflow changes
- Container configuration
- Deployment process updates

**Database/Storage**:
- Schema changes
- Migration files
- Data model updates

### 3. Identify Context Files

Check which context files exist:
- Read CLAUDE.md if present
- Read AGENTS.md if present
- Skip files that don't exist (DO NOT create new files)

### 4. Perform Systematic Checks

For each existing context file, verify accuracy:

**Module/Component Structure**:
- List actual modules/components in the codebase
- Compare with documented structure
- Check if descriptions match actual responsibilities
- Verify interaction documentation is accurate

**Agent Documentation** (if AGENTS.md exists or documented in CLAUDE.md):
- List all agents in agent directories (`.claude/agents/`, `.opencode/agent/`)
- Verify agent descriptions match capabilities
- Document delegation patterns between agents
- Include specializations and usage guidance

**Dependency Documentation**:
- Check dependency files (package.json, pyproject.toml, go.mod, Cargo.toml, etc.)
- Verify version numbers are current
- Ensure new dependencies are documented with purpose
- Remove documentation for deleted dependencies

**API/Interface Documentation**:
- Verify all public interfaces are documented
- Check schemas/types match implementation
- Ensure descriptions are accurate
- Update specification references if changed

**Testing Documentation**:
- Verify coverage targets are realistic
- Check testing patterns match actual tests
- Ensure CI/CD information is current
- Update test command examples if changed

### 5. Determine Needed Updates

Identify what needs updating in context files:

**Structure Updates**:
- Add new modules/components
- Update component responsibilities
- Fix outdated directory references

**Agent Documentation Updates**:
- Add newly created agents
- Update agent capabilities
- Document delegation patterns
- Specify when to use each agent

**Architecture Updates**:
- Document new design decisions
- Add architectural patterns
- Update system interaction diagrams
- Fix outdated implementation details

**Dependency Updates**:
- Add new dependencies with explanations
- Update version requirements
- Remove obsolete dependencies
- Document dependency purposes

**Practice Updates**:
- Update development workflows
- Add new coding standards
- Document new security considerations
- Update error handling patterns

### 6. Apply Updates Based on Mode

**Check-only Mode** (`--check-only`):
- Report all discrepancies found
- List components not documented or incorrectly described
- Show dependencies missing from documentation
- Identify outdated implementation details
- Provide suggested updates WITHOUT applying them

**Auto-update Mode** (`--auto-update` or default):
- Update structure to match actual codebase
- Synchronize dependency documentation
- Update interface documentation
- Fix implementation detail inaccuracies
- Add documentation for new architectural decisions
- Preserve existing valuable context and lessons learned

### 7. Maintain Context File Quality

For each file being updated:

**CLAUDE.md Specific**:
- **CRITICAL**: Keep file under 20,000 characters total
- Focus on helping AI assistants understand the codebase
- Preserve "Lessons Learned" and "Design Decisions" sections
- Maintain detailed explanations of complex algorithms
- Keep security rules prominent and clear
- Document cross-platform considerations
- Don't remove historical context that explains "why"
- If exceeding 20,000 characters, prioritize removing:
  * Verbose examples (use concise versions)
  * Redundant information
  * Overly detailed lists
  * Long code examples (reference files instead)

**AGENTS.md Specific**:
- **CRITICAL**: Keep file under 20,000 characters total
- Document all available agents and their specializations
- Include delegation patterns (which agents call others)
- Specify when to use each agent
- Document agent tools and permissions
- Keep agent descriptions concise but comprehensive
- If exceeding 20,000 characters, prioritize removing:
  * Verbose agent descriptions (use concise versions)
  * Redundant capability lists
  * Long example conversations (use short snippets)
  * Detailed implementation notes (reference agent files instead)

**General Quality**:
- Ensure accuracy over verbosity
- Use bullet points for clarity
- Reference other docs instead of duplicating
- Maintain consistent formatting
- Keep examples concise and relevant

### 8. Special Sections to Verify

**Available Agents Section**:
- Document all agents in tool-specific directories
- Include agent descriptions and specializations
- Document delegation patterns between agents
- Specify when to use each agent
- Example agent types to look for:
  * Backend/implementation engineers
  * Linting specialists (basic and advanced)
  * General-purpose research agents
  * Domain-specific experts

**Implementation Lessons Learned**:
- Keep valuable insights from development
- Add new lessons from recent changes
- Don't remove unless obsolete

**Design Decisions**:
- Document new architectural choices
- Explain rationale for major changes
- Keep record of what worked well

**Testing Requirements**:
- Verify environment handling rules
- Check isolation requirements
- Ensure safety guidelines are current

**Security Rules**:
- Keep all security validations documented
- Add new security measures
- Ensure credential handling rules are clear

### 9. Cross-Reference with Other Documentation

- Ensure context files don't contradict README.md
- Verify examples match actual implementation
- Check that commands work as documented
- Validate descriptions align with code comments

### 10. Final Character Count Check

**For CLAUDE.md**:
- After all edits, check file size with `wc -c CLAUDE.md`
- If over 20,000 characters, further condense:
  * Remove verbose sections
  * Use bullet points instead of paragraphs
  * Reference other docs instead of duplicating
- Target: Keep under 20,000 characters while maintaining essential information

**For AGENTS.md**:
- After all edits, check file size with `wc -c AGENTS.md`
- If over 20,000 characters, further condense:
  * Shorten agent descriptions
  * Remove redundant capability lists
  * Use concise examples
  * Reference agent files for detailed info
- Target: Keep under 20,000 characters while maintaining essential information

## Task Delegation for Complex Updates

For complex architectural documentation, delegate to specialized agents using the Task tool:

**Backend/Implementation Engineer**:
- Agent: `backend-engineer` (or language-specific variant)
- Use for: Generating comprehensive architectural documentation
- Handles: Detailed module descriptions, usage examples, design patterns
- Example:
  ```
  Task(description="Update architectural docs",
       prompt="Review architectural changes and update context documentation...",
       subagent_type="backend-engineer")
  ```

**General Purpose Agent**:
- Agent: `general-purpose`
- Use for: Reviewing architectural changes, validating design decisions
- Handles: Structure improvements, best practices validation
- Example:
  ```
  Task(description="Review architecture",
       prompt="Review architectural changes for best practices...",
       subagent_type="general-purpose")
  ```

## Examples of Changes Requiring Updates

- Adding new module → Update Project Structure
- Adding new dependency → Update Dependencies with purpose
- Refactoring responsibilities → Update component descriptions
- Adding new API endpoint → Update API documentation
- Adding new agent → Update Available Agents section
- Modifying agent capabilities → Update delegation patterns
- Changing testing approach → Update Testing Strategy
- Implementing security validation → Update Security Rules
- Adding database migration → Update Database Management
- Learning from bug/issue → Add to Lessons Learned

## Usage Examples

- Command with default mode (auto-update)
- Command with `--check-only` flag (report only)
- Command with `--auto-update` flag (explicit update)
