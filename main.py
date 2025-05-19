import datetime
import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask
from threading import Thread

# نام‌های سفارشی هفته
week_days = {
    "Saturday": "کیوان‌شید",
    "Sunday": "مهرشید",
    "Monday": "ماه‌شید",
    "Tuesday": "بهرام‌شید",
    "Wednesday": "تیرشید",
    "Thursday": "اورمزدشید",
    "Friday": "آدینه"
}

app = Flask('')


@app.route('/')
def main():
    return 'Your bot is alive!'


def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))


def keep_alive():
    server = Thread(target=run)
    server.start()


keep_alive()


# پاسخ به /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.datetime.now().strftime('%A')
    week_day = week_days.get(today, today)
    await update.message.reply_text(f"درود! امروز {week_day} است. ☀️")


# پیام روزانه به کانال
async def send_daily_message(application):
    today = datetime.datetime.now().strftime('%A')
    week_day = week_days.get(today, today)

    message = f"بامداد نیک! امروز «{week_day}» است. 🌞"
    chat_id = "@The_Persian_Gostar"  # آیدی کانالت رو اینجا گذاشتی

    try:
        await application.bot.send_message(chat_id=chat_id, text=message)
        print("✅ Daily message sent.")
    except Exception as e:
        print("❌ Error sending daily message:", e)


async def main():
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Scheduler راه‌اندازی
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_message,
                      CronTrigger(hour=1, minute=30),
                      args=[app])
    scheduler.start()

    print("🤖 Bot is running...")
    await app.run_polling()


import nest_asyncio

if __name__ == '__main__':
    import asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
