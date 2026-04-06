import sys
from PySide6.QtWidgets import QApplication
from views.main_window import MainWindow  # Импортируем главное окно

def main():
    """Запуск приложения"""  
    # 1. Создаем само приложение
    app = QApplication(sys.argv)
    
    # 2. Создаем главное окно
    window = MainWindow()
    window.show()  # Показываем окно
    
    # 3. Запускаем цикл обработки событий
    # (приложение работает, пока пользователь не закроет окно)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()