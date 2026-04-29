import flet as ft

class AboutUsTab(ft.Column): # Наследуемся от Column
    def __init__(self):
        super().__init__()
        self.spacing = 20

        self.controls = [
            ft.Text("TaskSlice", size=30, weight="bold", color="green"),
            ft.Text(
                "TaskSlice — это приложение от команды Mint-Company. "
                "Вдохновившись привычкой записывать задачи для проектов на листочках, "
                "мы создали инструмент, которым теперь можете пользоваться и вы.",
                size=16
            ),
            ft.Text("— Ваша Mint-Company", italic=True, color="grey")
        ]
