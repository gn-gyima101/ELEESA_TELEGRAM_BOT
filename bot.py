
import os
from uuid import uuid4
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, InlineQueryHandler, ContextTypes, filters

# Course structure with levels and semesters
course_links = {
    "L100": {
        "Semester 1": {
            "Linear Algebra": "https://drive.google.com/your_link_here",
            "Matlab": "https://drive.google.com/your_link_here",
            "Instrumentation": "https://drive.google.com/your_link_here",
            "Solid State": "https://drive.google.com/your_link_here",
            "Lab Work": "https://drive.google.com/your_link_here",
            "French": "https://drive.google.com/your_link_here",
            "Critical Thinking": "https://drive.google.com/your_link_here",
            "DC Machines": "https://drive.google.com/your_link_here",
            "Linear Circuit": "https://drive.google.com/your_link_here"
        },
        "Semester 2": {
            "Course 1": "https://drive.google.com/your_link_here",
            "Course 2": "https://drive.google.com/your_link_here",
            "Maths": "https://drive.google.com/your_link_here",
            "French": "https://drive.google.com/your_link_here",
            "Academic Writing": "https://drive.google.com/your_link_here",
            "Synchronous Machines": "https://drive.google.com/your_link_here",
            "Python": "https://drive.google.com/your_link_here",
            "Course 8": "https://drive.google.com/your_link_here"
        }
    },
    "L200": {
        "Semester 1": {
            "Linear Algebra": "https://drive.google.com/your_link_here",
            "Matlab": "https://drive.google.com/your_link_here",
            "Instrumentation": "https://drive.google.com/your_link_here",
            "Solid State": "https://drive.google.com/your_link_here",
            "Lab Work": "https://drive.google.com/your_link_here",
            "French": "https://drive.google.com/your_link_here",
            "Critical Thinking": "https://drive.google.com/your_link_here",
            "DC Machines": "https://drive.google.com/your_link_here",
            "Linear Circuit": "https://drive.google.com/your_link_here"
        },
        "Semester 2": {
            "Course 1": "https://drive.google.com/your_link_here",
            "Course 2": "https://drive.google.com/your_link_here",
            "Maths": "https://drive.google.com/your_link_here",
            "French": "https://drive.google.com/your_link_here",
            "Academic Writing": "https://drive.google.com/your_link_here",
            "Synchronous Machines": "https://drive.google.com/your_link_here",
            "Python": "https://drive.google.com/your_link_here",
            "Course 8": "https://drive.google.com/your_link_here"
        }
    },
    "L300": {
        "Semester 1": {
            "Linear Algebra": "https://drive.google.com/your_link_here",
            "Matlab": "https://drive.google.com/your_link_here",
            "Instrumentation": "https://drive.google.com/your_link_here",
            "Solid State": "https://drive.google.com/your_link_here",
            "Lab Work": "https://drive.google.com/your_link_here",
            "French": "https://drive.google.com/your_link_here",
            "Critical Thinking": "https://drive.google.com/your_link_here",
            "DC Machines": "https://drive.google.com/your_link_here",
            "Linear Circuit": "https://drive.google.com/your_link_here"
        },
        "Semester 2": {
            "Course 1": "https://drive.google.com/your_link_here",
            "Course 2": "https://drive.google.com/your_link_here",
            "Maths": "https://drive.google.com/your_link_here",
            "French": "https://drive.google.com/your_link_here",
            "Academic Writing": "https://drive.google.com/your_link_here",
            "Synchronous Machines": "https://drive.google.com/your_link_here",
            "Python": "https://drive.google.com/your_link_here",
            "Course 8": "https://drive.google.com/your_link_here"
        }
    },
    "L400": {
        "Semester 1": {
            "Linear Algebra": "https://drive.google.com/your_link_here",
            "Matlab": "https://drive.google.com/your_link_here",
            "Instrumentation": "https://drive.google.com/your_link_here",
            "Solid State": "https://drive.google.com/your_link_here",
            "Lab Work": "https://drive.google.com/your_link_here",
            "French": "https://drive.google.com/your_link_here",
            "Critical Thinking": "https://drive.google.com/your_link_here",
            "DC Machines": "https://drive.google.com/your_link_here",
            "Linear Circuit": "https://drive.google.com/your_link_here"
        },
        "Semester 2": {
            "Course 1": "https://drive.google.com/your_link_here",
            "Course 2": "https://drive.google.com/your_link_here",
            "Maths": "https://drive.google.com/your_link_here",
            "French": "https://drive.google.com/your_link_here",
            "Academic Writing": "https://drive.google.com/your_link_here",
            "Synchronous Machines": "https://drive.google.com/your_link_here",
            "Python": "https://drive.google.com/your_link_here",
            "Course 8": "https://drive.google.com/your_link_here"
        }
    }
}

user_session = {}
base_path = "materials"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["L100", "L200"], ["L300", "L400"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Welcome to the Digital Library Bot!\nPlease select your level:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    session = user_session.get(user_id, {})

    if text in course_links:
        user_session[user_id] = {"level": text}
        keyboard = [["Semester 1", "Semester 2"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(f"You selected {text}.\nNow choose a semester:", reply_markup=reply_markup)
        return

    if text in ["Semester 1", "Semester 2"] and "level" in session:
        session["semester"] = text
        level = session["level"]
        courses = list(course_links[level][text].keys())
        keyboard = [[course] for course in courses]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(f"You selected {text}.\nNow choose a course:", reply_markup=reply_markup)
        return

    if "level" in session and "semester" in session:
        level = session["level"]
        semester = session["semester"]
        course_data = course_links[level][semester].get(text)
        if course_data:
            await update.message.reply_text(f"*{text}* material link:\n{course_data}", parse_mode="Markdown")
            course_path = os.path.join(base_path, level, semester, text)
            if os.path.exists(course_path):
                for filename in os.listdir(course_path):
                    file_path = os.path.join(course_path, filename)
                    if os.path.isfile(file_path):
                        with open(file_path, "rb") as file:
                            await update.message.reply_document(document=file)
        else:
            await update.message.reply_text("Please select a valid course from the list.")
    else:
        await update.message.reply_text("Please start by selecting your level using /start.")

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.lower()
    results = []
    for level, semesters in course_links.items():
        for semester, courses in semesters.items():
            for name, link in courses.items():
                if query in name.lower():
                    results.append(
                        InlineQueryResultArticle(
                            id=str(uuid4()),
                            title=f"{name} ({level} {semester})",
                            input_message_content=InputTextMessageContent(f"{name} ({level} {semester}): {link}")
                        )
                    )
    await update.inline_query.answer(results[:10], cache_time=1)


# Reminder feature: Users can subscribe to reminders
reminder_subscribers = set()

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    reminder_subscribers.add(user_id)
    await update.message.reply_text("You are now subscribed to exam tips and update reminders!")

async def notify_all(context: ContextTypes.DEFAULT_TYPE, message="Don't forget to revise!"):
    for user_id in reminder_subscribers:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")
if __name__ == "__main__":
    
    
    
    app = ApplicationBuilder().token("7102796928:AAGmMM9cXw39734rk-1nSf_heuU3F2_r1KY").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("remind", remind))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(InlineQueryHandler(inline_query))
    print("Bot is running...")
    app.run_polling()






