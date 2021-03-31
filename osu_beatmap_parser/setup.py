from distutils.core import setup
setup(
  name = 'osu-beatmap-parser',
  packages = ['osureader'],
  version = '0.1',
  license='MIT',
  description = 'Easily parse .osu files into usable objects',
  author = 'Matthew Holmes',
  url = 'https://github.com/fifty/osu-beatmap-parser',
  download_url = 'https://github.com/fifty/osu-beatmap-parser/archive/v_0.1.tar.gz',
  keywords = ['osu', 'osu!', 'parser', 'beatmap'],
  install_requires=[            # I get to this in a second
          'os',
          'typing',
          'enum',
          'ctypes',
          'abc',
          'json'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
)