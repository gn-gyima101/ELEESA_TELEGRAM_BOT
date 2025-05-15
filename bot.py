# Full-featured Telegram bot using polling (sample layout)
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Start command — shows level options
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("L100", callback_data="level_L100")],
        [InlineKeyboardButton("L200", callback_data="level_L200")],
        [InlineKeyboardButton("L300", callback_data="level_L300")],
        [InlineKeyboardButton("L400", callback_data="level_L400")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text("Select your level:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text("Select your level:", reply_markup=reply_markup)

# Handle all button clicks
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # User selects a level — show semesters
    if data.startswith("level_"):
        level = data.split("_")[1]
        keyboard = [
            [InlineKeyboardButton("Semester 1", callback_data=f"{level}_sem1")],
            [InlineKeyboardButton("Semester 2", callback_data=f"{level}_sem2")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"Selected Level: {level}", reply_markup=reply_markup)

    # User selects a semester — show files and option to go back
    elif data.endswith("sem1") or data.endswith("sem2"):
        level, semester = data.split("_")
        await query.edit_message_text(f"Here are the materials for {level.upper()} {semester.upper()}")
        await query.message.reply_text("Sending all course files...")
        try:
            with open("sample_course_file.pdf", "rb") as doc:
                await query.message.reply_document(doc)
        except FileNotFoundError:
            await query.message.reply_text("⚠️ sample_course_file.pdf not found.")
        await query.message.reply_text("Google Drive link: https://drive.google.com/sample")
        await query.message.reply_text("⬅️ Tap /start to return.")

    # Back button to go back to main level menu
    elif data == "back_main":
        await start(update, context)

# /request command
async def request_material(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please send the name of the course or material you're requesting.")

# Entry point
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("request", request_material))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.run_polling()







