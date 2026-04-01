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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
