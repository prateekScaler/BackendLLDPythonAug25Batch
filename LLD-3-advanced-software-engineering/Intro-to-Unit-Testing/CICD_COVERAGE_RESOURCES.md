# Code Coverage, CI/CD Integration & Learning Resources

## Table of Contents
1. [Code Coverage](#code-coverage)
2. [CI/CD Integration with GitHub Actions](#cicd-integration-with-github-actions)
3. [Popular Open Source Repos with Great Test Suites](#popular-open-source-repos-with-great-test-suites)
4. [Platforms to Practice TDD and Unit Testing](#platforms-to-practice-tdd-and-unit-testing)

---

## Code Coverage

### What is Code Coverage?

Code coverage measures how much of your source code is executed when tests run. It helps identify untested parts of your codebase.

### Types of Coverage Metrics

| Metric | Description |
|--------|-------------|
| **Line Coverage** | % of code lines executed |
| **Branch Coverage** | % of if/else branches executed |
| **Function Coverage** | % of functions called |
| **Statement Coverage** | % of statements executed |

### Setting Up Coverage in Python

#### Install pytest-cov

```bash
pip install pytest-cov
```

#### Run Tests with Coverage

```bash
# Basic coverage report
pytest --cov=your_package tests/

# Coverage with missing lines shown
pytest --cov=your_package --cov-report=term-missing tests/

# Generate HTML report
pytest --cov=your_package --cov-report=html tests/
# Open htmlcov/index.html in browser

# Generate XML report (for CI tools)
pytest --cov=your_package --cov-report=xml tests/
```

#### Example Output

```
---------- coverage: platform darwin, python 3.11.0 -----------
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
src/user_service.py                 120     12    90%   45-48, 92-95
src/validators.py                    35      3    91%   28-30
src/repository.py                    50      0   100%
---------------------------------------------------------------
TOTAL                               205     15    93%
```

### Coverage Configuration

Create a `.coveragerc` file or add to `pyproject.toml`:

```ini
# .coveragerc
[run]
source = src
omit =
    */tests/*
    */__init__.py
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:

fail_under = 80
show_missing = true
```

Or in `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/__init__.py"]

[tool.coverage.report]
fail_under = 80
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
]
```

### Coverage Best Practices

1. **Aim for 80%+ coverage** - but don't obsess over 100%
2. **Focus on critical paths** - business logic, edge cases
3. **Don't test trivial code** - getters, setters, constants
4. **Track coverage trends** - watch for decreases
5. **Use branch coverage** - catches more bugs than line coverage

---

## CI/CD Integration with GitHub Actions

### Basic Test Workflow

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml tests/

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

### Complete CI/CD Pipeline

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  # Job 1: Linting
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install linters
      run: |
        pip install flake8 black isort mypy

    - name: Run flake8
      run: flake8 src tests

    - name: Check formatting with black
      run: black --check src tests

    - name: Check imports with isort
      run: isort --check-only src tests

    - name: Run mypy
      run: mypy src

  # Job 2: Unit Tests
  test:
    runs-on: ubuntu-latest
    needs: lint  # Run after lint passes

    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Cache pip dependencies
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-xdist

    - name: Run tests in parallel
      run: |
        pytest -n auto --cov=src --cov-report=xml --cov-report=term-missing tests/

    - name: Upload coverage reports
      uses: codecov/codecov-action@v4
      with:
        token: ${{ secrets.CODECOV_TOKEN }}
        files: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

  # Job 3: Integration Tests
  integration-test:
    runs-on: ubuntu-latest
    needs: test

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Run integration tests
      run: pytest tests/integration/ -v
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db

  # Job 4: Security Scan
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Run Bandit security scan
      uses: jpetrucciani/bandit-check@master
      with:
        path: 'src'

  # Job 5: Build & Deploy (only on main)
  deploy:
    runs-on: ubuntu-latest
    needs: [test, integration-test, security]
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v4

    - name: Build
      run: echo "Building application..."

    - name: Deploy
      run: echo "Deploying application..."
```

### Other CI/CD Platforms

#### GitLab CI (`.gitlab-ci.yml`)

```yaml
stages:
  - test
  - deploy

test:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
    - pytest --cov=src --cov-report=xml tests/
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

#### CircleCI (`.circleci/config.yml`)

```yaml
version: 2.1

jobs:
  test:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - run:
          name: Install dependencies
          command: pip install -r requirements.txt && pip install pytest pytest-cov
      - run:
          name: Run tests
          command: pytest --cov=src tests/
      - store_test_results:
          path: test-results

workflows:
  main:
    jobs:
      - test
```

#### Jenkins (`Jenkinsfile`)

```groovy
pipeline {
    agent any

    stages {
        stage('Install') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install pytest pytest-cov'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest --cov=src --cov-report=xml tests/'
            }
            post {
                always {
                    publishCoverage adapters: [coberturaAdapter('coverage.xml')]
                }
            }
        }
    }
}
```

---

## Popular Open Source Repos with Great Test Suites

These projects demonstrate excellent testing practices. Study their test structure, patterns, and CI configurations:

### 1. **requests** (Python HTTP Library)
- **Repository**: https://github.com/psf/requests
- **Tests**: https://github.com/psf/requests/tree/main/tests
- **Why it's great**: Clean, readable tests; good use of fixtures; extensive mocking
- **CI**: GitHub Actions with multiple Python versions

```bash
# Clone and run tests
git clone https://github.com/psf/requests.git
cd requests
pip install -e ".[socks]"
pip install pytest pytest-httpbin pytest-cov
pytest tests/
```

### 2. **Flask** (Web Framework)
- **Repository**: https://github.com/pallets/flask
- **Tests**: https://github.com/pallets/flask/tree/main/tests
- **Why it's great**: Comprehensive test coverage; testing web apps; fixtures
- **CI**: GitHub Actions with tox

```bash
git clone https://github.com/pallets/flask.git
cd flask
pip install -e ".[dev]"
pytest tests/
```

### 3. **httpx** (Async HTTP Client)
- **Repository**: https://github.com/encode/httpx
- **Tests**: https://github.com/encode/httpx/tree/master/tests
- **Why it's great**: Tests for async code; excellent organization

```bash
git clone https://github.com/encode/httpx.git
cd httpx
pip install -e ".[cli,http2,brotli]"
pip install pytest pytest-asyncio
pytest tests/
```

### 4. **pydantic** (Data Validation)
- **Repository**: https://github.com/pydantic/pydantic
- **Tests**: https://github.com/pydantic/pydantic/tree/main/tests
- **Why it's great**: Extensive parametrized tests; type checking tests

### 5. **Django** (Web Framework)
- **Repository**: https://github.com/django/django
- **Tests**: https://github.com/django/django/tree/main/tests
- **Why it's great**: One of the most comprehensive test suites; great docs

### 6. **fastapi** (Modern Web Framework)
- **Repository**: https://github.com/tiangolo/fastapi
- **Tests**: https://github.com/tiangolo/fastapi/tree/master/tests
- **Why it's great**: Testing async endpoints; OpenAPI testing

### 7. **pytest** (Testing Framework Itself!)
- **Repository**: https://github.com/pytest-dev/pytest
- **Tests**: https://github.com/pytest-dev/pytest/tree/main/testing
- **Why it's great**: Meta! See how the testing framework tests itself

### How to Study These Repos

1. **Look at test file structure** - How are tests organized?
2. **Study fixtures** - How is setup/teardown handled?
3. **Check conftest.py** - What shared fixtures exist?
4. **Read CI configuration** - How are tests automated?
5. **Look at parametrized tests** - How are edge cases covered?
6. **Check coverage reports** - What coverage % do they target?

---

## Platforms to Practice TDD and Unit Testing

### Dedicated Testing Practice

#### 5. **Cyber-Dojo**
- **URL**: https://cyber-dojo.org/
- **What it offers**:
  - Pure TDD practice environment
  - 200+ exercises
  - Traffic light (red/green/refactor) visual feedback
  - Pair programming support
- **Best for**: Pure TDD kata practice
- **Free**: Yes

#### 6. **Kata-Log**
- **URL**: https://kata-log.rocks/
- **What it offers**:
  - Collection of coding katas for TDD practice
  - Various difficulty levels
  - Language-agnostic problems
- **Best for**: Finding TDD exercises to practice

### Project-Based Learning

#### 7. **Real Python**
- **URL**: https://realpython.com/
- **Relevant tutorials**:
  - [Getting Started With Testing in Python](https://realpython.com/python-testing/)
  - [Pytest Tutorial](https://realpython.com/pytest-python-testing/)
  - [Mocking in Python](https://realpython.com/python-mock-library/)

#### 8. **Test-Driven Development with Python (Book)**
- **URL**: https://www.obeythetestinggoat.com/
- **What it offers**:
  - Free online book
  - Build a web app using TDD from scratch
  - Django + Selenium testing
- **Best for**: Complete TDD project walkthrough

---

## Quick Reference: Commands Cheat Sheet

```bash
# Run tests
pytest                              # All tests
pytest tests/test_file.py           # Specific file
pytest -k "test_name"               # Match test name
pytest -v                           # Verbose output
pytest -x                           # Stop on first failure
pytest --pdb                        # Debug on failure

# Coverage
pytest --cov=src                    # Basic coverage
pytest --cov=src --cov-report=html  # HTML report
pytest --cov=src --cov-fail-under=80 # Fail if < 80%

# Parallel testing
pip install pytest-xdist
pytest -n auto                      # Auto-detect CPU cores
pytest -n 4                         # Use 4 workers

# Watch mode
pip install pytest-watch
ptw                                 # Re-run tests on file change

# Markers
pytest -m "slow"                    # Run only @pytest.mark.slow
pytest -m "not slow"                # Skip slow tests

# Generate JUnit XML (for CI)
pytest --junitxml=results.xml
```

---

## Summary

1. **Code Coverage**: Use `pytest-cov` to measure and track test coverage
2. **CI/CD**: Automate tests with GitHub Actions (or GitLab CI, CircleCI, Jenkins)
3. **Learn from Open Source**: Study requests, Flask, FastAPI test suites

---

*"The best time to write tests was before writing the code. The second best time is now."*
