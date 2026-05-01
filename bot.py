import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from config import TELEGRAM_BOT_TOKEN
from services.claude import generate_claude_response
from services.huggingface import generate_huggingface_response

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /start command.
    """
    await update.message.reply_text("AI bot is ready. Send me a message to talk to Claude, or prefix with /hf to use Hugging Face!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles all incoming text messages. Routes to Claude or Hugging Face.
    """
    user_text = update.message.text
    
    if not user_text:
        return
        
    # Determine which AI to use and strip commands if present
    text_to_process = user_text
    use_huggingface = False
    
    if user_text.lower().startswith("/hf "):
        use_huggingface = True
        text_to_process = user_text[4:].strip()
    elif user_text.lower().startswith("/claude "):
        text_to_process = user_text[8:].strip()
        
    if not text_to_process:
        await update.message.reply_text("Please provide some text after the command.")
        return
        
    # Send "typing" action
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    # Process with the appropriate AI service
    if use_huggingface:
        response_text = generate_huggingface_response(text_to_process)
    else:
        response_text = generate_claude_response(text_to_process)
        
    # Fallback if no response is generated
    if not response_text or response_text.strip() == "":
        response_text = "I'm sorry, but I couldn't generate a response."
        
    # Send the response back to the user
    await update.message.reply_text(response_text)

def main():
    """
    Main function to start the bot using polling.
    """
    logger.info("Starting Telegram AI Bot...")
    
    # Initialize the application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers (first match handles the update in group 0)
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Start polling (NOT webhook)
    logger.info("Bot is polling for updates...")
    application.run_polling()

if __name__ == '__main__':
    main()
