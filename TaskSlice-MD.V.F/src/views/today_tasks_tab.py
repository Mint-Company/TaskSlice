from datetime import date
import flet as ft
from app.database.db import DataBase


class TodayTab(ft.Column):
    def __init__(self, c_page):
        super().__init__(expand=True)
        self.main_page = c_page
        self.database = DataBase()
        if not self.database.connection_database():
            print("Не удалось подключиться к базе!")

        # 1. Шапка (Header Container)
        self.label_myday = ft.Container(
            content=ft.Text(
                "Добрый день!",
                size=12,
                weight=ft.FontWeight.BOLD,
                color="#2C3E50",
            ),
            bgcolor="#F0F4FF",
            border_radius=12
        )

        self.label1 = ft.Text(
            "TaskSlice: задачи всегда под рукой)",
            size=12,
            italic=True,
            color=ft.Colors.BLACK,
            text_align=ft.TextAlign.CENTER,
            expand=True,
        )

        self.input_search = ft.TextField(
            hint_text="Найти задачу...",
            bgcolor="#d2e1fc",
            color="#1D1D1F",
            border_color="#D0D9E9",
            border_radius=12,
            text_size=14,
            expand=True,
            on_submit=lambda e: self.search_task(),
        )

        self.button_search = ft.IconButton(
            icon=ft.Icons.SEARCH,
            icon_color="#1D1D1F",
            bgcolor="#d2e1fc",
            on_click=lambda e: self.search_task(),
        )

        # Контейнер шапки
        header_container = ft.Container(
            content=ft.Row(
                controls=[
                    self.label_myday,
                    self.label1,
                    self.input_search,
                    self.button_search,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#f0f0f0",
            border_radius=10
        )

        # 2. Форма добавления задачи
        self.input_text = ft.TextField(
            hint_text="Введите задачу...",
            expand=True,
            on_submit=lambda e: self.add_task(),
        )

        self.priority = ft.Dropdown(
            hint_text="Приоритетность",
            value="Средний",
            options=[
                ft.dropdown.Option("Низкий"),
                ft.dropdown.Option("Средний"),
                ft.dropdown.Option("Высокий"),
            ],
            width=160,
        )

        self.bttn_add_task = ft.ElevatedButton(
            content="Добавить",
            on_click=lambda e: self.add_task(),
        )

        layout_for_add = ft.Row(
            controls=[
                self.input_text,
                self.priority,
                self.bttn_add_task,
            ],
            alignment=ft.MainAxisAlignment.START,
        )

        # 3. Список задач
        self.list_task = ft.ListView(
            spacing=5,
            expand=True,
        )

        # Главная компоновка
        self.controls = [
            header_container,
            layout_for_add,
            ft.Divider(),
            self.list_task,
        ]

    def did_mount(self):
        self.load_tasks()

    def add_task(self):
        title = self.input_text.value.strip() if self.input_text.value else ""
        if not title:
            return

        today_date = date.today()
        priority_val = self.priority.value or "Средний"

        # Сохраняем в БД (формат как в PySide6)
        self.database.add_into_tasks(
            "today_tasks", title, today_date.isoformat(), priority_val
        )

        self.input_text.value = ""
        self.load_tasks()

    def load_tasks(self):
        """Загружает задачи на сегодня из базы и выводит на экран"""
        self.list_task.controls.clear()

        # Вызов метода БД аналогично PySide6
        tasks_from_db = self.database.sort_tasks(date.today())

        if tasks_from_db:
            for task in tasks_from_db:
                task_id, desc, priority_val, _ = task
                self._append_task_to_list(task_id, desc, priority_val)

        self.update()

    def search_task(self):
        text = (
            self.input_search.value.strip() if self.input_search.value else ""
        )

        if text:
            self.list_task.controls.clear()
            try:
                # В точности повторяет поиск PySide6
                list_of_search_tasks = self.database.search_task(
                    text, "today_tasks"
                )

                if not list_of_search_tasks:
                    self.msg(f"Задача '{text}' не была найдена :(")
                else:
                    for task in list_of_search_tasks:
                        task_id, desc, priority_val, _ = task
                        self._append_task_to_list(task_id, desc, priority_val)

            except Exception as ex:
                self.msg(f"Ошибка: {ex}")

            self.update()
        else:
            self.load_tasks()

    def _append_task_to_list(self, task_id, desc, priority_val):
        """Вспомогательный метод для отрисовки элемента списка"""
        item_row = ft.Row(
            controls=[
                ft.Text(f"• {desc} [{priority_val}]", expand=True, size=14),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=ft.Colors.RED_400,
                    tooltip="Удалить",
                    on_click=lambda e, tid=task_id: self.delete_task(tid),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.list_task.controls.append(
            ft.Container(
                content=item_row
                )
            )

    def delete_task(self, task_id):
        """Удаляет из базы и обновляет экран"""
        self.database.delete_task(task_id, "today_tasks")
        self.load_tasks()

    def msg(self, text):
        """Показ всплывающего уведомления (аналог QMessageBox)"""
        snack_bar = ft.SnackBar(content=ft.Text(text))
        self.main_page.overlay.append(snack_bar)
        snack_bar.open = True
        self.main_page.update()
