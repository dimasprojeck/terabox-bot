import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from terabox_uploader import upload_file_to_terabox
import os
import requests

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Kirim link TeraBox atau gambar untuk diupload ke akun kamu.")

# Handle foto yang dikirim
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]  # ambil foto resolusi tertinggi
    file = await photo.get_file()
    file_path = f"temp_{update.message.from_user.id}.jpg"
    await file.download_to_drive(file_path)

    await update.message.reply_text("📥 Mengunduh gambar...")

    # Upload ke TeraBox
    link = upload_file_to_terabox("local_upload", file_path)

    await update.message.reply_text(
        f"✅ File berhasil diupload:\n{link}"
    )
    os.remove(file_path)

# Handle teks (link TeraBox)
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text.strip()
    if "terabox.com" not in link:
        await update.message.reply_text("❌ Itu bukan link TeraBox.")
        return

    await update.message.reply_text("📥 Mendownload dari link...")

    uploaded_link = upload_file_to_terabox(link)
    await update.message.reply_text(
        f"✅ File berhasil diupload:\n{uploaded_link}"
    )

# Main function
def main():
    BOT_TOKEN = "7898157058:AAFeG9RUG9BNi8S47Ea7lgRB65Vq_zGhy50"  # Ganti dengan token dari BotFather
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    print("🚀 Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
