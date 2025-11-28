import telebot
import requests
import os
from PIL import Image
import io

TOKEN = os.getenv("TOKEN")  # pega o token do Render

bot = telebot.TeleBot(TOKEN)

OCR_URL = "https://api.ocr.space/parse/image"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Fala irmão! Manda a imagem da tabela que eu leio tudo pra tu.")

@bot.message_handler(content_types=['photo'])
def process_image(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)

        # Enviar imagem para OCR API
        response = requests.post(
            OCR_URL,
            files={"file": ("image.jpg", downloaded)},
            data={"language": "por"},
        )

        result = response.json()

        if result.get("ParsedResults"):
            text = result["ParsedResults"][0]["ParsedText"]
            bot.send_message(message.chat.id, "Texto extraído:\n\n" + text)
        else:
            bot.send_message(message.chat.id, "Não consegui ler nada do print.")

    except Exception as e:
        bot.send_message(message.chat.id, f"Erro ao processar: {e}")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, "Manda a imagem do resultado que eu faço a leitura.")

bot.polling()
