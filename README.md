# Music Player

This is a simple command-line music player written in Python. It allows you to play songs and playlists in MP3 format. The player uses the `pydub` library for audio processing and the `simpleaudio` library for audio playback. (NOTE THIS IS ONLY FOR MACOS CURRENTLY)

## Features

- Play individual songs
- Play playlists with or without shuffle
- Adjust volume level
- Playlist information display

## Requirements

- Python 3.x
- `pydub` library
- `simpleaudio` library
- `colorama` library (for console coloring)

## Installation

1. Clone the repository:

```shell
git clone https://github.com/countervolts/python-music-player.git
```

2. Change into the project directory:

```shell
cd python-music-player
```

3. Install the required libraries:

```shell
pip install pydub simpleaudio colorama
```

4. Set the path to the ffprobe and ffmpeg executables:

```python
ffprobe_path = "/path/to/ffprobe"
ffmpeg_path = "/path/to/ffmpeg"
```

Replace `"/path/to/ffprobe"` and `"/path/to/ffmpeg"` with the actual paths to the `ffprobe` and `ffmpeg` executables on your system. These executables are used by `pydub` for audio file format detection and conversion.

## Usage

To start the music player, run the following command:

```shell
python main.py
```

The main menu will be displayed with the following options:

1. Play music - Select this option to choose a playlist and play songs.
2. Display playlists - View the available playlists.
3. Create a new playlist - Create a new playlist.
4. Total information - View total information about playlists and songs.
5. Quit - Exit the music player.

When you select the "Play music" option, you will be prompted to choose a playlist. Once a playlist is selected, the playlist menu will be displayed with the following options:

1. Play a random song - Play a random song from the playlist.
2. Quit - Go back to the main menu.

In the playlist menu, you can select the desired option to play songs from the playlist.
