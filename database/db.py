import sqlite3
import os

# Путь к папке и файлу базы данных
DB_DIR = "db"
DB_NAME = os.path.join(DB_DIR, "college_bot.db")

def ensure_db_dir():
    """Создаёт папку db, если она не существует."""
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        print(f"Папка '{DB_DIR}' успешно создана.")

def get_connection():
    """Возвращает соединение с базой данных."""
    ensure_db_dir()  # Гарантируем, что папка существует перед подключением
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Позволяет обращаться к столбцам по имени
    return conn

def init_db():
    """Инициализирует базу данных и создает таблицы, если их нет."""
    ensure_db_dir()
    conn = get_connection()
    cursor = conn.cursor()

    # Создание таблицы пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            is_subscribed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Создание таблицы предметов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    ''')

    # Создание таблицы кэша расписания
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_of_week TEXT NOT NULL,
            lesson_number INTEGER NOT NULL,
            time_range TEXT NOT NULL,
            subject_and_teacher TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print(f"База данных успешно инициализирована по пути: {DB_NAME}")

# Вспомогательные функции для работы с БД (базовый набор)

def add_user(telegram_id: int):
    """Добавляет нового пользователя в БД."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (telegram_id, is_subscribed) VALUES (?, 0)", 
            (telegram_id,)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Пользователь уже существует
    finally:
        conn.close()

def toggle_subscription(telegram_id: int, status: int):
    """Включает (1) или выключает (0) рассылку для пользователя."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET is_subscribed = ? WHERE telegram_id = ?", 
        (status, telegram_id)
    )
    conn.commit()
    conn.close()

def get_subscribed_users():
    """Возвращает список telegram_id всех пользователей с включенной рассылкой."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT telegram_id FROM users WHERE is_subscribed = 1")
    users = [row['telegram_id'] for row in cursor.fetchall()]
    conn.close()
    return users

def clear_and_update_schedule(schedule_data: list):
    """
    Полностью очищает кэш расписания и записывает новые данные.
    schedule_data: список кортежей (day_of_week, lesson_number, time_range, subject_and_teacher)
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM schedule_cache")
    cursor.executemany(
        "INSERT INTO schedule_cache (day_of_week, lesson_number, time_range, subject_and_teacher) VALUES (?, ?, ?, ?)",
        schedule_data
    )
    conn.commit()
    conn.close()

def get_schedule_by_day(day_of_week: str):
    """Возвращает расписание для указанного дня недели, отсортированное по номеру пары."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT time_range, subject_and_teacher FROM schedule_cache WHERE day_of_week = ? ORDER BY lesson_number ASC",
        (day_of_week,)
    )
    schedule = cursor.fetchall()
    conn.close()
    return schedule

if __name__ == "__main__":
    init_db()