import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from agent_utils import set_agent_status, init_db, update_last_seen
import logging
import asyncio

load_dotenv()
init_db()

logging.basicConfig(level=logging.INFO)

app = ApplicationBuilder().token(os.getenv("ADMIN_BOT_TOKEN")).build()

active_agents = set()

def is_authorized(user_id):
    return True  # Replace with real authorization check

async def activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_authorized(user.id):
        await update.message.reply_text("Unauthorized")
        return
    set_agent_status(user.id, user.username, user.full_name, 1)
    update_last_seen(user.id)
    active_agents.add(user.id)
    await update.message.reply_text("Activated")

async def deactivate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_authorized(user.id):
        await update.message.reply_text("Unauthorized")
        return
    set_agent_status(user.id, user.username, user.full_name, 0)
    active_agents.discard(user.id)
    await update.message.reply_text("Deactivated")

async def send_heartbeat():
    while True:
        for agent_id in list(active_agents):
            update_last_seen(agent_id)
        await asyncio.sleep(60)

app.add_handler(CommandHandler("activate", activate))
app.add_handler(CommandHandler("deactivate", deactivate))

async def main():
    asyncio.create_task(send_heartbeat())
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())