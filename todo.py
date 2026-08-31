# Simple command-line To-Do List app
# Features: add a task, list all tasks, mark a task as complete, remove a task
# Tasks are stored in memory using a list of dictionaries with 'task' and 'done' keys

def add_task(tasks, description):
    """Add a new task to the list."""
    tasks.append({'task': description, 'done': False})

def list_tasks(tasks):
    """List all tasks with their status."""
    for i, task in enumerate(tasks):
        status = 'Done' if task['done'] else 'Not Done'
        print(f"{i + 1}. {task['task']} - {status}")

def complete_task(tasks, index):
    """Mark a task as complete."""
    if 0 <= index < len(tasks):
        tasks[index]['done'] = True
    else:
        print("Invalid task number.")

def remove_task(tasks, index):
    """Remove a task from the list."""
    if 0 <= index < len(tasks):
        tasks.pop(index)
    else:
        print("Invalid task number.")

def main():
    tasks = []
    while True:
        print("\nTo-Do List App")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Complete Task")
        print("4. Remove Task")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            description = input("Enter task description: ")
            add_task(tasks, description)
        elif choice == '2':
            list_tasks(tasks)
        elif choice == '3':
            try:
                index = int(input("Enter task number to complete: ")) - 1
                complete_task(tasks, index)
            except ValueError:
                print("The number you entered is invalid.")
        elif choice == '4':
            try:
                index = int(input("Enter task number to remove: ")) - 1
                remove_task(tasks, index)
            except ValueError:
                print("The number you entered is invalid.")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()