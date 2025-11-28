import telebot

TOKEN = "8563989647:AAFQXyZltk7T4-GugA7UY_pcP4RRDmnNCYA"

bot = telebot.TeleBot(TOKEN)

# Comando /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Fala irmão, o bot do santzk1ng tá ON!")

# Receber FOTO
@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    bot.send_message(message.chat.id, "Recebi a imagem irmão!")

# Responder qualquer TEXTO
@bot.message_handler(func=lambda m: True, content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, f"Recebi: {message.text}")

bot.polling()

