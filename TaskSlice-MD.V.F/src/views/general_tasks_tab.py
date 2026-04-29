import flet as ft
from app.database import db

class GeneralTab(ft.Column): # Наследуемся напрямую от Column
    def __init__(self, c_page):
        super().__init__()
        self.main_page = c_page
        self.spacing = 10
        self.database = db.DataBase()
        self.database.connection_database()

        # Элементы
        self.input_text = ft.TextField(label="Задача", hint_text="Что сделать сегодня?", expand=True)
        self.input_date = ft.TextField(label="Дата", hint_text="ДД.ММ.ГГГГ", expand=True)
        
        self.bttn_add_task = ft.FilledButton(content=ft.Text("Добавить задачу"), expand=True)
        self.bttn_add_task.on_click = lambda e: self.add_task()
        
        self.priority = ft.Dropdown(
            label="Приоритетность",
            options=[
                ft.dropdown.Option("Низкая"),
                ft.dropdown.Option("Средняя"),
                ft.dropdown.Option("Высокая"),
            ], expand=True
        )
        
        self.list_task = ft.ListView(expand=True, spacing=10)
        

        self.controls = [
            ft.Container(
                content=ft.Column([
                    self.input_text,      # Поле задачи
                    ft.Row([self.input_date, self.priority]), # Время и приоритет рядом
                    self.bttn_add_task,   # Кнопка на всю ширину
                    ft.Divider(),
                    self.list_task        # Список, который тянется вниз
                ], scroll=ft.ScrollMode.ADAPTIVE),
                padding=10
            )
        ]

    def did_mount(self):
        self.load_tasks()
        
    def add_task(self):
        title = self.input_text.value.strip()
        if not title: return

        # Получаем данные из виджетов
        date = self.input_date.value.strip()
        priority = self.priority.value

        # Очищаем поле ввода
        self.input_text.value = ""
        self.input_date.value = ""
        self.priority.value = None

        self.main_page.update()
        
        # Сохраняем в базу
        self.database.add_into_tasks("tasks", title, date, priority)
        
        
        
        # Перерисовываем список задач из базы
        self.load_tasks()

    def load_tasks(self):
        """Загружает задачи из базы и выводит на экран"""
        self.list_task.controls.clear() # Очищаем визуальный список
        
        # Получаем данные 
        tasks_from_db = self.database.sort_tasks("tasks") 
        
        for task in tasks_from_db:
            # task это кортеж из базы: (id, description, priority, date)
            task_id, desc, priority, date = task
            
            new_tile = ft.ListTile(
                title=ft.Text(f"•{desc}: [{priority}], {date}"),
                trailing = ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    on_click=lambda e, checked=False, tid=task_id: self.delete_task(tid) # Передаем ссылку на элемент
                )
            )
        
            self.list_task.controls.append(new_tile)
        
        self.list_task.update()
            
    def delete_task(self, task_id):
        """Удаляет из базы и обновляет экран"""
        self.database.delete_task(task_id, "tasks")
        self.load_tasks()


