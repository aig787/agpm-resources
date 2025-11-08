---
agpm:
  version: "1.0.0"
---

# Rust Style Guide

This document defines the code style standards for Rust projects. It covers formatting, naming conventions, imports, documentation style, and code organization.

## Code Formatting

### Line Length

- **Maximum line length**: 100 characters (configurable per project)
- **Break long lines** at logical points for readability
- Use Rust's formatting rules for line continuation

### Indentation

- **Use 4 spaces** per indentation level (enforced by `rustfmt`)
- **Never mix tabs and spaces**
- Continuation lines align with opening delimiter or use hanging indent

### Whitespace

- **One blank line** between top-level items (functions, structs, enums)
- **No blank lines** between consecutive imports
- **One blank line** at end of file
- **No trailing whitespace** on any line
- **Spaces around operators**: `x = y + z`, not `x=y+z`
- **No spaces** inside brackets: `[1, 2, 3]`, not `[ 1, 2, 3 ]`
- **Spaces after commas**: `func(a, b, c)`, not `func(a,b,c)`

### Braces and Formatting

- **Opening brace on same line** for structs, functions, and control flow:
  ```rust
  fn example() {
      if condition {
          // code
      }
  }
  ```

- **Match arms**: One per line with proper alignment:
  ```rust
  match value {
      Variant::One => handle_one(),
      Variant::Two => handle_two(),
      Variant::Three => {
          // Multi-line handling
          handle_complex()
      }
  }
  ```

### Trailing Commas

**Use trailing commas in multi-line structures**:

```rust
let items = vec![
    "first",
    "second",
    "third",  // trailing comma
];

let config = Config {
    host: "localhost",
    port: 8080,
    timeout: Duration::from_secs(30),  // trailing comma
};
```

### String Literals

- **Use double quotes** for string literals: `"hello"`
- **Use raw strings** for regex or paths with escapes: `r"C:\path"`
- **Use byte strings** when working with bytes: `b"bytes"`
- **Multi-line strings**: Use consistent indentation

```rust
let text = "This is a \
            multi-line string";

let text = r#"
    Raw string with "quotes"
    and multiple lines
"#;
```

## Naming Conventions

### Variables and Functions

- **Use `snake_case`** for variables and functions
- **Use descriptive names** that convey intent
- **Avoid single-letter names** except in:
  - Iterators: `for i in 0..10`
  - Generic type parameters: `T`, `E`, `K`, `V`
  - Common mathematical variables: `x, y, z`
  - Closures: `|x| x * 2`

**Examples**:

```rust
// Good
let user_count = 10;
fn calculate_total(items: &[Item]) -> u64 {
    // implementation
}

// Avoid
let uc = 10;
fn calcTot(items: &[Item]) -> u64 {
    // implementation
}
```

### Types (Structs, Enums, Traits)

- **Use `PascalCase`** for type names
- **Use clear, descriptive names**
- **Enum variants**: Use `PascalCase`

**Examples**:

```rust
// Good
struct UserAccount {
    username: String,
    email: String,
}

enum HttpStatus {
    Ok,
    NotFound,
    InternalError,
}

trait Drawable {
    fn draw(&self);
}

// Avoid
struct user_account {
    username: String,
}

enum Http_Status {
    ok,
    not_found,
}
```

### Constants and Statics

- **Use `SCREAMING_SNAKE_CASE`** for constants and statics
- Define at module level or in appropriate scope

**Examples**:

```rust
const MAX_CONNECTIONS: usize = 100;
const DEFAULT_TIMEOUT: Duration = Duration::from_secs(30);
static API_BASE_URL: &str = "https://api.example.com";
```

### Module Names

- **Use `snake_case`** for module names
- **Use short, descriptive names** without underscores if possible
- **Avoid plurals**: `user` not `users` (unless it makes more sense)

**Examples**:

```rust
// Good
mod user;
mod config;
mod error;
mod user_service;

// Avoid
mod User;
mod user_services;  // plural
```

### Type Parameters

- **Single uppercase letter** for simple generics: `T`, `E`, `K`, `V`
- **Descriptive names** for complex generics: `TcpStream`, `Error`

**Examples**:

```rust
// Simple generics
struct Vec<T> {
    items: Vec<T>,
}

struct HashMap<K, V> {
    // implementation
}

// Complex generics
trait From<T> {
    fn from(value: T) -> Self;
}

struct Builder<BuilderState> {
    state: BuilderState,
}
```

### Lifetime Parameters

- **Use `'a`, `'b`, etc.** for generic lifetimes
- **Use descriptive names** when meaning is important: `'static`, `'src`, `'dest`

**Examples**:

```rust
// Generic lifetimes
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Descriptive lifetimes
struct Parser<'input> {
    source: &'input str,
    position: usize,
}
```

### Boolean Names

- **Use affirmative, descriptive names**: `is_valid`, `has_children`, `can_read`
- **Avoid negative names**: Not `is_not_valid`

**Examples**:

```rust
// Good
let is_active = true;
let has_permission = false;
let can_write = true;

fn is_empty(&self) -> bool {
    self.len() == 0
}

// Avoid
let active = true;  // ambiguous
let not_permitted = true;  // negative
```

### Private and Public

- **No prefix for public items**: `pub fn public_function()`
- **No special prefix for private items**: They're private by default
- Use modules to control visibility

**Examples**:

```rust
pub struct User {
    pub id: u64,           // Public field
    pub username: String,  // Public field
    email: String,         // Private field
}

impl User {
    pub fn new(id: u64, username: String) -> Self {
        // Public constructor
        Self { id, username, email: String::new() }
    }

    fn validate(&self) -> bool {
        // Private method
        !self.username.is_empty()
    }
}
```

## Import Organization

### Import Grouping

Organize imports in groups with one blank line between each:

1. **`std` library imports**
2. **External crate imports**
3. **Local crate imports** (`crate::`, `super::`, `self::`)

Within each group, sort imports alphabetically.

### Import Style

**Prefer imports over full paths**:

```rust
// Good
use crate::models::User;
use crate::services::UserService;

fn process(user: User) {
    // Use imported types
}

// Avoid
fn process(user: crate::models::User) {
    // Using full paths everywhere
}
```

**Group imports from same module**:

```rust
// Good
use std::collections::{HashMap, HashSet};
use std::io::{self, Read, Write};

// Acceptable
use std::collections::HashMap;
use std::collections::HashSet;
```

**Use absolute imports** (prefer `crate::` over relative):

```rust
// Good - absolute import
use crate::models::User;

// Acceptable for nearby modules
use super::config::Config;
use self::utils::helper;
```

**Avoid glob imports** (except for preludes):

```rust
// Avoid
use std::collections::*;

// Good
use std::collections::{HashMap, HashSet};

// Exception: Preludes are OK
use std::io::prelude::*;
```

### Import Example

```rust
// Standard library
use std::collections::HashMap;
use std::fs;
use std::io::{self, Read};

// External crates
use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use tokio::sync::Mutex;

// Local imports
use crate::config::Config;
use crate::models::User;
use crate::services::UserService;
```

### Re-exports

**Use re-exports to simplify public API**:

```rust
// In lib.rs
pub use crate::config::Config;
pub use crate::error::Error;
pub use crate::models::User;

// Users can now do:
// use mylib::{Config, Error, User};
```

## Documentation Style

### Doc Comment Format

- **Use '///' for item documentation**: Functions, structs, enums, traits
- **Use '//!' for module-level documentation**: At the top of files
- **First line**: Brief summary (one line)
- **Blank line** after summary if there's more content
- **Sections**: Use standard sections like `# Examples`, `# Errors`, `# Panics`

### Module Documentation

**Place at the top of every Rust file**:

```rust
//! User authentication and authorization module.
//!
//! This module provides functionality for user login, logout,
//! token generation, and permission checking.

use std::collections::HashMap;
```

### Function Documentation

**Standard format with sections**:

```rust
/// Calculates the total cost including tax.
///
/// # Arguments
///
/// * `items` - Slice of item prices
/// * `tax_rate` - Tax rate as a decimal (e.g., 0.08 for 8%)
///
/// # Returns
///
/// Total cost with tax applied
///
/// # Errors
///
/// Returns `Err` if `tax_rate` is negative
///
/// # Examples
///
/// ```
/// # use mylib::calculate_total;
/// let items = vec![10.0, 20.0, 30.0];
/// let total = calculate_total(&items, 0.08).unwrap();
/// assert_eq!(total, 64.8);
/// ```
pub fn calculate_total(items: &[f64], tax_rate: f64) -> Result<f64, String> {
    if tax_rate < 0.0 {
        return Err("Tax rate cannot be negative".to_string());
    }

    let subtotal: f64 = items.iter().sum();
    Ok(subtotal * (1.0 + tax_rate))
}
```

### Struct Documentation

```rust
/// Represents a user account with authentication capabilities.
///
/// This struct handles user registration, login, and profile management.
/// It integrates with the authentication service for token management.
///
/// # Examples
///
/// ```
/// # use mylib::UserAccount;
/// let user = UserAccount::new("alice", "alice@example.com");
/// assert_eq!(user.username(), "alice");
/// ```
pub struct UserAccount {
    /// The unique username for the account
    username: String,
    /// The user's email address
    email: String,
    /// Whether the account is currently active
    is_active: bool,
}

impl UserAccount {
    /// Creates a new user account.
    ///
    /// # Arguments
    ///
    /// * `username` - Unique username for the account
    /// * `email` - User's email address
    ///
    /// # Examples
    ///
    /// ```
    /// # use mylib::UserAccount;
    /// let user = UserAccount::new("alice", "alice@example.com");
    /// ```
    pub fn new(username: impl Into<String>, email: impl Into<String>) -> Self {
        Self {
            username: username.into(),
            email: email.into(),
            is_active: true,
        }
    }
}
```

### Enum Documentation

```rust
/// HTTP status codes.
///
/// Represents common HTTP response status codes used throughout the API.
pub enum HttpStatus {
    /// Request succeeded (200)
    Ok,
    /// Resource not found (404)
    NotFound,
    /// Server error (500)
    InternalError,
}
```

### Documentation Sections

**Standard sections** (in this order):

- Brief summary (first paragraph)
- Detailed description
- `# Arguments` - Function parameters
- `# Returns` - Return value description
- `# Errors` - When and why errors occur
- `# Panics` - When the function panics
- `# Safety` - For unsafe functions, invariants that must be upheld
- `# Examples` - Code examples showing usage
- `# See also` - Related functions or types

### Short Documentation

**For simple items, a one-line comment is sufficient**:

```rust
/// Returns the username for the account.
pub fn username(&self) -> &str {
    &self.username
}

/// The default timeout duration.
pub const DEFAULT_TIMEOUT: Duration = Duration::from_secs(30);
```

### Intra-doc Links

**Link to other items in documentation**:

```rust
/// Processes a user account.
///
/// This function validates the [`UserAccount`] and stores it using
/// the [`UserService`]. See also [`validate_user`].
///
/// [`UserAccount`]: crate::models::UserAccount
/// [`UserService`]: crate::services::UserService
/// [`validate_user`]: crate::validation::validate_user
pub fn process_user(user: UserAccount) -> Result<()> {
    // implementation
}
```

## Comments

### Inline Comments

- **Use sparingly**: Code should be self-documenting
- **Place on separate line** above the code when possible
- **Use for complex logic** that isn't obvious
- **Update comments** when code changes

```rust
// Good - explains non-obvious logic
// Apply 10% discount for orders over $100, otherwise 5%
let discount = if total > 100.0 { 0.10 } else { 0.05 };

// Avoid - stating the obvious
// Set x to 5
let x = 5;
```

### Block Comments

**Use for complex algorithms or business logic**:

```rust
// Check if user has permission to access this resource.
// Permission is granted if:
// 1. User is an admin
// 2. User owns the resource
// 3. Resource is marked as public
if user.is_admin || resource.owner == user.id || resource.is_public {
    grant_access();
}
```

### TODO Comments

**Use TODO for future improvements**:

```rust
// TODO: Add caching for better performance
// TODO: Refactor to use async/await
// TODO(username): Add validation for email format
// TODO: Issue #123 - Handle edge case for empty lists
```

## Error Handling

### Result Type Usage

**Always use `Result` for operations that can fail**:

```rust
fn parse_config(path: &Path) -> Result<Config, ConfigError> {
    let contents = fs::read_to_string(path)
        .map_err(|e| ConfigError::ReadError(e))?;

    toml::from_str(&contents)
        .map_err(|e| ConfigError::ParseError(e))
}
```

### Custom Error Types

**Define clear error hierarchies**:

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Configuration error: {0}")]
    Config(String),

    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("User not found: {user_id}")]
    UserNotFound { user_id: u64 },

    #[error("IO error")]
    Io(#[from] std::io::Error),
}
```

### Error Propagation

**Use `?` operator for clean error propagation**:

```rust
fn process_request() -> Result<Response, AppError> {
    let config = load_config()?;
    let db = connect_database(&config)?;
    let user = fetch_user(&db)?;

    Ok(Response::new(user))
}
```

### Context for Errors

**Provide helpful context with errors**:

```rust
use anyhow::{Context, Result};

fn load_user(id: u64) -> Result<User> {
    let user = database::find_user(id)
        .with_context(|| format!("Failed to load user {}", id))?;

    Ok(user)
}
```

## Pattern Matching

### Match Expressions

**Use exhaustive matching**:

```rust
match status {
    Status::Active => handle_active(),
    Status::Pending => handle_pending(),
    Status::Inactive => handle_inactive(),
    // Compiler ensures all variants are handled
}
```

**Use `if let` for single patterns**:

```rust
// Good for single pattern
if let Some(value) = optional {
    process(value);
}

// Use match for multiple patterns
match optional {
    Some(value) => process(value),
    None => handle_none(),
}
```

**Use match guards for conditions**:

```rust
match value {
    x if x > 100 => println!("Large"),
    x if x > 10 => println!("Medium"),
    _ => println!("Small"),
}
```

**Use `@` bindings to capture and match**:

```rust
match value {
    Some(x @ 1..=10) => println!("Small number: {}", x),
    Some(x @ 11..=100) => println!("Medium number: {}", x),
    Some(x) => println!("Large number: {}", x),
    None => println!("No value"),
}
```

## Code Organization

### File Organization

1. **Module documentation** ('//!' comments)
2. **Imports** (std → external → local)
3. **Module declarations** (`mod` statements)
4. **Type definitions** (structs, enums, type aliases)
5. **Constants and statics**
6. **Trait definitions**
7. **Trait implementations**
8. **Functions**
9. **Tests** (`#[cfg(test)]` module)

### Module Structure Example

```rust
//! User management module.

use std::collections::HashMap;

use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::error::AppError;

mod validation;

const MAX_USERNAME_LENGTH: usize = 50;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct User {
    pub id: Uuid,
    pub username: String,
}

impl User {
    pub fn new(username: String) -> Result<Self, AppError> {
        validation::validate_username(&username)?;
        Ok(Self {
            id: Uuid::new_v4(),
            username,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_user_creation() {
        let user = User::new("alice".to_string()).unwrap();
        assert_eq!(user.username, "alice");
    }
}
```

### Impl Block Organization

**Organize impl blocks in this order**:

1. **Constructors** (`new`, `from_*`, etc.)
2. **Public methods** (sorted logically, not alphabetically)
3. **Private methods**
4. **Trait implementations** (in separate `impl` blocks)

```rust
impl User {
    // 1. Constructors
    pub fn new(username: String) -> Self {
        Self { username, ..Default::default() }
    }

    pub fn from_id(id: u64) -> Option<Self> {
        // implementation
    }

    // 2. Public methods
    pub fn username(&self) -> &str {
        &self.username
    }

    pub fn update_email(&mut self, email: String) -> Result<()> {
        self.validate_email(&email)?;
        self.email = email;
        Ok(())
    }

    // 3. Private methods
    fn validate_email(&self, email: &str) -> Result<()> {
        // implementation
    }
}

// 4. Trait implementations (separate impl blocks)
impl Default for User {
    fn default() -> Self {
        Self {
            username: String::new(),
            email: String::new(),
        }
    }
}
```

## Formatting Tools

### Rustfmt Configuration

**Add to `rustfmt.toml` or `.rustfmt.toml`**:

```toml
# Rust edition
edition = "2021"

# Line width
max_width = 100
hard_tabs = false
tab_spaces = 4

# Imports
imports_granularity = "Crate"
group_imports = "StdExternalCrate"
reorder_imports = true

# Formatting
newline_style = "Unix"
use_small_heuristics = "Default"
use_field_init_shorthand = true
use_try_shorthand = true
```

### Running Rustfmt

```bash
# Format all code
cargo fmt

# Check formatting without modifying
cargo fmt -- --check

# Format specific files
rustfmt src/main.rs
```

## Summary

- **Formatting**: Use `cargo fmt`, 100-char lines, 4-space indents
- **Naming**: `snake_case` for functions/variables, `PascalCase` for types, `SCREAMING_SNAKE_CASE` for constants
- **Imports**: Group in std → external → local, sort alphabetically, prefer absolute imports
- **Documentation**: Use '///' for items, '//!' for modules, include examples and error descriptions
- **Error Handling**: Use `Result<T, E>`, provide context, define custom error types
- **Pattern Matching**: Exhaustive matching, use `if let` for single patterns
- **Code Organization**: Logical grouping, public before private, tests in separate module
- **Tools**: `cargo fmt` for formatting, `cargo clippy` for linting

This style guide ensures consistent, readable, and maintainable Rust code across all projects.
