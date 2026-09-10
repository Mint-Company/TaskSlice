import flet as ft
from app.database import db


class GeneralTab(ft.Column):
    def __init__(self, c_page):
        super().__init__()
        self.main_page = c_page
        self.spacing = 10
        self.expand = True

        self.database = db.DataBase()
        self.database.connection_database()

        # Элементы шапки
        self.label_myday = ft.Text(
            value="Все задачи",
            color="blue",
            size=30,
            weight="bold",
            expand=True,
        )
        self.label1 = ft.Text(
            value="TaskSlice: задачи всегда под рукой)",
            size=20,
            color="blue",
            expand=True,
        )

        # Поле поиска
        self.input_search = ft.TextField(
            label="Поиск", hint_text="Найти задачу...", expand=True
        )
        self.input_search.on_submit = lambda e: self.search_task()

        # Ввод параметров задачи
        self.input_text = ft.TextField(
            label="Задача", hint_text="Что нужно сделать?", expand=True
        )
        self.input_time = ft.TextField(
            label="Время / Дата", hint_text="ГГГГ-ММ-ДД ЧЧ:ММ", expand=True
        )

        self.priority = ft.Dropdown(
            label="Приоритет",
            options=[
                ft.dropdown.Option("Низкий"),
                ft.dropdown.Option("Средний"),
                ft.dropdown.Option("Высокий"),
            ],
            expand=True,
        )

        self.bttn_add_task = ft.FilledButton(
            content=ft.Text("Добавить"), expand=True
        )
        self.bttn_add_task.on_click = lambda e: self.add_task()

        # Список задач
        self.list_task = ft.ListView(spacing=10, expand=True)

        # Макет интерфейса
        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        self.label_myday,
                        self.input_search,
                        self.input_text,
                        ft.Row([self.input_time, self.priority]),
                        self.bttn_add_task,
                        ft.Divider(),
                        self.list_task,
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                )
            )
        ]

    def did_mount(self):
        self.load_tasks()

    def add_task(self):
        title = self.input_text.value.strip() if self.input_text.value else ""
        if not title:
            self.msg("Вы заполнили не все поля!")
            return

        task_time = (
            self.input_time.value.strip() if self.input_time.value else ""
        )
        priority = self.priority.value if self.priority.value else "Средний"

        self.database.add_into_tasks(
            "general_tasks", title, task_time, priority
        )

        self.input_text.value = ""
        self.input_time.value = ""
        self.priority.value = None

        if self.page:
            self.main_page.update()

        self.load_tasks()

    def load_tasks(self):
        """Загружает задачи из базы и выводит на экран"""
        self.list_task.controls.clear()

        tasks_from_db = self.database.get_all_tasks("general_tasks")

        if tasks_from_db:
            for task in tasks_from_db:
                task_id, desc, priority, task_date = task

                new_tile = ft.ListTile(
                    title=ft.Text(f"• {desc}: [{priority}], {task_date}"),
                    trailing=ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        on_click=lambda e, tid=task_id: self.delete_task(tid),
                    ),
                )
                self.list_task.controls.append(new_tile)

        if self.page:
            self.list_task.update()

    def delete_task(self, task_id):
        """Удаляет задачу из таблицы general_tasks и обновляет экран"""
        self.database.delete_task(task_id, "general_tasks")

        search_text = (
            self.input_search.value.strip() if self.input_search.value else ""
        )
        if search_text:
            self.search_task()
        else:
            self.load_tasks()

    def msg(self, text):
        """Уведомление"""
        snack_bar = ft.SnackBar(content=ft.Text(text))
        self.main_page.overlay.append(snack_bar)
        snack_bar.open = True
        self.main_page.update()

    def search_task(self):
        text = (
            self.input_search.value.strip() if self.input_search.value else ""
        )
        if text:
            self.list_task.controls.clear()
            try:
                list_of_search_tasks = self.database.search_task(
                    text, "general_tasks"
                )

                if not list_of_search_tasks:
                    self.msg(f"Задача '{text}' не была найдена :(")
                else:
                    for task in list_of_search_tasks:
                        task_id, desc, priority, task_date = task

                        new_tile = ft.ListTile(
                            title=ft.Text(
                                f"• {desc}: [{priority}], {task_date}"
                            ),
                            trailing=ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                on_click=lambda e, tid=task_id: self.delete_task(
                                    tid
                                ),
                            ),
                        )
                        self.list_task.controls.append(new_tile)

                if self.page:
                    self.list_task.update()

            except Exception as ex:
                self.msg(f"Ошибка: {ex}")
        else:
            self.load_tasks()