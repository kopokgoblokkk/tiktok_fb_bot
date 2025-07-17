from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from tiktok_downloader import download_tiktok
from fb_uploader import upload_to_facebook
import os

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "tiktok.com" in text:
        await update.message.reply_text("📥 Mendownload...")
        video = download_tiktok(text)
        if video:
            await update.message.reply_text("📤 Mengunggah ke Facebook...")
            result = upload_to_facebook(video)
            if "id" in result:
                await update.message.reply_text("✅ Sukses diunggah ke Fanspage!")
            else:
                await update.message.reply_text("❌ Gagal upload ke Facebook.")
            os.remove(video)
        else:
            await update.message.reply_text("❌ Gagal download video.")
    else:
        await update.message.reply_text("Kirimkan link TikTok.")

if __name__ == "__main__":
    from config import TELEGRAM_TOKEN
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot aktif...")
    app.run_polling()
