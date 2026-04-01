"""Automated tests for PawPal+ core behavior."""

from datetime import date, timedelta
import pytest

from pawpal_system import Owner, Pet, Task, Scheduler


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def owner_with_pets():
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)
    return owner, mochi, luna


# ---------------------------------------------------------------------------
# Task tests
# ---------------------------------------------------------------------------

def test_mark_complete_changes_status():
    """mark_complete() should flip completed from False to True."""
    task = Task("Morning walk", "07:30", 20, "daily")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    """add_task() should grow the pet's task list by one."""
    pet = Pet("Mochi", "dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Morning walk", "07:30", 20, "daily"))
    assert len(pet.tasks) == 1
    pet.add_task(Task("Evening walk", "18:00", 30, "daily"))
    assert len(pet.tasks) == 2


# ---------------------------------------------------------------------------
# Sorting tests
# ---------------------------------------------------------------------------

def test_sort_by_time_orders_tasks_chronologically(owner_with_pets):
    """sort_by_time should return tasks in HH:MM ascending order."""
    owner, mochi, _ = owner_with_pets
    today = date.today()
    mochi.add_task(Task("Evening walk", "18:00", 30, "daily", due_date=today))
    mochi.add_task(Task("Morning walk", "07:30", 20, "daily", due_date=today))
    mochi.add_task(Task("Lunchtime treat", "12:00", 5, "daily", due_date=today))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(scheduler.filter_by_pet("Mochi"))
    times = [task.time for _, task in sorted_tasks]
    assert times == sorted(times)


# ---------------------------------------------------------------------------
# Recurrence tests
# ---------------------------------------------------------------------------

def test_daily_task_next_occurrence_is_tomorrow():
    """next_occurrence for a daily task should land on due_date + 1 day."""
    today = date.today()
    task = Task("Morning walk", "07:30", 20, "daily", due_date=today)
    next_t = task.next_occurrence()
    assert next_t is not None
    assert next_t.due_date == today + timedelta(days=1)
    assert next_t.completed is False


def test_weekly_task_next_occurrence_is_seven_days():
    """next_occurrence for a weekly task should land on due_date + 7 days."""
    today = date.today()
    task = Task("Grooming", "10:00", 20, "weekly", due_date=today)
    next_t = task.next_occurrence()
    assert next_t is not None
    assert next_t.due_date == today + timedelta(weeks=1)


def test_once_task_has_no_next_occurrence():
    """next_occurrence for a one-time task should return None."""
    task = Task("Vet visit", "09:00", 60, "once")
    assert task.next_occurrence() is None


def test_mark_task_complete_creates_recurrence_for_daily(owner_with_pets):
    """Scheduler.mark_task_complete should add the next-day task to the pet."""
    owner, mochi, _ = owner_with_pets
    today = date.today()
    task = Task("Morning walk", "07:30", 20, "daily", due_date=today)
    mochi.add_task(task)

    scheduler = Scheduler(owner)
    next_t = scheduler.mark_task_complete(mochi, task)

    assert task.completed is True
    assert next_t is not None
    assert next_t.due_date == today + timedelta(days=1)
    assert next_t in mochi.tasks


# ---------------------------------------------------------------------------
# Conflict detection tests
# ---------------------------------------------------------------------------

def test_conflict_detection_flags_same_time_same_pet(owner_with_pets):
    """Two tasks for the same pet at the same time should produce a warning."""
    owner, mochi, _ = owner_with_pets
    today = date.today()
    mochi.add_task(Task("Morning walk", "07:30", 20, "daily", due_date=today))
    mochi.add_task(Task("Vet call", "07:30", 10, "once", due_date=today))

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()
    assert len(warnings) == 1
    assert "07:30" in warnings[0]
    assert "Mochi" in warnings[0]


def test_no_conflict_when_times_differ(owner_with_pets):
    """Tasks at different times should produce no conflict warnings."""
    owner, mochi, _ = owner_with_pets
    today = date.today()
    mochi.add_task(Task("Morning walk", "07:30", 20, "daily", due_date=today))
    mochi.add_task(Task("Evening walk", "18:00", 30, "daily", due_date=today))

    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []
