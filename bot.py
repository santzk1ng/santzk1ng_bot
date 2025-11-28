import telebot
import easyocr
from PIL import Image
import io

TOKEN = "8563989647:AAGuEH-4Q99pqGzeaLuVTv0uYm-jS-kZyco"

bot = telebot.TeleBot(TOKEN)
ocr = easyocr.Reader(['pt'])  # OCR em português

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Fala irmão! Manda o print que eu leio tudo pra tu!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)

        img = Image.open(io.BytesIO(downloaded))

        result = ocr.readtext(downloaded, detail=0)

        text = "\n".join(result)

        bot.send_message(message.chat.id, "Extraí isso do print:\n\n" + text)

    except Exception as e:
        bot.send_message(message.chat.id, f"Erro ao processar a imagem: {e}")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, "Manda a imagem do resultado que eu faço a leitura.")

bot.polling()
