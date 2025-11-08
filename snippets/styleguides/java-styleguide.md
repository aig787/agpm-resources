---
agpm:
  version: "1.1.0"
---
# Java Style Guide

This document defines the code style standards for Java projects. It covers formatting, naming conventions, type annotations, imports, and documentation style.

## Code Formatting

### Line Length
- **Maximum line length**: 100-120 characters (configurable per project)
- **Break long lines** at logical points for readability

### Indentation
- **Use 4 spaces** per indentation level
- **Never use tabs**
- Continuation lines should use hanging indent of 8 spaces

### Whitespace
- **One blank line** between class members (methods, fields, constructors)
- **Two blank lines** between top-level classes and interfaces
- **One blank line** at end of file
- **No trailing whitespace** on any line
- **Spaces around operators**: `x = y + z`, not `x=y+z`
- **No spaces** inside brackets: `[1, 2, 3]`, not `[ 1, 2, 3 ]`
- **Spaces after commas**: `method(a, b, c)`, not `method(a,b,c)`

### Braces
- **Use K&R style** for braces:
  ```java
  // Good
  if (condition) {
      doSomething();
  } else {
      doSomethingElse();
  }

  // Avoid
  if (condition)
  {
      doSomething();
  }
  else
  {
      doSomethingElse();
  }
  ```

- **Always use braces** even for single statements:
  ```java
  // Good
  if (condition) {
      doSomething();
  }

  // Avoid
  if (condition) doSomething();
  ```

### String Quotes
- **Use double quotes** for all string literals: `"hello"`
- **Use string concatenation** sparingly - prefer `StringBuilder` or formatted strings
- **Use text blocks** (Java 15+) for multi-line strings:
  ```java
  String json = """
      {
          "name": "John",
          "age": 30
      }
      """;
  ```

## Naming Conventions

### Variables and Methods
- **Use `camelCase`** for variables and methods
- **Use descriptive names** that convey intent
- **Avoid single-letter names** except in:
  - Loop counters: `for (int i = 0; i < 10; i++)`
  - Common mathematical variables: `x, y, z`
  - Lambda parameters: `.map(item -> item.getId())`

**Examples**:
```java
// Good
int userCount = 10;
public void calculateTotal(List<Item> items) {
    // implementation
}

// Avoid
int uc = 10;
public void calcTot(List<Item> items) {
    // implementation
}
```

### Classes and Interfaces
- **Use `PascalCase`** for class and interface names
- **Use nouns** for class names
- **Use adjectives** for interface names when appropriate
- **Use clear, descriptive names**

**Examples**:
```java
// Good - Classes
public class UserAccount {
    // implementation
}

public class HTTPResponse {
    // implementation
}

// Good - Interfaces
public interface Serializable {
    // implementation
}

public interface Runnable {
    // implementation
}

// Avoid
public class user_account {
    // implementation
}
```

### Constants
- **Use `SCREAMING_SNAKE_CASE`** for constants
- **Use `static final`** modifiers
- **Define at class level**

**Examples**:
```java
public class Config {
    public static final int MAX_CONNECTIONS = 100;
    public static final long DEFAULT_TIMEOUT = 30000L;
    public static final String API_BASE_URL = "https://api.example.com";
}
```

### Packages
- **Use lowercase** for package names
- **Use reverse domain name** convention: `com.example.project`
- **Use meaningful names** that reflect functionality

**Examples**:
```java
// Good
package com.example.user.service;
package org.apache.commons.lang3;

// Avoid
package com.example.User.Service;
package com.example.user_service;
```

### Enum Constants
- **Use `SCREAMING_SNAKE_CASE`** for enum constants
- **Use `PascalCase`** for enum class names

**Examples**:
```java
public enum Status {
    PENDING,
    APPROVED,
    REJECTED
}

public enum HttpStatus {
    OK(200),
    NOT_FOUND(404),
    INTERNAL_SERVER_ERROR(500);
    
    private final int code;
    
    HttpStatus(int code) {
        this.code = code;
    }
}
```

### Boolean Names
- **Prefix with `is`, `has`, or `should`** for clarity
- **Use affirmative names**

**Examples**:
```java
// Good
boolean isActive = true;
boolean hasPermission = false;
boolean shouldRetry = true;

// Avoid
boolean active = true;  // ambiguous
boolean noPermission = true;  // negative naming
```

### Generic Type Parameters
- **Use single uppercase letters** for generic type parameters
- **Use descriptive names** when multiple parameters are needed

**Examples**:
```java
// Good
public class Box<T> {
    private T value;
}

public interface Mapper<K, V> {
    V map(K key);
}

public class UserRepository<T extends User> {
    // implementation
}

// Avoid
public class Box<t> {
    private t value;
}
```

## Type Annotations

### Variable Declarations
- **Declare variables with their type** (avoid `var` unless type is obvious)
- **Use interfaces** for variable types when possible
- **Be explicit** about generic types

**Examples**:
```java
// Good
List<String> names = new ArrayList<>();
Map<String, Integer> scores = new HashMap<>();
User user = new User();

// Acceptable with var (Java 10+)
var names = new ArrayList<String>();  // Type is clear
var user = findUserById(123);         // Method name makes type clear

// Avoid
var data = someMethod();  // Type is not obvious
```

### Method Signatures
- **Always declare return types** explicitly
- **Use interfaces** for parameter types when appropriate
- **Use generics** for type safety

**Examples**:
```java
// Good
public List<User> findActiveUsers();
public Optional<User> findById(Long id);
public <T> T process(T input);
public void save(User user);

// Avoid
public findActiveUsers() {  // Missing return type
    // implementation
}
```

### Annotations
- **Use annotations** for metadata and configuration
- **Place annotations** before the element they modify
- **Use standard annotations** from `java.lang` and JSR-250

**Examples**:
```java
// Good
@Override
public String toString() {
    return "User{id=" + id + "}";
}

@Deprecated
public void oldMethod() {
    // implementation
}

@Component
public class UserService {
    // implementation
}

@GetMapping("/users/{id}")
public ResponseEntity<User> getUser(@PathVariable Long id) {
    // implementation
}
```

## Import Organization

### Import Grouping

Organize imports in groups with one blank line between each:

1. **Static imports**
2. **Java standard library imports** (`java.*`, `javax.*`)
3. **Third-party imports**
4. **Project imports**

Within each group, sort imports alphabetically.

### Import Style

- **One import per line** for clarity:
  ```java
  // Good
  import java.util.List;
  import java.util.Map;

  // Avoid
  import java.util.List, java.util.Map;
  ```

- **Use wildcard imports sparingly**:
  ```java
  // Acceptable for static constants
  import static java.util.Collections.*;

  // Avoid for regular imports
  import java.util.*;  // Too broad
  ```

- **Prefer specific imports**:
  ```java
  // Good
  import java.util.List;
  import java.util.ArrayList;

  // Avoid
  import java.util.*;
  ```

### Import Example

```java
// Static imports
import static java.util.Collections.emptyList;
import static org.junit.Assert.assertEquals;

// Java standard library
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

// Third-party imports
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.GetMapping;
import com.fasterxml.jackson.annotation.JsonIgnore;

// Project imports
import com.example.model.User;
import com.example.repository.UserRepository;
import com.example.service.UserService;
```

### Unused Imports

- **Remove unused imports** - avoid importing unused classes
- **Avoid importing** classes that are only used in comments or javadoc

## Documentation Style

### Javadoc Format

- **Use `/** */` for documentation blocks**
- **First line**: Brief summary (one line, fragment, no period)
- **Blank line** after summary if there's more content
- **Detailed description**: Multi-paragraph explanation if needed
- **Tags**: Document parameters, return values, and exceptions

### Class Documentation

Place at the top of every class:

```java
/**
 * User authentication and authorization service.
 *
 * This service provides functionality for user login, logout,
 * token generation, and permission checking. It integrates with
 * the UserRepository for data persistence.
 *
 * @author John Doe
 * @version 1.0
 * @since 1.0
 */
@Service
public class UserService {
    // implementation
}
```

### Method Documentation

```java
/**
 * Calculates the total cost including tax.
 *
 * @param items List of item prices
 * @param taxRate Tax rate as a decimal (e.g., 0.08 for 8%)
 * @return Total cost with tax applied
 * @throws IllegalArgumentException If taxRate is negative
 *
 * @see #calculateDiscount(List, double)
 *
 * @since 1.0
 */
public double calculateTotal(List<Double> items, double taxRate) {
    if (taxRate < 0) {
        throw new IllegalArgumentException("Tax rate cannot be negative");
    }
    
    double subtotal = items.stream().mapToDouble(Double::doubleValue).sum();
    return subtotal * (1 + taxRate);
}
```

### Field Documentation

```java
public class User {
    /**
     * The unique identifier for this user.
     */
    private Long id;

    /**
     * The user's full name.
     */
    private String name;

    /**
     * Whether the user account is currently active.
     */
    private boolean active;
}
```

### Short Documentation

For simple methods, a one-line comment is sufficient:

```java
/** Returns the username for the given user ID. */
public String getUsername(Long userId) {
    return userRepository.findById(userId).getUsername();
}

/** The default timeout duration in milliseconds. */
private static final long DEFAULT_TIMEOUT = 30000L;
```

### HTML in Javadoc

- **Use HTML tags sparingly** for formatting
- **Use `<p>`** for paragraphs
- **Use `<code>`** for code snippets
- **Use `<pre>`** for multi-line code

```java
/**
 * Processes the input string and returns the result.
 *
 * <p>This method performs the following steps:
 * <ol>
 *   <li>Validates the input</li>
 *   <li>Transforms the data</li>
 *   <li>Returns the result</li>
 * </ol>
 *
 * <p>Example usage:
 * <pre>{@code
 * String result = processor.process("input");
 * }</pre>
 */
public String process(String input) {
    // implementation
}
```

## Comments

### Inline Comments

- **Use sparingly**: Code should be self-documenting
- **Place on separate line** above the code when possible
- **Use for complex logic** that isn't obvious
- **Update comments** when code changes

```java
// Good - explains non-obvious logic
// Apply 10% discount for orders over $100, otherwise 5%
double discount = total > 100 ? 0.10 : 0.05;

// Avoid - stating the obvious
// Set x to 5
int x = 5;
```

### Block Comments

- **Use for complex algorithms** or business logic
- **Keep updated** with code changes
- **Indent to match** the code they describe

```java
// Check if user has permission to access this resource.
// Permission is granted if:
// 1. User is an admin
// 2. User owns the resource
// 3. Resource is marked as public
if (user.isAdmin() || resource.getOwner().equals(user) || resource.isPublic()) {
    grantAccess();
}
```

### TODO Comments

- **Use TODO** for future improvements:
  ```java
  // TODO: Add caching for better performance
  // TODO: Refactor to use Java 8 streams
  ```

- **Include context** when helpful:
  ```java
  // TODO(john.doe): Add validation for email format
  // TODO: Bug #123 - Handle edge case for empty lists
  ```

### Implementation Comments

- **Use for explaining implementation details**
- **Focus on "why" not "what"**

```java
// Using LinkedHashMap to preserve insertion order for iteration
Map<String, User> userCache = new LinkedHashMap<>();

// Synchronized on the list to prevent concurrent modification
synchronized (users) {
    users.add(newUser);
}
```

## Error Handling

### Exception Patterns

```java
// Custom exceptions
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(Long userId) {
        super("User with ID " + userId + " not found");
    }
}

public class DatabaseException extends RuntimeException {
    public DatabaseException(String message, Throwable cause) {
        super(message, cause);
    }
}

// Specific exception handling
try {
    User user = userService.findById(userId);
    return user;
} catch (UserNotFoundException e) {
    return null;
} catch (DatabaseException e) {
    logger.error("Database error: " + e.getMessage(), e);
    throw new ServiceException("Service temporarily unavailable", e);
}
```

### Try-with-Resources

```java
// Good - automatic resource management
try (Connection connection = dataSource.getConnection();
     PreparedStatement statement = connection.prepareStatement(sql)) {
    
    statement.setLong(1, userId);
    ResultSet resultSet = statement.executeQuery();
    return processResultSet(resultSet);
}

// Avoid - manual resource management
Connection connection = null;
try {
    connection = dataSource.getConnection();
    // use connection
} finally {
    if (connection != null) {
        try {
            connection.close();
        } catch (SQLException e) {
            logger.error("Failed to close connection", e);
        }
    }
}
```

### Validation and Error Messages

```java
// Fail fast with early validation
public User createUser(String username, String email, int age) {
    if (username == null || username.trim().isEmpty()) {
        throw new IllegalArgumentException("Username cannot be null or empty");
    }
    if (email == null || !email.contains("@")) {
        throw new IllegalArgumentException("Invalid email address: " + email);
    }
    if (age < 0 || age > 150) {
        throw new IllegalArgumentException("Age must be between 0 and 150, got: " + age);
    }
    
    return new User(username, email, age);
}

// Specific, actionable error messages
throw new IllegalArgumentException("Invalid user ID: " + userId + ". Must be a positive integer.");
throw new FileNotFoundException("Configuration file not found: " + configPath);
```

### Best Practices

- **Catch specific exceptions** - avoid broad `catch (Exception e)`
- **Use try-with-resources** for resource cleanup
- **Chain exceptions** with `cause` parameter to preserve context
- **Fail fast** - validate inputs early
- **Write descriptive error messages** with relevant context
- **Log exceptions appropriately** with stack traces when needed

## Modern Java Features

### Java 8+ Features to Use

**Streams API**:
```java
// Good - streams for collection processing
List<String> activeUsernames = users.stream()
    .filter(User::isActive)
    .map(User::getUsername)
    .collect(Collectors.toList());

// Avoid - traditional for loop for simple operations
List<String> usernames = new ArrayList<>();
for (User user : users) {
    if (user.isActive()) {
        usernames.add(user.getUsername());
    }
}
```

**Optional**:
```java
// Good - Optional for nullable return values
public Optional<User> findById(Long id) {
    User user = userRepository.findById(id);
    return Optional.ofNullable(user);
}

// Usage
Optional<User> userOpt = findById(123);
String username = userOpt.map(User::getUsername).orElse("Unknown");

// Avoid - null returns
public User findById(Long id) {
    return userRepository.findById(id);  // Might return null
}
```

**Lambda Expressions**:
```java
// Good - lambdas for functional interfaces
List<User> adults = users.stream()
    .filter(user -> user.getAge() >= 18)
    .collect(Collectors.toList());

button.addActionListener(event -> handleButtonClick());

// Avoid - anonymous classes for simple cases
List<User> adults = users.stream()
    .filter(new Predicate<User>() {
        @Override
        public boolean test(User user) {
            return user.getAge() >= 18;
        }
    })
    .collect(Collectors.toList());
```

**Method References**:
```java
// Good - method references when possible
List<String> names = users.stream()
    .map(User::getName)
    .collect(Collectors.toList());

users.forEach(System.out::println);

// Acceptable - lambdas when method references don't work
List<String> names = users.stream()
    .map(user -> user.getName().toUpperCase())
    .collect(Collectors.toList());
```

### Java 11+ Features

**var for Local Variables** (Java 10+):
```java
// Good - var when type is obvious
var users = new ArrayList<User>();  // Type is clear
var user = findUserById(123);       // Method name makes type clear

// Avoid - var when type is not obvious
var data = someMethod();  // What type is data?
```

**Text Blocks** (Java 15+):
```java
// Good - text blocks for multi-line strings
String html = """
    <html>
        <body>
            <h1>Hello, %s!</h1>
        </body>
    </html>
    """.formatted(name);

// Avoid - string concatenation for multi-line
String html = "<html>\n" +
    "    <body>\n" +
    "        <h1>Hello, " + name + "!</h1>\n" +
    "    </body>\n" +
    "</html>";
```

### Record Classes (Java 14+)

```java
// Good - records for immutable data carriers
public record User(Long id, String name, String email) {
    // Automatically provides constructor, getters, equals(), hashCode(), toString()
}

// Usage
User user = new User(1L, "John", "john@example.com");
String name = user.name();  // Accessor method
```

## Code Organization

### File Organization

1. **Package declaration**
2. **Import statements** (static → java → third-party → project)
3. **Class/interface documentation** (Javadoc)
4. **Class/interface declaration**
5. **Static fields** (constants first)
6. **Instance fields**
7. **Static initializer blocks**
8. **Instance initializer blocks**
9. **Constructors**
10. **Static methods**
11. **Instance methods** (public → protected → private)
12. **Inner classes**

### Class Organization Example

```java
package com.example.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;

import com.example.model.User;
import com.example.repository.UserRepository;

/**
 * Service for user management operations.
 *
 * @author John Doe
 * @version 1.0
 */
@Service
public class UserService {

    // Static constants
    private static final int MAX_LOGIN_ATTEMPTS = 3;

    // Instance fields
    private final UserRepository userRepository;
    private final EmailService emailService;

    // Constructor
    public UserService(UserRepository userRepository, EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }

    // Public methods
    public User createUser(User user) {
        validateUser(user);
        User savedUser = userRepository.save(user);
        emailService.sendWelcomeEmail(savedUser);
        return savedUser;
    }

    public Optional<User> findById(Long id) {
        return userRepository.findById(id);
    }

    // Protected methods
    protected void validateUser(User user) {
        if (user.getName() == null || user.getName().trim().isEmpty()) {
            throw new IllegalArgumentException("User name cannot be empty");
        }
    }

    // Private methods
    private boolean isValidEmail(String email) {
        return email != null && email.contains("@");
    }

    // Inner classes
    private static class UserValidator {
        // implementation
    }
}
```

## Formatting and Linting Tools

### Code Quality Tools

Use static analysis tools to maintain code quality:

- **Checkstyle**: Validates coding standards and conventions
- **SpotBugs**: Identifies potential bugs and security issues
- **PMD**: Detects bad coding practices

### Gradle Integration

**`build.gradle`**:

```groovy
plugins {
    id 'java'
    id 'checkstyle'
    id 'com.github.spotbugs' version '5.0.13'
    id 'pmd'
}

checkstyle {
    toolVersion = '10.9.3'
    configFile = file("${rootDir}/checkstyle.xml")
}

spotbugs {
    effort = 'max'
    reportLevel = 'low'
    excludeFilter = file("${rootDir}/spotbugs-exclude.xml")
}

pmd {
    toolVersion = '6.55.0'
    ruleSetFiles = files("${rootDir}/pmd.xml")
}
```

### Checkstyle Configuration

**`checkstyle.xml`**:

```xml
<?xml version="1.0"?>
<!DOCTYPE module PUBLIC
    "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN"
    "https://checkstyle.org/dtds/configuration_1_3.dtd">

<module name="Checker">
    <property name="charset" value="UTF-8"/>
    <property name="severity" value="warning"/>
    <property name="fileExtensions" value="java, properties, xml"/>

    <module name="TreeWalker">
        <module name="OuterTypeFilename"/>
        <module name="IllegalTokenText"/>
        <module name="AvoidEscapedUnicodeCharacters"/>
        <module name="LineLength">
            <property name="max" value="120"/>
        </module>
        <module name="AvoidStarImport"/>
        <module name="OneTopLevelClass"/>
        <module name="NoLineWrap"/>
        <module name="EmptyBlock"/>
        <module name="NeedBraces"/>
        <module name="LeftCurly"/>
        <module name="RightCurly"/>
        <module name="WhitespaceAround"/>
        <module name="OneStatementPerLine"/>
        <module name="MultipleVariableDeclarations"/>
        <module name="ArrayTypeStyle"/>
        <module name="MissingSwitchDefault"/>
        <module name="FallThrough"/>
        <module name="UpperEll"/>
        <module name="ModifierOrder"/>
        <module name="EmptyLineSeparator"/>
        <module name="SeparatorWrap"/>
        <module name="PackageName"/>
        <module name="TypeName"/>
        <module name="MemberName"/>
        <module name="ParameterName"/>
        <module name="LocalVariableName"/>
        <module name="ClassTypeParameterName"/>
        <module name="MethodTypeParameterName"/>
        <module name="InterfaceTypeParameterName"/>
        <module name="NoFinalizer"/>
        <module name="GenericWhitespace"/>
        <module name="Indentation"/>
        <module name="AbbreviationAsWordInName"/>
        <module name="OverloadMethodsDeclarationOrder"/>
        <module name="VariableDeclarationUsageDistance"/>
        <module name="CustomImportOrder"/>
        <module name="MethodParamPad"/>
        <module name="ParenPad"/>
        <module name="OperatorWrap"/>
        <module name="AnnotationLocation"/>
        <module name="NonEmptyAtclauseDescription"/>
        <module name="JavadocMethod"/>
        <module name="JavadocType"/>
        <module name="JavadocVariable"/>
        <module name="JavadocStyle"/>
    </module>
</module>
```

### SpotBugs Configuration

**`spotbugs.xml`**:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<FindBugsFilter>
    <Match>
        <Bug code="EI,EI2"/>  <!-- Expose internal representation -->
    </Match>
    <Match>
        <Bug code="Se"/>  <!-- Serializable field -->
    </Match>
    <Match>
        <Class name="~.*Test.*"/>
        <Bug code="RV"/>  <!-- Return value ignored -->
    </Match>
</FindBugsFilter>
```



## Summary

- **Formatting**: Use IDE auto-format, 100-120 char lines, 4-space indents, K&R braces
- **Naming**: `camelCase` for methods/variables, `PascalCase` for classes, `SCREAMING_SNAKE_CASE` for constants
- **Type Safety**: Explicit types, use interfaces, leverage generics
- **Imports**: Group in static → java → third-party → project, sort alphabetically
- **Error Handling**: Custom exceptions, try-with-resources, proper validation
- **Modern Features**: Use streams, Optional, lambdas, records appropriately
- **Documentation**: Javadoc blocks with examples and parameter descriptions
- **Tools**: Checkstyle, SpotBugs for code quality

This style guide ensures consistent, readable, and maintainable Java code across all projects.