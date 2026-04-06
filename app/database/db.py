import psycopg2
from psycopg2 import Error
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent 
env_path = BASE_DIR / '.env.local'
load_dotenv(dotenv_path=env_path)

logging.basicConfig(level=logging.INFO, filename='db.log', format='%(asctime)s - %(levelname)s - %(message)s')

class DataBase:
    def __init__(self):
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_pass = os.getenv("DB_PASSWORD")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.conn = None
        self.cur = None

    def sort_tasks(self):
        try:
            self.cur.execute("SELECT id, description, priority, date FROM tasks ORDER BY priority ASC;")
            return self.cur.fetchall()
        except Exception as e:
            self.conn.rollback() 
            logging.error(f"Ошибка в sort_tasks: {e}")
            raise e

    def add_into_tasks(self, description, date, priority):
        try:
            self.cur.execute("""
                INSERT INTO tasks (description, priority, date)
                VALUES (%s, %s, %s)""", (description, priority, date))
            self.conn.commit()
        except Exception as e:
            if self.conn: self.conn.rollback()
            logging.error(f"Ошибка в add_into_tasks: {e}")
            raise e

    def add_into_comp_tasks(self, priority, completed_at, pomodoros_spent):
        try:
            self.cur.execute("""
                INSERT INTO completed_tasks (priority, completed_at, pomodoros_spent)
                VALUES (%s, %s, %s)""", (priority, completed_at, pomodoros_spent))
            self.conn.commit()
        except Exception as e:
            if self.conn: self.conn.rollback()
            logging.error(f"Ошибка в add_into_comp_tasks: {e}")

    def delete_task(self, task_id):
        try:
            # ИСПРАВЛЕНО: дописан запрос
            self.cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            self.conn.commit()
        except Exception as e:
            if self.conn: self.conn.rollback()
            logging.error(f"Ошибка в delete_task: {e}")

    def connection_database(self):
        try:
            self.conn = psycopg2.connect(
                user=self.db_user, password=self.db_pass,
                host=self.db_host, port=self.db_port, database=self.db_name
            )
            self.cur = self.conn.cursor()
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    description VARCHAR(200) NOT NULL,
                    priority TEXT NOT NULL,
                    date DATE
                );
                CREATE TABLE IF NOT EXISTS completed_tasks (
                    id SERIAL PRIMARY KEY,
                    priority TEXT NOT NULL,
                    completed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    pomodoros_spent INT DEFAULT 1
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
