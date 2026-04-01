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
        pass

    def next_occurrence(self) -> Optional["Task"]:
        """Return a new Task for the next scheduled occurrence, or None if one-time."""
        pass


@dataclass
class Pet:
    """Represents a pet with a list of care tasks."""

    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        pass


class Owner:
    """Manages a collection of pets."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's roster."""
        pass

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's roster."""
        pass

    def get_all_tasks(self) -> List[Tuple[Pet, Task]]:
        """Return all tasks across all pets as (Pet, Task) tuples."""
        pass


class Scheduler:
    """Retrieves, organizes, and manages tasks across all pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def get_todays_schedule(self) -> List[Tuple[Pet, Task]]:
        """Return all tasks due today, sorted chronologically."""
        pass

    def sort_by_time(self, tasks: List[Tuple[Pet, Task]]) -> List[Tuple[Pet, Task]]:
        """Sort (Pet, Task) pairs by task time in HH:MM format."""
        pass

    def filter_by_pet(self, pet_name: str) -> List[Tuple[Pet, Task]]:
        """Return all tasks belonging to a pet with the given name."""
        pass

    def filter_by_status(self, completed: bool) -> List[Tuple[Pet, Task]]:
        """Return tasks filtered by completion status."""
        pass

    def detect_conflicts(self) -> List[str]:
        """Detect tasks scheduled at the same time for the same pet. Returns warning strings."""
        pass

    def mark_task_complete(self, pet: Pet, task: Task) -> Optional[Task]:
        """Mark a task complete and schedule the next occurrence if recurring."""
        pass
