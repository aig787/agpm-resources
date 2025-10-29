# Java Best Practices

This document defines technical best practices for Java development, covering tools, patterns, testing, security, and performance optimization.

## Core Principles

1. **Idiomatic Java**: Write code that follows Java conventions and modern standards
2. **Zero Warnings Policy**: All code must pass compilation without warnings
3. **Type Safety**: Leverage Java's strong typing system and generics
4. **Error Handling**: Implement proper exception handling and validation
5. **Clean Architecture**: Separate concerns with clear architectural layers
6. **Test Coverage**: Maintain >70% test coverage
7. **Security First**: Follow security best practices from the start

## Mandatory Completion Checklist

Before considering any Java code complete, you MUST:

1. ✅ Run formatter (auto-format code)
2. ✅ Run linter (static analysis tools)
3. ✅ Run tests (unit and integration tests)
4. ✅ Verify test coverage (target >70%)
5. ✅ Verify all dependencies are properly declared
6. ✅ Run security scan (dependency vulnerability check)

## Development Tools

### Build Tools: Gradle

**Use Gradle for Java projects**: Modern build tool with excellent dependency management and DSL support

```bash
# Create new Gradle project
gradle init --type java-application

# Build project
gradle build

# Run tests
gradle test

# Run application
gradle run

# Package application
gradle jar

# Dependency management
gradle dependencies
gradle dependencyCheck
```



### Dependency Best Practices

- **Use dependency management**: Specify versions in dependencyManagement section
- **Use semantic versioning**: Understand major.minor.patch versions
- **Keep dependencies updated**: Regularly review and update
- **Security auditing**: Use OWASP Dependency Check
- **Separate test dependencies**: Use test scope appropriately
- **Document dependency choices**: Explain why specific versions are required

**Gradle dependency management example**:

```groovy
// build.gradle
dependencies {
    implementation platform('org.springframework.boot:spring-boot-dependencies:3.1.0')
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}
```

## Type Safety and Generics

### Generic Best Practices

**Use generics for type safety**:

```java
// Good - generic collection
List<String> names = new ArrayList<>();
Map<String, User> userMap = new HashMap<>();

// Avoid - raw types
List names = new ArrayList();  // Raw type - unsafe
Map userMap = new HashMap();   // Raw type - unsafe
```

**Generic methods**:

```java
// Good - generic method
public <T> T first(List<T> items) {
    return items.isEmpty() ? null : items.get(0);
}

// Usage
String first = first(names);
User firstUser = first(users);
```

**Bounded type parameters**:

```java
// Good - bounded type parameter
public <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) > 0 ? a : b;
}

// Good - multiple bounds
public <T extends Number & Comparable<T>> T process(T value) {
    // implementation
}
```

### Wildcards

**Use wildcards appropriately**:

```java
// Good - PECS (Producer Extends, Consumer Super)
public void process(List<? extends Number> numbers) {  // Producer
    Number num = numbers.get(0);
}

public void add(List<? super Integer> numbers) {  // Consumer
    numbers.add(42);
}

// Avoid - unnecessary wildcards
public void process(List<Number> numbers) {  // Use when you need Number methods
    // implementation
}
```

### Optional Usage

**Use Optional for nullable return values**:

```java
// Good - Optional for return values
public Optional<User> findById(Long id) {
    User user = userRepository.findById(id);
    return Optional.ofNullable(user);
}

// Good - Optional chaining
String username = findById(id)
    .map(User::getName)
    .orElse("Unknown");

// Avoid - Optional for fields
public class User {
    private Optional<String> email;  // Bad - use null instead
    private String email;            // Good
}
```

## Error Handling

### Exception Hierarchy

**Create custom exception hierarchy**:

```java
// Base exception
public abstract class ApplicationException extends RuntimeException {
    protected ApplicationException(String message) {
        super(message);
    }
    
    protected ApplicationException(String message, Throwable cause) {
        super(message, cause);
    }
}

// Specific exceptions
public class ValidationException extends ApplicationException {
    public ValidationException(String message) {
        super(message);
    }
}

public class ResourceNotFoundException extends ApplicationException {
    public ResourceNotFoundException(String resource, Object id) {
        super(String.format("%s with id %s not found", resource, id));
    }
}

public class BusinessRuleException extends ApplicationException {
    public BusinessRuleException(String message) {
        super(message);
    }
}
```

### Exception Handling Patterns

**Use try-with-resources for resource management**:

```java
// Good - automatic resource cleanup
public String readFile(String path) throws IOException {
    try (BufferedReader reader = Files.newBufferedReader(Paths.get(path))) {
        return reader.lines().collect(Collectors.joining("\n"));
    }
}

// Good - multiple resources
try (Connection conn = dataSource.getConnection();
     PreparedStatement stmt = conn.prepareStatement(sql);
     ResultSet rs = stmt.executeQuery()) {
    
    return processResultSet(rs);
}
```

**Proper exception chaining**:

```java
// Good - preserve original exception
try {
    return externalService.getData();
} catch (ExternalServiceException e) {
    throw new ServiceException("Failed to fetch data from external service", e);
}

// Avoid - losing context
try {
    return externalService.getData();
} catch (ExternalServiceException e) {
    throw new ServiceException("Failed to fetch data");  // Lost original cause
}
```

### Validation Frameworks

**Use Bean Validation (JSR-380)**:

```java
// Good - declarative validation
public class User {
    @NotNull(message = "Name cannot be null")
    @Size(min = 2, max = 50, message = "Name must be between 2 and 50 characters")
    private String name;
    
    @Email(message = "Invalid email format")
    @NotBlank(message = "Email cannot be blank")
    private String email;
    
    @Min(value = 0, message = "Age must be non-negative")
    @Max(value = 150, message = "Age must be less than 150")
    private int age;
}

// Service layer validation
@Service
public class UserService {
    public User createUser(@Valid User user) {
        // Spring automatically validates the user object
        return userRepository.save(user);
    }
}
```

## Testing Strategy

### JUnit 5 Framework

**Project structure**:

```
myproject/
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/example/
│   │           ├── User.java
│   │           └── UserService.java
│   └── test/
│       └── java/
│           └── com/example/
│               ├── UserTest.java
│               └── UserServiceTest.java
├── pom.xml
└── README.md
```

### Writing Tests

**Basic test**:

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @InjectMocks
    private UserService userService;
    
    @Test
    @DisplayName("Should create user with valid data")
    void shouldCreateUserWithValidData() {
        // Given
        User user = new User("John", "john@example.com", 30);
        User savedUser = new User(1L, "John", "john@example.com", 30);
        
        when(userRepository.save(any(User.class))).thenReturn(savedUser);
        
        // When
        User result = userService.createUser(user);
        
        // Then
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getName()).isEqualTo("John");
        verify(userRepository).save(user);
    }
}
```

**Parameterized tests**:

```java
@ParameterizedTest
@ValueSource(strings = {"user@example.com", "test.domain.com", "simple@local"})
@NullAndEmptySource
void shouldValidateEmail(String email) {
    // Given
    User user = new User("John", email, 30);
    
    // When & Then
    assertDoesNotThrow(() -> userService.validateUser(user));
}

@ParameterizedTest
@CsvSource({
    "John, john@example.com, 30, true",
    "Jane, jane@test.com, 25, true",
    "InvalidEmail, invalid-email, 30, false",
    "NoName, valid@example.com, 30, false"
})
void shouldValidateUserData(String name, String email, int age, boolean expectedValid) {
    // Given
    User user = new User(name, email, age);
    
    // When
    boolean isValid = userService.isValid(user);
    
    // Then
    assertThat(isValid).isEqualTo(expectedValid);
}
```

**Testing async code**:

```java
@Test
void shouldHandleAsyncOperation() throws Exception {
    // Given
    CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
        try {
            Thread.sleep(100);
            return "result";
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    });
    
    // When
    String result = future.get(1, TimeUnit.SECONDS);
    
    // Then
    assertThat(result).isEqualTo("result");
}
```

### Mocking with Mockito

**Mock external dependencies**:

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock
    private EmailService emailService;
    
    @Mock
    private UserRepository userRepository;
    
    @InjectMocks
    private UserService userService;
    
    @Test
    void shouldSendWelcomeEmailWhenCreatingUser() {
        // Given
        User user = new User("John", "john@example.com", 30);
        User savedUser = new User(1L, "John", "john@example.com", 30);
        
        when(userRepository.save(any(User.class))).thenReturn(savedUser);
        doNothing().when(emailService).sendWelcomeEmail(any(User.class));
        
        // When
        User result = userService.createUser(user);
        
        // Then
        assertThat(result.getId()).isEqualTo(1L);
        verify(emailService).sendWelcomeEmail(savedUser);
    }
    
    @Test
    void shouldHandleEmailServiceFailure() {
        // Given
        User user = new User("John", "john@example.com", 30);
        User savedUser = new User(1L, "John", "john@example.com", 30);
        
        when(userRepository.save(any(User.class))).thenReturn(savedUser);
        doThrow(new EmailServiceException("SMTP server down"))
            .when(emailService).sendWelcomeEmail(any(User.class));
        
        // When & Then
        assertThrows(EmailServiceException.class, () -> userService.createUser(user));
        verify(userRepository).save(user);
    }
}
```

### Integration Testing

**Spring Boot integration tests**:

```java
@SpringBootTest
@TestPropertySource(properties = {
    "spring.datasource.url=jdbc:h2:mem:testdb",
    "spring.jpa.hibernate.ddl-auto=create-drop"
})
@Transactional
class UserRepositoryIntegrationTest {
    
    @Autowired
    private UserRepository userRepository;
    
    @Test
    void shouldSaveAndFindUser() {
        // Given
        User user = new User("John", "john@example.com", 30);
        
        // When
        User saved = userRepository.save(user);
        Optional<User> found = userRepository.findById(saved.getId());
        
        // Then
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("John");
    }
}
```

### Testing Best Practices

- **Aim for >70% coverage**: Use JaCoCo for coverage reports
- **Test isolation**: Each test should be independent
- **Use descriptive test names**: `shouldCreateUserWithValidData`
- **Test edge cases**: Null values, empty collections, boundary conditions
- **Use test categories**: `@Tag("unit")`, `@Tag("integration")`
- **Mock external dependencies**: Don't test external systems in unit tests
- **Use test builders**: For creating complex test objects

## Linting & Code Quality

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
        <!-- Naming conventions -->
        <module name="ConstantName"/>
        <module name="LocalVariableName"/>
        <module name="MemberName"/>
        <module name="MethodName"/>
        <module name="ParameterName"/>
        <module name="TypeName"/>
        
        <!-- Code quality -->
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
        
        <!-- Best practices -->
        <module name="MissingSwitchDefault"/>
        <module name="FallThrough"/>
        <module name="UpperEll"/>
        <module name="ModifierOrder"/>
        <module name="EmptyLineSeparator"/>
        <module name="SeparatorWrap"/>
        <module name="PackageName"/>
        <module name="IllegalTokenText"/>
        <module name="AvoidEscapedUnicodeCharacters"/>
        <module name="LineLength">
            <property name="max" value="120"/>
        </module>
        
        <!-- Javadoc -->
        <module name="JavadocMethod"/>
        <module name="JavadocType"/>
        <module name="JavadocVariable"/>
        <module name="JavadocStyle"/>
    </module>
</module>
```

### SpotBugs Configuration

**Enable SpotBugs in Gradle**:

```groovy
// build.gradle
plugins {
    id 'com.github.spotbugs' version '5.0.13'
}

spotbugs {
    effort = 'max'
    reportLevel = 'low'
    excludeFilter = file('spotbugs-exclude.xml')
}
```

**`spotbugs-exclude.xml`**:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<FindBugsFilter>
    <!-- Ignore test classes -->
    <Match>
        <Class name="~.*Test.*"/>
    </Match>
    
    <!-- Ignore specific patterns -->
    <Match>
        <Bug code="EI,EI2"/>  <!-- Expose internal representation -->
    </Match>
    
    <Match>
        <Bug code="Se"/>  <!-- Serializable field -->
    </Match>
</FindBugsFilter>
```

### PMD Configuration

**`pmd.xml`**:

```xml
<?xml version="1.0"?>
<ruleset name="Custom Rules"
    xmlns="http://pmd.sourceforge.net/ruleset/2.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://pmd.sourceforge.net/ruleset/2.0.0 https://pmd.sourceforge.io/ruleset_2_0_0.xsd">
    
    <description>Custom PMD ruleset</description>
    
    <!-- Best practices -->
    <rule ref="category/java/bestpractices.xml">
        <exclude name="SystemPrintln"/>
    </rule>
    
    <!-- Code style -->
    <rule ref="category/java/codestyle.xml">
        <exclude name="ShortVariable"/>
    </rule>
    
    <!-- Design -->
    <rule ref="category/java/design.xml">
        <exclude name="LooseCoupling"/>
    </rule>
    
    <!-- Error prone -->
    <rule ref="category/java/errorprone.xml"/>
    
    <!-- Performance -->
    <rule ref="category/java/performance.xml"/>
    
    <!-- Security -->
    <rule ref="category/java/security.xml"/>
</ruleset>
```

## Database Best Practices

### JPA/Hibernate Best Practices

**Entity design**:

```java
@Entity
@Table(name = "users")
@Data  // Lombok for getters/setters
@NoArgsConstructor
@AllArgsConstructor
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, length = 100)
    private String name;
    
    @Column(nullable = false, unique = true, length = 255)
    private String email;
    
    @Column(nullable = false)
    private Integer age;
    
    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;
    
    // Relationships
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Order> orders = new ArrayList<>();
}
```

**Repository pattern with Spring Data**:

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // Derived queries
    Optional<User> findByEmail(String email);
    List<User> findByNameContainingIgnoreCase(String name);
    List<User> findByAgeGreaterThan(int age);
    
    // Custom queries
    @Query("SELECT u FROM User u WHERE u.email = :email AND u.active = true")
    Optional<User> findActiveUserByEmail(@Param("email") String email);
    
    // Native queries
    @Query(value = "SELECT COUNT(*) FROM users WHERE created_at > :date", nativeQuery = true)
    long countUsersCreatedAfter(@Param("date") LocalDateTime date);
    
    // Modifying queries
    @Modifying
    @Query("UPDATE User u SET u.active = false WHERE u.lastLogin < :date")
    int deactivateInactiveUsers(@Param("date") LocalDateTime date);
}
```

### Query Optimization

**Avoid N+1 queries**:

```java
// Bad - N+1 queries
List<User> users = userRepository.findAll();
for (User user : users) {
    System.out.println(user.getOrders().size());  // Separate query for each user
}

// Good - fetch join
@Query("SELECT u FROM User u LEFT JOIN FETCH u.orders")
List<User> findAllWithOrders();

// Good - EntityGraph
@EntityGraph(attributePaths = {"orders"})
List<User> findAllWithOrders();
```

**Pagination**:

```java
@Service
public class UserService {
    
    public Page<User> getUsers(Pageable pageable) {
        return userRepository.findAll(pageable);
    }
    
    public Page<User> searchUsers(String keyword, Pageable pageable) {
        return userRepository.findByNameContainingIgnoreCase(keyword, pageable);
    }
}

// Controller
@GetMapping("/users")
public Page<User> getUsers(
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "20") int size,
    @RequestParam(defaultValue = "name") String sort) {
    
    Pageable pageable = PageRequest.of(page, size, Sort.by(sort));
    return userService.getUsers(pageable);
}
```

### Transaction Management

**Spring transaction management**:

```java
@Service
@Transactional
public class UserService {
    
    @Transactional(readOnly = true)
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));
    }
    
    @Transactional
    public User createUser(User user) {
        validateUser(user);
        User saved = userRepository.save(user);
        emailService.sendWelcomeEmail(saved);
        return saved;
    }
    
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void logUserActivity(Long userId, String activity) {
        // Always runs in a new transaction
        UserActivityLog log = new UserActivityLog(userId, activity, LocalDateTime.now());
        activityLogRepository.save(log);
    }
}
```

## Security Best Practices

### Input Validation

**Bean Validation**:

```java
public class CreateUserRequest {
    
    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 50, message = "Name must be between 2 and 50 characters")
    private String name;
    
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;
    
    @Pattern(regexp = "^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$", 
             message = "Password must be at least 8 characters with letters and numbers")
    private String password;
    
    @Min(value = 0, message = "Age must be non-negative")
    @Max(value = 150, message = "Age must be less than 150")
    private Integer age;
}
```

### Authentication and Authorization

**Spring Security configuration**:

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity(prePostEnabled = true)
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/users/**").hasAnyRole("USER", "ADMIN")
                .requestMatchers(HttpMethod.POST, "/api/users").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);
        
        return http.build();
    }
    
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

**Method-level security**:

```java
@Service
public class UserService {
    
    @PreAuthorize("hasRole('ADMIN') or #id == authentication.principal.id")
    public User getUserById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));
    }
    
    @PreAuthorize("hasRole('ADMIN')")
    public User createUser(User user) {
        return userRepository.save(user);
    }
    
    @PostAuthorize("returnObject.email == authentication.principal.username")
    public User getUserByEmail(String email) {
        return userRepository.findByEmail(email)
            .orElseThrow(() -> new ResourceNotFoundException("User", "email", email));
    }
}
```

### Security Guidelines

- **Validate all input**: Never trust external data
- **Use parameterized queries**: Prevent SQL injection
- **Implement authentication & authorization**: JWT, OAuth2, etc.
- **Enable HTTPS**: Always use TLS in production
- **Implement rate limiting**: Prevent abuse
- **Don't log sensitive data**: Passwords, tokens, API keys
- **Regular security audits**: Use OWASP Dependency Check
- **Implement CSRF protection**: For state-changing operations
- **Keep dependencies updated**: Address security vulnerabilities

```bash
# Security scanning
mvn dependency-check:check
gradle dependencyCheck
```

## Performance Optimization

### Profiling

**Use Java profilers**:

```bash
# VisualVM (comes with JDK)
jvisualvm

# JProfiler (commercial)
jprofiler

# YourKit (commercial)
yourkit

# Command-line profiling
java -XX:+FlightRecorder -XX:StartFlightRecording=duration=60s,filename=profile.jfr MyApp
```

### Memory Management

**Use appropriate data structures**:

```java
// Good - use HashMap for frequent lookups
Map<Long, User> userCache = new HashMap<>();

public User getUser(Long id) {
    User cached = userCache.get(id);
    if (cached != null) {
        return cached;
    }
    
    User user = userRepository.findById(id);
    userCache.put(id, user);
    return user;
}

// Avoid - linear search in large lists
public User getUserBad(Long id) {
    return allUsers.stream()
        .filter(user -> user.getId().equals(id))
        .findFirst()
        .orElse(null);
}
```

**String optimization**:

```java
// Good - StringBuilder for concatenation in loops
StringBuilder sb = new StringBuilder();
for (String item : items) {
    sb.append(item).append(",");
}
String result = sb.toString();

// Good - String.format for formatted strings
String message = String.format("User %s (ID: %d) has %d orders", 
    user.getName(), user.getId(), user.getOrders().size());

// Avoid - string concatenation in loops
String result = "";
for (String item : items) {
    result += item + ",";  // Creates new String objects
}
```

### Caching

**Spring Cache abstraction**:

```java
@Service
@CacheConfig(cacheNames = "users")
public class UserService {
    
    @Cacheable(key = "#id")
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));
    }
    
    @CachePut(key = "#result.id")
    public User updateUser(User user) {
        return userRepository.save(user);
    }
    
    @CacheEvict(key = "#id")
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
    
    @CacheEvict(allEntries = true)
    public void clearCache() {
        // Clear all cache entries
    }
}
```

### Performance Guidelines

- **Profile before optimizing**: Use profilers to identify bottlenecks
- **Use appropriate data structures**: HashMap for lookups, ArrayList for iteration
- **Implement caching**: Redis or in-memory for frequently accessed data
- **Use connection pooling**: For database and HTTP connections
- **Batch operations**: Reduce round trips to database/API
- **Use lazy loading**: Load data only when needed
- **Optimize database queries**: Proper indexing, avoid N+1
- **Consider streaming**: For large data processing
- **Choose appropriate algorithms**: Based on data size and access patterns

## Project Structure

**Recommended project structure**:

```
myproject/
├── build.gradle               # Gradle build configuration
├── settings.gradle            # Gradle settings
├── README.md                  # Project documentation
├── .gitignore                 # Git ignore file
├── .env.example               # Environment variables template
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── example/
│   │   │           ├── MyApplication.java    # Main class
│   │   │           ├── config/               # Configuration
│   │   │           │   ├── SecurityConfig.java
│   │   │           │   └── DatabaseConfig.java
│   │   │           ├── controller/           # REST controllers
│   │   │           │   ├── UserController.java
│   │   │           │   └── AuthController.java
│   │   │           ├── service/              # Business logic
│   │   │           │   ├── UserService.java
│   │   │           │   └── AuthService.java
│   │   │           ├── repository/           # Data access
│   │   │           │   ├── UserRepository.java
│   │   │           │   └── OrderRepository.java
│   │   │           ├── model/                # Domain models
│   │   │           │   ├── User.java
│   │   │           │   └── Order.java
│   │   │           ├── dto/                  # Data transfer objects
│   │   │           │   ├── UserDto.java
│   │   │           │   └── CreateUserRequest.java
│   │   │           ├── exception/            # Custom exceptions
│   │   │           │   ├── ApplicationException.java
│   │   │           │   └── ResourceNotFoundException.java
│   │   │           └── util/                 # Utility classes
│   │   │               ├── DateUtil.java
│   │   │               └── ValidationUtil.java
│   │   └── resources/
│   │       ├── application.yml               # Application configuration
│   │       ├── application-dev.yml           # Development profile
│   │       ├── application-prod.yml          # Production profile
│   │       └── db/migration/                 # Flyway migrations
│   └── test/
│       └── java/
│           └── com/
│               └── example/
│                   ├── controller/
│                   ├── service/
│                   ├── repository/
│                   └── integration/
├── docs/                        # Documentation
└── scripts/                     # Utility scripts
```

## CI/CD Integration

### Gradle Build Pipeline

**`.github/workflows/ci.yml`**:

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'
    
    - name: Cache Gradle packages
      uses: actions/cache@v3
      with:
        path: |
          ~/.gradle/caches
          ~/.gradle/wrapper
        key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
        restore-keys: |
          ${{ runner.os }}-gradle-
    
    - name: Run tests
      run: ./gradlew test
    
    - name: Generate test report
      uses: dorny/test-reporter@v1
      if: success() || failure()
      with:
        name: Gradle Tests
        path: build/test-results/test/TEST-*.xml
        reporter: java-junit
    
    - name: Check code coverage
      run: ./gradlew jacocoTestReport
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: build/reports/jacoco/test/jacocoTestReport.xml
    
    - name: Run Checkstyle
      run: ./gradlew checkstyleMain checkstyleTest
    
    - name: Run SpotBugs
      run: ./gradlew spotbugsMain spotbugsTest
    
    - name: Dependency security check
      run: ./gradlew dependencyCheck
    
    - name: Build application
      run: ./gradlew build -x test
```

### Pre-commit Hooks

**`.pre-commit-config.yaml`**:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: local
    hooks:
      - id: checkstyle
        name: Checkstyle
        entry: ./gradlew checkstyleMain checkstyleTest
        language: system
        pass_filenames: false
        always_run: true

      - id: spotbugs
        name: SpotBugs
        entry: ./gradlew spotbugsMain spotbugsTest
        language: system
        pass_filenames: false
        always_run: true

      - id: test
        name: Test
        entry: ./gradlew test
        language: system
        pass_filenames: false
        always_run: true
```

## Context7 Integration

Always use Context7 MCP server for current documentation when developing Java projects:

### Key Libraries

- `/spring-projects/spring-boot` - Modern application framework
- `/spring-projects/spring-framework` - Core Spring framework
- `/hibernate/hibernate-orm` - Object-relational mapping
- `/junit-team/junit5` - Testing framework
- `/mockito/mockito` - Mocking framework
- `/eclipse-ee4j/jakartaee-platform` - Java EE specifications
- `/openjdk/jdk` - Java Development Kit
- `/gradle/gradle` - Build tool

### Example Usage

```
Create a Spring Boot application with JWT authentication and PostgreSQL integration.
Include proper async patterns, validation, and error handling.
use context7 /spring-projects/spring-boot /hibernate/hibernate-orm /junit-team/junit5
```

## Summary

- **Use modern tools**: Gradle, Spring Boot, JUnit 5, Mockito
- **Type everything**: Leverage Java's strong typing and generics
- **Test thoroughly**: >70% coverage, unit + integration tests
- **Validate all input**: Never trust external data
- **Handle errors properly**: Custom exceptions, proper hierarchy
- **Optimize when needed**: Profile first, then optimize
- **Secure by default**: Authentication, validation, encryption
- **Follow clean architecture**: Separate concerns, clear layers
- **Automate quality checks**: CI/CD, pre-commit hooks
- **Keep dependencies updated**: Security and features

These practices ensure robust, maintainable, and secure Java applications.