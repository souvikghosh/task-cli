#!/usr/bin/env python3
"""
task-cli: A simple command-line task manager with file persistence.

Usage:
    task add <description>    Add a new task
    task list                 List all tasks
    task done <id>            Mark a task as complete
    task delete <id>          Delete a task
    task clear                Remove all completed tasks
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

TASKS_FILE = Path.home() / ".task-cli" / "tasks.json"


def load_tasks() -> list[dict]:
    """Load tasks from the JSON file."""
    if not TASKS_FILE.exists():
        return []
    try:
        return json.loads(TASKS_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks: list[dict]) -> None:
    """Save tasks to the JSON file."""
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    TASKS_FILE.write_text(json.dumps(tasks, indent=2))


def get_next_id(tasks: list[dict]) -> int:
    """Get the next available task ID."""
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


def add_task(description: str) -> None:
    """Add a new task."""
    tasks = load_tasks()
    task = {
        "id": get_next_id(tasks),
        "description": description,
        "done": False,
        "created_at": datetime.now().isoformat(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task {task['id']}: {description}")


def list_tasks() -> None:
    """List all tasks."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found. Add one with: task add <description>")
        return

    pending = [t for t in tasks if not t["done"]]
    completed = [t for t in tasks if t["done"]]

    if pending:
        print("Pending:")
        for t in pending:
            print(f"  [{t['id']}] {t['description']}")

    if completed:
        print("Completed:")
        for t in completed:
            print(f"  [{t['id']}] {t['description']}")

    print(f"\nTotal: {len(pending)} pending, {len(completed)} completed")


def mark_done(task_id: int) -> None:
    """Mark a task as complete."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                print(f"Task {task_id} is already completed")
                return
            task["done"] = True
            task["completed_at"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Completed task {task_id}: {task['description']}")
            return
    print(f"Task {task_id} not found")
    sys.exit(1)


def delete_task(task_id: int) -> None:
    """Delete a task."""
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted = tasks.pop(i)
            save_tasks(tasks)
            print(f"Deleted task {task_id}: {deleted['description']}")
            return
    print(f"Task {task_id} not found")
    sys.exit(1)


def clear_completed() -> None:
    """Remove all completed tasks."""
    tasks = load_tasks()
    pending = [t for t in tasks if not t["done"]]
    removed = len(tasks) - len(pending)
    if removed == 0:
        print("No completed tasks to clear")
        return
    save_tasks(pending)
    print(f"Cleared {removed} completed task(s)")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="task",
        description="A simple command-line task manager",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", nargs="+", help="Task description")

    # list command
    subparsers.add_parser("list", help="List all tasks")

    # done command
    done_parser = subparsers.add_parser("done", help="Mark a task as complete")
    done_parser.add_argument("id", type=int, help="Task ID")

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # clear command
    subparsers.add_parser("clear", help="Remove all completed tasks")

    args = parser.parse_args()

    if args.command == "add":
        add_task(" ".join(args.description))
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        mark_done(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "clear":
        clear_completed()


if __name__ == "__main__":
    main()
