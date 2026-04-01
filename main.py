"""CLI demo script for PawPal+ - exercises the backend classes end-to-end."""

from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(schedule, title="Schedule"):
    print(f"\n--- {title} ---")
    if not schedule:
        print("  (no tasks)")
        return
    for pet, task in schedule:
        status = "DONE" if task.completed else "    "
        print(
            f"  [{status}] {task.time}  {pet.name:<10} {task.description:<25} "
            f"({task.duration_minutes} min, {task.priority}, {task.frequency})"
        )


def main():
    # Set up owner and pets
    owner = Owner("Jordan")

    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    today = date.today()

    # Add tasks out of order to demonstrate sorting
    mochi.add_task(Task("Evening walk", "18:00", 30, "daily", "high", due_date=today))
    mochi.add_task(Task("Morning walk", "07:30", 20, "daily", "high", due_date=today))
    mochi.add_task(Task("Heartworm pill", "08:00", 5, "once", "high", due_date=today))
    mochi.add_task(Task("Enrichment puzzle", "15:00", 15, "weekly", "low", due_date=today))

    luna.add_task(Task("Breakfast feeding", "07:00", 5, "daily", "high", due_date=today))
    luna.add_task(Task("Dinner feeding", "18:30", 5, "daily", "medium", due_date=today))
    luna.add_task(Task("Grooming", "10:00", 20, "weekly", "low", due_date=today))

    scheduler = Scheduler(owner)

    # Today's full schedule sorted by time
    print_schedule(scheduler.get_todays_schedule(), "Today's Schedule (sorted)")

    # Filter by pet
    print_schedule(scheduler.filter_by_pet("Mochi"), "Mochi's Tasks")

    # Mark a task complete and show recurrence
    _, heartworm = scheduler.filter_by_pet("Mochi")[0]  # first task after sort
    todays_mochi = scheduler.filter_by_pet("Mochi")
    # find the heartworm pill specifically
    for pet, task in todays_mochi:
        if task.description == "Heartworm pill":
            print(f"\nMarking '{task.description}' complete...")
            next_t = scheduler.mark_task_complete(pet, task)
            if next_t:
                print(f"  Next occurrence scheduled for {next_t.due_date} (frequency: {next_t.frequency})")
            else:
                print("  One-time task, no recurrence scheduled.")
            break

    # Show pending vs. done
    print_schedule(scheduler.filter_by_status(False), "Pending Tasks")
    print_schedule(scheduler.filter_by_status(True), "Completed Tasks")

    # Conflict detection demo
    mochi.add_task(Task("Vet call", "07:30", 10, "once", "high", due_date=today))
    conflicts = scheduler.detect_conflicts()
    print("\n--- Conflict Check ---")
    if conflicts:
        for warning in conflicts:
            print(f"  WARNING: {warning}")
    else:
        print("  No conflicts found.")


if __name__ == "__main__":
    main()
