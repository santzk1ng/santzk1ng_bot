import telebot

TOKEN = "8563989647:AAFQXyZltk7T4-GugA7UY_pcP4RRDmnNCYA"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Fala irmão, o bot do santzk1ng tá ON!")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, f"Recebi: {message.text}")

bot.polling()
