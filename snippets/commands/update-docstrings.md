# Update Documentation Command

## Your task

Review current code changes and ensure all related documentation accurately reflects the implementation.

**CRITICAL**: Use the Task tool to delegate to specialized documentation agents for comprehensive updates. Do NOT attempt to update extensive documentation manually.

## Argument Parsing

Parse the review mode from arguments:
- `--check-only`: Only report documentation issues without making changes
- `--auto-update`: Update documentation to match code changes (default)
- `--focus=<module>`: Focus on specific module or component
- Arguments: $ARGUMENTS

## Change Analysis

Analyze the version control diff to identify code changes:
- New functions, classes, or modules added
- Modified function signatures or behavior
- Removed or deprecated functionality
- Changed error types or handling
- Modified data structures or APIs
- New or changed configuration options
- Algorithm or logic changes

**For comprehensive documentation updates, delegate to specialized agents using Task:**
- Use the Task tool with appropriate subagent_type for your language/project
- Example delegation:
  ```
  Task(description="Update code documentation",
       prompt="Review code changes in [files] and update documentation to match implementation. Add missing docs for public APIs...",
       subagent_type="<appropriate-backend-engineer-agent>")
  ```
- The agent will handle:
  * Adding missing documentation to new or undocumented code
  * Improving existing documentation with examples
  * Ensuring all public APIs have proper documentation
  * Adding module-level documentation where missing
  * Generating comprehensive architectural documentation
- The agent will handle complex documentation patterns and ensure consistency

## Documentation Review

Review documentation accuracy for changed code:

**Documentation types to check**:
- **Inline documentation**: Function, class, and module-level documentation (docstrings, JSDoc, XML docs, etc.)
- **Type annotations**: Function signatures and return types
- **Module documentation**: Top-level module or package descriptions
- **Architecture documentation**: High-level design documents (CLAUDE.md, README.md, etc.)
- **API documentation**: REST/GraphQL/RPC specifications
- **Examples in docs**: Code examples in documentation

## Issue Identification

Identify documentation issues based on changes:

**Common documentation problems**:
- Documentation describing old behavior
- Missing documentation for new public APIs
- Outdated parameter descriptions
- Incorrect return type documentation
- Stale examples that won't run
- Module docs not reflecting new responsibilities
- Architecture documentation outdated
- API endpoints without documentation

## Update Application

Apply updates based on mode:

**Check-only mode (--check-only)**:
- List all documentation discrepancies found
- Show specific lines needing updates
- Highlight missing documentation
- Report outdated or incorrect information
- Suggest documentation improvements

**Auto-update mode (--auto-update or default)**:
- Use Task to delegate to appropriate backend engineer agent for documentation updates
- Update inline documentation to match implementation
- Add missing documentation for public items
- Fix parameter and return type descriptions
- Update examples to run with current code
- Correct module-level documentation
- Update architecture documentation if design changed
- Ensure API endpoints are documented

## Documentation Standards

Enforce language-appropriate documentation conventions:

**General documentation best practices**:
- Start with brief description
- Follow language-specific documentation format (Google style, JSDoc, XML docs, etc.)
- Document all public items
- Include parameter descriptions
- Document return values
- Document exceptions/errors that can be raised
- Add type annotations where applicable
- Use examples section for code examples
- Ensure examples are runnable

## Module-Specific Checks

When `--focus=<module>` is specified:
- Concentrate documentation review on the specified module or component
- Check both the module's internal documentation and its public API
- Verify cross-references to/from other modules remain accurate
- Ensure module-level documentation reflects current responsibilities

## Architecture Documentation Synchronization

**Sections to keep updated in architecture docs**:
- Module organization and responsibilities
- Key architecture decisions
- Testing strategy and requirements
- Security rules and validations
- Implementation lessons learned
- Critical requirements and constraints

## Quality Criteria

**Documentation quality checks**:
- **Accuracy**: Matches current implementation
- **Completeness**: All public APIs documented
- **Clarity**: Easy to understand
- **Consistency**: Uniform style and terminology
- **Examples**: Working code examples where helpful
- **Cross-references**: Links between related items

## Examples of Changes Requiring Documentation Updates

- New public function → Add documentation comment
- Changed function behavior → Update documentation
- New error type → Document in error documentation
- Modified algorithm → Update implementation comments
- New module → Add module-level documentation
- Architecture change → Update architecture docs
- New requirements → Document in module/project documentation

## Usage Examples

```
/update-docstrings                    # automatically update docs based on code changes
/update-docstrings --check-only       # report documentation issues without changes
/update-docstrings --focus=<module>   # focus on specific module documentation
```
