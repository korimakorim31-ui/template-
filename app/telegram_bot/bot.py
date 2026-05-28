"""Telegram bot for meme caption generation"""

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from app.config import settings
from app.services.meme_service import MemeService
import asyncio

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class MemeBot:
    """Telegram bot for meme caption generation"""
    
    def __init__(self):
        self.meme_service = MemeService()
        self.app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup command and message handlers"""
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("meme", self.meme_command))
        self.app.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        await update.message.reply_text(
            "🤖 Welcome to AI Crypto Meme Bot!\n\n"
            "Send me a meme image and I'll generate a funny crypto caption for it.\n\n"
            "Use /help for more commands."
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command handler"""
        help_text = """
        🚀 Available Commands:
        
        /start - Start the bot
        /help - Show this help message
        /meme - Generate a random crypto meme caption
        
        📸 Just send me a photo and I'll caption it!
        """
        await update.message.reply_text(help_text)
    
    async def meme_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Meme command handler"""
        await update.message.reply_text(
            "📸 Send me a meme image and I'll generate a funny crypto caption!\n\n"
            "Or use /meme with a topic: /meme bitcoin"
        )
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle photo messages"""
        try:
            await update.message.reply_text("⏳ Generating caption...")
            
            # Get photo file
            photo = update.message.photo[-1]
            file = await context.bot.get_file(photo.file_id)
            
            # Generate caption
            caption = await self.meme_service.generate_caption(
                image_url=file.file_path,
                topic="crypto",
                language="en",
            )
            
            await update.message.reply_text(
                f"💡 Suggested Caption:\n\n{caption}"
            )
        except Exception as e:
            logger.error(f"Error handling photo: {str(e)}")
            await update.message.reply_text(
                f"❌ Error generating caption: {str(e)}"
            )
    
    def run(self):
        """Run the bot"""
        logger.info("Starting Telegram bot...")
        self.app.run_polling()

if __name__ == "__main__":
    bot = MemeBot()
    bot.run()
