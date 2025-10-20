# AI Coding Agents and Commands

This repository provides a comprehensive collection of AI agents and commands designed to work with both **Claude Code** and **OpenCode**. These resources help you automate common development tasks, enforce coding standards, and accelerate your workflow.

## Quick Start

### Installation with AGPM

**IMPORTANT**: These agents, commands, and snippets are designed to be installed using [AGPM (AI Generated Prompt Manager)](https://github.com/aig787/agpm).

AGPM is a Git-based package manager for AI coding assistant resources that:

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

## Available Agents

### Backend Engineers

#### Python Backend Engineer
- **Purpose**: Design, implement, and optimize Python backend systems
- **Capabilities**: API design, database architecture, performance optimization
- **Usage**: Use for FastAPI, Django, Flask projects, microservices, and backend refactoring

#### Advanced Backend Engineer  
- **Purpose**: Complex backend architecture and enterprise-scale systems
- **Capabilities**: System design, scalability, security patterns, advanced optimization
- **Usage**: Large-scale applications, performance-critical systems, architectural decisions

### Code Quality Specialists

#### Standard Linting Agent
- **Purpose**: Basic code quality fixes and formatting
- **Capabilities**: Mechanical fixes, style corrections, import organization
- **Usage**: Day-to-day code maintenance, CI/CD pipelines, quick fixes

#### Advanced Linting Agent
- **Purpose**: Complex code quality improvements and refactoring
- **Capabilities**: Security fixes, performance optimizations, architectural improvements
- **Usage**: Code reviews, security audits, performance tuning

### General Purpose Agent
- **Purpose**: Versatile agent for various development tasks
- **Capabilities**: File operations, debugging, documentation, general coding assistance
- **Usage**: Multi-language projects, general development tasks, learning new codebases

## Available Commands

### Code Quality Commands

#### `/lint` - Code Quality Checks
Run comprehensive code quality checks with multiple modes:

```bash
/lint                    # standard checks
/lint --fix              # apply automatic fixes  
/lint --fix --test       # apply fixes and run tests
/lint --check            # CI mode with strict validation
/lint --all              # all checks including type checking
/lint --doc              # improve documentation
```

**Features**:
- Language-agnostic (configurable per project)
- Automatic fix application
- CI/CD integration
- Test verification
- Documentation improvement

#### `/commit` - Smart Commits
Create conventional commits with validation:

```bash
/commit "feat: add user authentication"           # create commit
/commit --fixup "fix: resolve login bug"         # fixup commit  
/commit --amend                                  # amend last commit
/commit --rebase                                 # interactive rebase
```

**Features**:
- Conventional commit format validation
- Automatic commit message generation
- Git history management
- Branch protection integration

### Documentation Commands

#### `/update-docs` - Documentation Updates
Keep project documentation synchronized:

```bash
/update-docs                                     # update all docs
/update-docs --api                               # update API docs only
/update-docs --readme                            # update README only
/update-docs --force                             # force regeneration
```

#### `/update-docstrings` - Code Documentation
Update inline code documentation:

```bash
/update-docstrings                               # update all docstrings
/update-docstrings --module                      # module-level only
/update-docstrings --function                    # function-level only
/update-docstrings --class                       # class-level only
```

### Review Commands

#### `/pr-self-review` - Pull Request Review
Automated PR review and quality checks:

```bash
/pr-self-review                                  # full PR review
/pr-self-review --security                       # security-focused review
/pr-self-review --performance                    # performance-focused review
/pr-self-review --docs                           # documentation review
```

#### `/review-docs` - Documentation Review
Review and improve documentation quality:

```bash
/review-docs                                     # review all docs
/review-docs --api                               # API documentation review
/review-docs --user-guide                        # user guide review
```

### Development Commands

#### `/update-agentic-context` - Context Management
Update AI agent context and configuration:

```bash
/update-agentic-context                          # update all context
/update-agentic-context --agents                 # agent context only
/update-agentic-context --commands               # command context only
```

## Tool-Specific Usage

### Claude Code

**Installation**:
```bash
npm install -g @anthropic-ai/claude-code
claude  # Navigate to your project first
```

**Using Agents**:
```bash
# Load an agent
@backend-engineer

# Use commands
/lint --fix
/commit "feat: add new endpoint"
```

**Key Features**:
- Native terminal integration
- Task tool for delegation
- MCP (Model Context Protocol) support
- Unix philosophy composability

### OpenCode  

**Installation**:
```bash
curl -fsSL https://opencode.ai/install | bash
opencode  # Navigate to your project first
```

**Using Agents**:
```bash
# Switch to agent mode
/agent backend-engineer

# Use commands  
/lint --fix
/commit "feat: add new endpoint"
```

**Key Features**:
- Terminal UI (TUI) interface
- Plan/Build modes
- Multi-provider support
- Visual theme system

## Project Configuration

### Language-Specific Configuration

Many commands support language-specific configuration. Create a `.agpm/snippets/` directory in your project:

```bash
# Python project configuration
.agpm/snippets/lint-config.md

# JavaScript project configuration  
.agpm/snippets/eslint-config.md

# Go project configuration
.agpm/snippets/gofmt-config.md
```

### Example: Python Lint Configuration

Create `.agpm/snippets/lint-config.md`:

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
- **Agent**: python-linting-standard
- **Purpose**: Mechanical fixes

### Complex Fixes  
- **Agent**: python-linting-advanced
- **Purpose**: Refactoring, security

## Best Practices
- Use async libraries
- Keep mock signatures matching APIs
- Follow PEP 8 style guide
```

## Architecture

This repository uses a **split architecture** pattern:

```
agpm-resources/
├── snippets/                    # Shared business logic (tool-agnostic)
│   ├── agents/                  # Core agent instructions
│   ├── commands/                # Core command logic
│   └── standards/               # Language-specific configurations
├── claude-code/                 # Claude Code specific wrappers
│   ├── agents/                  # Claude Code agent frontmatter
│   └── commands/                # Claude Code command frontmatter
└── opencode/                    # OpenCode specific wrappers
    ├── agents/                  # OpenCode agent frontmatter
    └── commands/                # OpenCode command frontmatter
```

**Benefits**:
1. **Single Source of Truth**: Core logic in `snippets/` eliminates duplication
2. **Tool-Specific Customization**: Wrappers add tool-specific context and frontmatter
3. **Maintainability**: Updates to core logic only need to happen once
4. **Consistency**: Agents and commands behave consistently across tools

## Best Practices

1. **Start with AGPM**: Use AGPM to manage installations and dependencies
2. **Configure per Project**: Customize `.agpm/snippets/` for your project's needs
3. **Use Appropriate Agents**: Choose specialized agents for complex tasks
4. **Leverage Commands**: Use commands for repetitive tasks and automation
5. **Keep Updated**: Regularly update agents and commands for latest improvements
6. **Test Locally**: Test agents and commands in your development environment first
7. **Contribute Back**: Share improvements and new agents with the community

## Getting Help

- **AGPM Documentation**: https://github.com/aig787/agpm
- **Claude Code Docs**: https://docs.claude.com/en/docs/claude-code
- **OpenCode Docs**: https://opencode.ai/docs/
- **Community**: Join our Discord for support and discussions

## Contributing

We welcome contributions! Please see our contribution guidelines for:

- Adding new agents and commands
- Improving existing ones  
- Supporting new languages and frameworks
- Documentation improvements
- Bug reports and feature requests

---

**Note**: This repository is actively maintained. Check back regularly for new agents, commands, and improvements to existing ones.