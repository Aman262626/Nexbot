import subprocess
import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

process = None

async def start_bot():
    global process
    process = subprocess.Popen(
        ["python", "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global process

    if not process:
        await start_bot()

    user_msg = update.message.text + "\n"

    process.stdin.write(user_msg)
    process.stdin.flush()

    await asyncio.sleep(2)

    output = ""

    while True:
        line = process.stdout.readline()
        if not line:
            break
        output += line
        if "NexGPT" in line:
            break

    if not output.strip():
        output = "No response."

    await update.message.reply_text(output)


async def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await start_bot()

    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
