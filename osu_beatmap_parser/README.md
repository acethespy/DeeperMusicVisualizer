# osu-beatmap-parser
Python library to read and parse osu files. 

**Usage**
```
Usage:
Where song_path is an absolute path to the .osu file

>>> from osureader.reader import BeatmapParser
>>> from osureader.beatmap import Beatmap

>>> parser = BeatmapParser()
>>> res = parser.parser(song_path)
>>> beatmap = Beatmap(res)
```

**Installation options**
