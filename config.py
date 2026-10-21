import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ссылка на Google Таблицу
GOOGLE_SHEET_URL = os.getenv("GOOGLE_SHEET_URL")

# Проверка, что все необходимые переменные заданы
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в .env файле!")

if not GOOGLE_SHEET_URL:
    raise ValueError("GOOGLE_SHEET_URL не задан в .env файле!")

# Функция для извлечения ID таблицы и листа из URL
def get_sheet_ids():
    """
    Извлекает ID таблицы и ID листа из URL Google Sheets.
    Пример URL: https://docs.google.com/spreadsheets/d/1ABC123.../edit#gid=0
    """
    try:
        # Извлекаем ID таблицы
        sheet_id = GOOGLE_SHEET_URL.split("/d/")[1].split("/")[0]
        
        # Извлекаем ID листа (gid)
        if "gid=" in GOOGLE_SHEET_URL:
            gid = GOOGLE_SHEET_URL.split("gid=")[1].split("&")[0]
        else:
            gid = "0"  # По умолчанию первый лист
        
        return sheet_id, gid
    except Exception as e:
        raise ValueError(f"Не удалось извлечь ID из URL таблицы: {e}")

# Получаем ID таблицы и листа при импорте
SHEET_ID, SHEET_GID = get_sheet_ids()

# URL для CSV-экспорта (используется в парсере)
CSV_EXPORT_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={SHEET_GID}"