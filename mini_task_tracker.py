import json
from pathlib import Path

DATA_FILE = Path("tasks.json")


def load_tasks():
    """Load saved tasks. If the file does not exist, start with an empty list."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
            return tasks if isinstance(tasks, list) else []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: tasks.json is invalid. Starting with an empty task list.")
        return []


def save_tasks(tasks):
    """Save all tasks to tasks.json."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def add_task(tasks):
    title = input("Task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print("Task added.")


def view_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    for number, task in enumerate(tasks, start=1):
        status = "Done" if task.get("done", False) else "Pending"
        print(f"{number}. {task.get('title', '(untitled)')} [{status}]")


def get_task_number(tasks, prompt):
    if not tasks:
        print("No tasks available.")
        return None
    raw = input(prompt).strip()
    try:
        number = int(raw)
    except ValueError:
        print("Please enter a valid whole number.")
        return None
    if number < 1 or number > len(tasks):
        print(f"Choose a task number from 1 to {len(tasks)}.")
        return None
    return number - 1


def complete_task(tasks):
    index = get_task_number(tasks, "Task number to complete: ")
    if index is None:
        return
    tasks[index]["done"] = True
    save_tasks(tasks)
    print("Task completed.")


def delete_task(tasks):
    index = get_task_number(tasks, "Task number to delete: ")
    if index is None:
        return
    removed = tasks.pop(index)
    save_tasks(tasks)
    print(f"Deleted: {removed.get('title', '(untitled)')}")


def main():
    tasks = load_tasks()
    while True:
        print("\n--- TASK TRACKER ---")
        print("1. Add   2. View   3. Complete   4. Delete   5. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid menu choice. Enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
