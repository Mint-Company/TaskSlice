import sqlite3
import os
import logging

logging.basicConfig(level=logging.INFO, filename='db.log', format='%(asctime)s - %(levelname)s - %(message)s')

class DataBase:
    def __init__(self):
        self.db_path = "taskslice.db"
        self.conn = None
        self.cur = None

    def connection_database(self):
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cur = self.conn.cursor()
            
            # Создаем таблицы (синтаксис почти идентичен, SERIAL заменен на INTEGER PRIMARY KEY)
            self.cur.executescript("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    date TEXT
                );
                CREATE TABLE IF NOT EXISTS today_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    date TEXT
                );
            """)
            self.conn.commit()
            logging.info("Успешное подключение к SQLite")
            return True
        except Exception as error:
            logging.error(f"Ошибка подключения к SQLite: {error}")
            return False

    def sort_tasks(self, table):
        try:
            query = f"""
                SELECT id, description, priority, date FROM {table} 
                ORDER BY CASE priority 
                    WHEN 'Высокий' THEN 1  
                    WHEN 'Средний' THEN 2  
                    WHEN 'Низкий' THEN 3 
                END;
            """
            self.cur.execute(query)
            return self.cur.fetchall()
        except Exception as e:
            logging.error(f"Ошибка в sort_tasks: {e}")
            raise e

    def add_into_tasks(self, table, description, date, priority):
        try:
            query = f"INSERT INTO {table} (description, priority, date) VALUES (?, ?, ?)"
            self.cur.execute(query, (description, priority, date))
            self.conn.commit()
        except Exception as e:
            if self.conn: self.conn.rollback()
            logging.error(f"Ошибка в add_into_tasks: {e}")
            raise e

    def delete_task(self, task_id, table):
        try:
            query = f"DELETE FROM {table} WHERE id = ?"
            self.cur.execute(query, (task_id,))
            self.conn.commit()
        except Exception as e:
            if self.conn: self.conn.rollback()
            logging.error(f"Ошибка в delete_task: {e}")

    def search_task(self, text):
        search_text = f"%{text}%"
        query = f"SELECT * FROM today_tasks WHERE description LIKE LOWER(?)"
        self.cur.execute(query, (search_text ,))
        return self.cur.fetchall()
        

    def close_database(self):
        if self.conn:
            self.conn.close()