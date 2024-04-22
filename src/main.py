import json
import os


active_tasks_path = r"C:\Users\user\PycharmProjects\python_project_todo_list\data\active_tasks.json"
completed_tasks_path = r"C:\Users\user\PycharmProjects\python_project_todo_list\data\completed_tasks.json"


def create_task():
    tasks = []
    if os.path.getsize(active_tasks_path) > 0:
        with open(active_tasks_path, 'r') as file:
            tasks = json.load(file)
    task_name = input("Enter a task name: ")
    task_due_date = input("Enter a task due date: ")
    task_comment = input("Enter your comments to a task: ")
    new_task_info = {'task_name': task_name, 'task_due_date': task_due_date, 'task_comment': task_comment}
    tasks.append(new_task_info)
    with open(active_tasks_path, 'w') as file:
        json.dump(tasks, file)
    print(f"Task '{new_task_info['task_name']}' is successfully created.")


def display_tasks():
    if os.path.getsize(active_tasks_path) == 0:
        print("There are no active tasks")
    else:
        print("Here are your active tasks:")
        with open(active_tasks_path, 'r') as file:
            tasks = json.load(file)
        for task in tasks:
            print(task)


def update_task():
    if os.path.getsize(active_tasks_path) == 0:
        print("There are no active tasks to update")
    else:
        with open(active_tasks_path, 'r') as file:
            tasks = json.load(file)
        task_index_to_update = int(input("Enter a task index to update: "))
        task_element_to_update = input("Enter a task element to update: ")
        updated_task_element = input("Enter your update: ")
        tasks[task_index_to_update][task_element_to_update] = updated_task_element
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
        task_to_complete_index = int(input("Enter the index of the task to complete: "))
        task_to_complete = active_tasks[task_to_complete_index]
        completed_tasks.append(task_to_complete)
        with open(completed_tasks_path, 'w') as file:
            json.dump(completed_tasks, file)
        active_tasks.remove(task_to_complete)
        with open(active_tasks_path, 'w') as file:
            json.dump(active_tasks, file)
        print(f"Task '{task_to_complete['task_name']}' is completed.")


create_task()
# display_tasks()
# update_task()
# complete_task()