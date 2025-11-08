---
agpm:
  version: "1.0.0"
---

# Python Style Guide

This document defines the code style standards for Python projects. It covers formatting, naming conventions, type hints, imports, and documentation style.

## Code Formatting

### Line Length
- **Maximum line length**: 88-100 characters (configurable per project)
- **Break long lines** at logical points for readability
- Use parentheses for implicit line continuation

### Indentation
- **Use 4 spaces** per indentation level
- **Never mix tabs and spaces**
- Continuation lines should align with opening delimiter or use hanging indent

### Whitespace
- **Two blank lines** between top-level classes and functions
- **One blank line** between methods within a class
- **One blank line** at end of file
- **No trailing whitespace** on any line
- **Spaces around operators**: `x = y + z`, not `x=y+z`
- **No spaces** inside brackets: `[1, 2, 3]`, not `[ 1, 2, 3 ]`
- **Spaces after commas**: `func(a, b, c)`, not `func(a,b,c)`

### Trailing Commas
- Use trailing commas in multi-line structures:
  ```python
  items = [
      "first",
      "second",
      "third",  # trailing comma
  ]
  ```

### String Quotes
- **Prefer double quotes** for strings: `"hello"`
- **Use single quotes** to avoid escaping: `'He said "hi"'`
- **Triple double quotes** for docstrings: `"""Docstring"""`
- Be consistent within a project

## Naming Conventions

### Variables and Functions
- **Use `snake_case`** for variables and functions
- **Use descriptive names** that convey intent
- **Avoid single-letter names** except in:
  - List comprehensions: `[x for x in items]`
  - Loop counters: `for i in range(10)`
  - Common mathematical variables: `x, y, z`
  - Lambda parameters: `lambda x: x * 2`

Examples:
```python
# Good
user_count = 10
def calculate_total(items):
    pass

# Avoid
uc = 10
def calcTot(items):
    pass
```

### Classes
- **Use `PascalCase`** for class names
- **Use nouns** for class names
- **Use clear, descriptive names**

Examples:
```python
# Good
class UserAccount:
    pass

class HTTPResponse:
    pass

# Avoid
class user_account:
    pass

class Http_Response:
    pass
```

### Constants
- **Use `SCREAMING_SNAKE_CASE`** for constants
- Define at module level

Examples:
```python
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"
```

### Private and Protected
- **Single underscore prefix** for protected attributes: `_protected`
- **Double underscore prefix** for name-mangled attributes: `__private`
- **No leading/trailing underscores** for public attributes

Examples:
```python
class MyClass:
    def __init__(self):
        self.public = "accessible"
        self._protected = "internal use"
        self.__private = "name mangled"
```

### Boolean Names
- **Prefix with `is_`, `has_`, or `should_`** for clarity
- Use affirmative names

Examples:
```python
is_active = True
has_permission = False
should_retry = True

# Avoid
active = True  # ambiguous
no_permission = True  # negative naming
```

### Module Names
- **Use short, lowercase names** without underscores if possible
- **Use underscores** if it improves readability
- **Avoid dashes** in module names

Examples:
```python
# Good
import users
import user_service

# Avoid
import Users
import user-service  # syntax error
```

## Type Hints

Type hints improve code readability, enable better IDE support, and catch errors early through static type checking with mypy.

### When to Use Type Hints

- **Always annotate function signatures**: Parameters and return types
- **Annotate public APIs**: All public functions and methods
- **Annotate complex variables**: When type isn't obvious from assignment
- **Skip obvious cases**: Simple literals where type is clear

### Basic Type Annotations

```python
# Function parameters and return types
def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old"

# Variable annotations
user_count: int = 0
items: list[str] = []
mapping: dict[str, int] = {}

# Multiple return values
def get_coordinates() -> tuple[float, float]:
    return (1.0, 2.0)
```

### Optional and Union Types

```python
from typing import Optional, Union

# Optional - value can be None
def find_user(user_id: int) -> Optional[str]:
    """Return username or None if not found."""
    return None

# Modern syntax (Python 3.10+)
def find_user(user_id: int) -> str | None:
    return None

# Union - multiple possible types
def process_id(user_id: Union[int, str]) -> str:
    return str(user_id)

# Modern syntax (Python 3.10+)
def process_id(user_id: int | str) -> str:
    return str(user_id)
```

### Collections and Generics

```python
from typing import Any, Dict, List, Set, Tuple

# Generic collections (older style)
def get_users() -> List[str]:
    return ["alice", "bob"]

def count_items(items: Dict[str, int]) -> int:
    return sum(items.values())

# Modern generic syntax (Python 3.9+)
def get_users() -> list[str]:
    return ["alice", "bob"]

def count_items(items: dict[str, int]) -> int:
    return sum(items.values())

# Nested generics
def get_user_groups() -> dict[str, list[str]]:
    return {"admins": ["alice"], "users": ["bob"]}

# Sets and tuples
def get_unique_ids() -> set[int]:
    return {1, 2, 3}

def get_range() -> tuple[int, int]:
    return (0, 100)
```

### Callable Types

```python
from typing import Callable

# Function that takes a callback
def process_data(
    data: list[int],
    transform: Callable[[int], str]
) -> list[str]:
    return [transform(x) for x in data]

# Usage
def int_to_str(x: int) -> str:
    return str(x)

result = process_data([1, 2, 3], int_to_str)
```

### TypedDict for Structured Dictionaries

```python
from typing import TypedDict, NotRequired

class UserDict(TypedDict):
    username: str
    email: str
    age: int

class PartialUser(TypedDict):
    username: str
    age: NotRequired[int]  # Optional field
```

### Type Aliases

```python
# Simple aliases
UserId = int
JsonValue = Union[str, int, float, bool, None, dict[str, "JsonValue"], list["JsonValue"]]
Callback = Callable[[int, str], bool]
```

### Protocols for Structural Typing

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

# Any class with draw() method satisfies Drawable
def render(shape: Drawable) -> None:
    shape.draw()
```

### Generic Classes

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()
```

### Special Types

```python
from typing import Any, ClassVar, Literal, cast

# Any - use sparingly, prefer generics
def process_unknown(data: Any) -> Any:
    return data

# ClassVar for class attributes
class Counter:
    total_count: ClassVar[int] = 0
    count: int

# Literal for specific values
def set_mode(mode: Literal["read", "write", "append"]) -> None:
    pass

# Cast for type assertions
config = cast(dict[str, str], get_config())
```

### Best Practices

- **Prefer built-in generics** (`list`, `dict`) over `typing.List`, `typing.Dict` (Python 3.9+)
- **Use `Optional[T]` or `T | None`** instead of `Union[T, None]`
- **Avoid `Any`** when possible - use generics or protocols
- **Use `TypedDict`** for structured dictionaries instead of `dict[str, Any]`
- **Document complex types** with comments when the signature isn't clear
- **Enable strict mode** in mypy for maximum type safety

## Import Organization

### Import Grouping
Organize imports in three distinct groups with one blank line between each:

1. **Standard library imports**
2. **Third-party imports**
3. **Local application imports**

Within each group, sort imports alphabetically.

### Import Style
- **One import per line** for clarity:
  ```python
  # Good
  import os
  import sys

  # Avoid
  import os, sys
  ```

- **Group imports from same module**:
  ```python
  from typing import Any, Dict, List, Optional
  ```

- **Use absolute imports** for clarity:
  ```python
  # Good
  from myapp.core import config

  # Avoid (in most cases)
  from ..core import config
  ```

- **Exception**: Relative imports acceptable within packages

- **Avoid wildcard imports**:
  ```python
  # Avoid
  from module import *

  # Good
  from module import specific_function
  ```

### Import Example
```python
# Standard library
import os
import sys
from typing import Any, Dict, List, Optional

# Third-party
import numpy as np
from fastapi import FastAPI
from sqlalchemy import create_engine

# Local
from myapp.core import config
from myapp.models import User
from myapp.services import user_service
```

## Documentation Style

### Docstring Format
- **Use triple double quotes**: `"""Docstring"""`
- **First line**: Brief summary (one line, imperative mood)
- **Blank line** after summary if there's more content
- **Detailed description**: Multi-paragraph explanation if needed
- **Args, Returns, Raises**: Document function parameters and behavior

### Module Docstrings
Place at the top of every Python file:

```python
"""User authentication and authorization module.

This module provides functionality for user login, logout,
token generation, and permission checking.
"""

import os
```

### Function Docstrings

#### Google Style (Recommended)
```python
def calculate_total(items: list[float], tax_rate: float) -> float:
    """Calculate the total cost including tax.

    Args:
        items: List of item prices
        tax_rate: Tax rate as a decimal (e.g., 0.08 for 8%)

    Returns:
        Total cost with tax applied

    Raises:
        ValueError: If tax_rate is negative
    """
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")

    subtotal = sum(items)
    return subtotal * (1 + tax_rate)
```

#### NumPy Style (Alternative)
```python
def calculate_total(items: list[float], tax_rate: float) -> float:
    """Calculate the total cost including tax.

    Parameters
    ----------
    items : list[float]
        List of item prices
    tax_rate : float
        Tax rate as a decimal (e.g., 0.08 for 8%)

    Returns
    -------
    float
        Total cost with tax applied

    Raises
    ------
    ValueError
        If tax_rate is negative
    """
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")

    subtotal = sum(items)
    return subtotal * (1 + tax_rate)
```

### Class Docstrings
```python
class UserAccount:
    """Represents a user account with authentication capabilities.

    This class handles user registration, login, and profile management.
    It integrates with the authentication service for token management.

    Attributes:
        username: The unique username for the account
        email: The user's email address
        is_active: Whether the account is currently active
    """

    def __init__(self, username: str, email: str):
        """Initialize a new user account.

        Args:
            username: Unique username for the account
            email: User's email address
        """
        self.username = username
        self.email = email
        self.is_active = True
```

### Short Docstrings
For simple functions, a one-line docstring is sufficient:

```python
def get_username(user_id: int) -> str:
    """Return the username for the given user ID."""
    return database.query(user_id).username
```

## Comments

### Inline Comments
- **Use sparingly**: Code should be self-documenting
- **Place on separate line** above the code when possible
- **Use for complex logic** that isn't obvious
- **Update comments** when code changes

```python
# Good - explains non-obvious logic
# Calculate discount: 10% for orders over $100, 5% otherwise
discount = 0.10 if total > 100 else 0.05

# Avoid - stating the obvious
# Set x to 5
x = 5
```

### Block Comments
- **Use for complex algorithms** or business logic
- **Keep updated** with code changes
- **Indent to match** the code they describe

```python
# Check if user has permission to access this resource.
# Permission is granted if:
# 1. User is an admin
# 2. User owns the resource
# 3. Resource is marked as public
if user.is_admin or resource.owner == user or resource.is_public:
    grant_access()
```

### TODO Comments
- **Use TODO** for future improvements:
  ```python
  # TODO: Add caching for better performance
  # TODO: Refactor to use async/await
  ```

- **Include context** when helpful:
  ```python
  # TODO(username): Add validation for email format
  # TODO: Bug #123 - Handle edge case for empty lists
  ```

## Error Handling

### Exception Patterns

```python
# Custom exceptions
class UserNotFoundError(Exception):
    """Raised when a user cannot be found."""
    pass

class DatabaseError(Exception):
    """Base class for database-related errors."""
    pass

# Specific exception handling
try:
    user = get_user(user_id)
except UserNotFoundError:
    return None
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    raise

# Multiple exceptions
try:
    result = risky_operation()
except (ValueError, TypeError) as e:
    handle_error(e)

# Never use bare except (hides KeyboardInterrupt, SystemExit)
except Exception as e:  # Use this instead
    logger.error(f"Unexpected error: {e}")
    raise
```

### Context Managers and Exception Chaining

```python
from contextlib import contextmanager

# Context managers ensure cleanup
with open("file.txt") as f:
    content = f.read()

# Custom context manager
@contextmanager
def timer(name: str):
    start = time.time()
    try:
        yield
    finally:
        print(f"{name} took {time.time() - start:.2f}s")

# Exception chaining preserves context
try:
    user_data = fetch_user_data()
except ConnectionError as e:
    raise UserServiceError("Failed to fetch user") from e
```

### Validation and Error Messages

```python
# Fail fast with early validation
def create_user(username: str, email: str, age: int) -> User:
    if not username:
        raise ValueError("Username cannot be empty")
    if not email or "@" not in email:
        raise ValueError("Invalid email address")
    if age < 0 or age > 150:
        raise ValueError("Age must be between 0 and 150")
    return User(username, email, age)

# Specific, actionable error messages
raise ValueError(f"Invalid user ID: {user_id}. Must be a positive integer.")
raise FileNotFoundError(f"Configuration file not found: {config_path}")

# Logging with traceback
logger.exception("Unexpected error in process_data")  # Includes full traceback
```

### Best Practices

- **Catch specific exceptions** - avoid broad `except Exception`
- **Use context managers** for resource cleanup
- **Chain exceptions** with `raise ... from` to preserve context
- **Fail fast** - validate inputs early
- **Write descriptive error messages** with relevant context

## Async/Await Style

### When to Use Async

- **I/O-bound operations**: Database queries, API calls, file operations
- **Concurrent tasks**: Running multiple operations simultaneously
- **High throughput**: Handling many connections (web servers, bots)
- **Avoid for CPU-bound**: Use threading or multiprocessing instead

### Basic Async Functions

```python
import asyncio

# Define async function
async def fetch_user(user_id: int) -> User:
    """Fetch user from database asynchronously."""
    async with database.connection() as conn:
        result = await conn.fetch_one(
            "SELECT * FROM users WHERE id = ?", user_id
        )
        return User(**result)

# Call async function
async def main():
    user = await fetch_user(123)
    print(user)

# Run async code
asyncio.run(main())
```

### Async Context Managers and Concurrency

```python
from contextlib import asynccontextmanager

# Async context manager
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.json()

# Custom async context manager
@asynccontextmanager
async def database_transaction():
    conn = await database.connect()
    try:
        yield conn
        await conn.commit()
    except Exception:
        await conn.rollback()
        raise
    finally:
        await conn.close()

# Concurrent execution with gather
async def fetch_multiple_users(user_ids: list[int]) -> list[User]:
    tasks = [fetch_user(user_id) for user_id in user_ids]
    return await asyncio.gather(*tasks)

# Handle errors in concurrent tasks
results = await asyncio.gather(*tasks, return_exceptions=True)

# Timeouts
result = await asyncio.wait_for(long_running_task(), timeout=5.0)
```

### Async Iteration and Synchronization

```python
# Async generator
async def fetch_users_paginated() -> AsyncIterator[User]:
    page = 0
    while True:
        users = await fetch_page(page)
        if not users:
            break
        for user in users:
            yield user
        page += 1

# Consume async generator
async for user in fetch_users_paginated():
    process_user(user)

# Locks for critical sections
lock = asyncio.Lock()
async with lock:
    await modify_shared_resource()

# Semaphores for rate limiting
semaphore = asyncio.Semaphore(5)
async with semaphore:
    return await fetch(url)
```

### Mixing Sync and Async

```python
import concurrent.futures

# Run blocking code in thread pool
executor = concurrent.futures.ThreadPoolExecutor()
result = await asyncio.get_event_loop().run_in_executor(
    executor, blocking_function, arg1, arg2
)

# Run async from sync context (use sparingly)
asyncio.run(async_function())
```

### Best Practices

- **Use `async with` for async resources**: Connections, sessions, locks
- **Prefer `asyncio.gather()` for concurrency**: Better than sequential awaits
- **Set timeouts**: Prevent hanging on slow operations
- **Use async libraries**: aiohttp, asyncpg, aiofiles instead of sync versions
- **Avoid blocking calls**: Don't use `time.sleep()`, use `asyncio.sleep()`
- **Handle cancellation**: Use `try/except asyncio.CancelledError` when needed
- **Document async functions**: Make it clear when functions are async

## Code Organization

### File Organization
1. **Module docstring**
2. **Imports** (standard → third-party → local)
3. **Module-level constants**
4. **Module-level functions**
5. **Classes**

### Class Organization
1. **Class docstring**
2. **Class attributes**
3. **`__init__` method**
4. **Special methods** (`__str__`, `__repr__`, etc.)
5. **Public methods**
6. **Protected methods** (prefixed with `_`)
7. **Private methods** (prefixed with `__`)

Example:
```python
class UserService:
    """Service for user management operations."""

    # Class attribute
    MAX_LOGIN_ATTEMPTS = 3

    def __init__(self, database):
        """Initialize the user service."""
        self.database = database
        self._cache = {}

    def __repr__(self):
        """Return string representation."""
        return f"UserService(database={self.database})"

    def create_user(self, username, email):
        """Create a new user account."""
        pass

    def _validate_email(self, email):
        """Validate email format (internal use)."""
        pass

    def __hash_password(self, password):
        """Hash password using bcrypt (private)."""
        pass
```

## Formatting and Type Checking Tools

This project uses two primary tools for code quality: **ruff** for formatting and linting, and **mypy** for static type checking.

### Ruff - Formatting and Linting

Ruff is an extremely fast Python linter and formatter written in Rust. It combines the functionality of multiple tools (Flake8, isort, Black) into one.

#### Formatting with Ruff

```bash
# Format all Python files
ruff format .

# Check formatting without modifying
ruff format --check .

# Format specific files
ruff format path/to/file.py
```

#### Linting with Ruff

```bash
# Run linter
ruff check .

# Auto-fix issues
ruff check --fix .

# Show violations with explanations
ruff check --output-format=verbose .
```

#### Ruff Configuration

Add to `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py311"
line-length = 88
fix = true
exclude = [".git", ".mypy_cache", ".ruff_cache", ".venv", "__pycache__"]

# Enable rule sets
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort
    "N",      # pep8-naming
    "UP",     # pyupgrade
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "SIM",    # flake8-simplify
    "ARG",    # flake8-unused-arguments
    "PTH",    # flake8-use-pathlib
    "PL",     # pylint
    "PERF",   # perflint
]

ignore = ["E501"]  # line-too-long (handled by formatter)

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.ruff.lint.isort]
known-first-party = ["myapp"]

[tool.ruff.lint.pydocstyle]
convention = "google"
```

### Mypy - Static Type Checking

Mypy is a static type checker for Python that verifies type hints and catches type-related errors before runtime.

#### Running Mypy

```bash
# Check all Python files
mypy .

# Check specific file or directory
mypy path/to/file.py
mypy src/

# Check with verbose output
mypy --show-error-codes --pretty .

# Generate HTML report
mypy --html-report ./mypy-report .
```

#### Mypy Configuration

Add to `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.11"
strict = true
show_error_codes = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

# Per-module configuration
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "third_party_lib.*"
ignore_missing_imports = true
```

Common commands:
```bash
mypy .                              # Check all files
mypy --ignore-missing-imports .     # Ignore missing stubs
mypy --show-error-codes .           # Show error codes
```

Handling libraries without type stubs:
```python
import untyped_library  # type: ignore
```

### Best Practices

- **Run `ruff format` for consistent code style**
- **Run `ruff check --fix` to auto-fix linting issues**
- **Run `mypy` to catch type errors**
- **Enable strict mypy mode for maximum type safety**

## Summary

- **Formatting**: Use `ruff format`, 88-100 char lines, 4-space indents
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes, `SCREAMING_SNAKE_CASE` for constants
- **Type Hints**: Annotate all function signatures, use modern syntax (`list[str]`, `str | None`), avoid `Any`
- **Imports**: Group in stdlib → third-party → local, sort alphabetically
- **Error Handling**: Use specific exceptions, context managers for resources, chain exceptions with `from`
- **Async/Await**: Use for I/O-bound operations, prefer `asyncio.gather()` for concurrency
- **Documentation**: Triple-quoted docstrings, Google or NumPy style
- **Tools**: `ruff format` + `ruff check` for linting, `mypy --strict` for type checking
