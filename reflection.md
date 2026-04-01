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

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
