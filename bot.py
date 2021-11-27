from telebot import TeleBot
import generator
import database
import wave
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
    print("Message from user: ", message.from_user.first_name)
    if message.text == "1":
        bot.send_message(message.from_user.id, "Cooking up....")
        list_of_dir = ["Samples/Cymbals", "Samples/Kick Drums", "Samples/Claps", "Samples/808s"]
        list_of_samples_names = [generator.get_random_file(i) for i in list_of_dir]
        # for i in list_of_samples_names:
        #     print("FILE: ", i)
        list_samp = generator.readSamples(list_of_samples_names)
        instrumental, sample_rate, sample_width = generator.read_wav(generator.get_random_file("Samples2"))
        channels_out = generator.sum_of_channels(generator.generate_notrnd_music(list_samp), instrumental)
        generator.write_wav("bot_result.wav", channels_out, 44100, 2)
        bot.send_audio(message.from_user.id, audio=open("bot_result.wav", 'rb'))
    if message.text == "2":
        bot.send_message(message.from_user.id, "Ого, а ты творец! Скидывай мне в сообщения файлы в формате .wav(не сжатые, иначе я их проигнорирую), а когда закончишь - напиши мне '3' и я скину результат")
    if message.text == "3":
        list_of_samples_names = database.get_by_id(message.from_user.id)
        database.clear(message.from_user.id)
        if len(list_of_samples_names) == 0:
            bot.send_message(message.from_user.id, "Ты не отправил файлы или что-то сломалось;( А еще я медленный, так что может быть просто не успел все обработать")
            return

        bot.send_message(message.from_user.id, "Try to open your files....")
        list_samp = generator.readSamples(list_of_samples_names)
        bot.send_message(message.from_user.id, "Cooking up....")

        # instrumental, sample_rate, sample_width = generator.read_wav(generator.get_random_file("Samples2"))
        # channels_out = generator.sum_of_channels(generator.generate_notrnd_music(list_samp), instrumental)
        generator.write_wav("bot_result.wav", generator.generate_music(list_samp), 44100, 2)
        bot.send_audio(message.from_user.id, audio=open("bot_result.wav", 'rb'))



@bot.message_handler(content_types=["audio"])
def handle_docs_document(message):
    print("Audio from user:", message.from_user.first_name)
    file_info = bot.get_file(message.audio.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
    if not os.path.exists("audios/" + str(message.from_user.id)):
        os.makedirs("audios/" + str(message.from_user.id))
    filename = "audios/" + str(message.from_user.id) + "/" + str(file_info.file_id) + ".wav"
    with open(filename, 'wb') as f:
        f.write(file.content)
    try:
        wav_file = wave.open(filename, 'r')
    except wave.Error:
        print("Incorret file" + filename)
        bot.send_message(message.from_user.id, "Ну и что за хрень ты скинул?")
        return
    database.insert(message.from_user.id, filename)
    bot.send_message(message.from_user.id, "Я скушал твой файл))")

@bot.message_handler(content_types=["document"])
def handle_docs_document(message):
    print("Document from user:", message.from_user.first_name)
    file_info = bot.get_file(message.document.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
    if not os.path.exists("audios/" + str(message.from_user.id)):
        os.makedirs("audios/" + str(message.from_user.id))
    filename = "audios/" + str(message.from_user.id) + "/" + str(file_info.file_id) + ".wav"
    with open(filename, 'wb') as f:
        f.write(file.content)
    try:
        wav_file = wave.open(filename, 'r')
    except wave.Error:
        print("Incorret file" + filename)
        bot.send_message(message.from_user.id, "Ну и что за хрень ты скинул, да еще и документ а не аудио?")
        return
    database.insert(message.from_user.id, filename)
    bot.send_message(message.from_user.id, "Я скушал твой файл))")
bot.polling(none_stop=True, interval=0)