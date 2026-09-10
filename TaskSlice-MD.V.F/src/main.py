import flet as ft
from views.general_tasks_tab import GeneralTab 
from views.today_tasks_tab import TodayTab 
from views.tomorrow_tasks_tab import TomorrowTab 
from views.stats_tab import StatsTab


def main(page: ft.Page):
    page.title = "TaskSlice MOBILE.V.P-0.65.2"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 420
    page.window.height = 700

    # Область, где будут отображаться вкладки
    content_area = ft.Container(expand=True)

    # Инициализация всех вкладок
    today_tab = TodayTab(page)
    tomorrow_tab = TomorrowTab(page)
    general_tab = GeneralTab(page)
    static_tab = StatsTab(page)

    # Функция переключения вкладок
    def change_tab(e):
        index = e.control.selected_index
        if index == 0:
            content_area.content = today_tab
        elif index == 1:
            content_area.content = tomorrow_tab
        elif index == 2:
            content_area.content = general_tab
        elif index == 3:
            content_area.content = static_tab
        
        page.update()

    # Нижняя навигация для смартфона
    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=change_tab,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.TODAY, label="Сегодня"),
            ft.NavigationBarDestination(icon=ft.Icons.EVENT_REPEAT, label="На завтра"),
            ft.NavigationBarDestination(icon=ft.Icons.TASK_ALT, label="Основные"),
            ft.NavigationBarDestination(icon=ft.Icons.BAR_CHART, label="Статистика"),
        ],
    )

    # Добавляем центральную область на страницу
    page.add(content_area)

    # Показываем первую вкладку сразу при запуске
    content_area.content = today_tab
    page.update()


if __name__ == "__main__":
    ft.app(target=main)

    