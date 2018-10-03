#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 22:29:06 2018

@author: gionuno
"""

import numpy as np;
import matplotlib.pyplot as plt;
import scipy.signal as scisig;
import pypianoroll;
import pyaudio;

A4   = 440.0; #Hz
RATE = 44100.0; #Hz
VOL  = 0.0625;

def num2freq(n):
    return A4*np.power(2.0,(n-69.0)/12.0);

def get_square(n,s):
    s_ = np.arange(int(RATE*s));
    return scisig.square(2.0*np.pi*(num2freq(n)/RATE)*s_);

def play(sound):
    p = pyaudio.PyAudio();
    puerto = p.open(format=pyaudio.paFloat32,channels=1,rate=44100,output=True);
    
    puerto.write(sound.astype(np.float32).tobytes());
    puerto.stop_stream();
    
    puerto.close();

def convert_to_wav(pitch,bpm,br):
    X = np.zeros((0,));
    for i in range(pitch.shape[0]):
        s = 60.0/(bpm[i]*br);
        l = int(RATE*s);
        print i;
        aux_X = np.zeros((l,));
        j_0 = 0;
        for j in range(128):
            if pitch[i,j] > 0:
                aux_X += get_square(j,s);
                j_0 = j_0 + 1;
        if j_0 > 0:
            X = np.r_[X,aux_X/j_0];
        else:
            X = np.r_[X,aux_X];
    return X;

def transform_pitch(mapping,pitch):
    new_pitch = np.zeros(pitch.shape);    
    for i in range(pitch.shape[0]):
        for j in range(128):
            n_o = j/12;
            n_j = 12*n_o + mapping[j%12];
            if n_j < 128:
                new_pitch[i,n_j] = pitch[i,j];
    return new_pitch;

#Get first 4 bars of Ode to Joy
SONG = pypianoroll.parse("ode_to_joy.mid");
SONG.tracks[0].transpose(-5);
SONG_br    = SONG.beat_resolution;
SONG_bpm   = SONG.tempo;
SONG_pitch = SONG.tracks[0].pianoroll;

MAX_LEN = int(0.25*SONG_bpm.shape[0]);
SONG_pitch = SONG_pitch[:MAX_LEN,:];
SONG_bpm   = SONG_bpm[:MAX_LEN];

SONG_audio = convert_to_wav(SONG_pitch,SONG_bpm,SONG_br);

#Make multiplicative inverse table for the multiplicative Z13 group
nnames = np.array(['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']);

Z13 = np.zeros((12,12),dtype=int);
for i in range(12):
    for j in range(12):
        Z13[i,j] = ((i+1)*(j+1))%13-1;
plt.imshow(Z13),plt.show();

invZ13 = np.zeros((12,),dtype=int);
for i in range(12):
    for j in range(12):
        invZ13[i] = np.argwhere(Z13[i,:] == 0);

print nnames[invZ13];

G13 = np.zeros((12,12),dtype=int);
for i in range(12):
    for j in range(12):
        G13[i,j] = (invZ13[(12+j-i)%12]+i)%12;

print nnames[G13[0,:]];

TRANS_pitch = np.zeros((12,SONG_pitch.shape[0],SONG_pitch.shape[1]));
TRANS_audio = np.zeros((12,SONG_audio.shape[0]));
for i in range(12):
    TRANS_pitch[i,:,:] = transform_pitch(G13[i,:],SONG_pitch);
    TRANS_audio[i,:] = convert_to_wav(TRANS_pitch[i,:,:],SONG_bpm,SONG_br);

play(VOL*SONG_audio);

#Butcher the Ode To Joy
play(VOL*TRANS_audio[0,:]);
