#!/usr/bin/evn pythoni

import python_modules
import os

try:
    from pytube import YouTube, Playlist
    from python_modules.file_ops import write_file_data, get_diff_btwn_two_files, read_file_data, read_json_file_data, write_json_file_data
except ModuleNotFoundError:
    raise ModuleNotFoundError("Module pytube is not installed yet ....") from None


def check_if_video_already_exists(url_file_path: str, url: str):
    url_file_data = read_file_data(url_file_path);
    if url in str(url_file_data):
       return True;
    return False;


def download_audio_video(url: str):

    """
    Downlaods the video or audio of a given url.
    """

    video = YouTube(url)
    print('\nTitle of the video - ', video.title);

    print("\nEnter A for only Audio, V for only video, AV for both Audio and Video.")
    user_AV_selection = input("A or V or AV: ")

    print(f"\nYou selcted \"{user_AV_selection}\": ");

    downloadable_streams = [];

    if user_AV_selection == "A":
        downloadable_streams = video.streams.filter(only_audio=True);
    if user_AV_selection == "V":
        downloadable_streams = video.streams.filter(only_video=True).order_by('resolution').asc();
    if user_AV_selection == "AV":
        downloadable_streams = video.streams.filter(progressive=True);


    for a_stream in downloadable_streams:
        mime_type = a_stream.mime_type.split("/")[1];

        if user_AV_selection == "V":
            codec = list(a_stream.parse_codecs())[0];
            print(f"{a_stream.itag} | Resolution - {a_stream.resolution}; Type - {mime_type}; File Size - {round(a_stream.filesize*0.000001, 2)} MB; Codec - {codec}");
        elif user_AV_selection == "A":
            codec = list(a_stream.parse_codecs())[1];
            print(f"{a_stream.itag} | Type - {mime_type}; File Size - {round(a_stream.filesize*0.000001, 2)} MB; Codec - {codec}");
        else:
            codec = a_stream.parse_codecs();
            print(f"{a_stream.itag} | Resolution - {a_stream.resolution}; Type - {mime_type}; File Size - {round(a_stream.filesize*0.000001, 2)} MB; Codec - {codec}");

    itag_selected = input("\nEnter the record number from the above list: ");

    selected_stream = downloadable_streams.get_by_itag(itag_selected)

    #print("\nDetails of selected record: ")
    #print("Includes Audio - ", selected_stream.includes_audio_track);
    #print("Includes Video - ", selected_stream.includes_video_track);
    #print("Resolution -", selected_stream.resolution);
    type_of_file = selected_stream.mime_type.split("/")[1];
    #print(f"Type - {type_of_file}");
    file_size = round(selected_stream.filesize*0.000001, 2);
    #print(f"File Size - {file_size} MB");

    metadata = dict()
    md_video_details = dict()
    md_video = dict()
    md_video_details["Title"] = video.title[0:25];
    md_video_details["URL"] = url;
    md_video_details["Includes Audo"] = selected_stream.includes_audio_track;
    md_video_details["Resolution"] = selected_stream.resolution;
    md_video_details["Includes Video"] = selected_stream.includes_video_track
    md_video_details["File Size"] = file_size
    md_video_details["Type"] = type_of_file
    md_video["Video"] = md_video_details
#    metadata = read_json_file_data(os.path.dirname(__file__) + "/YTVD_data.json")
    metadata["Videos"] = list()
    metadata["Videos"].append(md_video["Video"])

    print("\nDownload started !!!")
    selected_stream.download()
    print("\nDownload complete !!!")

    ytvd_metadata = os.path.dirname(__file__) + "/YTVD_metadata.json"
    write_json_file_data(metadata, ytvd_metadata)


def download_playlist(url: str):
    playlist_data = Playlist(url)
    print(f"Playlist - {playlist_data.title}")
    for video_url in playlist_data.video_urls:
        download_video(video_url);


def download_video(url: str):

    ytvd_data_file = os.path.dirname(__file__) + "/YTVD_data.txt"
    video_exists = check_if_video_already_exists(ytvd_data_file, url)
    continue_download = "N";
    if video_exists is True:
        print("\nThis video already exists, you want to continue downloading?")
        continue_download = input("\nY or N: ")
        if continue_download == "Y":
            download_audio_video(url)
        else:
            print("\nNot downloading!!!")
    else:
        download_audio_video(url)



def youtube_downloader():
    print("\nWelcome to YTVd!!!\n");
    print("Enter the url of the video you want to download.");
    video_url = input("Video URL: ");
    if "list" in video_url:
        download_playlist(video_url);
    else:
        download_video(video_url);

    print("\nThank you!!!")


if __name__ == "__main__":
    print(f"\nScript: {__file__}\n")
    youtube_downloader()
