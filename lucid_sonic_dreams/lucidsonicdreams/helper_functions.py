import numpy as np
import random
import pickle 
import requests
import json
import pandas as pd

import librosa
import pygit2
import gdown 
from mega import Mega

from data_manager.data_manager import DataManager as DM
from osu_beatmap_parser.osureader.beatmap import Beatmap
from osu_beatmap_parser.osureader.objects import HitObjectType

def download_weights(url, output):
  '''Download model weights from URL'''

  if 'drive.google.com' in url: 
    gdown.download(url, output = output, quiet = False)

  elif 'mega.nz' in url:
    m = Mega()
    m.login().download_url(url, 
                           dest_filename = output)

  elif 'yadi.sk' in url:
    endpoint = 'https://cloud-api.yandex.net/v1/disk/'\
               'public/resources/download?public_key='
    r_pre = requests.get(endpoint + url)
    r_pre_href = r_pre.json().get('href')
    r = requests.get(r_pre_href)
    with open(output, 'wb') as f:
      f.write(r.content)
      
  else:
    r = requests.get(url)
    with open(output, 'wb') as f:
      f.write(r.content)


def consolidate_models():
  '''Consolidate JSON dictionaries of pre-trained StyleGAN(2) weights'''

  # Define URL's for pre-trained StyleGAN and StyleGAN2 weights
  stylegan_url = 'https://raw.githubusercontent.com/justinpinkney/'\
  'awesome-pretrained-stylegan/master/models.csv'
  stylegan2_url = 'https://raw.githubusercontent.com/justinpinkney/'\
  'awesome-pretrained-stylegan2/master/models.json'

  # Load JSON dictionary of StyleGAN weights
  models_stylegan = pd.read_csv(stylegan_url)\
                    .to_dict(orient='records')

  # Load JSON dictionary of StyleGAN2 weights
  r = requests.get(stylegan2_url)
  models_stylegan2 = json.loads(r.text)

  # Consolidate StyleGAN and StyleGAN2 weights
  all_models = models_stylegan + models_stylegan2

  return all_models


def get_spec_norm(wav, sr, n_mels, hop_length):
  '''Obtain maximum value for each time-frame in Mel Spectrogram, 
     and normalize between 0 and 1'''

  # Generate Mel Spectrogram
  spec_raw= librosa.feature.melspectrogram(y=wav, sr=sr,
                                           n_mels=n_mels,
                                           hop_length=hop_length)
  
  # Obtain maximum value per time-frame
  spec_max = np.amax(spec_raw,axis=0)

  # Normalize all values between 0 and 1
  spec_norm = (spec_max - np.min(spec_max))/np.ptp(spec_max)

  return spec_norm


def interpolate(array_1: np.ndarray, array_2: np.ndarray, steps: int):
  '''Linear interpolation between 2 arrays'''

  # Obtain evenly-spaced ratios between 0 and 1
  linspace = np.linspace(0, 1, steps)

  # Generate arrays for interpolation using ratios
  arrays = [(1-l)*array_1 + (l)*array_2 for l in linspace]

  return np.asarray(arrays)


def full_frame_interpolation(frame_init, steps, len_output):
  '''Given a list of arrays (frame_init), produce linear interpolations between
     each pair of arrays. '''

  # Generate list of lists, where each inner list is a linear interpolation
  # sequence between two arrays.
  frames = [interpolate(frame_init[i], frame_init[i+1], steps) \
            for i in range(len(frame_init)-1)]

  # Flatten list of lists
  frames = [vec for interp in frames for vec in interp]

  # Repeat final vector until output is of the desired length
  while len(frames) < len_output:
    frames.append(frames[-1])

  return frames

def extract_osu(osu_file, result_length, frame_duration, sr):
  def to_frames(time):
    #time: time in ms
    # ms = (i * frame_duration)/sr * 1000
    return round(time / 1000 * sr / frame_duration)
  print(result_length, frame_duration, sr)
  print(to_frames(100))
  print(round(100 / 1000 * sr / frame_duration))
  def slider_duration(length, multiplier, beat_length):
    return length / (multiplier * 100) * beat_length

  if '.npy' in osu_file:
    data = np.load(osu_file, allow_pickle=True)
    pulse = np.zeros(result_length)
    motion = np.zeros(result_length)
    PULSE_DURATION = 100 #ms
    OSU_PULSE_REACT = 1.0
    OSU_MOTION_REACT = 1.0
    pulse_vec = np.ones(to_frames(PULSE_DURATION)) * OSU_PULSE_REACT
    print(len(pulse_vec))
    for event in data: #event = [time in ms, 0hit or 1slide, duration in ms]
      if event[1] == 0:
        #hit
        start = to_frames(event[0]) - len(pulse_vec)//2
        if start+len(pulse_vec) > len(pulse):
          print(f'last_time:{event[0]}')
          break;
        print(len(pulse_vec))
        pulse[start:start+len(pulse_vec)] += pulse_vec
      else:
        #slide
        start = to_frames(event[0])
        motion_vec = OSU_MOTION_REACT * np.ones(to_frames(event[2]))
        print(f'motion_frames:{len(motion_vec)}')
        if start + len(motion_vec) > len(motion):
          print(f'last_time:{event[0]}')
          break;
        motion[start:start+len(motion_vec)] += motion_vec
    return pulse, motion
  beatmap, _ = DM.get_beatmap(osu_file)
  # (len(self.spec_norm_pulse) * frame_duration + 1)/sr

  print(f'duration_ms:{(result_length * frame_duration/sr * 1000)}')

  pulse = np.zeros(result_length)
  motion = np.zeros(result_length)

  PULSE_DURATION = 100 #ms
  OSU_PULSE_REACT = 1.0
  OSU_MOTION_REACT = 1.0
  print(f'pulse_frames: {to_frames(PULSE_DURATION)}')
  pulse_vec = np.ones(to_frames(PULSE_DURATION)) * OSU_PULSE_REACT
  hit_objects = beatmap.hit_objects
  timing_objects = beatmap.timing_objects

  slider_multiplier = beatmap.difficult_settings.slider_multiplier
  slider_multiplier_multiplier = 1
  timing_object = timing_objects[0]

  for hit_object in hit_objects:
    while len(timing_objects) > 0 and hit_object.time >= timing_objects[0].time:
      temp = timing_objects.pop(0)
      if temp.uninherited == 1:
        timing_object = temp
        slider_multiplier_multiplier = 1
      else:
        slider_multiplier_multiplier = 100/(-temp.beat_length)
    if HitObjectType.SLIDER in hit_object.type:
      start = to_frames(hit_object.time)
      motion_vec = OSU_MOTION_REACT * np.ones(to_frames(slider_duration(float(hit_object.length), slider_multiplier_multiplier * slider_multiplier, timing_object.beat_length)))
      print(f'motion_frames:{len(motion_vec)},time:{hit_object.time}')
      if start + len(motion_vec) > len(motion):
        print(f'last_time:{hit_object.time}')
        break;
      motion[start:start+len(motion_vec)] += motion_vec
    elif HitObjectType.CIRCLE in hit_object.type:
      start = to_frames(hit_object.time) - len(pulse_vec)//2
      if start+len(pulse_vec) > len(pulse):
        print(f'last_time:{hit_object.time}')
        break;
      pulse[start:start+len(pulse_vec)] += pulse_vec

  return pulse, motion