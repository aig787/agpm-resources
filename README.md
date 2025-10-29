# AGPM Resources - AI Coding Agent & Command Library

[![AGPM Version](https://img.shields.io/badge/AGPM-compatible-blue.svg)](https://github.com/aig787/agpm)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)

A comprehensive collection of AI agents, commands, and resources for **Claude Code** and **OpenCode**. This repository provides production-ready artifacts that automate development tasks, enforce coding standards, and accelerate your workflow.

## 🚀 Quick Start

### Prerequisites

Install [AGPM (AI Generated Prompt Manager)](https://github.com/aig787/agpm) - the Git-based package manager for AI coding resources:

```bash
# macOS/Linux via Homebrew
brew install aig787/agpm/agpm-cli

# Cross-platform via Cargo
cargo install agpm-cli

# Pre-built binaries
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/aig787/agpm/releases/latest/download/agpm-installer.sh | sh
```

### Installation

1. **Initialize your project**:
   ```bash
   cd your-project
   agpm init
   ```

2. **Add this repository as a source** in `agpm.toml`:
   ```toml
   [sources]
   agpm-resources = "https://github.com/aig787/agpm-resources.git"
   ```

3. **Add resources** to your `agpm.toml`:
   ```toml
   [agents]
   backend-engineer = { source = "agpm-resources", path = "claude-code/agents/backend-engineer.md" }
   linting-standard = { source = "agpm-resources", path = "claude-code/agents/linting-standard.md" }
   
   [commands]
   lint = { source = "agpm-resources", path = "claude-code/commands/lint.md" }
   commit = { source = "agpm-resources", path = "claude-code/commands/commit.md" }
   ```

4. **Install dependencies**:
   ```bash
   agpm install
   ```

## 📦 Available Resources

### 🤖 AI Agents

Specialized agents for different development domains and expertise levels:

#### Backend Development
- **`backend-engineer`** - General backend development (APIs, databases, services)
- **`backend-engineer-advanced`** - Complex architecture and enterprise systems
- **`backend-pair-programmer`** (OpenCode) - Interactive pair programming

#### Frontend Development  
- **`frontend-engineer`** - Modern frontend development (React, Vue, Angular)

#### Code Quality
- **`linting-standard`** - Basic code quality fixes and formatting
- **`linting-advanced`** - Complex refactoring and security improvements

#### Specialized Expertise
- **`git-expert`** - Git workflows and advanced operations
- **`github-actions-expert`** - CI/CD pipeline automation
- **`k8s-expert`** - Kubernetes deployment and management
- **`general-purpose`** - Versatile agent for various tasks

### ⚡ Commands

Automation commands for common development workflows:

#### Code Quality
- **`/lint`** - Comprehensive code quality checks with auto-fix
- **`/pr-self-review`** - Automated pull request review
- **`/review-docs`** - Documentation quality review

#### Git Workflow
- **`/commit`** - Smart conventional commits with validation
- **`/squash`** - Git history cleanup
- **`/checkpoint`** - Development milestone management

#### Documentation
- **`/update-docs`** - Keep project documentation synchronized
- **`/update-docstrings`** - Update inline code documentation
- **`/update-agentic-context`** - Manage AI agent context

#### Deployment
- **`/gh-pr-create`** - Automated pull request creation

### 🛠️ Language & Framework Support

#### Languages
- **Python** - FastAPI, Django, Flask best practices
- **JavaScript/TypeScript** - Node.js, React, Vue patterns
- **Go** - Microservices, concurrent programming
- **Java** - Spring Boot, enterprise patterns
- **Rust** - Systems programming, performance optimization

#### Frameworks
- **React** - Component architecture, hooks, state management
- **Vue** - Composition API, reactive patterns
- **Angular** - Services, dependency injection, RxJS

## 🎯 Template System

This repository uses AGPM's powerful template system to generate language-specific variants. Template variables can be set globally in the `[project]` section or overridden per-resource.

### Setting Project Variables (Recommended)

Define variables once in the `[project]` section:

```toml
[project]
language = "python"
framework = "django"
best_practices = "best_practices.md"
styleguide = "styleguide.md"
```

All resources will automatically use these variables unless explicitly overridden.

### Language-Specific Agents

Generate agents tailored to your project's language:

```toml
# Uses global project variables
backend-engineer = { 
  source = "agpm-resources", 
  path = "claude-code/agents/backend-engineer.md"
}

# Override specific variables for this resource only
frontend-engineer-react = { 
  source = "agpm-resources", 
  path = "claude-code/agents/frontend-engineer.md",
  filename = "frontend-engineer-react",
  template_vars = { project = { language = "javascript", framework = "react" } }
}
```

### Available Template Variables

- **`project.language`** - Programming language (python, javascript, golang, java, rust)
- **`project.framework`** - Framework (react, vue, angular, django, spring-boot)
- **`project.best_practices`** - Language-specific best practices guide
- **`project.styleguide`** - Language style guide

**Note**: `template_vars` are optional and only needed when you want to override the global `[project]` settings for a specific resource.

## 🏗️ Repository Architecture

```
agpm-resources/
├── snippets/                    # Core business logic (tool-agnostic)
│   ├── agents/                  # Agent core instructions
│   ├── commands/                # Command core logic
│   ├── best-practices/          # Language-specific best practices
│   ├── frameworks/              # Framework-specific patterns
│   └── styleguides/             # Language style guides
├── claude-code/                 # Claude Code specific wrappers
│   ├── agents/                  # Claude Code agent frontmatter
│   ├── commands/                # Claude Code command frontmatter
│   ├── hooks/                   # Claude Code hooks
│   └── mcp-servers/             # MCP server configurations
├── opencode/                    # OpenCode specific wrappers
│   ├── agents/                  # OpenCode agent frontmatter
│   ├── commands/                # OpenCode command frontmatter
│   └── mcp-servers/             # MCP server configurations
├── private/                     # Private/internal resources
└── examples/                    # Configuration examples
```

### Split Architecture Benefits

1. **Single Source of Truth** - Core logic in `snippets/` eliminates duplication
2. **Tool-Specific Customization** - Wrappers add tool-specific context
3. **Maintainability** - Updates only need to happen once
4. **Consistency** - Uniform behavior across tools

## 🔧 Tool Integration

### Claude Code

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Navigate to project and use agents
cd your-project
claude

# Load an agent
@backend-engineer-python

# Use commands
/lint --fix
/commit "feat: add user authentication"
```

### OpenCode

```bash
# Install OpenCode
curl -fsSL https://opencode.ai/install | bash

# Navigate to project and use agents
cd your-project
opencode

# Switch to agent mode
/agent backend-engineer-python

# Use commands
/lint --fix
/commit "feat: add user authentication"
```

## 📋 Configuration Examples

### Complete Python Project Setup

```toml
# agpm.toml
[project]
language = "python"
best_practices = "best_practices.md"
styleguide = "styleguide.md"

[sources]
agpm-resources = "https://github.com/aig787/agpm-resources.git"

[agents]
backend-engineer = { source = "agpm-resources", path = "claude-code/agents/backend-engineer.md" }
linting-standard = { source = "agpm-resources", path = "claude-code/agents/linting-standard.md" }

[commands]
lint = { source = "agpm-resources", path = "claude-code/commands/lint.md" }
commit = { source = "agpm-resources", path = "claude-code/commands/commit.md" }
pr-self-review = { source = "agpm-resources", path = "claude-code/commands/pr-self-review.md" }

[snippets]
python-best-practices = { source = "agpm-resources", path = "snippets/best-practices/python-best-practices.md" }
python-styleguide = { source = "agpm-resources", path = "snippets/styleguides/python-styleguide.md" }
```

### React Frontend Project Setup

```toml
# agpm.toml
[project]
language = "javascript"
framework = "react"

[sources]
agpm-resources = "https://github.com/aig787/agpm-resources.git"

[agents]
frontend-engineer = { source = "agpm-resources", path = "claude-code/agents/frontend-engineer.md" }

[snippets]
react-patterns = { source = "agpm-resources", path = "snippets/frameworks/react.md" }
javascript-best-practices = { source = "agpm-resources", path = "snippets/best-practices/javascript-best-practices.md" }
```

## 🎨 Customization

### Project-Specific Configuration

Create `.agpm/snippets/` in your project for custom configurations:

```bash
# Project-specific linting configuration
.agpm/snippets/lint-config.md

# Team-specific conventions
.agpm/snippets/team-conventions.md

# Company standards
.agpm/snippets/company-standards.md
```

### Custom Agent Variants

You can create highly specific agent variants by setting project variables or using overrides:

```toml
# Option 1: Set globally for all resources
[project]
language = "java"
framework = "spring-boot"
architecture = "microservices"
scale = "enterprise"

[agents]
backend-engineer = { 
  source = "agpm-resources", 
  path = "claude-code/agents/backend-engineer.md",
  filename = "backend-engineer-enterprise"
}

# Option 2: Override for specific resource only
[agents]
backend-engineer-standard = { source = "agpm-resources", path = "claude-code/agents/backend-engineer.md" }
backend-engineer-enterprise = { 
  source = "agpm-resources", 
  path = "claude-code/agents/backend-engineer.md",
  filename = "backend-engineer-enterprise",
  template_vars = { 
    project = { 
      language = "java",
      framework = "spring-boot",
      architecture = "microservices",
      scale = "enterprise"
    } 
  }
}
```

## 🔄 Maintenance

### Updating Resources

```bash
# Check for updates
agpm outdated

# Update within version constraints
agpm update

# Update to latest versions
agpm update --latest
```

### Version Management

AGPM uses semantic versioning and Git references:

```toml
# Specific version
backend-engineer = { source = "agpm-resources", path = "...", version = "v1.2.0" }

# Version range
linting-standard = { source = "agpm-resources", path = "...", version = "~1.0.0" }

# Git branch/commit
experimental-agent = { source = "agpm-resources", path = "...", ref = "develop" }
```

## 🤝 Contributing

We welcome contributions! See our contribution guidelines for:

- Adding new agents and commands
- Improving existing ones
- Supporting new languages and frameworks
- Documentation improvements
- Bug reports and feature requests

### Development Workflow

1. Fork this repository
2. Create a feature branch
3. Add your improvements to `snippets/` (core logic)
4. Update tool-specific wrappers if needed
5. Submit a pull request

## 📚 Documentation

- **[AGPM Documentation](https://github.com/aig787/agpm)** - Package manager usage
- **[Claude Code Docs](https://docs.claude.com/en/docs/claude-code)** - Claude Code guide
- **[OpenCode Docs](https://opencode.ai/docs/)** - OpenCode guide
- **[Examples](./examples/)** - Configuration examples
- **[Agent Catalog](./AGENTS.md)** - Detailed agent descriptions

## 🆘 Support

- 🐛 [Issue Tracker](https://github.com/aig787/agpm-resources/issues)
- 💬 [Discussions](https://github.com/aig787/agpm-resources/discussions)
- 📖 [AGPM Documentation](https://github.com/aig787/agpm)

## 📄 License

MIT License - see [LICENSE.md](LICENSE.md) for details.

---

**Built with ❤️ for the AI development community**

*This repository is actively maintained. Check back regularly for new agents, commands, and improvements.*