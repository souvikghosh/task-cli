# task-cli

A simple command-line task manager with file persistence.

## Features

- Add, list, complete, and delete tasks
- Persistent storage in JSON format
- Clean, minimal interface

## Installation

```bash
# Clone the repository
git clone https://github.com/souvikghosh/task-cli.git
cd task-cli

# Install with pip
pip install -e .
```

## Usage

```bash
# Add a new task
task add Buy groceries

# List all tasks
task list

# Mark a task as complete
task done 1

# Delete a task
task delete 1

# Clear all completed tasks
task clear
```

## Example

```
$ task add Learn Python
Added task 1: Learn Python

$ task add Build a portfolio
Added task 2: Build a portfolio

$ task list
Pending:
  [1] Learn Python
  [2] Build a portfolio

Total: 2 pending, 0 completed

$ task done 1
Completed task 1: Learn Python

$ task list
Pending:
  [2] Build a portfolio
Completed:
  [1] Learn Python

Total: 1 pending, 1 completed
```

## Data Storage

Tasks are stored in `~/.task-cli/tasks.json`.

## License

MIT
