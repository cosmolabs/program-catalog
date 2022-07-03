#!/usr/bin/evn python

try:
    from pytube import YouTube
except ModuleNotFoundError:
    raise ModuleNotFoundError("Module pytube is not installed yet ....") from None

video = YouTube('https://www.youtube.com/watch?v=KGD2N5hJ2e0')
print('Process will start now ..........')
print('Name of the video - ', video.title);
video_streams = video.streams
print("Available Streams are: ");
for stream in video_streams:
    print("Includes Audio - ", stream.includes_audio_track);
    print("Includes Video - ", stream.includes_video_track);
    print("Codecs -", stream.parse_codecs())
    print("Resolution -", stream.res)
    print("\n")
