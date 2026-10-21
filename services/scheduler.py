from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot

def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    """
    Настраивает планировщик задач.
    Здесь будет логика утренней рассылки в 6:00.
    """
    scheduler = AsyncIOScheduler()
    
    # Временно: заглушка задачи (будет реализована позже)
    # scheduler.add_job(send_morning_schedule, 'cron', hour=6, minute=0, args=[bot])
    
    return scheduler