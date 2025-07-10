import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# Configuration (replace with your links)
CHANNEL_LINK = "https://t.me/your_channel"
GROUP_LINK = "https://t.me/your_group"
TWITTER_LINK = "https://twitter.com/your_profile"
ADMIN_USER_ID = 12345678  # Your Telegram user ID for notifications
BOT_TOKEN = "7590734352:AAEsiYSPgpZAl_1exkKirjQz3K_j-GLXg9A"  # Your test token

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_msg = (
        f"👋 Hello {user.first_name}!\n\n"
        "🎉 Get FREE 10 SOL by completing these steps:\n\n"
        "1. Join our Telegram Channel\n"
        "2. Join our Telegram Group\n"
        "3. Follow our Twitter\n"
        "4. Submit your Solana wallet address"
    )
    
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("👥 Join Group", url=GROUP_LINK)],
        [InlineKeyboardButton("🐦 Follow Twitter", url=TWITTER_LINK)],
        [InlineKeyboardButton("✅ I've Joined", callback_data="joined")]
    ]
    
    await update.message.reply_text(
        welcome_msg,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("👇 Please send your Solana wallet address now:")

async def handle_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallet = update.message.text.strip()
    user = update.effective_user
    
    # Simple SOL address validation (basic pattern check)
    if not wallet.startswith("SOL") and len(wallet) > 30:  # Basic validation
        await update.message.reply_text("❌ Invalid Solana address. Please resend.")
        return
    
    # Send confirmation
    await update.message.reply_text(
        "🎉 Congratulations!\n"
        "10 SOL is on its way to your wallet!\n\n"
        f"Transaction ID: `TX{os.urandom(8).hex()}`\n"
        "Allow 24-48 hours for processing.",
        parse_mode="Markdown"
    )
    
    # Notify admin (optional)
    admin_msg = (
        f"⚠️ New Wallet Submission\n\n"
        f"User: {user.full_name} (@{user.username})\n"
        f"Wallet: `{wallet}`"
    )
    await context.bot.send_message(
        chat_id=ADMIN_USER_ID,
        text=admin_msg,
        parse_mode="Markdown"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_join, pattern="^joined$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet))
    
    # Webhook configuration for Render
    port = int(os.environ.get("PORT", 5000))
    webhook_url = os.getenv("WEBHOOK_URL")
    
    if webhook_url:
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path="/",
            webhook_url=f"{webhook_url}/"
        )
    else:
        print("Bot is running in polling mode...")
        app.run_polling()

if __name__ == "__main__":
    main()
