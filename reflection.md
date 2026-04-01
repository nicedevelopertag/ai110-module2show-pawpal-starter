# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core actions a user needs to perform: (1) add a pet with basic info, (2) schedule a care task
for a specific pet at a given time, and (3) view today's plan sorted chronologically.

To support these, I designed four classes:

- **Task** (dataclass) - holds a single activity: description, scheduled time (HH:MM), duration,
  frequency (once/daily/weekly), priority, completion flag, and due date. Responsible for knowing
  when it recurs.
- **Pet** (dataclass) - stores name, species, and an owned list of Tasks. Responsible for managing
  its own task collection.
- **Owner** - holds a list of Pets and provides a flat view of all tasks across every pet.
- **Scheduler** - the "brain"; takes an Owner and provides sorted schedules, filters, conflict
  detection, and recurring-task promotion.

The UML relationship chain is: `Owner 1--* Pet 1--* Task`, and `Scheduler --> Owner`.

**b. Design changes**

During implementation I moved `next_occurrence()` onto the `Task` class itself rather than keeping
it entirely in `Scheduler`. Initially I placed the recurrence logic in `Scheduler.mark_task_complete`,
but that caused the Task to have no self-knowledge about its own cadence. Moving the method to
`Task` respected the principle that each class should own its own behavior, and it made the
`Scheduler` method a thin coordinator rather than a big logic block.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers: scheduled time (HH:MM), due date, and priority level (low/medium/high).
Sorting is done by time so the owner sees tasks in the order they need to act on them. Priority is
surfaced in the UI so the owner can make manual judgment calls about what to skip if time is short.
Time was treated as the primary constraint because pet care is largely time-anchored (a dog needs
its morning walk before work, not "sometime today").

**b. Tradeoffs**

Conflict detection only flags exact time matches for the same pet on the same date. It does not
check for overlapping durations (e.g., a 30-minute walk starting at 07:30 and a 10-minute task
starting at 07:45 technically overlap but won't trigger a warning). This is a reasonable tradeoff
for a personal pet-care app because most tasks are short and the owner can eyeball duration
overlap - adding full interval overlap logic would significantly complicate the detection algorithm
with little practical payoff in this use case.

---

## 3. AI Collaboration

**a. How you used AI**

AI was used at three distinct stages:

1. **Design** - asked for a Mermaid.js class diagram from a natural-language description of the four
   classes. The output gave a useful starting structure, though I trimmed several attributes it added
   (like `email` on Owner) that weren't needed for this scope.
2. **Implementation** - used inline chat to generate method bodies for `next_occurrence()` and the
   `detect_conflicts()` dictionary approach. The prompts "How should Scheduler retrieve all tasks
   from Owner's pets?" and "Give me a lightweight conflict detection strategy that returns warnings
   instead of raising exceptions" were the most targeted and returned usable code on the first try.
3. **Testing** - asked for a test plan given the codebase, then refined the generated test functions
   to use fixtures and cover edge cases (weekly recurrence, no-conflict baseline) that the first
   draft skipped.

**b. Judgment and verification**

The AI initially placed all recurrence logic inside `Scheduler.mark_task_complete`, making `Task`
a passive data container. I rejected this because it violated the principle that an object should
own its own behavior - a `Task` is the natural home for "what comes next after me?". I moved the
logic into `Task.next_occurrence()` and reduced `mark_task_complete` to a thin coordinator. I
verified the change by running the full test suite and checking that the recurrence tests still
passed with the new structure.

---

## 4. Testing and Verification

**a. What you tested**

The nine tests in `tests/test_pawpal.py` cover:

1. `mark_complete()` flips `Task.completed` from False to True - confirms the state mutation works
2. `add_task()` increments the pet's task list length - guards against silent failures on append
3. `sort_by_time` returns tasks in HH:MM ascending order - verifies the lambda key handles strings
4. Daily `next_occurrence()` lands exactly one day ahead - core recurrence contract
5. Weekly `next_occurrence()` lands exactly seven days ahead - same for weekly cadence
6. One-time task `next_occurrence()` returns None - ensures no phantom tasks are created
7. `mark_task_complete` adds the next occurrence to the pet's task list - integration test for recurrence
8. Duplicate `(pet, time, date)` triggers a conflict warning - validates the detection algorithm
9. Different task times produce no warnings - verifies no false positives

These are the behaviors most likely to break during a refactor, so having them automated saves time
and catches regressions immediately.

**b. Confidence**

**4 out of 5 stars.** All 9 tests pass and cover the main happy paths and key edge cases. The main
gap is overlapping-duration detection: two tasks that start at different times but overlap when
duration is factored in are not currently flagged. I would also add a test for a pet with zero tasks
to ensure `get_todays_schedule()` returns an empty list rather than raising an exception.

---

## 5. Reflection

**a. What went well**

The clean separation between the logic layer (`pawpal_system.py`) and the UI (`app.py`) worked well.
Because the backend was tested independently through `main.py` before touching Streamlit, the UI
integration phase had zero backend bugs to debug - every issue was a Streamlit-specific one (mostly
`st.session_state` rerun behavior). The "CLI-first" workflow paid off.

**b. What you would improve**

The recurring task model appends the next occurrence to the same flat task list, which means after
several weeks of daily tasks the list grows unbounded. In a second iteration I would add a
`completed_tasks` archive list to `Pet` so the active task list only shows upcoming work, and the
history is still queryable.

**c. Key takeaway**

The most valuable skill was knowing when to accept AI output and when to override it. The AI
consistently produced working code but sometimes traded design cleanliness for brevity (e.g., lumping
all logic in one class). Acting as the "lead architect" meant holding the design principles (single
responsibility, objects own their behavior) and using AI as a fast code-generator rather than a
decision-maker. The human's job is to stay in charge of the design; the AI's job is to fill in the
implementation details quickly.
