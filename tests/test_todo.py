from todo import add_task, complete_task, remove_task

def test_add_task():
    tasks = []
    add_task(tasks, "Buy groceries")
    assert len(tasks) == 1
    assert tasks[0]['task'] == "Buy groceries"
    assert tasks[0]['done'] == False

def test_complete_task():
    tasks = []
    add_task(tasks, "Finish assignment")
    complete_task(tasks, 0)
    assert tasks[0]['done'] == True

def test_remove_task():
    tasks = []
    add_task(tasks, "Task A")
    add_task(tasks, "Task B")
    remove_task(tasks, 0)
    assert len(tasks) == 1
    assert tasks[0]['task'] == "Task B"