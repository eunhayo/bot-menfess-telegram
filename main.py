import os
import telebot
from flask import Flask

# Mengambil data rahasia dari environment variable server
API_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

bot = telebot.TeleBot(API_TOKEN)

# Fitur tambahan agar server Render tidak mati (Web Server dummy)
app = Flask('')
@app.route('/')
def home():
    return "Bot Menfess is Running!"

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_menfess(message):
    if "[fess]" in message.text.lower():
        try:
            # Kirim ulang pesan secara anonim ke channel
            bot.send_message(CHANNEL_ID, message.text)
            bot.reply_to(message, "✅ Menfess kamu sudah terkirim secara anonim ke Channel!")
        except Exception as e:
            bot.reply_to(message, "❌ Gagal mengirim. Pastikan bot sudah menjadi admin di channel.")
    else:
        bot.reply_to(message, "⚠️ Gagal. Pesan kamu harus mengandung kata '[fess]' agar terkirim.")

# Menjalankan bot
if __name__ == "__main__":
    import threading
    # Jalankan bot di thread terpisah agar web server tetap merespon
    threading.Thread(target=bot.infinity_polling).start()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
