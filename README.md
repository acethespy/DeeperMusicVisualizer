# DeeperMusicVisualizer
UC Berkeley CS194 Final Project

## osu_beatmap_parser
pulled from https://github.com/fifty/osu-beatmap-parser, contains code to parse osu beatmaps

will probably modify this to be more fit for our use case

## data_manager
a module to help select which song to use from a directory of osu beatmaps and loads all relevant data into a Beatmap object from osu_beatmap_parser

useful starting point for building dataloader for rhythm model training

## rhythm
folder for rhythm model

## visualizer
contains ipynb used to generate visuals from preexisting osu beatmaps

# Drive setup
Pull the repo into a Drive folder, and then move the two shared "data" and "results" folders to the root directory of this repository
![Screen Shot 2021-03-30 at 1 29 31 AM](https://user-images.githubusercontent.com/18081264/112958495-6160fc80-90f7-11eb-99d2-973a396b787a.png)
These two folders are ignored in the .gitignore so they won't be pushed to GitHub
