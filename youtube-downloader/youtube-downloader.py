#!/usr/bin/evn python

try:
    from pytube import YouTube
except ModuleNotFoundError:
    raise ModuleNotFoundError("Module pytube is not installed yet ....") from None

print("\nWelcome to YTVd!!!\n")

print("Enter the url of the video you want to download.");
video_url = input("Video URL: ");
video = YouTube(video_url)

print('\nTitle of the video - ', video.title);

print("\nEnter A for only Audio, V for only video, AV for both Audio and Video.")
user_AV_selection = input("A or V or AV: ")

audio_streams = video.streams.filter(only_audio=True)
video_streams = video.streams.filter(only_video=True)
downloadable_streams = [];

if user_AV_selection == "A":
    downloadable_streams = audio_streams;
if user_AV_selection == "V":
    downloadable_streams = video_streams.order_by('resolution').asc();
if user_AV_selection == "AV":
    downloadable_Streams = "";

for a_stream in downloadable_streams:
    print(f"{a_stream.itag} | Codecs(Video, Audio) - {a_stream.parse_codecs()}; Resolution - {a_stream.resolution}; Type - {a_stream.mime_type}; File Size - {round(a_stream.filesize*0.000001, 2)} MB");

itag_selected = input("\nEnter the record number from the above list: ");

selected_stream = downloadable_streams.get_by_itag(itag_selected)

print("\nDetails of selected record: ")
print("Includes Audio - ", selected_stream.includes_audio_track);
print("Includes Video - ", selected_stream.includes_video_track);
print("Resolution -", selected_stream.resolution)
print("Type -", selected_stream.mime_type)
print(f"File Size - {round(selected_stream.filesize*0.000001, 2)} MB");

print("\nDownload started !!!")
selected_stream.download()
print("\nDownload complete !!!")
