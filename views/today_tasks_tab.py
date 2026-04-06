from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                               QListWidget, QListWidgetItem, QPushButton, 
                               QLineEdit, QComboBox, QCheckBox, QDateTimeEdit,
                               QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from app.models.task_model import Task
from app.database.db import DataBase


class TodayTab(QWidget): # тоже самое но для задач на сегодня (черновик).
    def __init__(self, parent=None):
        super().__init__(parent)
        self.database = DataBase() # Создаем объект
        if not self.database.connection_database():
            print("Не удалось подключиться к базе!")

        self.main_layout = QVBoxLayout() # Главный лояут
        self.setLayout(self.main_layout) # Раставляем по этому лояуту

        
        layout_for_info = QGridLayout()
        label_myday = QLabel("Добрый день!")
        label_myday.setStyleSheet("""
            background-color: #F0F4FF; 
            color: #2C3E50; 
            border: 2px solid #D0D9E9; 
            border-radius: 12px; 
            padding: 15px 20px; 
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            font-size: 16px;
            font-weight: bold;
        """)
        layout_for_info.addWidget(label_myday, 0, 0)
        layout_for_info.setColumnStretch(1, 1)

        input_search = QLineEdit()
        input_search.setStyleSheet("""
            background-color: #d2e1fc;  
            color: #1D1D1F;    
            border: 2px solid #282829;     
            border-radius: 20px;            
            padding: 8px 15px;             
            font-size: 14px;
        """)
        layout_for_info.addWidget(input_search, 0, 2)


        # Создаем список задач
        layout_for_add = QHBoxLayout() # лояут для добавления строки с заполнением данных для задачи

        self.list_task = QListWidget()
        self.input_text = QLineEdit()
        self.input_date = QDateTimeEdit()
        self.input_text.setPlaceholderText("Введите задачу...")

        self.priority = QComboBox() # для приоритетов
        self.priority.addItems(["Низкий", "Средний", "Высокий"])
        self.priority.setPlaceholderText("Приоритетность")

        self.bttn_add_task = QPushButton("Добавить") # кнопка что бы добавить
        self.bttn_add_task.clicked.connect(self.add_task)

        layout_for_add.addWidget(self.input_text)
        layout_for_add.addWidget(self.input_date)
        layout_for_add.addWidget(self.priority)
        layout_for_add.addWidget(self.bttn_add_task)
        layout_for_add.addWidget(self.list_task)

        # БЫСТРАЯ КЛАВИША ДОБАВЛЕНИЯ ЗАДАЧи (вместо кнопки)
        hotkey_add_action = QAction("Создать задачу", self)
        hotkey_add_action.setShortcut("Ctrl+N")
        hotkey_add_action.triggered.connect(self.add_task)
        self.addAction(hotkey_add_action)

        # Показ всех задач
        self.main_layout.addLayout(layout_for_info)
        self.main_layout.addLayout(layout_for_add)
        self.main_layout.addWidget(self.list_task)


    def add_task(self):
        title = self.input_text.text().strip()
        if not title: return

        # Получаем данные из виджетов
        date = self.input_date.date().toPython() 
        priority = self.priority.currentText()
        
        # Сохраняем в базу
        self.database.add_into_tasks(title, date, priority)
        
        # Очищаем поле ввода
        self.input_text.clear()
        
        # 3. Перерисовываем список задач из базы
        self.load_tasks()

    def load_tasks(self):
        """Загружает задачи из базы и выводит на экран"""
        self.list_task.clear() # Очищаем визуальный список
        
        # Получаем данные 
        tasks_from_db = self.database.sort_tasks() 
        
        for task in tasks_from_db:
            # task это кортеж из базы: (id, description, priority, date)
            task_id, desc, priority, date = task
            
            item = QListWidgetItem(self.list_task)
            row_widget = QWidget()
            layout = QHBoxLayout(row_widget)
            
            # Контент строки
            lbl_text = QLabel(f"• {desc} [{priority}]")
            btn_delete = QPushButton("🗑️")
            btn_delete.setFixedSize(30, 30)
            
            # Привязываем удаление к ID из базы
            btn_delete.clicked.connect(lambda checked=False, tid=task_id: self.delete_task(tid))
            
            layout.addWidget(lbl_text)
            layout.addStretch()
            layout.addWidget(btn_delete)
            
            item.setSizeHint(row_widget.sizeHint())
            self.list_task.setItemWidget(item, row_widget)

    def delete_task(self, task_id):
        """Удаляет из базы и обновляет экран"""
        self.database.delete_task(task_id)
        self.load_tasks()
