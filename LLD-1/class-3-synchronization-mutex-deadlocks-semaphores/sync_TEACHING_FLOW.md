# Teaching Flow: Synchronization Class

## Class Structure (90-100 minutes)

### Part 1: Revision & Setup (10 minutes)

**Files:** 
- `sync_00_revision.py`
- `sync_README_TODAYS_CLASS.md`

**What to do:**
1. Run `sync_00_revision.py`
2. Quick Q&A: "What is GIL?", "ThreadPool vs ProcessPool?"
3. Set up the BIG QUESTION: "If GIL locks threads, why need Mutex?"

**Key Point:** Build intrigue around GIL vs Mutex difference

---

### Part 2: THE BIG REVEAL - GIL vs Mutex (15 minutes)

**Files:**
- `sync_README_TODAYS_CLASS.md` (GIL vs Mutex section)
- `sync_01_race_condition_problem.py`

**Teaching Steps:**
1. **Ask first:** "If only 1 thread executes at a time (GIL), why do we need locks?"
2. **Explain:** GIL locks interpreter, NOT data
3. **Show on iPad:** The bytecode breakdown (count += 1 is 3 steps)
4. **Run:** `sync_01_race_condition_problem.py`
5. **Point out:** Small iterations OK, large iterations FAIL
6. **Explain:** Context switch happens between bytecode operations!

**Key Phrases:**
- "GIL = Lock on WHO can execute"
- "Mutex = Lock on WHAT can be accessed"
- "count += 1 is NOT atomic!"

---

### Part 3: Solution - Mutex Locks (15 minutes)

**Files:**
- `sync_02_mutex_solution.py`

**Teaching Steps:**
1. **Introduce:** `threading.Lock()`
2. **Explain:** Only one thread can hold lock at a time
3. **Show syntax:** `lock.acquire()` and `lock.release()`
4. **Run:** `sync_02_mutex_solution.py`
5. **Compare:** With vs without lock results
6. **Emphasize:** Critical section must be protected

**Live Coding (Optional):**
- Modify iterations, show it always works with lock
- Remove lock, show it breaks

**Key Concepts:**
- Critical section
- Mutual exclusion
- acquire() blocks if lock is held

---

### Part 4: Context Managers (10 minutes)

**Files:**
- `sync_03_context_manager.py`

**Teaching Steps:**
1. **Problem:** What if exception before release()?
2. **Solution:** Context managers (`with lock:`)
3. **Run:** `sync_03_context_manager.py`
4. **Compare:** Manual vs context manager
5. **Emphasize:** ALWAYS use `with lock:`

**Key Points:**
- Automatic release (even on error)
- Cleaner code
- Pythonic way
- "Never use acquire/release directly!"

---

### Part 5: Deadlocks (15 minutes)

**Files:**
- `sync_04_deadlock.py`

**Teaching Steps:**
1. **Setup scenario:** "What if we need 2 locks?"
2. **Predict:** "What could go wrong?"
3. **Run:** `sync_04_deadlock.py` (will timeout showing deadlock)
4. **Explain:** Circular wait condition
5. **Show solution:** Same lock order
6. **Run:** No deadlock example

**Visual on iPad:**
```
Thread A: Has Lock1 → Wants Lock2
Thread B: Has Lock2 → Wants Lock1
Result: Both stuck forever!
```

**Prevention Strategies:**
1. Lock ordering (always same order)
2. Timeout on acquire
3. Avoid nested locks
4. Use single lock

**Key Phrase:** "Lock order matters!"

---

### Part 6: Semaphores (15 minutes)

**Files:**
- `sync_05_semaphore.py`

**Teaching Steps:**
1. **Question:** "What if we want 3 threads, not just 1?"
2. **Introduce:** `Semaphore(N)`
3. **Run:** Compare Lock vs Semaphore
4. **Real example:** Database connection pool
5. **Explain:** Real-world use cases

**Key Concepts:**
- Lock = Semaphore(1)
- Semaphore = Limited access
- Use cases: connection pools, rate limiting

---

### Part 7: Summary & Q&A (15-20 minutes)

**What to cover:**
1. **Recap:** GIL vs Mutex difference
2. **Review:** Lock → Context Manager → Deadlock → Semaphore
3. **Practice scenarios:** 
   - "Thread-safe counter?" → Lock
   - "Max 5 API calls?" → Semaphore(5)
   - "Two locks needed?" → Watch lock order!
4. **Open Q&A**

**Quick Reference Sheet (Show on iPad):**
```
Problem              Solution
─────────────────    ─────────────────
Shared data          Lock
Multiple data        Single lock or lock ordering
Limited resource     Semaphore(N)
Forgotten release    Context manager (with)
```

---

## Key Teaching Techniques

### Start with Intrigue
- "If GIL locks threads, why do we need more locks?"
- This hooks students into understanding the difference

### Show, Don't Just Tell
- Run the broken code first (race condition)
- Then run the fixed code (with lock)
- Visual impact > verbal explanation

### Use Real Examples
- Adder/Subtractor (simple, relatable)
- Database connections (real-world)
- Avoid abstract examples

### Emphasize Common Mistakes
- Forgetting to release lock
- Wrong lock order (deadlock)
- Using acquire/release instead of `with`

### Ask Predictive Questions
- "What will the final count be?"
- "Will this deadlock?"
- "How many threads can run simultaneously?"

---

## Important Points to Stress

### Critical Understanding
1. **GIL ≠ Mutex**
   - GIL locks interpreter
   - Mutex locks data
   - Need both for thread safety

2. **Atomicity**
   - `count += 1` is NOT atomic
   - It's 3 bytecode operations
   - Context switch can happen between them

3. **Context Managers**
   - ALWAYS use `with lock:`
   - Never manual acquire/release
   - This is the professional way

4. **Deadlock Prevention**
   - Lock order consistency
   - Avoid nested locks when possible
   - Use timeout for safety

5. **Lock vs Semaphore**
   - Lock = exclusive access (1 thread)
   - Semaphore = limited access (N threads)
   - Choose based on use case

---

## Expected Questions & Answers

**Q: Why doesn't GIL prevent race conditions?**
A: GIL locks interpreter, not data. Context switch happens between bytecode operations.

**Q: When do I use Lock vs Semaphore?**
A: Lock for exclusive access (shared variable). Semaphore for limited resources (connection pool).

**Q: Can I nest locks?**
A: Yes, but be careful of lock order! Always acquire in same order.

**Q: What if I forget to release lock?**
A: Use context manager (`with lock:`). It auto-releases even on errors.

**Q: Does ProcessPool need locks?**
A: No! Processes have separate memory. Threads share memory, need locks.

---

## Timing Breakdown

| Section | Time | Activity |
|---------|------|----------|
| Revision | 10 min | Quick recap + set up question |
| GIL vs Mutex | 15 min | THE reveal + race condition |
| Mutex Solution | 15 min | Lock basics + demo |
| Context Manager | 10 min | Better syntax |
| Deadlocks | 15 min | Problem + prevention |
| Semaphores | 15 min | Limited access |
| Summary/Q&A | 20 min | Recap + questions |
| **Total** | **100 min** | |

---

## Success Metrics

Students should be able to:
- [ ] Explain difference between GIL and Mutex
- [ ] Identify when locks are needed
- [ ] Write code with context managers
- [ ] Recognize potential deadlocks
- [ ] Choose between Lock and Semaphore
- [ ] Understand why count += 1 isn't atomic

---

## Materials Checklist

**iPad:**
- [ ] sync_README_TODAYS_CLASS.md (main concepts)
- [ ] Visual diagrams (GIL vs Mutex section)
- [ ] Quick reference for Q&A

**PyCharm:**
- [ ] sync_00_revision.py
- [ ] sync_01_race_condition_problem.py
- [ ] sync_02_mutex_solution.py
- [ ] sync_03_context_manager.py
- [ ] sync_04_deadlock.py
- [ ] sync_05_semaphore.py

**All files tested and ready to run!**

---

## Teaching Tips

1. **The Hook:** Start with the paradox (GIL exists, why need locks?)
2. **Show Failure First:** Run broken code, let them see the problem
3. **Build Understanding:** Explain bytecode operations visually
4. **Show Solution:** Run fixed code, immediate satisfaction
5. **Warn About Pitfalls:** Deadlocks, forgotten releases
6. **Real Examples:** Database pools, not abstract scenarios
7. **Repeat Key Phrases:** "GIL locks interpreter, Mutex locks data"
8. **End with Confidence:** They now understand something subtle!

Good luck! 🚀
