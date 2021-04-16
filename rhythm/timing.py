# -*- coding: utf-8 -*-

#
# Timing
#

import numpy as np
from os_tools import run_command
import subprocess
import os
import re

from subprocess import PIPE, run
import essentia
from essentia.standard import *

def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stderr



def get_timing(music_path):
    """
    Obtain timing by running TimingAnlyz.exe
    """
    #full_path = os.path.abspath("TimingAnalyz.exe")
    #bashCommand = f"./TimingAnalyz.exe {music_path} 0"
    #import subprocess
    #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    #output, error = process.communicate()
    #"content/drive/MyDrive/cs194/DeeperMusicVisualizer/rhythm/TimingAnalyz.exe"
    #print(output)
    #bashcommand = f"{full_path} {music_path} 0"
    #print(bashcommand)
    #result = os.system(bashcommand) #.stdout.read() #decode("utf-8")
    #test= subprocess.check_output(bashcommand, shell=True)
    #test = os.popen(bashcommand).read()
    #test = out(bashcommand)
    #print(result)
    #print("??",test)
    
    #result = run_command(bashcommand).decode("utf-8")#["TimingAnalyz.exe", music_path, "0"]).decode("utf-8")
    #bpm = float(re.findall("BPM:\W*([0-9\.]+)", result)[0])
    #ofs = float(re.findall("Offset:\W*([0-9\.]+)", result)[0])
    
    
    # Loading audio file
    audio = MonoLoader(filename=music_path)()

    # Compute beat positions and BPM
    rhythm_extractor = RhythmExtractor2013(method="multifeature")
    bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)
    ofs = beats[0]*1000
    print("BPM:", bpm)
    #print("Beat positions (sec.):", beats)
    #print("Beat estimation confidence:", beats_confidence)
    print("Offset:", ofs)   
    
    if np.abs(bpm - np.round(bpm)) < 0.05:
        #result = run_command(["./TimingAnlyz.exe", music_path, str(np.round(bpm))]).decode("utf-8")
        #bpm = float(re.findall("BPM:\W*([0-9\.]+)", result)[0])
        #ofs = float(re.findall("Offset:\W*([0-9\.]+)", result)[0])
        bpm = np.round(bpm)
        
    print("Final BPM:", bpm)
    return bpm, ofs