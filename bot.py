from telebot import TeleBot
import generator
import requests # request нужен для загрузки файлов от пользователя

import os
import random
token = '2086005166:AAFMFBM38e3eXiPp-mG79CfEbegfB36Cvec'
bot = TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
                 'Привет, ' + message.from_user.first_name + '! Я бот, который умеет генерировать простенькую музыку, напиши мне "1" и я покажу что умею, или напиши "2" и попробуем что-то сделать из твоих звуков!')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # bot.send_message(message.from_user.id, "Напиши '1', чтобы сгенерить бит")
    if message.text == "1":
        bot.send_message(message.from_user.id, "Cooking up....")
        list_of_dir = ["Samples/Cymbals", "Samples/Kick Drums", "Samples/Claps", "Samples/808s"]
        list_of_samples_names = [generator.get_random_file(i) for i in list_of_dir]
        for i in list_of_samples_names:
            print("FILE: ", i)
        list_samp = generator.readSamples(list_of_samples_names)
        instrumental, sample_rate, sample_width = generator.read_wav(generator.get_random_file("Samples2"))
        channels_out = generator.sum_of_channels(generator.generate_notrnd_music(list_samp), instrumental)
        generator.write_wav("bot_result.wav", channels_out, 44100, 2)
        bot.send_audio(message.from_user.id, audio=open("bot_result.wav", 'rb'))
    if message.text == "2":
        bot.send_message(message.from_user.id, "Ого, а ты творец! Скидывай мне в сообщения файлы в формате .wav(не сжатые, иначе я их проигнорирую), а когда закончишь - напиши мне '3' и я скину результат")

5
@bot.message_handler(content_types=["audio"])
def handle_docs_document(message):
    file_info = bot.get_file(message.audio.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
    # fileobj = open("audios/3.wav", "w+")
    with open("audios/3.wav", 'wb') as f:
        f.write(file.content)
bot.polling(none_stop=True, interval=0)
