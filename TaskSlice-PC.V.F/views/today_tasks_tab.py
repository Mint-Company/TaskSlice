import flet as ft
from app.database import db

class TodayTab(ft.Column):
    def __init__(self, c_page):
        super().__init__()
        self.main_page = c_page
        self.spacing = 10
        self.database = db.DataBase()
        self.database.connection_database()
        

        # Элементы
        self.label_myday = ft.Text(value="Добрый день!", color="blue", size=30, weight="bold", expand=True)
        self.label1 = ft.Text(value="TaskSlice: задачи всегда под рукой)", size=20, color="blue", expand=True)

        
        self.input_search = ft.TextField(label="Поиск", hint_text="Найти задачу...", expand=True)
        self.input_search.on_submit = lambda e: self.search_task()

        self.input_text = ft.TextField(label="Задача", hint_text="Что сделать сегодня?", expand=True)
        self.input_time = ft.TextField(label="Время", hint_text="ЧЧ.ММ", expand=True)
        
        self.bttn_add_task = ft.FilledButton(content=ft.Text("Добавить"), expand=True)
        self.bttn_add_task.on_click = lambda e: self.add_task()
        
        self.priority = ft.Dropdown(
            label="Приоритет",
            options=[
                ft.dropdown.Option("Низкая"),
                ft.dropdown.Option("Средняя"),
                ft.dropdown.Option("Высокая"),
            ], expand=True
        )
        
        self.list_task = ft.ListView(spacing=10, expand=True)
        

        self.controls = [
            ft.Container(
                content=ft.Column([
                    self.label_myday,          # Заголовки сверху
                    self.input_search,    # Поиск под ними
                    self.input_text,      # Поле задачи
                    ft.Row([self.input_time, self.priority]), # Время и приоритет рядом
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
        date = self.input_time.value.strip()
        priority = self.priority.value

        # Очищаем поле ввода
        self.input_text.value = ""
        self.input_time.value = ""
        self.priority.value = None

        self.main_page.update()
        
        # Сохраняем в базу
        self.database.add_into_tasks("today_tasks", title, date, priority)
        
        
        # Перерисовываем список задач из базы
        self.load_tasks()

    def load_tasks(self):
        """Загружает задачи из базы и выводит на экран"""
        self.list_task.controls.clear() # Очищаем визуальный список
        
        # Получаем данные 
        tasks_from_db = self.database.sort_tasks("today_tasks") 
        
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
        self.database.delete_task(task_id, "today_tasks")
        self.load_tasks()

    def msg(self, text):
        # Короткий способ показать уведомление
        self.main_page.open(ft.SnackBar(ft.Text(text)))

    def search_task(self):
        text = self.input_search.value.strip()
        if text:
            self.list_task.controls.clear() 
            try:
                list_of_search_tasks = self.database.search_task(text)
                
                if not list_of_search_tasks:
                    self.msg("Ничего не найдено")

                else:
                    for task in list_of_search_tasks:
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


            except Exception as ex:
                self.msg(f"Ошибка: {ex}.")

            

        else:
            self.load_tasks()

        


