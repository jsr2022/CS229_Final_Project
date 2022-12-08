# Python Modules
import numpy as np
import librosa
import matplotlib.pyplot as plt
import pydub
import wave
import scipy
import pandas as pd

class Sound_Analysis:

    def __init__(self):
        self.attributes = {'num_channels': 0, 'sample_width': 0, 'frame_rate': 0, 'frame_width': 0, 'length': 0,
                           'frame_count': 0, 'intensity': 0}
        self.librosa_rms_norm = None
        self.librosa_rms_time = None


    def create_obj(self, path_and_song, song_name):
        pydub_sound = pydub.AudioSegment.from_file(path_and_song, format="wav")
        self.attach_attributes(pydub_sound)
        self.song_name = song_name

        # Prepping Librosa Setup
        bool_mono = True
        #if self.attributes['num_channels'] == 2:
        #    bool_mono = False #two channel = 16 bytes single channel = 8 bytes
        # Librosa Audio                                          #Lowering Frame Rate (Default is 44,000 per sec sr=self.attributes['frame_count']
        song_sample_rate = 1000
        librosa_audio_ts, sample_rate = librosa.load(path_and_song, sr=song_sample_rate, mono=bool_mono)
        fr_len = len(librosa_audio_ts)
        librosa_rms = librosa.feature.rms(y=librosa_audio_ts, frame_length=fr_len).T
        librosa_rms_norm = librosa.util.normalize(S=librosa_rms)
        t = np.linspace(0, (self.attributes['length'] / song_sample_rate), len(librosa_rms_norm))
        self.librosa_rms_norm = librosa_rms_norm
        self.librosa_rms_time = t

        chroma_cq = librosa.feature.chroma_cqt(y=librosa_audio_ts, sr=sample_rate, n_octaves=1)
        chroma_diff = np.diff(chroma_cq, n=1, axis=1)
        chroma_max_dat = np.abs(chroma_diff).max(axis=1)
        self.chroma_max_dat = chroma_max_dat
        self.chroma_cq = chroma_cq
        #self.plot_rms(librosa_rms_norm, t)

    def attach_attributes(self, sound):
        self.attributes['num_channels'] = sound.channels
        self.attributes['sample_width'] = sound.sample_width
        self.attributes['frame_rate'] = sound.frame_rate
        self.attributes['frame_width'] = sound.frame_width
        self.attributes['length'] = len(sound)  # in milliseconds
        self.attributes['frame_count'] = sound.frame_count()
        self.attributes['intensity'] = sound.max_dBFS



