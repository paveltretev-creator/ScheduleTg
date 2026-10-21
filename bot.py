import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database.db import init_db
from handlers import start, schedule, subjects, settings
from services.scheduler import setup_scheduler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Главная функция запуска бота."""
    
    # Инициализация базы данных
    logger.info("Инициализация базы данных...")
    init_db()
    
    # Создание экземпляров бота и диспетчера
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    # Подключение роутеров (обработчиков команд)
    dp.include_router(start.router)
    dp.include_router(schedule.router)
    dp.include_router(subjects.router)
    dp.include_router(settings.router)
    
    # Настройка планировщика задач (рассылка в 6:00)
    logger.info("Настройка планировщика задач...")
    scheduler = setup_scheduler(bot)
    scheduler.start()
    
    logger.info("Бот запущен!")
    
    try:
        # Запуск polling (получение обновлений от Telegram)
        await dp.start_polling(bot)
    finally:
        # Остановка планировщика при завершении работы
        scheduler.shutdown()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен пользователем")