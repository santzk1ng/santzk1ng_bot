import telebot
import requests
import os
import base64
import io
from PIL import Image

TOKEN = os.getenv("TOKEN")
VISION_KEY = os.getenv("GOOGLE_VISION_KEY")

bot = telebot.TeleBot(TOKEN)

VISION_URL = f"https://vision.googleapis.com/v1/images:annotate?key={VISION_KEY}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Fala irmão! Manda o print que eu leio tudo pra tu!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # baixar imagem
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)

        img_base64 = base64.b64encode(downloaded).decode()

        # enviar pra API google vision
        payload = {
            "requests": [
                {
                    "image": {"content": img_base64},
                    "features": [{"type": "TEXT_DETECTION"}]
                }
            ]
        }

        response = requests.post(VISION_URL, json=payload)
        data = response.json()

        text = data["responses"][0].get("fullTextAnnotation", {}).get("text", "")

        if not text:
            bot.send_message(message.chat.id, "Não consegui ler nada irmão. Tenta mandar de novo.")
            return

        bot.send_message(message.chat.id, "Extraí isso do print:\n\n" + text)

    except Exception as e:
        bot.send_message(message.chat.id, f"Erro ao processar a imagem: {e}")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, "Manda o print da tabela que eu leio pra tu!")

bot.polling()
