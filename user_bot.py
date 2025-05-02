import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from agent_utils import get_active_agents, init_db

load_dotenv()
init_db()

async def active(update: Update, context: ContextTypes.DEFAULT_TYPE):
    agents = get_active_agents()
    if not agents:
        await update.message.reply_text("No agents available")
        return
    buttons = [[InlineKeyboardButton(agent['full_name'], url=f"https://t.me/{agent['username']}")]
               for agent in agents]
    await update.message.reply_text("Available Agents:", reply_markup=InlineKeyboardMarkup(buttons))

app = ApplicationBuilder().token(os.getenv("USER_BOT_TOKEN")).build()
app.add_handler(CommandHandler("active", active))
app.run_polling()