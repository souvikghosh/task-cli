"""Tests for task-cli."""

import json
from unittest.mock import patch

import pytest

from src import task_cli


@pytest.fixture
def temp_tasks_file(tmp_path):
    """Use a temporary file for tasks during tests."""
    tasks_file = tmp_path / "tasks.json"
    with patch.object(task_cli, "TASKS_FILE", tasks_file):
        yield tasks_file


class TestLoadSaveTasks:
    def test_load_empty_when_no_file(self, temp_tasks_file):
        assert task_cli.load_tasks() == []

    def test_save_and_load_tasks(self, temp_tasks_file):
        tasks = [{"id": 1, "description": "Test", "done": False}]
        task_cli.save_tasks(tasks)
        assert task_cli.load_tasks() == tasks


class TestGetNextId:
    def test_returns_1_for_empty_list(self):
        assert task_cli.get_next_id([]) == 1

    def test_returns_next_id(self):
        tasks = [{"id": 1}, {"id": 3}, {"id": 2}]
        assert task_cli.get_next_id(tasks) == 4


class TestAddTask:
    def test_add_task(self, temp_tasks_file, capsys):
        task_cli.add_task("Test task")
        tasks = task_cli.load_tasks()
        assert len(tasks) == 1
        assert tasks[0]["description"] == "Test task"
        assert tasks[0]["done"] is False
        assert "Added task 1" in capsys.readouterr().out


class TestListTasks:
    def test_list_empty(self, temp_tasks_file, capsys):
        task_cli.list_tasks()
        assert "No tasks found" in capsys.readouterr().out

    def test_list_with_tasks(self, temp_tasks_file, capsys):
        task_cli.add_task("Task 1")
        task_cli.add_task("Task 2")
        task_cli.list_tasks()
        output = capsys.readouterr().out
        assert "Task 1" in output
        assert "Task 2" in output
        assert "2 pending" in output


class TestMarkDone:
    def test_mark_done(self, temp_tasks_file, capsys):
        task_cli.add_task("Test task")
        task_cli.mark_done(1)
        tasks = task_cli.load_tasks()
        assert tasks[0]["done"] is True
        assert "Completed task 1" in capsys.readouterr().out

    def test_mark_done_not_found(self, temp_tasks_file):
        with pytest.raises(SystemExit):
            task_cli.mark_done(999)


class TestDeleteTask:
    def test_delete_task(self, temp_tasks_file, capsys):
        task_cli.add_task("Test task")
        task_cli.delete_task(1)
        assert task_cli.load_tasks() == []
        assert "Deleted task 1" in capsys.readouterr().out

    def test_delete_not_found(self, temp_tasks_file):
        with pytest.raises(SystemExit):
            task_cli.delete_task(999)


class TestClearCompleted:
    def test_clear_completed(self, temp_tasks_file, capsys):
        task_cli.add_task("Task 1")
        task_cli.add_task("Task 2")
        task_cli.mark_done(1)
        capsys.readouterr()  # Clear output
        task_cli.clear_completed()
        tasks = task_cli.load_tasks()
        assert len(tasks) == 1
        assert tasks[0]["id"] == 2
        assert "Cleared 1 completed" in capsys.readouterr().out
