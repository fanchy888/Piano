import pygame
from scipy.io import wavfile
import numpy as np

KEY_NUMS = 48


def speedx(snd_array, factor):
    """ Speeds up / slows down a sound, by some factor. """
    indices = np.round(np.arange(0, len(snd_array), factor))
    indices = indices[indices < len(snd_array)].astype(int)
    return snd_array[indices]


def stretch(snd_array, factor, window_size, h):
    """ Stretches/shortens a sound, by some factor. """
    phase = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros(int(len(snd_array) / factor + window_size))

    for i in np.arange(0, len(snd_array) - (window_size + h), h*factor):
        i = int(i)
        # Two potentially overlapping subarrays
        a1 = snd_array[i: i + window_size]
        a2 = snd_array[i + h: i + window_size + h]

        # The spectra of these arrays
        s1 = np.fft.fft(hanning_window * a1)
        s2 = np.fft.fft(hanning_window * a2)

        # Rephase all frequencies
        phase = (phase + np.angle(s2/s1)) % 2*np.pi

        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
        i2 = int(i/factor)
        result[i2: i2 + window_size] += hanning_window*a2_rephased.real

    # normalize (16bit)
    result = ((2**(16-4)) * result/result.max())

    return result.astype('int16')


def pitchshift(snd_array, n, window_size=2**13, h=2**10):
    """ Changes the pitch of a sound by ``n`` semitones. """
    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    return speedx(stretched[window_size:], factor)


print('parsing sound file...')

fps, sound = wavfile.read("Music_Notes\\C.wav")
sound = sound[:, -1]
pygame.mixer.pre_init(fps, -16, 1, 512)
pygame.init()

file_names = ['C', 'C_s', 'D', 'D_s', 'E', 'F', 'F_s', 'G', 'G_s', 'A', 'Bb', 'B', 'C1', 'C_s1', 'D1', 'D_s1', 'E1', 'F1']
folder_name = "Music_Notes\\"
notes = []

for i in range(KEY_NUMS):
    note = pitchshift(sound, i - 24)
    note = np.array([[i, i] for i in note])
    notes.append(pygame.sndarray.make_sound(note))


keys = [
        'left ctrl', 'left alt', 'z', 'a', 'x', 's', 'c', 'd', 'v', 'f', 'b', 'g',
        'tab', '`', 'q', '1', 'w', '2', 'e', '3', 'r', '4', 't', '5',
        'n', 'h', 'm', 'j', ',', 'k', '.', 'l', '/', ';', "'", 'right alt',
        'y', '6', 'u', '7', 'i', '8', 'o', '9', 'p', '0', '[', '-'
        ]
KEYS = {x[0]: x[1] for x in zip(keys, notes)}

if __name__ == '__main__':
    print(len(notes), len(keys))

