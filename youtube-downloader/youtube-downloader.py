#!/usr/bin/evn python

try:
    from pytube import YouTube
except ModuleNotFoundError:
    raise ModuleNotFoundError("Module pytube is not installed yet ....") from None

url = input("Enter video url: ");
video = YouTube(url)
#video = YouTube('https://www.youtube.com/watch?v=5-OqPhet-NU')
print('Process will start now ..........')
print('Name of the video - ', video.title);
video_streams = video.streams
#print(video_streams)
print("Available Streams are: \n");
for stream in video_streams.order_by('resolution').asc():
    print(f"{stream.itag}|Audio - {stream.includes_audio_track}; Video - {stream.includes_video_track}; Codecs - {stream.parse_codecs()}; Resolution - {stream.resolution}; Type - {stream.mime_type}");

itag_selected = input("Enter an itag from the above list: ");
selected_stream = video_streams.get_by_itag(itag_selected)
print("Includes Audio - ", selected_stream.includes_audio_track);
print("Includes Video - ", selected_stream.includes_video_track);
print("Codecs -", selected_stream.parse_codecs())
print("Resolution -", selected_stream.resolution)
print("itag -", selected_stream.itag)
print("Type -", selected_stream.mime_type)
print(f"File Size - {round(selected_stream.filesize*0.000001, 2)} MB");
print("Downloading the selected stream .......")
selected_stream.download()
print("Download Completed .....")
