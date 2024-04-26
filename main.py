import json
import os
from datetime import datetime


active_tasks_path = r"C:\Users\user\PycharmProjects\python_project_todo_list/active_tasks.json"
completed_tasks_path = r"C:\Users\user\PycharmProjects\python_project_todo_list/completed_tasks.json"


def json_parser(json_file_path):
    tasks = []
    if os.path.getsize(json_file_path) > 0:
        with open(json_file_path, 'r') as file:
            tasks = json.load(file)
    return tasks


def json_loader(tasks, json_file_path):
    with open(json_file_path, 'w') as file:
        json.dump(tasks, file)


def validate_date(date_string):
    while True:
        try:
            date = datetime.strptime(date_string, "%Y-%m-%d").date()
            if date < datetime.now().date():
                print("Invalid date. Due date should be greater than or equal to today.")
                date_string = input("Enter a task due date (YYYY-MM-DD format): ")
                continue
            return date_string
        except ValueError:
            print("Invalid date format. Only YYYY-MM-DD format is allowed.")
            date_string = input("Enter a task due date (YYYY-MM-DD format): ")


def validate_index(index, choices_list):
    while True:
        try:
            index = int(index)
            if index not in choices_list:
                print(f"Invalid index. Available choices: {choices_list}")
                index = input("Enter an index again: ")
                continue
            return index
        except ValueError:
            print("Invalid format. Index should be an integer")
            index = input("Enter an index again: ")


def create_task():
    task_name = input("Enter a task name: ")
    task_due_date = validate_date(input("Enter a task due date (YYYY-MM-DD format): "))
    task_comment = input("Enter your comments to a task: ")
    new_task_info = {'task_name': task_name, 'task_due_date': task_due_date, 'task_comment': task_comment}
    tasks_list = json_parser(active_tasks_path)
    tasks_list.append(new_task_info)
    json_loader(tasks_list, active_tasks_path)
    print(f"Task '{new_task_info['task_name']}' is successfully created.")


def display_tasks(source_file, task_status):
    if os.path.getsize(source_file) == 0:
        print(f"There are no {task_status} tasks")
    else:
        print(f"{task_status.upper()} TASKS:")
        print("*" * 44)
        print("Task Index: Task Name || Due Date || Comment")
        print("*" * 44)
        tasks = json_parser(source_file)
        for index, task in enumerate(tasks):
            print(f"{index}: {task['task_name']} || {task['task_due_date']} || {task['task_comment']}")
        print("*" * 44)


def update_task():
    if os.path.getsize(active_tasks_path) == 0:
        print("There are no active tasks to update")
    else:
        tasks = json_parser(active_tasks_path)
        task_index_list = list(range(0, len(tasks)))
        task_to_update_index = validate_index(input("Enter a task index to update: "), task_index_list)
        task_component_to_update_index = validate_index(input("Enter a task component to update "
                                                              "(1-name, 2-due date, 3-comment): "), [1, 2, 3])
        task_component_mapping = {1: "task_name", 2: "task_due_date", 3: "task_comment"}
        task_component_to_update = task_component_mapping[task_component_to_update_index]
        if task_component_to_update == "task_due_date":
            task_update = validate_date(input("Enter your update: "))
        else:
            task_update = input("Enter your update: ")
        tasks[task_to_update_index][task_component_to_update] = task_update
        json_loader(tasks, active_tasks_path)
        print(f"Task '{tasks[task_to_update_index]['task_name']}' is successfully updated.")


def move_task(source_file, destination_file, action):
    if os.path.getsize(source_file) == 0:
        print("There are no tasks to {action}")
    else:
        source_tasks = json_parser(source_file)
        destination_tasks = []
        if os.path.getsize(destination_file) > 0:
            destination_tasks = json_parser(destination_file)
        task_index_list = list(range(0, len(source_tasks)))
        task_to_move_index = validate_index(input(f"Enter the index of the task to {action}: "), task_index_list)
        task_to_move = source_tasks[task_to_move_index]
        destination_tasks.append(task_to_move)
        json_loader(destination_tasks, destination_file)
        source_tasks.remove(task_to_move)
        json_loader(source_tasks, source_file)
        if action == "complete":
            print(f"Task '{task_to_move['task_name']}' is successfully completed.")
        else:
            print(f"Task '{task_to_move['task_name']}' is successfully re-opened.")


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
            display_tasks(active_tasks_path, "active")
        elif function == "3":
            display_tasks(completed_tasks_path, "completed")
        elif function == "4":
            update_task()
        elif function == "5":
            move_task(active_tasks_path, completed_tasks_path, "complete")
        elif function == "6":
            move_task(completed_tasks_path, active_tasks_path, "re-open")
        elif function == "7":
            break
        else:
            print("Unknown command. Available choices: 1, 2, 3, 4, 5, 6, 7")


if __name__ == "__main__":
    main()
