import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from services.google_sheets import write_to_sheet  # corrected import
from services.chatgpt import generate_response

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

AUTHORIZED_USERS = [1249737429, 1232363365]  # Replace these numbers with your actual Telegram IDs

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the user is authorized
    if update.effective_user.id not in AUTHORIZED_USERS:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this bot.")
        return

    logging.info(f"Received update_id: {update.update_id}, text: {update.message.text}")
    user_message = update.message.text
    chatgpt_response_b, chatgpt_response_c = write_to_sheet('1O4fKy9WYVEljNWQjC73mf3WBcIBnC_sOOZNnQhLg_pc', 'A',
                                                            [[user_message]])
    logging.info(f'ChatGPT Response B: {chatgpt_response_b}')
    logging.info(f'ChatGPT Response C: {chatgpt_response_c}')
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Message received!")


if __name__ == '__main__':
    application = ApplicationBuilder().token('6666206665:AAFiqsOyv0zD54FzEvLiAzTzdE46SHEuNG0').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    application.add_handler(message_handler)

    application.run_polling()
