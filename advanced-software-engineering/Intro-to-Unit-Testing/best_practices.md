# Unit Testing Best Practices

## Why Best Practices Matter

```
┌─────────────────────────────────────────────────────────────┐
│              WITHOUT BEST PRACTICES                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ❌ Tests are slow → Developers skip running them           │
│  ❌ Tests are flaky → "It fails randomly, ignore it"        │
│  ❌ Tests are unclear → Can't understand what broke         │
│  ❌ Tests are coupled → Change one thing, 50 tests fail     │
│                                                             │
│  Result: Tests become BURDEN, not BENEFIT                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                WITH BEST PRACTICES                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ Tests are fast → Run on every save                      │
│  ✅ Tests are reliable → Trust the results                  │
│  ✅ Tests are clear → Instant understanding of failures     │
│  ✅ Tests are isolated → Change safely                      │
│                                                             │
│  Result: Tests become SAFETY NET                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Practice 1: One Assertion Per Behavior

### The Problem
```
┌─────────────────────────────────────────────────────────────┐
│  MULTIPLE ASSERTIONS IN ONE TEST                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  def test_calculator():                                     │
│      self.assertEqual(add(2, 3), 5)      # ✅ Pass          │
│      self.assertEqual(add(0, 0), 0)      # ❌ FAIL          │
│      self.assertEqual(add(-1, 1), 0)     # ??? Never runs   │
│      self.assertEqual(multiply(2, 3), 6) # ??? Never runs   │
│                                                             │
│  Problem: Test stops at first failure                       │
│  You don't know if other cases work!                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### The Solution
```
┌─────────────────────────────────────────────────────────────┐
│  SEPARATE TESTS FOR EACH BEHAVIOR                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  def test_add_positive_numbers():                           │
│      self.assertEqual(add(2, 3), 5)      # ✅ Pass          │
│                                                             │
│  def test_add_zeros():                                      │
│      self.assertEqual(add(0, 0), 0)      # ❌ FAIL          │
│                                                             │
│  def test_add_negative_and_positive():                      │
│      self.assertEqual(add(-1, 1), 0)     # ✅ Pass          │
│                                                             │
│  def test_multiply_positive_numbers():                      │
│      self.assertEqual(multiply(2, 3), 6) # ✅ Pass          │
│                                                             │
│  Benefit: Each test runs independently                      │
│  You see EXACTLY what's broken!                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Practice 2: Descriptive Test Names

### Naming Convention
```
test_<function>_<scenario>_<expected_result>
```

### Examples
```
┌─────────────────────────────────────────────────────────────┐
│                    TEST NAMING                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ❌ BAD NAMES (What do these test??)                        │
│  ├── test_add()                                             │
│  ├── test_1()                                               │
│  ├── test_calculator()                                      │
│  └── test_it_works()                                        │
│                                                             │
│  ✅ GOOD NAMES (Self-documenting!)                          │
│  ├── test_add_positive_numbers_returns_sum()                │
│  ├── test_add_negative_numbers_returns_correct_sum()        │
│  ├── test_divide_by_zero_raises_value_error()               │
│  └── test_multiply_with_zero_returns_zero()                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Why It Matters
```
Test failure output:

❌ BAD:  FAILED test_add
   (What scenario failed? No clue!)

✅ GOOD: FAILED test_add_negative_numbers_returns_correct_sum
   (Immediately know: negative number handling is broken)
```

---

## Practice 3: Tests Must Be Fast

```
┌─────────────────────────────────────────────────────────────┐
│                    TEST SPEED                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SLOW TESTS                     FAST TESTS                  │
│  ┌─────────────────┐            ┌─────────────────┐         │
│  │ time.sleep(1)   │            │ Pure functions  │         │
│  │ Database calls  │            │ No I/O          │         │
│  │ Network calls   │            │ No sleep        │         │
│  │ File I/O        │            │ Mocked deps     │         │
│  └─────────────────┘            └─────────────────┘         │
│         │                              │                    │
│         ▼                              ▼                    │
│  "I'll run tests                "I run tests               │
│   before lunch"                  every save"                │
│                                                             │
│  100 tests × 1 sec = 100 sec    100 tests × 1ms = 0.1 sec   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Rule of Thumb
- Unit tests should run in **milliseconds**
- Your entire test suite should run in **seconds**
- If tests are slow, developers won't run them

---

## Practice 4: Test Behavior, Not Implementation

```
┌─────────────────────────────────────────────────────────────┐
│           TESTING IMPLEMENTATION (BAD)                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  class Calculator:                                          │
│      def __init__(self):                                    │
│          self._cache = {}        # Internal detail          │
│                                                             │
│      def add(self, a, b):                                   │
│          key = (a, b)                                       │
│          if key not in self._cache:                         │
│              self._cache[key] = a + b                       │
│          return self._cache[key]                            │
│                                                             │
│  # BAD TEST - tests internal cache                          │
│  def test_add_uses_cache():                                 │
│      calc = Calculator()                                    │
│      calc.add(2, 3)                                         │
│      assert (2, 3) in calc._cache    # ❌ Testing internals │
│                                                             │
│  Problem: If you change caching strategy, test breaks       │
│  even though behavior is still correct!                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│             TESTING BEHAVIOR (GOOD)                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  # GOOD TEST - tests input → output                         │
│  def test_add_returns_correct_sum():                        │
│      calc = Calculator()                                    │
│      result = calc.add(2, 3)                                │
│      assert result == 5          # ✅ Testing behavior      │
│                                                             │
│  Benefit: Implementation can change freely                  │
│  Test only cares: does add(2,3) return 5?                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Practice 5: Test Edge Cases

```
┌─────────────────────────────────────────────────────────────┐
│                   EDGE CASES TO TEST                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  For NUMBERS:                                               │
│  ├── Zero                                                   │
│  ├── Negative numbers                                       │
│  ├── Very large numbers                                     │
│  └── Floating point precision                               │
│                                                             │
│  For STRINGS:                                               │
│  ├── Empty string ""                                        │
│  ├── Single character                                       │
│  ├── Very long strings                                      │
│  └── Special characters                                     │
│                                                             │
│  For LISTS/COLLECTIONS:                                     │
│  ├── Empty list []                                          │
│  ├── Single element                                         │
│  ├── Duplicates                                             │
│  └── Very large collections                                 │
│                                                             │
│  For ANY FUNCTION:                                          │
│  ├── Boundary values                                        │
│  ├── Invalid inputs                                         │
│  └── Error conditions                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Practice 6: Isolate Tests (No Shared State)

```
┌─────────────────────────────────────────────────────────────┐
│              SHARED STATE PROBLEM                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  counter = 0                    # Global state!             │
│                                                             │
│  def test_increment():                                      │
│      global counter                                         │
│      counter += 1                                           │
│      assert counter == 1        # ✅ Pass (runs first)      │
│                                                             │
│  def test_increment_again():                                │
│      global counter                                         │
│      counter += 1                                           │
│      assert counter == 1        # ❌ FAIL! counter is 2     │
│                                                             │
│  Problem: Test order matters!                               │
│  Tests are not independent.                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                ISOLATED TESTS                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  class TestCounter(unittest.TestCase):                      │
│                                                             │
│      def setUp(self):           # Runs before EACH test     │
│          self.counter = 0       # Fresh state every time    │
│                                                             │
│      def test_increment(self):                              │
│          self.counter += 1                                  │
│          assert self.counter == 1   # ✅ Always pass        │
│                                                             │
│      def test_increment_again(self):                        │
│          self.counter += 1                                  │
│          assert self.counter == 1   # ✅ Always pass        │
│                                                             │
│  Each test gets fresh state!                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes to Avoid

```
┌─────────────────────────────────────────────────────────────┐
│                 COMMON MISTAKES                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Writing tests AFTER bugs reach production               │
│     → Write tests BEFORE or WHILE writing code              │
│                                                             │
│  2. Testing everything in one giant test                    │
│     → One test = One behavior                               │
│                                                             │
│  3. Skipping edge cases                                     │
│     → Bugs hide in edges (zero, empty, null)                │
│                                                             │
│  4. Depending on real APIs / databases                      │
│     → Use mocks (covered in advanced topics)                │
│                                                             │
│  5. Not running tests frequently                            │
│     → Run after every change                                │
│                                                             │
│  6. Ignoring failing tests                                  │
│     → Fix immediately or delete                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Reference Checklist

Before pushing code, ask:

- [ ] Does each test have a descriptive name?
- [ ] Does each test follow AAA pattern?
- [ ] Is each test independent (no shared state)?
- [ ] Are edge cases covered?
- [ ] Do tests run fast (no sleep/network/db)?
- [ ] Am I testing behavior, not implementation?

---

## Summary

| Practice | Why |
|----------|-----|
| One assertion per behavior | Know exactly what broke |
| Descriptive names | Self-documenting tests |
| Fast tests | Developers will run them |
| Test behavior | Refactor without breaking tests |
| Test edge cases | Bugs hide at boundaries |
| Isolate tests | Reliable, order-independent |


> [!WARNING]
> **Goodhart's Law**
>
> "When a measure becomes a target, it ceases to be a good measure."
>
> Code coverage can be gamed—tests that execute every line without meaningful assertions still achieve 100% coverage. True test quality comes from testing behavior, edge cases, and failure modes, not just hitting line counts.