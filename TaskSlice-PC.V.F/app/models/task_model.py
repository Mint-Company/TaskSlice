class Task:
    def __init__(self, title, date, priority, completed=False):
        self.title = title
        self.completed = completed
        self.priority = priority