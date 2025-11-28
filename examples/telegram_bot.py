"""
Telegram Bot Example - PHShorts Async API

This example shows how to integrate PHShorts with a Telegram bot
using the async API.

Requirements:
    pip install python-telegram-bot PHShorts

Note: This is a sample implementation. You'll need to:
1. Get a bot token from @BotFather on Telegram
2. Replace YOUR_BOT_TOKEN with your actual token
"""

import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PHShorts import AsyncVideoDownloader


# Replace with your bot token from BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "👋 Hi! Send me a PornHub Shorts URL and I'll download it for you!\n\n"
        "Example: https://www.pornhub.com/view_video.php?viewkey=xxxxx"
    )


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video download requests."""
    url = update.message.text.strip()
    
    # Validate URL
    if "pornhub.com" not in url:
        await update.message.reply_text("❌ Please send a valid PornHub URL!")
        return
    
    # Send initial message
    status_message = await update.message.reply_text("⏳ Processing your request...")
    
    try:
        # Initialize async downloader
        async with AsyncVideoDownloader(output_dir="./telegram_downloads") as downloader:
            # Get video info
            await status_message.edit_text("📋 Getting video information...")
            info = await downloader.get_info(url)
            
            # Update status
            await status_message.edit_text(
                f"⬇️ Downloading: {info['title']}\n"
                f"Quality: Best available ({max(info['available_qualities'])}p)"
            )
            
            # Download video
            video_path = await downloader.download(url, quality="best")
            
            # Send video to user
            await status_message.edit_text("📤 Uploading video...")
            
            with open(video_path, 'rb') as video_file:
                await update.message.reply_video(
                    video=video_file,
                    caption=f"✅ {info['title']}"
                )
            
            # Delete status message
            await status_message.delete()
            
    except Exception as e:
        await status_message.edit_text(f"❌ Error: {str(e)}")


def main():
    """Start the bot."""
    print("🤖 Starting Telegram Bot...")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    # Run bot
    print("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
