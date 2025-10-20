# Rust Best Practices

This document defines technical best practices for Rust development, covering tools, patterns, testing, security, and performance optimization.

## Core Principles

1. **Idiomatic Rust**: Write code that follows Rust conventions and patterns
2. **Zero Warnings Policy**: All code must pass `cargo clippy -- -D warnings`
3. **Consistent Formatting**: All code must be formatted with `cargo fmt`
4. **Memory Safety**: Leverage Rust's ownership system effectively
5. **Error Handling**: Use `Result<T, E>` and proper error propagation
6. **Performance**: Write efficient code without premature optimization
7. **Documentation**: Add doc comments for public APIs

## Mandatory Completion Checklist

Before considering any Rust code complete, you MUST:

1. ✅ Run `cargo fmt` to ensure proper formatting
2. ✅ Run `cargo clippy -- -D warnings` to catch all lints
3. ✅ Run `cargo nextest run` (or `cargo test`) to verify tests pass
4. ✅ Run `cargo test --doc` to verify doctests pass
5. ✅ Run `cargo doc --no-deps` to verify documentation builds

## Development Tools

### Cargo Commands

**Essential commands**:

```bash
# Build and run
cargo build                         # Debug build
cargo build --release              # Optimized build
cargo run                          # Build and run
cargo run --release                # Build and run optimized

# Testing
cargo test                         # Run all tests
cargo nextest run                  # Run tests in parallel (recommended)
cargo test --doc                   # Run doctests
cargo bench                        # Run benchmarks

# Code quality
cargo fmt                          # Format code
cargo fmt -- --check              # Check formatting
cargo clippy                       # Run lints
cargo clippy -- -D warnings       # Fail on warnings
cargo clippy --fix                # Auto-fix issues

# Documentation
cargo doc                          # Build documentation
cargo doc --no-deps --open        # Build and open docs
```

### Clippy Configuration

**Enforce these lints** (add to `lib.rs` or `main.rs`):

```rust
#![warn(
    clippy::all,
    clippy::pedantic,
    clippy::nursery,
    clippy::cargo,
    missing_docs,
    missing_debug_implementations,
    missing_copy_implementations,
    trivial_casts,
    trivial_numeric_casts,
    unsafe_code,
    unstable_features,
    unused_import_braces,
    unused_qualifications,
)]
```

**Allow these when appropriate**:

```rust
#![allow(
    clippy::module_name_repetitions,  // Common in Rust APIs
    clippy::must_use_candidate,       // Can be too noisy
    clippy::missing_errors_doc,       // Use selectively
)]
```

### Cross-Platform Development

**Path separator handling**: CRITICAL for Windows/macOS/Linux compatibility

- **Storage/serialization**: Always use forward slashes `/` in:
  - Lockfiles and manifest files (TOML, JSON)
  - `.gitignore` entries (Git requirement)
  - Any serialized path representation

- **Runtime operations**: Use `Path`/`PathBuf` for filesystem operations (automatic platform handling)

- **`Path::display()` gotcha**: Produces platform-specific separators (backslashes on Windows)
  - Always use helper when storing: `normalize_path_for_storage()`
  - Example: `normalize_path_for_storage(format!("{}/{}", path.display(), file))`

- **Use `join()` not string concatenation**: `path.join("file")` not `format!("{}/file", path)`

**Windows-specific considerations**:

- Absolute paths: `C:\path` or `\\server\share` (UNC paths)
- Reserved filenames: CON, PRN, AUX, NUL, COM1-9, LPT1-9
- Case-insensitive filesystem (but preserves case)
- `file://` URLs use forward slashes even on Windows
- Test on real Windows, not WSL (different behavior)

**Additional guidelines**:

- **Line endings**: Use `\n` in code, let Git handle CRLF conversion
- **Environment variables**: Use `std::env::var_os` for non-UTF8 safety
- **Path validation**: Consider `dunce` crate to normalize Windows paths
- **Testing**: Run CI on all target platforms (Windows, macOS, Linux)

## Error Handling

### Result and Option

**Use `Result<T, E>` for operations that can fail**:

```rust
use anyhow::{Context, Result};

fn read_config(path: &Path) -> Result<Config> {
    let contents = std::fs::read_to_string(path)
        .context("Failed to read config file")?;

    let config: Config = toml::from_str(&contents)
        .context("Failed to parse config")?;

    Ok(config)
}
```

**Use `Option<T>` for values that may not exist**:

```rust
fn find_user(id: u64) -> Option<User> {
    database.get(id)
}

// Using combinators
let name = find_user(42)
    .map(|u| u.name)
    .unwrap_or_else(|| "Unknown".to_string());
```

### Error Library Selection

**For applications**: Use `anyhow` for flexible error handling

```rust
use anyhow::{Context, Result};

fn process_data() -> Result<()> {
    let data = fetch_data()
        .context("Failed to fetch data")?;

    validate_data(&data)
        .with_context(|| format!("Invalid data format: {:?}", data))?;

    Ok(())
}
```

**For libraries**: Use `thiserror` for structured error types

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ParseError {
    #[error("Invalid header: {0}")]
    InvalidHeader(String),

    #[error("Missing field: {field}")]
    MissingField { field: String },

    #[error("I/O error")]
    Io(#[from] std::io::Error),
}
```

### Error Handling Best Practices

- **Provide context**: Use `.context()` and `.with_context()` for actionable error messages
- **Return `Result<T, E>`**: Instead of panicking
- **Use `?` operator**: For error propagation
- **Use `.expect()` only when panic is acceptable**: With descriptive messages
- **Handle all error cases explicitly**: Avoid ignoring errors
- **Chain errors properly**: Use `#[from]` attribute or manual conversion

## Ownership & Borrowing

### Borrowing Principles

**Prefer borrowing over ownership when possible**:

```rust
// Good - borrows data
fn process(data: &str) {
    println!("{}", data);
}

// Avoid - takes ownership unnecessarily
fn process_owned(data: String) {
    println!("{}", data);
}
```

**Use `&mut` sparingly**:

```rust
// Good - immutable borrow
fn read_data(data: &Data) -> String {
    data.to_string()
}

// Only when mutation is needed
fn update_data(data: &mut Data) {
    data.counter += 1;
}
```

### Smart Pointers

**`Box<T>`**: Heap allocation, trait objects, recursive types

```rust
enum List {
    Cons(i32, Box<List>),
    Nil,
}
```

**`Rc<T>`**: Single-threaded reference counting (avoid in async code)

```rust
use std::rc::Rc;

let shared = Rc::new(5);
let shared_clone = Rc::clone(&shared);
```

**`Arc<T>`**: Thread-safe reference counting for shared ownership

```rust
use std::sync::Arc;

let shared = Arc::new(data);
let shared_clone = Arc::clone(&shared);
```

**`Cow<T>`**: Clone-on-write for conditional ownership

```rust
use std::borrow::Cow;

fn process(input: Cow<str>) -> Cow<str> {
    if input.contains("special") {
        Cow::Owned(input.replace("special", "normal"))
    } else {
        input  // No clone needed
    }
}
```

### Interior Mutability

**`Cell<T>`**: Copy types, single-threaded

```rust
use std::cell::Cell;

struct Counter {
    count: Cell<u32>,
}

impl Counter {
    fn increment(&self) {
        self.count.set(self.count.get() + 1);
    }
}
```

**`RefCell<T>`**: Runtime borrow checking, single-threaded

```rust
use std::cell::RefCell;

let data = RefCell::new(vec![1, 2, 3]);
data.borrow_mut().push(4);
```

**`Mutex<T>`**: Exclusive access, multi-threaded

```rust
use std::sync::Mutex;

let counter = Mutex::new(0);
let mut num = counter.lock().unwrap();
*num += 1;
```

**`RwLock<T>`**: Multiple readers or single writer, multi-threaded

```rust
use std::sync::RwLock;

let lock = RwLock::new(data);
let r1 = lock.read().unwrap();
let r2 = lock.read().unwrap();  // Multiple readers OK
```

**Use `Arc<Mutex<T>>` or `Arc<RwLock<T>>`** for shared mutable state across threads:

```rust
use std::sync::{Arc, Mutex};

let counter = Arc::new(Mutex::new(0));
let counter_clone = Arc::clone(&counter);

std::thread::spawn(move || {
    let mut num = counter_clone.lock().unwrap();
    *num += 1;
});
```

## Type Safety & Traits

### Newtype Pattern

**Use newtypes for domain-specific types**:

```rust
struct UserId(u64);
struct Email(String);

impl Email {
    fn new(s: String) -> Result<Self, EmailError> {
        if s.contains('@') {
            Ok(Email(s))
        } else {
            Err(EmailError::InvalidFormat)
        }
    }
}
```

### Trait Design

**Prefer composition over inheritance**:

```rust
trait Drawable {
    fn draw(&self);
}

trait Clickable {
    fn on_click(&self);
}

struct Button;

impl Drawable for Button {
    fn draw(&self) { /* ... */ }
}

impl Clickable for Button {
    fn on_click(&self) { /* ... */ }
}
```

**Associated types vs generics**:

```rust
// Use associated types when there's one natural implementation
trait Container {
    type Item;
    fn get(&self) -> &Self::Item;
}

// Use generics for flexibility
trait From<T> {
    fn from(value: T) -> Self;
}
```

**Implement standard traits thoughtfully**:

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
struct MyType {
    field: String,
}

impl Default for MyType {
    fn default() -> Self {
        Self {
            field: String::from("default"),
        }
    }
}
```

**Conversion traits**:

```rust
struct UserId(u64);

impl From<u64> for UserId {
    fn from(id: u64) -> Self {
        UserId(id)
    }
}

// Now you can use .into()
let user_id: UserId = 42.into();
```

### Builder Pattern

**Use for structs with many optional fields**:

```rust
pub struct Config {
    host: String,
    port: u16,
    timeout: Option<Duration>,
}

pub struct ConfigBuilder {
    host: Option<String>,
    port: Option<u16>,
    timeout: Option<Duration>,
}

impl ConfigBuilder {
    pub fn host(mut self, host: String) -> Self {
        self.host = Some(host);
        self
    }

    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }

    pub fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = Some(timeout);
        self
    }

    pub fn build(self) -> Result<Config, BuildError> {
        Ok(Config {
            host: self.host.ok_or(BuildError::MissingHost)?,
            port: self.port.unwrap_or(8080),
            timeout: self.timeout,
        })
    }
}

// Usage
let config = ConfigBuilder::default()
    .host("localhost".to_string())
    .port(3000)
    .build()?;
```

## Testing Strategy

### Unit Tests

**Write unit tests in the same file as the code**:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_addition() {
        assert_eq!(add(2, 2), 4);
    }

    #[test]
    fn test_error_case() {
        let result = parse_number("invalid");
        assert!(result.is_err());
    }
}
```

### Integration Tests

**Put integration tests in `tests/` directory**:

```
myproject/
├── src/
│   └── lib.rs
└── tests/
    ├── integration_test.rs
    └── common/
        └── mod.rs
```

### Testing Best Practices

**Use cargo nextest**: Run tests with `cargo nextest run` for parallel execution

**All tests must be parallel-safe**:

- Avoid `serial_test` crate when possible
- **Never use `std::env::set_var`** (causes data races between parallel tests)
- Each test should use its own isolated temp directory
- Use `tokio::fs` in async tests, not `std::fs`

**Doctest configuration**:

```rust
/// Calculate the sum of two numbers.
///
/// # Examples
///
/// ```
/// # use mylib::add;
/// assert_eq!(add(2, 2), 4);
/// ```
///
/// This example demonstrates usage but doesn't execute:
///
/// ```no_run
/// # use mylib::connect;
/// let conn = connect("localhost:8080");
/// ```
///
/// This example won't compile (for demonstration):
///
/// ```ignore
/// let x = some_unstable_api();
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

**Property-based testing**:

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_reversing_twice(s: String) {
        let reversed = reverse(&s);
        let double_reversed = reverse(&reversed);
        assert_eq!(s, double_reversed);
    }
}
```

**Mock external dependencies**:

```rust
#[cfg(test)]
mod tests {
    use mockall::predicate::*;
    use mockall::*;

    #[automock]
    trait DataSource {
        fn fetch(&self, id: u64) -> Result<Data>;
    }

    #[test]
    fn test_with_mock() {
        let mut mock = MockDataSource::new();
        mock.expect_fetch()
            .with(eq(1))
            .returning(|_| Ok(Data::default()));

        let result = process(&mock);
        assert!(result.is_ok());
    }
}
```

### Test Organization

- **Aim for >70% test coverage**: Use `cargo tarpaulin` or `cargo llvm-cov`
- **Test isolation**: Each test should be independent
- **Use descriptive test names**: `test_user_creation_with_valid_email`
- **Test edge cases**: Empty inputs, None values, boundary conditions
- **Use `#[cfg(test)]` for test modules**: Excluded from release builds

## Async Rust

### When to Use Async

- **I/O-bound operations**: Database queries, API calls, file operations
- **Concurrent tasks**: Running multiple operations simultaneously
- **High throughput**: Handling many connections (web servers, bots)
- **Avoid for CPU-bound**: Use threading or `rayon` instead

### Basic Async Patterns

**Use `tokio` for async runtime**:

```rust
use tokio;

#[tokio::main]
async fn main() {
    let result = fetch_data().await;
    println!("{:?}", result);
}

async fn fetch_data() -> Result<String> {
    // Async operation
    Ok("data".to_string())
}
```

**Concurrent execution**:

```rust
use tokio;

async fn fetch_all(urls: Vec<String>) -> Vec<Result<String>> {
    let futures: Vec<_> = urls.into_iter()
        .map(|url| fetch_url(url))
        .collect();

    futures::future::join_all(futures).await
}
```

**Timeouts**:

```rust
use tokio::time::{timeout, Duration};

async fn fetch_with_timeout(url: &str) -> Result<String> {
    timeout(Duration::from_secs(5), fetch_url(url))
        .await
        .context("Request timed out")?
}
```

### Async Best Practices

- **Use `tokio::fs` for file I/O**: Never mix blocking `std::fs` in async code
- **Avoid blocking in async contexts**: Use `tokio::task::spawn_blocking` for blocking operations
- **Use async context managers**: For async resources
- **Handle cancellation properly**: Use `tokio::select!` and cancellation tokens
- **Consider using `futures` combinators**: For complex async operations

```rust
use tokio::fs::File;
use tokio::io::AsyncReadExt;

async fn read_file(path: &Path) -> Result<String> {
    let mut file = File::open(path).await?;
    let mut contents = String::new();
    file.read_to_string(&mut contents).await?;
    Ok(contents)
}
```

## Concurrency

### Channel Communication

**Use channels for thread communication**:

```rust
use std::sync::mpsc;

let (tx, rx) = mpsc::channel();

std::thread::spawn(move || {
    tx.send("Hello").unwrap();
});

let received = rx.recv().unwrap();
println!("{}", received);
```

**For async**: Use `tokio::sync::mpsc`

```rust
use tokio::sync::mpsc;

let (tx, mut rx) = mpsc::channel(32);

tokio::spawn(async move {
    tx.send("Hello").await.unwrap();
});

while let Some(msg) = rx.recv().await {
    println!("{}", msg);
}
```

### Concurrency Best Practices

- **Use channels for communication between threads**: Message passing over shared state
- **Prefer `Arc` for shared ownership**: Thread-safe reference counting
- **Use `Mutex` or `RwLock` for shared mutable state**: Prevent data races
- **Consider using `crossbeam`**: For advanced concurrency patterns
- **Use `rayon`**: For data parallelism and parallel iterators

```rust
use rayon::prelude::*;

let sum: i32 = (0..1000)
    .into_par_iter()
    .map(|x| x * x)
    .sum();
```

## Logging & Tracing

### Structured Logging

**Use `tracing` crate for structured logs**:

```rust
use tracing::{info, warn, error, debug, trace};

#[tracing::instrument]
async fn process_request(user_id: u64) -> Result<()> {
    info!(user_id, "Processing request");

    let data = fetch_data(user_id).await?;
    debug!(size = data.len(), "Fetched data");

    Ok(())
}
```

**Tracing spans for context**:

```rust
use tracing::{info_span, Instrument};

async fn install_package(name: &str) {
    let span = info_span!("install", package = %name);

    async {
        info!("Downloading package");
        download().await;
        info!("Installing package");
        install().await;
    }
    .instrument(span)
    .await
}
```

### Logging Best Practices

- **Use structured logging**: Leverage `tracing` for structured logs with key-value pairs
- **Log levels**:
  - `trace!`: Very detailed debugging information
  - `debug!`: Debugging information for developers
  - `info!`: General informational messages
  - `warn!`: Warning messages for potentially problematic situations
  - `error!`: Error messages for failures
- **Avoid `println!`**: Use logging macros instead
- **Configure subscribers**: Set up `tracing_subscriber` in main/tests
- **Progress indication**: Use `indicatif` crate for progress bars

## Dependency Management

### Cargo.toml Best Practices

**Pin versions for applications, use ranges for libraries**:

```toml
# Application
[dependencies]
serde = "1.0.195"
tokio = { version = "1.35.1", features = ["full"] }

# Library
[dependencies]
serde = "1.0"
tokio = { version = "1.35", features = ["full"] }
```

**Use workspace dependencies for multi-crate projects**:

```toml
[workspace]
members = ["crate-a", "crate-b"]

[workspace.dependencies]
serde = "1.0"
tokio = { version = "1.35", features = ["full"] }
```

### Dependency Guidelines

- **Prefer well-maintained crates**: Check recent updates and stars
- **Check for security advisories**: Run `cargo audit` regularly
- **Keep dependencies minimal**: Only include what you need
- **Audit dependencies regularly**: `cargo audit` and `cargo deny`
- **Check license compatibility**: Ensure compliance with your project's license

```bash
# Security scanning
cargo audit

# License checking
cargo deny check licenses

# Unused dependencies
cargo machete

# Outdated dependencies
cargo outdated
```

## Performance Considerations

### General Guidelines

- **Profile before optimizing**: Use `cargo flamegraph`, `perf`, or `valgrind`
- **Use `&str` instead of `String` when possible**: Avoid unnecessary allocations
- **Prefer iterators over collecting**: Lazy evaluation
- **Use `Arc` and `Rc` judiciously**: Reference counting has overhead
- **Consider zero-copy patterns**: Use `Cow`, `&str`, borrowing
- **Leverage const generics and const functions**: Compile-time computation
- **Use `#[inline]` judiciously**: For small, frequently-called functions
- **Avoid unnecessary heap allocations**: Use stack allocation when possible
- **Consider using `SmallVec`**: For small collections to avoid heap allocation

### Iterator Patterns

```rust
// Good - lazy evaluation
let sum: i32 = vec.iter()
    .filter(|x| x > &0)
    .map(|x| x * 2)
    .sum();

// Avoid - unnecessary collection
let filtered: Vec<_> = vec.iter()
    .filter(|x| x > &0)
    .collect();
let doubled: Vec<_> = filtered.iter()
    .map(|x| x * 2)
    .collect();
```

### Pre-allocation

```rust
// Pre-allocate when size is known
let mut vec = Vec::with_capacity(1000);
for i in 0..1000 {
    vec.push(i);
}
```

## Macro Usage

### When to Use Macros

**Prefer functions over macros**: Macros should be a last resort

- Macros are harder to debug and understand
- Functions provide better type checking and error messages

**Use macros when necessary**:

- Reducing boilerplate (e.g., `vec!`, `format!`)
- Generating repetitive code at compile time
- Creating DSLs (domain-specific languages)
- Variadic functions (different number of arguments)

### Declarative Macros

```rust
macro_rules! create_function {
    ($func_name:ident) => {
        fn $func_name() {
            println!("Called {:?}", stringify!($func_name));
        }
    };
}

create_function!(foo);
create_function!(bar);
```

### Procedural Macros

```rust
use proc_macro::TokenStream;
use quote::quote;
use syn;

#[proc_macro_derive(Builder)]
pub fn derive_builder(input: TokenStream) -> TokenStream {
    let ast = syn::parse(input).unwrap();
    impl_builder(&ast)
}
```

### Macro Best Practices

- **Document macro usage**: Include examples
- **Test macros thoroughly**: Macro errors can be cryptic
- **Use hygiene**: Be aware of variable capture and naming conflicts

## Unsafe Code

### When to Use Unsafe

**Avoid unsafe unless absolutely necessary**:

- FFI (Foreign Function Interface)
- Performance-critical sections (after profiling!)
- Low-level system programming
- Implementing safe abstractions over unsafe operations

### Unsafe Best Practices

```rust
/// # Safety
///
/// The caller must ensure that:
/// - `ptr` is valid for reads of `len` bytes
/// - `ptr` is properly aligned
/// - The memory range does not overlap with any other mutable references
pub unsafe fn read_bytes(ptr: *const u8, len: usize) -> Vec<u8> {
    // Unsafe operation with documented invariants
    std::slice::from_raw_parts(ptr, len).to_vec()
}
```

**Guidelines**:

- **Document safety invariants clearly**: Use `# Safety` section
- **Use `unsafe` blocks minimally**: Keep them small and focused
- **Consider safe abstractions first**: Avoid unsafe if possible
- **Run Miri**: For undefined behavior detection
- **Use `#[deny(unsafe_code)]`**: Prevent accidental usage in most of codebase
- **Validate assumptions**: With comments and assertions
- **Encapsulate unsafe in safe APIs**: Hide unsafe internals
- **Review extra carefully**: During code review

```bash
# Run Miri for UB detection
cargo +nightly miri test
```

## Documentation

### Doc Comments

**Document all public APIs**:

```rust
/// Calculates the sum of two numbers.
///
/// # Arguments
///
/// * `a` - The first number
/// * `b` - The second number
///
/// # Returns
///
/// The sum of `a` and `b`
///
/// # Examples
///
/// ```
/// # use mylib::add;
/// let result = add(2, 3);
/// assert_eq!(result, 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

**Module-level documentation**:

```rust
//! This module provides utilities for working with user data.
//!
//! It includes functions for validation, serialization, and persistence.

use std::fs;
```

### Documentation Best Practices

- **Include examples in doc comments**: Show how to use the API
- **Use `#[doc(hidden)]`**: For internal implementation details
- **Keep documentation up-to-date**: Update with code changes
- **Document errors and panics**: Using `# Errors` and `# Panics` sections
- **Use intra-doc links**: `[`Type`]` syntax for linking

## CI/CD Integration

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/doublify/pre-commit-rust
    rev: v1.0
    hooks:
      - id: fmt
      - id: clippy
        args: ['--', '-D', 'warnings']
```

### CI Pipeline Steps

```bash
# 1. Format check
cargo fmt -- --check

# 2. Clippy with warnings as errors
cargo clippy --all-targets --all-features -- -D warnings

# 3. Run tests
cargo nextest run

# 4. Run doctests
cargo test --doc

# 5. Security audit
cargo audit

# 6. Build documentation
cargo doc --no-deps

# 7. Check for outdated dependencies
cargo outdated
```

## Summary

- **Use modern tools**: `cargo`, `clippy`, `rustfmt`, `nextest`
- **Zero warnings policy**: Pass all clippy lints
- **Test thoroughly**: >70% coverage, unit + integration + doctests
- **Document all public APIs**: With examples and clear explanations
- **Handle errors properly**: Use `Result<T, E>`, provide context
- **Optimize when needed**: Profile first, then optimize
- **Leverage the type system**: Use newtypes, traits, and generics
- **Follow ownership rules**: Borrow when possible, clone only when necessary
- **Automate quality checks**: CI/CD, pre-commit hooks
- **Keep dependencies updated**: Security and features

These practices ensure robust, maintainable, and performant Rust applications.
