"""PawPal+ backend: Owner, Pet, Task, and Scheduler classes."""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional, Tuple


@dataclass
class Task:
    """Represents a single pet care activity."""

    description: str
    time: str  # "HH:MM" 24-hour format
    duration_minutes: int
    frequency: str  # "once", "daily", or "weekly"
    priority: str = "medium"  # "low", "medium", or "high"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Return a new Task for the next scheduled occurrence, or None if one-time."""
        if self.frequency == "daily":
            return Task(
                description=self.description,
                time=self.time,
                duration_minutes=self.duration_minutes,
                frequency=self.frequency,
                priority=self.priority,
                due_date=self.due_date + timedelta(days=1),
            )
        if self.frequency == "weekly":
            return Task(
                description=self.description,
                time=self.time,
                duration_minutes=self.duration_minutes,
                frequency=self.frequency,
                priority=self.priority,
                due_date=self.due_date + timedelta(weeks=1),
            )
        return None


@dataclass
class Pet:
    """Represents a pet with a list of care tasks."""

    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)


class Owner:
    """Manages a collection of pets."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's roster."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's roster."""
        self.pets.remove(pet)

    def get_all_tasks(self) -> List[Tuple[Pet, Task]]:
        """Return all tasks across all pets as (Pet, Task) tuples."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Retrieves, organizes, and manages tasks across all pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def get_todays_schedule(self) -> List[Tuple[Pet, Task]]:
        """Return all tasks due today, sorted chronologically."""
        today = date.today()
        todays = [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if task.due_date == today
        ]
        return self.sort_by_time(todays)

    def sort_by_time(self, tasks: List[Tuple[Pet, Task]]) -> List[Tuple[Pet, Task]]:
        """Sort (Pet, Task) pairs by task time in HH:MM format."""
        return sorted(tasks, key=lambda pt: pt[1].time)

    def filter_by_pet(self, pet_name: str) -> List[Tuple[Pet, Task]]:
        """Return all tasks belonging to a pet with the given name."""
        return [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if pet.name.lower() == pet_name.lower()
        ]

    def filter_by_status(self, completed: bool) -> List[Tuple[Pet, Task]]:
        """Return tasks filtered by completion status."""
        return [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if task.completed == completed
        ]

    def detect_conflicts(self) -> List[str]:
        """Detect tasks at the same time and date for the same pet. Returns warning strings."""
        seen: dict = {}
        warnings: List[str] = []
        for pet, task in self.owner.get_all_tasks():
            key = (pet.name, task.time, task.due_date)
            if key in seen:
                warnings.append(
                    f"Conflict: {pet.name} has two tasks at {task.time} on {task.due_date} "
                    f"('{seen[key]}' and '{task.description}')"
                )
            else:
                seen[key] = task.description
        return warnings

    def mark_task_complete(self, pet: Pet, task: Task) -> Optional[Task]:
        """Mark a task complete and schedule the next occurrence if recurring."""
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task:
            pet.add_task(next_task)
        return next_task
