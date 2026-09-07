import flet as ft
from app.database import db


class StatsTab(ft.Column):

    def __init__(self, c_page):
        super().__init__()  # Важно: вызов без аргументов
        self.main_page = c_page
        self.spacing = 10
        self.expand = True

        self.database = db.DataBase()
        self.database.connection_database()

        # Элементы интерфейса
        self.label_title = ft.Text(
            value="Статистика", color="blue", size=30, weight="bold"
        )

        self.stats_text = ft.Text(value="Загрузка статистики...", size=16)

        # Макет
        self.controls = [
            ft.Container(
                content=ft.Column(
                    [self.label_title, ft.Divider(), self.stats_text]
                )
            )
        ]

    def did_mount(self):
        self.load_stats()

    def load_stats(self):
        """Пример загрузки статистики из БД"""
        try:
            # Ваша логика получения статистики
            total_general = len(self.database.get_all_tasks("general_tasks"))
            self.stats_text.value = f"Всего задач в общем списке: {total_general}"
        except Exception as ex:
            self.stats_text.value = f"Ошибка при загрузке: {ex}"

        if self.page:
            self.update()