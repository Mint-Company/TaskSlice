import flet as ft
# Импортируем ТВОИ классы из ТВОИХ файлов
from views.general_tasks_tab import GeneralTab 
from views.today_tasks_tab import TodayTab  
from views.about_us import AboutUsTab

def main(page: ft.Page):
    page.title = "TaskSlice"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 500
    page.window_height = 700

    # Область, где будут отображаться вкладки
    content_area = ft.Container(expand=True)

    def change_tab(e):
        # Очищаем и ставим нужный класс
        if e.control.data == 0:
            content_area.content = TodayTab(page)
        elif e.control.data == 1:
            content_area.content = GeneralTab(page)
        elif e.control.data == 2:
            content_area.content = AboutUsTab()
        
        page.update()


    # Кнопки навигации
    tab_buttons = ft.Row([
        ft.TextButton("Мой день", on_click=change_tab, data=0),
        ft.TextButton("Основные задачи", on_click=change_tab, data=1),
        ft.TextButton("О нас", on_click=change_tab, data=2),
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Добавляем всё на страницу
    page.add(tab_buttons, ft.Divider(), content_area)

    # Показываем первую вкладку сразу при запуске
    content_area.content = TodayTab(page)
    page.update()

# ЗАПУСК ПРИЛОЖЕНИЯ
if __name__ == "__main__":
    ft.app(target=main)

