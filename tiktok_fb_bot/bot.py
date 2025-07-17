import os
import logging
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from config import TELEGRAM_TOKEN, FB_PAGE_ID, FB_ACCESS_TOKEN
from tiktok_downloader import download_tiktok
from fb_uploader import upload_to_facebook

# ======= Fungsi untuk resolve shortlink TikTok =======
def resolve_tiktok_link(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        return response.url
    except Exception as e:
        print("❌ Gagal resolve link TikTok:", e)
        return None

# ======= LOGGING AKTIVITAS ========
logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ======= ADMIN TELEGRAM ID ========
ADMIN_ID = 123456789  # Ganti dengan ID Telegram kamu

# ======= /start dan /help ========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Maaf, bot ini hanya untuk admin.")
        return
    await update.message.reply_text("👋 Kirim link TikTok ke sini, nanti saya upload ke Fanspage otomatis!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Cukup kirim link TikTok, saya akan unduh dan unggah ke Fanspage Facebook.")

# ======= Handler Pesan Utama ========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text

    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Maaf, bot ini hanya untuk admin.")
        return

    if "tiktok.com" not in message:
        await update.message.reply_text("⚠️ Kirim link TikTok yang valid.")
        return

    if "vm.tiktok.com" in message:
        resolved = resolve_tiktok_link(message)
        if not resolved:
            await update.message.reply_text("❌ Gagal memproses link pendek TikTok.")
            return
        message = resolved

    logging.info(f"User {user_id} mengirim link: {message}")
    msg = await update.message.reply_text("📥 Sedang mengunduh video dari TikTok...")

    video_path = download_tiktok(message)
    if not video_path:
        await msg.edit_text("❌ Gagal mengunduh video.")
        logging.error("Gagal unduh video TikTok.")
        return

    await msg.edit_text("📤 Mengunggah video ke Facebook Fanspage...")

    success = upload_to_facebook(video_path, FB_PAGE_ID, FB_ACCESS_TOKEN)

    if success:
        await msg.edit_text("✅ Video berhasil diunggah ke Fanspage.")
        logging.info("Upload sukses.")
    else:
        await msg.edit_text("❌ Gagal upload ke Facebook.")
        logging.error("Upload gagal.")

    os.remove(video_path)

# ======= MAIN ========
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == '__main__':
    main()
