import os
import glob
import random
import time
import mutagen.mp3
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio, play

ffprobe_path = "fill in with the parh of ffprobe"
ffmpeg_path = "fill in the path with ffmpeg"

os.environ["PATH"] += os.pathsep + os.path.dirname(ffprobe_path)

_play_with_simpleaudio.player = "simpleaudio"

def get_song_info(song_path):
    _, file_extension = os.path.splitext(song_path)
    if file_extension.lower() == '.mp3':
        audio = mutagen.mp3.MP3(song_path)
    else:
        return "Unknown Song", "Unknown Artist", 0

    song_name = audio.get("title", "Unknown Song")
    artist = audio.get("artist", "Unknown Artist")
    duration = int(audio.info.length)
    return song_name, artist, duration

def change_volume():
    volume = float(input("Enter the volume (in dB): "))
    return volume

def play_song(song_path, volume):
    _, file_extension = os.path.splitext(song_path)
    if file_extension.lower() == '.mp3':
        audio = AudioSegment.from_file(song_path, format='mp3')
    else:
        print(f"Unsupported file format: {file_extension}")
        return

    print(f"Now playing: {os.path.basename(song_path)}")

    adjusted_audio = audio + volume

    play(adjusted_audio)

def play_playlist(playlist_path, shuffle=False):
    songs = glob.glob(os.path.join(playlist_path, '*.mp3'))
    if len(songs) == 0:
        print("No songs found in the playlist.")
        return

    if shuffle:
        random.shuffle(songs)

    volume = -1

    for song_path in songs:
        song_name, artist, duration = get_song_info(song_path)

        print(f"Now playing: {song_name} - {artist}")

        progress_bar = ProgressBar(duration)
        audio_thread = play_song(song_path, volume)

        while audio_thread.is_alive():
            progress_bar.update(audio_thread.get_position())

            if audio_thread.get_position() >= duration:
                break

            time.sleep(0.1)

        choice = input("Enter 's' to skip, 'v' to change volume, 'e' to exit, or press Enter to continue playing: ")

        if choice == 's':
            audio_thread.stop()
            continue
        elif choice == 'v':
            volume = change_volume()
            audio_thread.stop()
            play_song(song_path, volume)
        elif choice == 'e':
            audio_thread.stop()
            break

class ProgressBar:
    def __init__(self, duration):
        self.duration = duration

    def update(self, current_time):
        filled_length = int(50 * current_time / self.duration)
        remaining_length = 50 - filled_length
        progress_bar = '[' + '#' * filled_length + '-' * remaining_length + ']'
        time_left = self.duration - current_time
        print(f"\r{progress_bar} {current_time:.2f}s/{self.duration}s - Time Left: {time_left:.2f}s", end='')

def playlist_menu(playlist_path):
    while True:
        print("\n===== Playlist Menu =====")
        print("1. Pick a song (p)")
        print("2. Play playlist with shuffle (ps)")
        print("3. Play playlist without shuffle (pws)")
        print("4. Playlist information (i)")
        print("5. Change volume (v)")
        print("6. Go back (b)")

        choice = input("Enter your choice: ")

        if choice == 'p':
            song_choice = input("Enter the song number to play: ")
            if song_choice.isdigit() and int(song_choice) in range(1, len(songs) + 1):
                song_path = songs[int(song_choice) - 1]
                play_song(song_path)
            else:
                print("Invalid song choice.")

        elif choice == 'ps':
            play_playlist(playlist_path, shuffle=True)

        elif choice == 'pws':
            play_playlist(playlist_path, shuffle=False)

        elif choice == 'i':
            playlist_information(playlist_path)

        elif choice == 'v':
            volume = change_volume()

        elif choice == 'b':
            break

        else:
            print("Invalid choice. Please try again.")

def main_menu():
    while True:
        print("\n===== Main Menu =====")
        print("1. Play music")
        print("2. Display playlists (d)")
        print("3. Create a new playlist (n)")
        print("4. Total information (i)")
        print("5. Quit (q)")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("\n===== Playlists =====")
            playlists = glob.glob('playlists/*')
            if len(playlists) == 0:
                print("No playlists found.")
                continue

            for i, playlist in enumerate(playlists):
                print(f"{i+1}. {os.path.basename(playlist)}")

            playlist_choice = input("Enter the playlist number to play: ")
            if playlist_choice.isdigit() and int(playlist_choice) in range(1, len(playlists) + 1):
                playlist_path = playlists[int(playlist_choice) - 1]
                playlist_menu(playlist_path)
            else:
                print("Invalid playlist choice.")

        elif choice == 'd':
            print("\n===== Playlists =====")
            playlists = glob.glob('playlists/*')
            if len(playlists) == 0:
                print("No playlists found.")
                continue

            for i, playlist in enumerate(playlists):
                print(f"{i+1}. {os.path.basename(playlist)}")

        elif choice == 'n':
            playlist_name = input("Enter the name of the new playlist: ")
            playlist_path = os.path.join('playlists', playlist_name)
            if not os.path.exists(playlist_path):
                os.makedirs(playlist_path)
                print("New playlist created successfully!")
            else:
                print("Playlist already exists.")

        elif choice == 'i':
            print("\n===== Total Information =====")
            playlists = glob.glob('playlists/*')
            print("Total playlists:", len(playlists))
            total_songs = sum([len(glob.glob(os.path.join(playlist, '*.mp3'))) for playlist in playlists])
            print("Total songs downloaded:", total_songs)
            favorite_playlist = input("Enter the name of your favorite playlist: ")
            print("Favorite playlist:", favorite_playlist)

        elif choice == 'q':
            break

        else:
            print("Invalid choice. Please try again.")

def start_music_player():
    print("Welcome to the Music Player!")
    main_menu()

start_music_player()
