#!/usr/bin/env python3

import wave
import random
import os
# import numpy as np
# import subprocess
# import sounddevice as sd  # for opening bad wav files
# import scipy.io.wavfile as wavee

# Шаблон для обработки звука.
#
# В секции "вспомогательный код" внизу файла уже написаны функции для чтения
# и записи .wav файлов (read_wav и write_wav).
#
# В основной функции main:
# 1. Читается .wav файл, путь к которому указан в переменной INPUT_FILE
# 2. Вызывается функция process, которая должна обработать сигнал и вернуть
#    результат обработки
# 3. Результат проверяется на корректность (количество каналов, равное количество
#    сэмплов в канале и т.д.)
# 4. Результат записывается в .wav файл, путь к которому указан в переменной
#    OUTPUT_FILE
#
# Как сделать новый фильтр:
# 1. Определить новую функцию, используя change_amp как пример
# 2. Изменить функцию process, чтобы она использовала новый фильтр для обработки
#    и возвращала результат
# 3. Если вы хотите применить к исходному сигналу несколько разных фильтров,
#    то можно последовательно вызвать эти фильтры в функции process

# Тут можно поменять пути к входному и результирующему файлам
INPUT_FILE = "Samples2/MV2 - STR Vibra.wav"
INPUT_FILE2 = "sounds/mad-world.wav"
INPUT_FILE_LIST = ["Samples/Cymbals/Hihat Closed 031 Super Hero Music.wav", "Samples/Claps/Clap 018 Cardiak.wav",
                   "Samples/Kick Drums/Kick Drum 001 Tight.wav", "Samples/808s/808 Bass G#m Boom Kick Hi.wav"]

OUTPUT_FILE = "not_so_random.wav"


# HiHat smth - fast / / / / // / / // / // //
# Kick - 2
# snare
# Bass
# Clap - 1
# Melody - TODO

def get_random_file(directory):
    n = 0
    random.seed()
    for root, dirs, files in os.walk(directory):
        for name in files:
            n += 1
            if random.uniform(0, n) < 1: rfile = os.path.join(root, name)
    return rfile


def sum_of_channels(channels, channels2):
    # Двумерный список для результирующего сигнала такого же размера, как channels
    # Если  в сhannels2 больше, то очень жаль
    if len(channels[0]) < len(channels2[0]):
        channels, channels2 = channels2, channels
    result = [[0] * len(ch) for ch in channels]

    # Код для обработки аудио-сигнала.
    n_channels = len(channels)
    for k in range(n_channels):
        for i in range(len(channels[k])):
            result[k][i] = channels[k][i]
            if (k < len(channels2) and i < len(channels2[k])):
                result[k][i] += channels2[k][i]
    return result


def sum_of_channels_from_pos(channels, channels2, pos):
    # Двумерный список для результирующего сигнала такого же размера, как channels
    # Если  в сhannels2 больше, то очень жаль
    # Код для обработки аудио-сигнала.
    n_channels = len(channels)
    for k in range(n_channels):
        for i in range(len(channels2[k])):
            if i + pos >= len(channels[k]):
                print("ERROR!\n!\n!\n!\nfirst channel too small\n\n\n")
                return channels
            channels[k][i + pos] += channels2[k][i]

    return channels


def concatenate_of_channles(channel, channel2):
    for i in range(len(channel)):
        for j in channel2[i]:
            channel[i].append(j)
    return channel


def try_make_beat(channel, sample_rate=44800):
    length = len(channel[0]) // sample_rate  # seconds
    k = sample_rate // 4
    dop = [[0 for i in range(k)] for j in range(len(channel))]
    # print(dop)
    dop = concatenate_of_channles(dop, channel)
    return sum_of_channels(dop, channel)


def random_mix_of_beat(channel, sample_rate=44100, beats_count=5, duration=20, pause_time=[0.4, 0.6, 0.8, 1.]):
    # print("Starting another sample...")

    pause_len = [int(pause_time[i] * sample_rate) for i in range(len(pause_time))]
    random_pause = [pause_len[random.randint(0, len(pause_len) - 1)] for i in range(beats_count)]
    loop_duration = 0
    loop_size = len(random_pause)
    for i in random_pause:
        loop_duration += i
    for j in range(((duration * sample_rate) // loop_duration) * loop_size):
        random_pause.append(random_pause[j])
    result = [[0 for i in range(sample_rate * (duration * 5 // 2) + len(channel[j]))] for j in range(len(channel))]
    delay = 0
    for cur_pause in random_pause:
        delay += cur_pause
        # dop2 = [[0 for i in range(delay)] for j in range(len(channel))]
        # dop2 = concatenate_of_channles(dop2, channel)
        # result = sum_of_channels(result, dop2)
        result = sum_of_channels_from_pos(result, channel, delay)
    # print("End Sample")
    return clear_back(result)


def generate_music(list_of_channels, duration=10):
    result = [[], []]
    for i in range(len(list_of_channels)):
        channel = list_of_channels[i]
        pause_time = [0.4, 0.6, 0.8, 0.8, 0.9, 1., 1.1]

        # for generating smth not so random
        # if i == 0: # Hi Hat
        #     pause_time = [0.2, 0.2, 0.2, 0.2, 0.3, 0.1, 0.1]
        # elif i == 1: # Clap
        #     pause_time = [0.5, 0.7, 0.7, 0.8, 0.9, 0.9, 1.2, 1.]
        # elif i == 2: # Kick
        #     pause_time = [2.5, 3.1, 2.1]
        # elif i == 3: # Bass
        #     pause_time = [0.8, 0.8, 0.9, 1., 1.1]

        loop_sample = clear_back(random_mix_of_beat(channel, beats_count=10, pause_time=pause_time))
        loop = loop_sample
        # for i in range(2):
        # loop = concatenate_of_channles(loop, loop_sample)
        # print("kek", i)

        result = sum_of_channels(loop, result)

    return result


def generate_notrnd_music(list_of_channels, duration=10):
    result = [[], []]
    for i in range(len(list_of_channels)):
        channel = list_of_channels[i]
        pause_time = [0.4, 0.6, 0.8, 0.8, 0.9, 1., 1.1]

        # for generating smth not so random
        if i == 0:  # Hi Hat
            pause_time = [0.25, 0.25, 0.25, 0.4, 0.3, 0.2, 0.1]
        elif i == 1:  # Clap
            pause_time = [0.5, 0.6, 0.7, 0.8, 0.9, 0.9, 1.2, 1.]
        elif i == 2:  # Kick
            pause_time = [2.5, 3.1, 2.1]
        elif i == 3:  # Bass
            pause_time = [0.8, 0.8, 0.9, 1., 1.1]

        loop_sample = clear_back(random_mix_of_beat(channel, beats_count=10, pause_time=pause_time))
        loop = loop_sample
        # for i in range(2):
        # loop = concatenate_of_channles(loop, loop_sample)
        # print("kek", i)

        result = sum_of_channels(loop, result)

    return result


def clear_back(channel):
    bl = True
    while bl:
        for i in channel:
            if len(i) <= 1:
                continue
            if i[-1] != 0:
                bl = False
        if bl:
            for i in range(len(channel)):
                channel[i].pop()
    return channel


def readSamples(list_of_samples=INPUT_FILE_LIST):
    res = []
    for i in list_of_samples:
        channels, sample_rate, sample_width = read_wav(i)
        res.append(channels)
    return res


def main():
    instrumental, sample_rate, sample_width = read_wav(INPUT_FILE)
    # channels2, sample_rate2, sample_width2 = read_wav(INPUT_FILE2)

    # print('Обработка... ', end='')
    list_samp = readSamples()

    channels_out = sum_of_channels(generate_music(list_samp), instrumental)

    # channels_out = concatenate_of_channles(channels, channels2)
    #
    if not check_result(channels_out):
        return
    # print('Готово')
    write_wav(OUTPUT_FILE, channels_out, 44100, 2)


################################################################################
# Вспомогательный код
################################################################################


def read_wav(filename):
    # myrecording = sd.rec(int(5 * 44100), samplerate=44100, channels=2)
    # sd.wait()  # Wait until recording is finished
    # wavee.write(filename, 44100, myrecording.astype(np.int16))
    try:
        wav_file = wave.open(filename, 'r')
    except wave.Error:
        print("ERROR\n!\n!\n!\n!\n!\n" + filename)
        channels = [[0 for i in range(44100 * 3)] for j in range(2)]
        return channels, 44100, 2
    # print("Trying to open: ", filename, end=' ')
    # print("Succes!")

    n_channels = wav_file.getnchannels()
    # print('Количество каналов:', n_channels)

    sample_width = wav_file.getsampwidth()
    # print('Размер сэмпла:', sample_width)

    sample_rate = wav_file.getframerate()
    # print('Частота сэмплирования:', sample_rate)

    n_frames = wav_file.getnframes()
    # print('Количество фреймов:', n_frames)

    mn, mx = bounds_for_sample_width(sample_width)

    # print('\nЧтение файла... ', end='')
    frames = wav_file.readframes(n_frames)
    all_samples = [
        (int.from_bytes(frames[i:i + sample_width], byteorder='little', signed=True) - mn) / (mx - mn) * 2 - 1
        for i in range(0, len(frames), sample_width)
    ]
    channels = [all_samples[i::n_channels] for i in range(n_channels)]
    # print('Готово')
    # print(channels)
    return channels, sample_rate, sample_width


def write_wav(filename, channels, sample_rate, sample_width):
    # print('Запись файла... ', end='')

    mn, mx = bounds_for_sample_width(sample_width)

    all_samples = (min(max(-1, sample), 1) for frame in zip(*channels) for sample in frame)
    frames = b''.join(
        round((sample + 1) / 2 * (mx - mn) + mn).to_bytes(sample_width, byteorder='little', signed=True) for sample in
        all_samples)

    result_wav = wave.open(filename, 'w')
    result_wav.setnchannels(len(channels))
    result_wav.setsampwidth(sample_width)
    result_wav.setframerate(sample_rate)
    result_wav.setnframes(len(channels[0]))
    result_wav.writeframes(frames)
    # print('Готово')


def check_result(channel_samples):
    if len(channel_samples) == 0:
        print('Ошибка: результат обработки содержит 0 каналов')
        return False

    for i in range(len(channel_samples)):
        len_0 = len(channel_samples[0])
        len_i = len(channel_samples[i])
        if len_0 != len_i:
            print('Ошибка: количество сэмплов в каналах 1 ({}) и {} ({}) не совпадает'.format(len_0, i + 1, len_i))
            return False

    # TODO: слишком большие сэмплы

    return True


def bounds_for_sample_width(sample_width):
    power = 1 << (8 * sample_width - 1)
    return -power, power - 1

