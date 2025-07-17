import os
import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import TELEGRAM_TOKEN, FB_PAGE_ID, FB_ACCESS_TOKEN
from tiktok_downloader import download_tiktok
from fb_uploader import upload_to_facebook

# ======= Fungsi untuk resolve shortlink TikTok =======
def resolve_tiktok_link(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        return response.url
    except Exception as e:
        print("? Gagal resolve link TikTok:", e)
        return None

# ======= LOGGING AKTIVITAS ========
logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ======= ADMIN TELEGRAM ID ========
ADMIN_ID = 7835929586  # Ganti dengan ID Telegram kamu

# ======= /start dan /help ========
def start(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("? Maaf, bot ini hanya untuk admin.")
        return
    update.message.reply_text("?? Kirim link TikTok ke sini, nanti saya upload ke Fanspage otomatis!")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("?? Cukup kirim link TikTok, saya akan unduh dan unggah ke Fanspage Facebook.")

# ======= Handler Pesan Utama ========
def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    message = update.message.text

    # Hanya admin yang bisa pakai
    if user_id != ADMIN_ID:
        update.message.reply_text("? Maaf, bot ini hanya untuk admin.")
        return

    # Validasi link TikTok
    if "tiktok.com" not in message:
        update.message.reply_text("?? Kirim link TikTok yang valid.")
        return

    # Resolve jika shortlink TikTok
    if "vm.tiktok.com" in message:
        resolved = resolve_tiktok_link(message)
        if not resolved:
            update.message.reply_text("? Gagal memproses link pendek TikTok.")
            return
        message = resolved

    logging.info(f"User {user_id} mengirim link: {message}")
    msg = update.message.reply_text("?? Sedang mengunduh video dari TikTok...")

    # Unduh video
    video_path = download_tiktok(message)
    if not video_path:
        msg.edit_text("? Gagal mengunduh video.")
        logging.error("Gagal unduh video TikTok.")
        return

    msg.edit_text("?? Mengunggah video ke Facebook Fanspage...")

    # Upload ke Facebook
    success = upload_to_facebook(video_path, FB_PAGE_ID, FB_ACCESS_TOKEN)

    if success:
        msg.edit_text("? Video berhasil diunggah ke Fanspage.")
        logging.info("Upload sukses.")
    else:
        msg.edit_text("? Gagal upload ke Facebook.")
        logging.error("Upload gagal.")

    os.remove(video_path)

# ======= MAIN ========
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

