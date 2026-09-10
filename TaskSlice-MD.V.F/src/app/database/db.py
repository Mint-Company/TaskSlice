import sqlite3
import logging

logging.basicConfig(level=logging.INFO, filename='db.log', format='%(asctime)s - %(levelname)s - %(message)s')

# Белый список разрешённых таблиц — защита от SQL-инъекции через параметр table,
# т.к. в sqlite3 нет аналога sql.Identifier() для безопасной подстановки имени таблицы
ALLOWED_TABLES = {"tasks", "today_tasks", "tomorrow_tasks", "completed_tasks"}


class DataBase:
    def __init__(self):
        self.db_path = "task_slice.db"
        self.conn = None
        self.cur = None

    def _validate_table(self, table):
        if table not in ALLOWED_TABLES:
            raise ValueError(f"Недопустимое имя таблицы: {table}")

    def sort_tasks(self, date):
        try:
            query = f"""SELECT * FROM (
                SELECT id, description, priority, date FROM today_tasks WHERE date = '{date}'
                UNION
                SELECT id, description, priority, date FROM tomorrow_tasks WHERE date = '{date}'
                UNION
                SELECT id, description, priority, date FROM tasks WHERE date = '{date}'
                )
                    ORDER BY CASE priority
                        WHEN 'Высокий' THEN 1
                        WHEN 'Средний' THEN 2
                        WHEN 'Низкий' THEN 3
                    END;"""

            self.cur.execute(query)
            return self.cur.fetchall()
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Ошибка в sort_tasks: {e}")
            raise e

    def sort_all_tasks(self):
        try:
            query = f"""SELECT * FROM (
                SELECT id, description, priority, date FROM today_tasks
                UNION
                SELECT id, description, priority, date FROM tomorrow_tasks
                UNION
                SELECT id, description, priority, date FROM tasks
                )
                    ORDER BY CASE priority
                        WHEN 'Высокий' THEN 1
                        WHEN 'Средний' THEN 2
                        WHEN 'Низкий' THEN 3
                    END;"""
        
            self.cur.execute(query)
            return self.cur.fetchall()
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Ошибка в sort_general_tasks: {e}")
            raise e

    def add_into_tasks(self, table, description, date, priority):
        self._validate_table(table)
        try:
            self.cur.execute(
                f"INSERT INTO {table} (description, priority, date) VALUES (?, ?, ?)",
                (description, priority, date)
            )

            self.conn.commit()
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logging.error(f"Ошибка в add_into_tasks: {e}")
            raise e

    def add_into_general_tasks(self, table, description, date, priority):
        self._validate_table(table)
        cur_date = date.date()
        try:
            self.cur.execute(
                f"INSERT INTO {table} (description, priority, date, cur_date) VALUES (?, ?, ?, ?)",
                (description, priority, date, cur_date)
            )
            self.conn.commit()
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logging.error(f"Ошибка в add_into_tasks: {e}")
            raise e

    def get_all_tasks(self, table=None):
        """Возвращает задачи. Если table не указан, собирает все задачи из всех таблиц."""
        try:
            if table:
                self._validate_table(table)
                query = f"SELECT id, description, priority, date FROM {table}"
                self.cur.execute(query)
            else:
                # Объединяем задачи из всех трех активных таблиц
                query = """
                    SELECT id, description, priority, date FROM today_tasks
                    UNION ALL
                    SELECT id, description, priority, date FROM tomorrow_tasks
                    UNION ALL
                    SELECT id, description, priority, date FROM tasks
                """
                self.cur.execute(query)

            return self.cur.fetchall()
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logging.error(f"Ошибка в get_all_tasks: {e}")
            return []

    def search_task(self, text, table):
        self._validate_table(table)

        query = f"SELECT * FROM {table}"
        self.cur.execute(query)
        all_tasks = self.cur.fetchall()

        search_lower = text.lower()

        result = []
        for task in all_tasks:
            # task - это кортеж (id, description, priority, date)
            description = task[1]
            if search_lower in description.lower():
                result.append(task)

        return result

    def delete_task(self, task_id, table):
        self._validate_table(table)
        try:
            self.cur.execute(f"DELETE FROM {table} WHERE id = ?", (task_id,))
            self.conn.commit()
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logging.error(f"Ошибка в delete_task: {e}")

    def connection_database(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cur = self.conn.cursor()
            self.cur.executescript("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    date DATE
                );
                CREATE TABLE IF NOT EXISTS today_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    date DATE
                );
                CREATE TABLE IF NOT EXISTS tomorrow_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    date DATE
                );
                CREATE TABLE IF NOT EXISTS completed_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    priority TEXT NOT NULL,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    pomodoros_spent INTEGER DEFAULT 1,
                    cur_date DATE
                );
            """)
            self.conn.commit()
            logging.info("Успешное подключение")
            return True
        except Exception as error:
            logging.error(f"Ошибка подключения: {error}")
            return False

    def close_database(self):
        if self.conn:
            self.conn.close()