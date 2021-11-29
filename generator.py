#!/usr/bin/env python3
import wave
import random
import os

INPUT_FILE = "Samples2/MV2 - STR Vibra.wav"
INPUT_FILE2 = "sounds/mad-world.wav"
INPUT_FILE_LIST = ["Samples/Cymbals/Hihat Closed 031 Super Hero Music.wav", "Samples/Claps/Clap 018 Cardiak.wav",
                   "Samples/Kick Drums/Kick Drum 001 Tight.wav", "Samples/808s/808 Bass G#m Boom Kick Hi.wav"]

OUTPUT_FILE = "not_so_random.wav"


# SOME USELESS NOTES ABOUT GENERATION
# HiHat smth - fast / / / / // / / // / // //
# Kick - 2
# snare - 3
# Bass - Not so fast, can damage a lot
# Clap - 1
# Melody - can't generate this so easy

def get_random_file(directory):  # Getting path to random file in directory
    n = 0
    random.seed()
    for root, dirs, files in os.walk(directory):
        for name in files:
            n += 1
            if random.uniform(0, n) < 1:
                rfile = os.path.join(root, name)
    return rfile


def sum_of_channels(channels, channels2):  # getting sum of two audio lines
    if len(channels[0]) < len(channels2[0]):
        channels, channels2 = channels2, channels
    result = [[0] * len(ch) for ch in channels]

    n_channels = len(channels)
    for k in range(n_channels):
        for i in range(len(channels[k])):
            result[k][i] = channels[k][i]
            if (k < len(channels2) and i < len(channels2[k])):
                result[k][i] += channels2[k][i]
    return result


def sum_of_channels_from_pos(channels, channels2, pos):  # add second audio line to the first from pos position
    n_channels = len(channels)
    for k in range(n_channels):
        for i in range(len(channels2[k])):
            if i + pos >= len(channels[k]):
                print("ERROR!\n!\n!\n!\nfirst channel too small\n\n\n")
                return channels
            channels[k][i + pos] += channels2[k][i]

    return channels


def concatenate_of_channles(channel, channel2):  # concatenate two audios
    for i in range(len(channel)):
        for j in channel2[i]:
            channel[i].append(j)
    return channel


# Making loop with random pauses(from pause_time list) between beats. There are beats_count  beatsin one lopp.
# Then looping it up to duration time
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
        result = sum_of_channels_from_pos(result, channel, delay)
    # print("End Sample")
    return clear_back(result)


def generate_music(list_of_channels, duration=20):  # getting list of audios and generating random beat
    result = [[], []]
    for i in range(len(list_of_channels)):
        channel = list_of_channels[i]
        pause_time = [0.4, 0.6, 0.8, 0.8, 0.9, 1., 1.1]
        loop_sample = clear_back(random_mix_of_beat(channel, duration=duration, beats_count=10, pause_time=pause_time))
        result = sum_of_channels(loop_sample, result)
    return result


def generate_notrnd_music(list_of_channels,
                          duration=20):  # same as generate_music but trying to make smth not so random and pretty
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

        loop_sample = clear_back(random_mix_of_beat(channel, duration=duration, beats_count=10, pause_time=pause_time))
        result = sum_of_channels(loop_sample, result)

    return result


def clear_back(channel):  # deleting silence from the end
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


def cut_big_file(channels, sample_rate = 44100, max_duration = 5):
    result = [[] for i in range(len(channels))]
    mx_len = sample_rate * max_duration
    for i in range(len(channels)):
        for j in range(min(mx_len, len(channels[i]))):
            result[i].append(channels[i][j])
    return result



def readSamples(list_of_samples=INPUT_FILE_LIST):  # reading audio lines from list of files
    res = []
    for i in list_of_samples:
        channels, sample_rate, sample_width = read_wav(i)
        res.append(channels)
    return res


################################################################################
# Вспомогательный код, основа взята у Артема Таболина https://github.com/citxx/dsp-class
################################################################################


def read_wav(filename):
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
