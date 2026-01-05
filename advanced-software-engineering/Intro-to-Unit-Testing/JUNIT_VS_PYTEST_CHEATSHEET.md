# JUnit (Java) vs pytest (Python) - Quick Reference

## Annotation/Decorator Mapping

| JUnit 5 (Java) | pytest (Python) | Purpose |
|----------------|-----------------|---------|
| `@Test` | `def test_*()` | Mark a test method (pytest uses naming convention) |
| `@BeforeEach` | `@pytest.fixture` | Run before each test |
| `@AfterEach` | `@pytest.fixture` with `yield` | Run after each test (teardown) |
| `@BeforeAll` | `@pytest.fixture(scope="class")` | Run once before all tests in class |
| `@AfterAll` | `@pytest.fixture(scope="class")` with `yield` | Run once after all tests in class |
| `@Disabled` | `@pytest.mark.skip` | Skip a test |
| `@DisplayName` | Docstring or test name | Human-readable test name |
| `@Tag("slow")` | `@pytest.mark.slow` | Categorize tests |
| `@ParameterizedTest` | `@pytest.mark.parametrize` | Run test with multiple inputs |
| `@Nested` | Inner class | Group related tests |
| `@RepeatedTest(5)` | `@pytest.mark.repeat(5)` | Run test multiple times |
| `@Timeout(5)` | `@pytest.mark.timeout(5)` | Fail if test takes too long |

---

## Side-by-Side Examples

### Basic Test

```java
// Java - JUnit 5
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {
    @Test
    void testAddition() {
        Calculator calc = new Calculator();
        assertEquals(5, calc.add(2, 3));
    }
}
```

```python
# Python - pytest
def test_addition():
    calc = Calculator()
    assert calc.add(2, 3) == 5
```

---

### Setup & Teardown

```java
// Java - JUnit 5
class DatabaseTest {
    private Connection conn;

    @BeforeAll
    static void setupClass() {
        // Runs once before all tests
    }

    @BeforeEach
    void setup() {
        conn = Database.connect();
    }

    @AfterEach
    void teardown() {
        conn.close();
    }

    @AfterAll
    static void teardownClass() {
        // Runs once after all tests
    }

    @Test
    void testQuery() {
        // uses conn
    }
}
```

```python
# Python - pytest
import pytest

@pytest.fixture(scope="class")
def setup_class():
    """Runs once before all tests in class"""
    print("Setting up class")
    yield
    print("Tearing down class")  # AfterAll equivalent

@pytest.fixture
def connection():
    """Runs before each test (BeforeEach)"""
    conn = Database.connect()
    yield conn  # Test runs here
    conn.close()  # AfterEach - teardown

class TestDatabase:
    def test_query(self, connection):
        # uses connection fixture
        pass
```

**Alternative: Using `setup_method` / `teardown_method`**

```python
# Python - More JUnit-like style
class TestDatabase:
    def setup_method(self):
        """BeforeEach equivalent"""
        self.conn = Database.connect()

    def teardown_method(self):
        """AfterEach equivalent"""
        self.conn.close()

    def setup_class(cls):
        """BeforeAll equivalent"""
        pass

    def teardown_class(cls):
        """AfterAll equivalent"""
        pass

    def test_query(self):
        # uses self.conn
        pass
```

---

### Assertions

| JUnit 5 | pytest | Purpose |
|---------|--------|---------|
| `assertEquals(expected, actual)` | `assert actual == expected` | Equality |
| `assertNotEquals(a, b)` | `assert a != b` | Inequality |
| `assertTrue(condition)` | `assert condition` | Boolean true |
| `assertFalse(condition)` | `assert not condition` | Boolean false |
| `assertNull(obj)` | `assert obj is None` | Null check |
| `assertNotNull(obj)` | `assert obj is not None` | Not null |
| `assertThrows(Exception.class, () -> ...)` | `with pytest.raises(Exception):` | Exception expected |
| `assertAll(...)` | Multiple asserts (soft asserts with plugin) | Multiple assertions |
| `assertArrayEquals(a, b)` | `assert a == b` (lists) | Array/List equality |
| `assertTimeout(Duration.ofSeconds(1), () -> ...)` | `@pytest.mark.timeout(1)` | Timeout |

```java
// Java - Exception testing
@Test
void testDivideByZero() {
    Calculator calc = new Calculator();
    assertThrows(ArithmeticException.class, () -> {
        calc.divide(10, 0);
    });
}
```

```python
# Python - Exception testing
def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)

# With message matching
def test_divide_by_zero_message():
    with pytest.raises(ValueError, match="cannot be zero"):
        calc.divide(10, 0)
```

---

### Parameterized Tests

```java
// Java - JUnit 5
@ParameterizedTest
@CsvSource({
    "1, 1, 2",
    "2, 3, 5",
    "10, 20, 30"
})
void testAdd(int a, int b, int expected) {
    assertEquals(expected, calculator.add(a, b));
}
```

```python
# Python - pytest
@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 2),
    (2, 3, 5),
    (10, 20, 30),
])
def test_add(a, b, expected):
    assert calculator.add(a, b) == expected
```

---

### Skip & Conditional Skip

```java
// Java
@Disabled("Bug #123 not fixed yet")
@Test
void testBroken() { }

@EnabledOnOs(OS.LINUX)
@Test
void testLinuxOnly() { }

@EnabledIf("customCondition")
@Test
void testConditional() { }
```

```python
# Python
@pytest.mark.skip(reason="Bug #123 not fixed yet")
def test_broken():
    pass

@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
def test_linux_only():
    pass

@pytest.mark.skipif(not HAS_DATABASE, reason="No DB available")
def test_conditional():
    pass
```

---

### Mocking

```java
// Java - Mockito
@ExtendWith(MockitoExtension.class)
class ServiceTest {
    @Mock
    private Repository repo;

    @InjectMocks
    private Service service;

    @Test
    void testFindUser() {
        when(repo.findById(1)).thenReturn(new User("John"));

        User result = service.getUser(1);

        assertEquals("John", result.getName());
        verify(repo).findById(1);
    }
}
```

```python
# Python - unittest.mock (built-in)
from unittest.mock import Mock, patch, MagicMock

def test_find_user():
    # Create mock
    repo = Mock()
    repo.find_by_id.return_value = User("John")

    service = Service(repo)
    result = service.get_user(1)

    assert result.name == "John"
    repo.find_by_id.assert_called_once_with(1)

# Using patch decorator
@patch('module.Repository')
def test_with_patch(mock_repo):
    mock_repo.return_value.find_by_id.return_value = User("John")
    # ...

# Using patch as context manager
def test_with_context():
    with patch('module.Repository') as mock_repo:
        mock_repo.return_value.find_by_id.return_value = User("John")
        # ...
```

---

## Terminology Mapping

| Java/JUnit Term | Python/pytest Term |
|-----------------|-------------------|
| Test Class | Test class or test module |
| Test Method | Test function |
| Annotation | Decorator |
| Assertion | Assert statement |
| Test Suite | Test module/directory |
| Test Runner | pytest (command) |
| `@Mock` | `Mock()` or `@patch` |
| `@InjectMocks` | Constructor injection |
| Test Fixture | Fixture (`@pytest.fixture`) |
| `@ExtendWith` | Plugin or `conftest.py` |
| `pom.xml` (Maven) | `requirements.txt` / `pyproject.toml` |
| `mvn test` | `pytest` |

---

## Libraries Comparison

| Purpose | Java | Python |
|---------|------|--------|
| Test Framework | JUnit 5 | pytest (or unittest) |
| Mocking | Mockito | unittest.mock (built-in), pytest-mock |
| Assertions | JUnit assertions, AssertJ | Built-in assert, pytest assertions |
| Parameterized | JUnit @ParameterizedTest | pytest.mark.parametrize |
| Coverage | JaCoCo | pytest-cov (coverage.py) |
| BDD | Cucumber | pytest-bdd, behave |
| HTTP Mocking | WireMock | responses, httpretty, pytest-httpserver |
| Test Containers | Testcontainers | testcontainers-python |

---

## Key Differences

| Aspect | JUnit (Java) | pytest (Python) |
|--------|--------------|-----------------|
| **Test Discovery** | `@Test` annotation | `test_` prefix naming convention |
| **Fixtures** | Annotations (`@BeforeEach`) | Functions with `@pytest.fixture` |
| **Assertions** | Methods: `assertEquals()` | Simple: `assert x == y` |
| **Fixture Injection** | Constructor/field injection | Function parameters |
| **Configuration** | XML/annotations | `conftest.py`, `pytest.ini` |
| **Fixture Scope** | Class-level only | function, class, module, session |
| **Parallel Execution** | JUnit Platform | pytest-xdist plugin |
| **Shared Fixtures** | Inheritance or extensions | `conftest.py` (auto-discovered) |

---

## conftest.py - Python's Secret Weapon

`conftest.py` is pytest's way to share fixtures across multiple test files (no Java equivalent):

```python
# conftest.py (auto-discovered by pytest)

import pytest

@pytest.fixture
def database():
    """Available to ALL tests in this directory and subdirectories"""
    db = Database.connect()
    yield db
    db.close()

@pytest.fixture
def logged_in_user(database):
    """Fixtures can depend on other fixtures"""
    user = database.create_user("test@example.com")
    return user
```

```python
# test_anything.py - fixtures auto-injected
def test_something(database, logged_in_user):
    # Both fixtures available without any import!
    pass
```

---

## Quick Command Comparison

| Action | Java (Maven) | Python (pytest) |
|--------|--------------|-----------------|
| Run all tests | `mvn test` | `pytest` |
| Run specific class | `mvn test -Dtest=MyTest` | `pytest test_file.py` |
| Run specific method | `mvn test -Dtest=MyTest#testMethod` | `pytest test_file.py::test_method` |
| Run with tag | `mvn test -Dgroups=slow` | `pytest -m slow` |
| Skip tests | `mvn test -DskipTests` | `pytest --ignore=tests/` |
| Verbose output | `mvn test -X` | `pytest -v` |
| Coverage | `mvn jacoco:report` | `pytest --cov=src` |
| Fail fast | `mvn test -Dfailfast` | `pytest -x` |

---

## TL;DR - Minimal Translation

```
@Test              →  def test_*():
@BeforeEach        →  @pytest.fixture
@AfterEach         →  yield in fixture
@BeforeAll         →  @pytest.fixture(scope="class")
assertEquals(a,b)  →  assert a == b
assertThrows       →  with pytest.raises()
@Mock              →  Mock() or @patch
@Disabled          →  @pytest.mark.skip
@ParameterizedTest →  @pytest.mark.parametrize
```
