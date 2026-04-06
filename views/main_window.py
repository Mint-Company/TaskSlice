from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from views.general_tasks_tab import GeneralTab 
from views.today_tasks_tab import TodayTab  


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Настройки окна
        self.setWindowTitle("To-Do List")
        self.setMinimumSize(420, 400)  # Можно сделать поменьше
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный слой   
        tabs = QTabWidget()

        self.today_tab = TodayTab()
        self.general_tab = GeneralTab()

        tabs.addTab(self.today_tab, "Мой день")
        tabs.addTab(self.general_tab, "Основные задачи")

        self.setCentralWidget(tabs)
        
        # Применяем стиль
        self.apply_style()
    
    def apply_style(self):
        """Красивое оформление"""
        self.setStyleSheet("""
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
        """)