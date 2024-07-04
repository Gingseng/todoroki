# task_management.py

class Task:
    def __init__(self, name):
        self.name = name
        self.done = False

    def mark_done(self):
        self.done = True

    def toggle_done(self):
        self.done = not self.done

    def __str__(self):
        return f"Task: {self.name}, Done: {self.done}"

class TaskGroup:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def mark_task_done(self, task_name):
        for task in self.tasks:
            if task.name == task_name:
                task.mark_done()
                return
        print(f"Task {task_name} not found in group {self.name}")

    def toggle_task_done(self, task_name):
        for task in self.tasks:
            if task.name == task_name:
                task.toggle_done()
                return
        print(f"Task {task_name} not found in group {self.name}")

    def all_tasks_done(self):
        return all(task.done for task in self.tasks)

    def __str__(self):
        tasks_str = "\n  ".join(str(task) for task in self.tasks)
        return f"Task Group: {self.name}\n  {tasks_str}"

class Timeline:
    def __init__(self):
        self.task_groups = []

    def add_task_group(self, task_group):
        self.task_groups.append(task_group)

    def mark_task_done(self, group_name, task_name):
        for group in self.task_groups:
            if group.name == group_name:
                group.mark_task_done(task_name)
                return
        print(f"Task group {group_name} not found")

    def toggle_task_done(self, group_name, task_name):
        for group in self.task_groups:
            if group.name == group_name:
                group.toggle_task_done(task_name)
                return
        print(f"Task group {group_name} not found")

    def check_group_completion(self, group_name):
        for group in self.task_groups:
            if group.name == group_name:
                return group.all_tasks_done()
        print(f"Task group {group_name} not found")
        return False

    def __str__(self):
        groups_str = "\n".join(str(group) for group in self.task_groups)
        return f"Timeline:\n{groups_str}"
