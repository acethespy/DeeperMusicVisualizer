import sys, os
from osureader.reader import BeatmapParser
from osureader.beatmap import Beatmap
import numpy as np

class DataManager:
	# def __init__(self, beatmaps_dir):
		
	# 	### Probably a lil too over complicated		
	# 	# beatmaps = {}
	# 	# for bname in os.listdir(beatmaps_dir):
 #  #   		if os.path.isdir(bname):
 #  #   			bmap = {}
 #  #   			for file in os.listdir(os.path.join(beatmaps_dir, bname)):
 #  #   				if file.endswith(".osu"):
 #  #   			beatmaps[bname] = bmap
 #    	self.beatmaps = [{'name': bname, 'dir': beatmaps_dir} for bname in os.listdir(beatmaps_dir) if os.path.isdir(bname)]
 #    	self.parser = BeatmapParser()

	def get_beatmap(beatmap_dir, autoselect_difficulty = True, two=False):
		beatmap = None
		music_path = None
		parser = BeatmapParser()
		if not beatmap_dir.endswith('.osu'):
			beatmaps = [{'name': bname, 'dir_path': os.path.join(beatmap_dir, bname)} for bname in os.listdir(beatmap_dir) if os.path.isdir(os.path.join(beatmap_dir, bname))]
			print('Available Songs: ')
			for i in range(len(beatmaps)):
				print(f'{i:02d}) {beatmaps[i]["name"]}')
			print(f'song selection(0-{len(beatmaps) - 1}):')
			i = input()
			while not (i.isdigit() and int(i) < len(beatmaps)):
				print(f'Invalid input {i}, please retry(0-{len(beatmaps) - 1}): ')
				i = input()
			choice = beatmaps[int(i)]
			options = []
			for filename in os.listdir(choice['dir_path']):
				if filename.endswith(".osu"):
					start = filename.rfind('[')
					end = filename.rfind(']')
					if start != -1 and end != -1:
						name = filename[start+1:end]
					else:
						name = filename
					bm=Beatmap(parser.parse(os.path.join(choice['dir_path'], filename)))
					options.append({'name': name, 'filename': filename, 'difficulty': bm.difficult_settings.overall_difficulty, 'beatmap': bm})
			assert(len(options) > 0, f'no .osu files found for {choice["name"]}')
			options = sorted(options, reverse=True ,key=lambda entry: entry['difficulty'])
			if autoselect_difficulty:
				if two:
					beatmap = [options[0]['beatmap'], options[len(options)-1]['beatmap']]
					music_path = os.path.join(choice['dir_path'], beatmap[0].general_settings.audio_file_name.strip())

				else:
					beatmap = options[0]['beatmap']
					music_path = os.path.join(choice['dir_path'], beatmap.general_settings.audio_file_name.strip())

				print(f'Autoselected highest difficulty: {options[0]["name"]}{options[0]["difficulty"]}')
			else:
				print('Available .osu maps')
				for i in range(len(options)):
					print(f'{i:02d}) {options[i]["name"]} {options[i]["difficulty"]}')
				print(f'.osu map selection(0-{len(options)-1}):')
				i = input()
				while not (i.isdigit() and int(i) < len(options)):
					print(f'Invalid input {i}, please retry(0-{len(options) - 1}): ')
					i = input()
				beatmap = options[int(i)]['beatmap']
				music_path = os.path.join(choice['dir_path'], beatmap.general_settings.audio_file_name.strip())
		else:
			beatmap = Beatmap(parser.parse(beatmap_dir))
			music_path = beatmap_dir[:beatmap_dir.rfind('/') + 1] + beatmap.general_settings.audio_file_name.strip()


		return beatmap, music_path



	def read_beatmap(beatmap_file):
		beatmap=Beatmap(self.parser.parse(beatmap_file))
		return beatmap;



