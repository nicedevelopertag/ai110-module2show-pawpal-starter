"""PawPal+ Streamlit UI - connects to backend classes in pawpal_system.py."""

from datetime import date
import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A smart pet care scheduler for busy owners.")

# ---------------------------------------------------------------------------
# Session state - keeps Owner alive across Streamlit reruns
# ---------------------------------------------------------------------------

if "owner" not in st.session_state:
    st.session_state.owner = None

# ---------------------------------------------------------------------------
# Owner setup
# ---------------------------------------------------------------------------

st.header("Owner & Pets")

with st.form("owner_form"):
    owner_name = st.text_input("Your name", value="Jordan")
    submitted = st.form_submit_button("Set / update owner")
    if submitted:
        if st.session_state.owner is None:
            st.session_state.owner = Owner(owner_name)
        else:
            st.session_state.owner.name = owner_name
        st.success(f"Owner set to **{owner_name}**")

if st.session_state.owner is None:
    st.info("Enter your name above to get started.")
    st.stop()

owner: Owner = st.session_state.owner

# ---------------------------------------------------------------------------
# Add a pet
# ---------------------------------------------------------------------------

with st.expander("Add a pet", expanded=len(owner.pets) == 0):
    with st.form("add_pet_form"):
        pet_name = st.text_input("Pet name", value="Mochi")
        species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"])
        add_pet_btn = st.form_submit_button("Add pet")
        if add_pet_btn:
            existing = [p.name.lower() for p in owner.pets]
            if pet_name.lower() in existing:
                st.warning(f"A pet named {pet_name} already exists.")
            else:
                owner.add_pet(Pet(pet_name, species))
                st.success(f"Added {species} **{pet_name}**!")

if owner.pets:
    st.write(f"**{owner.name}'s pets:** " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")
    st.stop()

# ---------------------------------------------------------------------------
# Add a task
# ---------------------------------------------------------------------------

st.header("Schedule a Task")

pet_names = [p.name for p in owner.pets]

with st.form("add_task_form"):
    col1, col2 = st.columns(2)
    with col1:
        target_pet = st.selectbox("Pet", pet_names)
        task_desc = st.text_input("Task description", value="Morning walk")
        task_time = st.text_input("Time (HH:MM)", value="07:30")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=480, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
    due = st.date_input("Due date", value=date.today())
    add_task_btn = st.form_submit_button("Add task")

    if add_task_btn:
        # Basic time format validation
        parts = task_time.split(":")
        if len(parts) != 2 or not all(p.isdigit() for p in parts):
            st.error("Time must be in HH:MM format (e.g. 07:30).")
        else:
            pet_obj = next(p for p in owner.pets if p.name == target_pet)
            pet_obj.add_task(
                Task(
                    description=task_desc,
                    time=task_time,
                    duration_minutes=int(duration),
                    frequency=frequency,
                    priority=priority,
                    due_date=due,
                )
            )
            st.success(f"Added task '{task_desc}' for {target_pet}.")

# ---------------------------------------------------------------------------
# Schedule view
# ---------------------------------------------------------------------------

st.header("Today's Schedule")

scheduler = Scheduler(owner)
todays = scheduler.get_todays_schedule()

# Conflict warnings
conflicts = scheduler.detect_conflicts()
for warning in conflicts:
    st.warning(warning)

if todays:
    rows = []
    for pet, task in todays:
        rows.append(
            {
                "Time": task.time,
                "Pet": pet.name,
                "Task": task.description,
                "Duration": f"{task.duration_minutes} min",
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Done": "Yes" if task.completed else "No",
            }
        )
    st.table(rows)
else:
    st.info("No tasks scheduled for today. Add tasks above.")

# ---------------------------------------------------------------------------
# Mark a task complete
# ---------------------------------------------------------------------------

if todays:
    st.header("Mark Task Complete")
    pending = [(pet, task) for pet, task in todays if not task.completed]
    if pending:
        task_labels = [f"{task.time} - {pet.name}: {task.description}" for pet, task in pending]
        chosen = st.selectbox("Select task to mark done", task_labels)
        if st.button("Mark complete"):
            idx = task_labels.index(chosen)
            pet_obj, task_obj = pending[idx]
            next_t = scheduler.mark_task_complete(pet_obj, task_obj)
            if next_t:
                st.success(
                    f"Done! Next '{next_t.description}' scheduled for **{next_t.due_date}**."
                )
            else:
                st.success("Task marked complete.")
            st.rerun()
    else:
        st.success("All tasks for today are complete!")
