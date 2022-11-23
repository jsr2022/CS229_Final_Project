import numpy as np
import pandas as pd
import librosa
import pydub
import wave
import pydub
import scipy
import matplotlib.pyplot as plt


class Sound_Analysis:

    def __init__(self):
        self.attributes = {'num_channels': 0, 'sample_width': 0, 'frame_rate': 0, 'frame_width': 0, 'length': 0,
                           'frame_count': 0, 'intensity': 0}
        self.librosa_rms_norm = None


    def create_obj(self, path_and_song, song_name):
        pydub_sound = pydub.AudioSegment.from_file(path_and_song, format="wav")
        self.attach_attributes(pydub_sound)
        self.song_name = song_name

        # Prepping Librosa Setup
        bool_mono = True
        #if self.attributes['num_channels'] == 2:
        #    bool_mono = False #two channel = 16 bytes single channel = 8 bytes
        # Librosa Audio                                          #Lowering Frame Rate (Default is 44,000 per sec sr=self.attributes['frame_count']
        librosa_audio_ts, sample_rate = librosa.load(path_and_song, sr=1000, mono=bool_mono)
        fr_len = len(librosa_audio_ts)
        librosa_rms = librosa.feature.rms(y=librosa_audio_ts, frame_length=fr_len).T
        librosa_rms_norm = librosa.util.normalize(S=librosa_rms)
        t = np.linspace(0, (self.attributes['length'] / 1000), len(librosa_rms_norm))
        self.librosa_rms_norm = librosa_rms_norm
        self.librosa_rms_time = t
        self.plot_rms(librosa_rms_norm, t)


    def attach_attributes(self, sound):
        self.attributes['num_channels'] = sound.channels
        self.attributes['sample_width'] = sound.sample_width
        self.attributes['frame_rate'] = sound.frame_rate
        self.attributes['frame_width'] = sound.frame_width
        self.attributes['length'] = len(sound)  # in milliseconds
        self.attributes['frame_count'] = sound.frame_count()
        self.attributes['intensity'] = sound.max_dBFS

    def plot_rms(self, rms, t):
        plt.figure()
        plt.plot(t, rms)
        plt.title(self.song_name)
        plt.xlabel("Song Time [S]")
        plt.ylabel("Normalized RMS of Volume/Intensity")
        plt.show()


