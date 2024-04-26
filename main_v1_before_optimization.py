import json
import os
from datetime import datetime


active_tasks_path = r"C:\Users\user\PycharmProjects\python_project_todo_list/active_tasks.json"
completed_tasks_path = r"C:\Users\user\PycharmProjects\python_project_todo_list/completed_tasks.json"


def create_task():
    tasks = []
    if os.path.getsize(active_tasks_path) > 0:
        with open(active_tasks_path, 'r') as file:
            tasks = json.load(file)
    task_name = input("Enter a task name: ")
    while True:
        task_due_date = input("Enter a task due date (YYYY-MM-DD format): ")
        try:
            datetime.strptime(task_due_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Only YYYY-MM-DD format is allowed.")
            continue
        if datetime.strptime(task_due_date, "%Y-%m-%d").date() < datetime.now().date():
            print("Invalid date. Due date should be greater than or equal to today.")
            continue
        break
    task_comment = input("Enter your comments to a task: ")
    new_task_info = {'task_name': task_name, 'task_due_date': task_due_date, 'task_comment': task_comment}
    tasks.append(new_task_info)
    with open(active_tasks_path, 'w') as file:
        json.dump(tasks, file)
    print(f"Task '{new_task_info['task_name']}' is successfully created.")


def display_active_tasks():
    if os.path.getsize(active_tasks_path) == 0:
        print("There are no active tasks")
    else:
        print("ACTIVE TASKS:")
        print("*" * 44)
        print("Task Index: Task Name || Due Date || Comment")
        print("*" * 44)
        with open(active_tasks_path, 'r') as file:
            tasks = json.load(file)
        for index, task in enumerate(tasks):
            print(f"{index}: {task['task_name']} || {task['task_due_date']} || {task['task_comment']}")
        print("*" * 44)


def display_completed_tasks():
    if os.path.getsize(completed_tasks_path) == 0:
        print("There are no completed tasks")
    else:
        print("COMPLETED TASKS:")
        print("*" * 44)
        print("Task Index: Task Name || Due Date || Comment")
        print("*" * 44)
        with open(completed_tasks_path, 'r') as file:
            tasks = json.load(file)
        for index, task in enumerate(tasks):
            print(f"{index}: {task['task_name']} || {task['task_due_date']} || {task['task_comment']}")
        print("*" * 44)


def update_task():
    if os.path.getsize(active_tasks_path) == 0:
        print("There are no active tasks to update")
    else:
        with open(active_tasks_path, 'r') as file:
            tasks = json.load(file)
        while True:
            try:
                task_index_to_update = int(input("Enter a task index to update: "))
            except ValueError:
                print("Invalid format. Task index should be an integer")
                continue
            if task_index_to_update not in [index for index, _ in enumerate(tasks)]:
                print(f"Index is unavailable. List of available indexes: {[index for index, _ in enumerate(tasks)]}")
                continue
            break
        while True:
            try:
                task_element_to_update_index = int(input("Enter a task element to update "
                                                         "(1-name, 2-due date, 3-comment): "))
            except ValueError:
                print("Invalid format. Task element should be an integer")
            else:
                if task_element_to_update_index not in [1, 2, 3]:
                    print("Invalid option. Possible options: 1, 2, 3")
                    continue
                element_mapping = {1: "task_name", 2: "task_due_date", 3: "task_comment"}
                task_element_to_update = element_mapping[task_element_to_update_index]
                break
        if task_element_to_update_index == 2:
            while True:
                task_update = input("Enter your update: ")
                try:
                    datetime.strptime(task_update, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format. Only YYYY-MM-DD format is allowed.")
                    continue
                if datetime.strptime(task_update, "%Y-%m-%d").date() < datetime.now().date():
                    print("Invalid date. Due date should be greater than or equal to today.")
                    continue
                break
        else:
            task_update = input("Enter your update: ")
        tasks[task_index_to_update][task_element_to_update] = task_update
        with open(active_tasks_path, 'w') as file:
            json.dump(tasks, file)
        print(f"Task '{tasks[task_index_to_update]['task_name']}' is successfully updated.")


def complete_task():
    if os.path.getsize(active_tasks_path) == 0:
        print("There are no active tasks to complete")
    else:
        with open(active_tasks_path, 'r') as file:
            active_tasks = json.load(file)
        completed_tasks = []
        if os.path.getsize(completed_tasks_path) > 0:
            with open(completed_tasks_path, 'r') as file:
                completed_tasks = json.load(file)
        while True:
            try:
                task_to_complete_index = int(input("Enter the index of the task to complete: "))
            except ValueError:
                print("Invalid format. Task index should be an integer")
                continue
            else:
                if task_to_complete_index not in range(0, len(active_tasks)):
                    print(f"Task index is unavailable. List of available indexes: "
                          f"{[index for index, _ in enumerate(active_tasks)]}")
                    continue
            break
        task_to_complete = active_tasks[task_to_complete_index]
        completed_tasks.append(task_to_complete)
        with open(completed_tasks_path, 'w') as file:
            json.dump(completed_tasks, file)
        active_tasks.remove(task_to_complete)
        with open(active_tasks_path, 'w') as file:
            json.dump(active_tasks, file)
        print(f"Task '{task_to_complete['task_name']}' is completed.")


def reopen_task():
    if os.path.getsize(completed_tasks_path) == 0:
        print("There are no completed tasks to re-open")
    else:
        with open(completed_tasks_path, 'r') as file:
            completed_tasks = json.load(file)
        active_tasks = []
        if os.path.getsize(active_tasks_path) > 0:
            with open(active_tasks_path, 'r') as file:
                active_tasks = json.load(file)
        while True:
            try:
                task_to_reopen_index = int(input("Enter the index of the task to re-open: "))
            except ValueError:
                print("Invalid format. Task index should be an integer")
                continue
            else:
                if task_to_reopen_index not in range(0, len(completed_tasks)):
                    print(f"Task index is unavailable. List of available indexes: "
                          f"{[index for index, _ in enumerate(completed_tasks)]}")
                    continue
            break
        task_to_reopen = completed_tasks[task_to_reopen_index]
        active_tasks.append(task_to_reopen)
        with open(active_tasks_path, 'w') as file:
            json.dump(active_tasks, file)
        completed_tasks.remove(task_to_reopen)
        with open(completed_tasks_path, 'w') as file:
            json.dump(completed_tasks, file)
        print(f"Task '{task_to_reopen['task_name']}' is re-opened.")


def main():
    while True:
        print("\nMAIN MENU")
        print("1. Create Task")
        print("2. Display Active Tasks")
        print("3. Display Completed Tasks")
        print("4. Update Task")
        print("5. Complete Task")
        print("6. Re-open Task")
        print("7. Exit")
        function = input("Enter your choice: ")
        if function == "1":
            create_task()
        elif function == "2":
            display_active_tasks()
        elif function == "3":
            display_completed_tasks()
        elif function == "4":
            update_task()
        elif function == "5":
            complete_task()
        elif function == "6":
            reopen_task()
        elif function == "7":
            break
        else:
            print("Unknown command. Available choices: 1, 2, 3, 4, 5, 6, 7")


if __name__ == "__main__":
    main()
