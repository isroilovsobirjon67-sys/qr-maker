import telebot
import qrcode
import io

# Bot tokeningiz
TOKEN = '8990800228:AAGoRWttZ1VwyKR23Yzs7fIxpq20XyPRTX8'
bot = telebot.TeleBot(TOKEN)

# /start buyrug'i
@bot.message_handler(commands=['start'])
def start_message(message):
    user_name = message.from_user.first_name
    bot.reply_to(
        message, 
        f"👋 Salom, {user_name}! QR maker botiga xush kelibsiz! 🎯\n\n"
        "Men siz yuborgan har qanday kontentni 1 soniyada sifatli va chiroyli QR-kodga aylantirib beraman! 🚀\n\n"
        "Yordam uchun /help buyrug'ini bosing."
    )

# /help buyrug'i
@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = (
        "📖 <b>Botdan foydalanish yo'riqnomasi:</b>\n\n"
        "• Matn yoki ssilkalar (link) yuboring -> Matnli QR-kod olasiz.\n"
        "• Rasm, dokument yoki media fayl yuboring -> Fayl havolasiga QR-kod chiqadi.\n\n"
        "⚡️ Tezkor, oson va 100% bepul xizmat!"
    )
    bot.reply_to(message, help_text, parse_mode='HTML')

# Barcha turdagi xabarlarni qayta ishlash
@bot.message_handler(content_types=['text', 'photo', 'document', 'audio', 'video', 'voice'])
def handle_all(message):
    final_link = ""

    # 1. Matn yoki havola
    if message.content_type == 'text':
        final_link = message.text
    
    # 2. Fayl, rasm yoki media
    else:
        file_id = None
        if message.content_type == 'photo':
            file_id = message.photo[-1].file_id
        elif message.content_type == 'document':
            file_id = message.document.file_id
        elif message.content_type == 'audio':
            file_id = message.audio.file_id
        elif message.content_type == 'video':
            file_id = message.video.file_id
        elif message.content_type == 'voice':
            file_id = message.voice.file_id

        if file_id:
            try:
                file_info = bot.get_file(file_id)
                final_link = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
            except Exception as e:
                bot.reply_to(message, "❌ Fayl havolasini olishda xatolik yuz berdi.")
                return

    # 3. QR-kod yaratish va yuborish
    if final_link:
        try:
            qr = qrcode.make(final_link)
            in_memory_file = io.BytesIO()
            qr.save(in_memory_file, format='PNG')
            in_memory_file.seek(0)

            bot.send_photo(
                message.chat.id, 
                photo=in_memory_file, 
                caption="✨ <b>QR-kod tayyor!</b>\n\nSiz yuborgan kontent uchun QR-kod yaratildi. 🎯",
                parse_mode='HTML'
            )
        except Exception:
            bot.reply_to(message, "❌ QR-kod yaratishda texnik xatolik yuz berdi.")
    else:
        bot.reply_to(message, "❌ Iltimos, yaroqli matn yoki fayl yuboring.")

# Botni uzluksiz ishlash rejimi
print("Bot ishga tushdi...")
bot.infinity_polling()
