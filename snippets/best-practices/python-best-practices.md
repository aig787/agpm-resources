# Python Best Practices

This document defines technical best practices for Python development, covering tools, patterns, testing, security, and performance optimization.

## Core Principles

1. **Idiomatic Python**: Write code that follows Python conventions and PEP standards
2. **Zero Warnings Policy**: All code must pass linting without warnings
3. **Type Safety**: Use comprehensive type hints throughout the codebase
4. **Error Handling**: Implement proper exception handling and validation
5. **Clean Architecture**: Separate concerns with clear architectural layers
6. **Test Coverage**: Maintain >70% test coverage
7. **Security First**: Follow security best practices from the start

## Mandatory Completion Checklist

Before considering any Python code complete, you MUST:

1. ✅ Run formatter (`ruff format .` or `black .`)
2. ✅ Run linter (`ruff check .`)
3. ✅ Run type checker (`mypy .`)
4. ✅ Run tests (`pytest`)
5. ✅ Verify test coverage (`pytest --cov` - target >70%)
6. ✅ Verify all dependencies are properly declared

## Development Tools

### Package Management: uv (Recommended)

**Use `uv` for modern Python projects**: Fast, reliable dependency management

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize new project
uv init myproject
cd myproject

# Add dependencies
uv add fastapi sqlalchemy pydantic

# Add dev dependencies
uv add --dev pytest ruff mypy

# Run scripts
uv run python main.py
uv run pytest
uv run ruff check .

# Manage virtual environments
uv venv
source .venv/bin/activate  # Unix
# or
.venv\Scripts\activate  # Windows
```

### Alternative: Poetry

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Create new project
poetry new myproject
cd myproject

# Add dependencies
poetry add fastapi sqlalchemy pydantic

# Add dev dependencies
poetry add --group dev pytest ruff mypy

# Run scripts
poetry run python main.py
poetry run pytest
```

### Dependency Best Practices

- **Pin exact versions in production**: `package==1.2.3`
- **Use version ranges in libraries**: `package>=1.2,<2.0`
- **Keep dependencies updated**: Regularly review and update
- **Security auditing**: Use `pip-audit` or `safety check`
- **Separate dev dependencies**: Keep development tools separate from production deps
- **Document dependency choices**: Explain why specific versions are required

## Type Annotations

### Modern Type Syntax

**Use modern type syntax (Python 3.9+)**:

```python
# Good - Python 3.9+
def process_data(items: list[str], count: int) -> dict[str, int]:
    """Process a list of items."""
    return {item: count for item in items}

# Old style - only for Python 3.8 compatibility
from typing import List, Dict

def process_data(items: List[str], count: int) -> Dict[str, int]:
    return {item: count for item in items}
```

### Optional and Union Types

```python
from typing import Optional

# Python 3.9+
def find_user(user_id: int) -> dict[str, str] | None:
    """Find user by ID."""
    pass

# Python 3.10+ (preferred)
def find_user(user_id: int) -> dict[str, str] | None:
    """Find user by ID."""
    pass

# Python 3.8-3.9
def find_user(user_id: int) -> Optional[dict[str, str]]:
    """Find user by ID."""
    pass
```

### Protocol for Structural Typing

```python
from typing import Protocol

class Drawable(Protocol):
    """Any object with a draw method."""
    def draw(self) -> None:
        ...

def render(obj: Drawable) -> None:
    """Render any drawable object."""
    obj.draw()
```

### Generic Types with TypeVar

```python
from typing import TypeVar

T = TypeVar('T')

def first(items: list[T]) -> T | None:
    """Return first item or None."""
    return items[0] if items else None
```

### Callable Types

```python
from typing import Callable

def apply_transform(
    func: Callable[[int], str],
    value: int
) -> str:
    """Apply transformation function."""
    return func(value)
```

## Error Handling

### Exception Best Practices

**Use specific exceptions**:

```python
# Good
raise ValueError("Invalid user input: expected positive integer")

# Avoid
raise Exception("Something went wrong")
```

**Create custom exception hierarchy**:

```python
class AppError(Exception):
    """Base exception for application errors."""
    pass

class ValidationError(AppError):
    """Raised when validation fails."""
    pass

class DatabaseError(AppError):
    """Raised when database operation fails."""
    pass

class NotFoundError(AppError):
    """Raised when resource is not found."""
    pass
```

**Handle exceptions properly**:

```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise  # Re-raise to let caller handle
except AnotherError as e:
    # Handle and transform
    raise InternalError("Processing failed") from e
else:
    # Runs if no exception occurred
    logger.info("Operation succeeded")
finally:
    # Always runs
    cleanup_resources()
```

**Use context managers for resources**:

```python
# Good - automatic cleanup
with open('file.txt') as f:
    data = f.read()

# Avoid - manual cleanup required
f = open('file.txt')
try:
    data = f.read()
finally:
    f.close()
```

## Data Validation

### Pydantic Models

```python
from pydantic import BaseModel, Field, field_validator, EmailStr

class User(BaseModel):
    """User model with validation."""
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=0, le=150)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate name is not just whitespace."""
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

# Usage
user = User(id=1, name="John", email="john@example.com", age=30)
```

### Validation Best Practices

- **Validate at API boundaries**: Never trust external input
- **Use Pydantic** for automatic validation and serialization
- **Provide clear error messages**: Help users understand what went wrong
- **Consider dataclasses** for simpler internal data structures

```python
from dataclasses import dataclass

@dataclass
class Point:
    """2D point with coordinates."""
    x: float
    y: float

    def distance_from_origin(self) -> float:
        """Calculate distance from origin."""
        return (self.x ** 2 + self.y ** 2) ** 0.5
```

## Testing Strategy

### Pytest Framework

**Project structure**:

```
myproject/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/
│   ├── conftest.py        # Shared fixtures
│   ├── test_core.py       # Core module tests
│   └── test_utils.py      # Utils module tests
└── pyproject.toml
```

### Writing Tests

**Basic test**:

```python
def test_calculate_total():
    """Test total calculation."""
    result = calculate_total([10, 20, 30])
    assert result == 60
```

**Using fixtures**:

```python
import pytest

@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return User(id=1, name="Test User", email="test@example.com")

def test_user_name(sample_user):
    """Test user name attribute."""
    assert sample_user.name == "Test User"
```

**Parametrized tests**:

```python
@pytest.mark.parametrize("input,expected", [
    (0, 0),
    (1, 2),
    (2, 4),
    (5, 10),
])
def test_double(input, expected):
    """Test doubling function with multiple inputs."""
    assert double(input) == expected
```

**Testing async code**:

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await async_fetch_data()
    assert result is not None
```

**Mocking external dependencies**:

```python
from unittest.mock import Mock, patch

@patch('myapp.external_service.call')
def test_with_mock(mock_call):
    """Test with mocked external service."""
    mock_call.return_value = "mocked"
    result = my_function()
    assert result == "mocked"
    mock_call.assert_called_once()
```

### Testing Best Practices

- **Aim for >70% coverage**: Use `pytest --cov`
- **Test isolation**: Each test should be independent
- **Use descriptive test names**: `test_user_creation_with_valid_data`
- **Test edge cases**: Empty inputs, None values, boundary conditions
- **Use markers for organization**:
  ```python
  @pytest.mark.slow
  @pytest.mark.integration
  def test_database_integration():
      pass
  ```

## Linting & Code Quality

### Ruff Configuration

**Recommended `pyproject.toml` configuration**:

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
    "ARG",  # flake8-unused-arguments
    "SIM",  # flake8-simplify
    "S",    # bandit security
    "ANN",  # flake8-annotations
    "C90",  # mccabe complexity
]

ignore = [
    "ANN101",  # Missing type annotation for self
    "ANN102",  # Missing type annotation for cls
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
    "S101",    # Allow assert in tests
    "ANN",     # Don't require annotations in tests
]

[tool.ruff.lint.mccabe]
max-complexity = 10
```

### Linting Categories

**Mechanical fixes (safe to auto-fix)**:

- **F401**: Unused imports
- **I001, I002**: Import sorting and grouping
- **F841**: Unused variables (review first)
- **E501**: Line length violations
- **W series**: Whitespace issues
- **UP series**: Syntax updates (dict() → {})

**Complex fixes (requires analysis)**:

- **C901**: Cyclomatic complexity - refactor complex functions
- **S series**: Security issues - review carefully
- **B series**: Bug-prone patterns - understand before fixing
- **ARG series**: Unused arguments - consider API contracts
- **PLR series**: Refactoring suggestions - evaluate impact

### Mypy Type Checking

**Configuration**:

```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
```

**Usage**:

```bash
# Run type checking
mypy .

# Ignore specific errors when necessary
result = some_func()  # type: ignore[error-code]
```

## Async Programming

### Async Best Practices

**Use async for I/O-bound operations**:

```python
import asyncio
import aiohttp

async def fetch_data(url: str) -> dict:
    """Fetch data from URL asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

**Concurrent operations with gather**:

```python
async def fetch_all(urls: list[str]) -> list[dict]:
    """Fetch data from multiple URLs concurrently."""
    results = await asyncio.gather(
        *[fetch_data(url) for url in urls]
    )
    return results
```

**Handle blocking code properly**:

```python
import asyncio

async def process():
    """Process with blocking operation."""
    # Run blocking code in thread pool
    result = await asyncio.to_thread(blocking_operation)
    return result
```

**Async context managers**:

```python
async def process_resource():
    """Process resource with async context manager."""
    async with async_resource() as resource:
        await resource.process()
```

### Async Guidelines

- **Use async database drivers**: `asyncpg`, `aiomysql`
- **Don't mix blocking and async**: Use `asyncio.to_thread()` for blocking calls
- **Use async context managers** for resource management
- **Handle errors properly** in async code
- **Avoid blocking the event loop**: No CPU-intensive work in async functions

## Database Best Practices

### SQLAlchemy Modern Syntax

**Declarative models with Mapped**:

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    """Base class for all models."""
    pass

class User(Base):
    """User model."""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

class Post(Base):
    """Post model."""
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    author: Mapped[User] = relationship(back_populates="posts")
```

### Query Optimization

**Avoid N+1 queries**:

```python
from sqlalchemy.orm import selectinload

# Bad - N+1 queries
users = session.query(User).all()
for user in users:
    print(user.posts)  # Separate query for each user

# Good - single query with join
users = session.query(User).options(
    selectinload(User.posts)
).all()
```

**Use proper indexing**:

```python
from sqlalchemy import Index

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]

    __table_args__ = (
        Index('ix_user_email', 'email'),
    )
```

**Implement pagination**:

```python
def get_users_page(page: int, page_size: int = 20):
    """Get paginated users."""
    return session.query(User)\
        .offset(page * page_size)\
        .limit(page_size)\
        .all()
```

### Database Guidelines

- **Use Alembic for migrations**: Track all schema changes
- **Implement connection pooling**: Better performance
- **Use proper transaction management**: Commit or rollback explicitly
- **Batch operations when possible**: Bulk insert/update for large datasets
- **Monitor query performance**: Enable SQLAlchemy logging in development

## Security Best Practices

### Input Validation

**Always validate and sanitize input**:

```python
# Good - parameterized queries prevent SQL injection
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# Bad - vulnerable to SQL injection
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

### Password Hashing

**Use proper password hashing**:

```python
from passlib.hash import bcrypt

# Hash password
hashed = bcrypt.hash("user_password")

# Verify password
is_valid = bcrypt.verify("user_password", hashed)
```

### Secrets Management

**Never hardcode credentials**:

```python
import os
from dotenv import load_dotenv

# Load from environment
load_dotenv()
api_key = os.getenv("API_KEY")
database_url = os.getenv("DATABASE_URL")

# Avoid
api_key = "hardcoded-api-key-123"  # Bad!
```

### Security Guidelines

- **Validate all user input**: Never trust external data
- **Use parameterized queries**: Prevent SQL injection
- **Implement authentication & authorization**: JWT, OAuth2, etc.
- **Enable HTTPS**: Always use TLS in production
- **Implement rate limiting**: Prevent abuse
- **Don't log sensitive data**: Passwords, tokens, API keys
- **Regular security audits**: Use `bandit` for security linting
- **Implement CSRF protection**: For state-changing operations
- **Keep dependencies updated**: Address security vulnerabilities

```bash
# Security scanning
bandit -r src/
pip-audit  # or safety check
```

## Performance Optimization

### Profiling

**Profile before optimizing**:

```python
import cProfile

cProfile.run('my_function()')
```

### Use Generators

**Memory-efficient iteration**:

```python
def read_large_file(file_path: str):
    """Read file line by line efficiently."""
    with open(file_path) as f:
        for line in f:
            yield line.strip()

# Process without loading entire file
for line in read_large_file('huge.txt'):
    process(line)
```

### Caching

**Use caching for expensive operations**:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    """Cached expensive computation."""
    # Complex computation
    return result
```

### Performance Guidelines

- **Profile before optimizing**: Use `cProfile` or `py-spy`
- **Use generators** for memory efficiency with large datasets
- **Implement caching**: Redis or in-memory for frequently accessed data
- **Use connection pooling**: For database and HTTP connections
- **Batch operations**: Reduce round trips to database/API
- **Use lazy loading**: Load data only when needed
- **Optimize database queries**: Proper indexing, avoid N+1
- **Consider async I/O**: For I/O-bound operations
- **Choose appropriate data structures**: Based on access patterns

## Project Structure

**Recommended structure**:

```
myproject/
├── pyproject.toml          # Project configuration
├── README.md              # Project documentation
├── .gitignore             # Git ignore file
├── .env.example           # Environment variables template
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── main.py        # Application entry point
│       ├── api/           # API layer
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── dependencies.py
│       ├── core/          # Core business logic
│       │   ├── __init__.py
│       │   ├── config.py
│       │   └── security.py
│       ├── models/        # Data models
│       │   ├── __init__.py
│       │   └── user.py
│       ├── services/      # Business services
│       │   ├── __init__.py
│       │   └── user_service.py
│       ├── db/            # Database
│       │   ├── __init__.py
│       │   ├── base.py
│       │   └── session.py
│       └── utils/         # Utilities
│           └── __init__.py
├── tests/                 # Tests
│   ├── conftest.py
│   ├── test_api/
│   ├── test_models/
│   └── test_services/
├── migrations/            # Database migrations (Alembic)
└── scripts/              # Utility scripts
```

## CI/CD Integration

### Pre-commit Hooks

**`.pre-commit-config.yaml`**:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

### CI Pipeline Steps

1. **Run linting**: `ruff check .`
2. **Run type checking**: `mypy .`
3. **Run tests with coverage**: `pytest --cov --cov-report=html`
4. **Security scanning**: `bandit -r src/`
5. **Dependency auditing**: `pip-audit`
6. **Check formatting**: `ruff format --check .`

## Context7 Integration

Always use Context7 MCP server for current documentation when developing Python projects:

### Key Libraries

- `/astral-sh/uv` - Modern Python package manager
- `/astral-sh/ruff` - Fast Python linter and formatter
- `/python/mypy` - Static type checker
- `/pytest-dev/pytest` - Testing framework
- `/pydantic/pydantic` - Data validation
- `/sqlalchemy/sqlalchemy` - SQL toolkit and ORM
- `/fastapi/fastapi` - Modern async web framework
- `/django/django` - Full-featured web framework
- `/pallets/flask` - Lightweight web framework

### Example Usage

```
Create a FastAPI application with JWT authentication and PostgreSQL integration.
Include proper async patterns, validation, and error handling.
use context7 /fastapi/fastapi /pydantic/pydantic /sqlalchemy/sqlalchemy
```

## Summary

- **Use modern tools**: `uv`, `ruff`, `mypy`, `pytest`
- **Type everything**: Comprehensive type hints for safety
- **Test thoroughly**: >70% coverage, unit + integration tests
- **Validate all input**: Never trust external data
- **Handle errors properly**: Specific exceptions, proper hierarchy
- **Optimize when needed**: Profile first, then optimize
- **Secure by default**: Authentication, validation, encryption
- **Follow clean architecture**: Separate concerns, clear layers
- **Automate quality checks**: CI/CD, pre-commit hooks
- **Keep dependencies updated**: Security and features

These practices ensure robust, maintainable, and secure Python applications.
