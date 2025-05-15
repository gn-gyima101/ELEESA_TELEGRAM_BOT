
import os
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Set this in Render e.g., https://your-app-name.onrender.com

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("L100", callback_data="level_L100")],
        [InlineKeyboardButton("L200", callback_data="level_L200")],
        [InlineKeyboardButton("L300", callback_data="level_L300")],
        [InlineKeyboardButton("L400", callback_data="level_L400")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select your level:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("level_"):
        level = data.split("_")[1]
        keyboard = [
            [InlineKeyboardButton("Semester 1", callback_data=f"{level}_sem1")],
            [InlineKeyboardButton("Semester 2", callback_data=f"{level}_sem2")],
            [InlineKeyboardButton("Back", callback_data="back_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"Selected Level: {level}", reply_markup=reply_markup)

    elif data.endswith("sem1") or data.endswith("sem2"):
        level, semester = data.split("_")
        await query.edit_message_text(f"Here are the materials for {level.upper()} {semester.upper()}")
        await query.message.reply_text("Sending all course files...")
        await query.message.reply_document(open("sample_course_file.pdf", "rb"))
        await query.message.reply_text("Google Drive link: https://drive.google.com/sample")

    elif data == "back_main":
        await start(update, context)

async def request_material(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please send the name of the course or material you're requesting.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("request", request_material))
    app.add_handler(CallbackQueryHandler(handle_callback))

    await app.initialize()
    await app.start()

    # Set webhook
    await app.bot.set_webhook(WEBHOOK_URL)

    # Start listening for webhooks
    await app.updater.start_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        url_path="",
        webhook_url=WEBHOOK_URL,
    )

    print("Bot running via webhook...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
