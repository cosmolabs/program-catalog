#!/usr/bin/evn pythoni

import python_modules, os
import datetime as datetimeutils

try:
    from pytube import YouTube, Playlist
    from python_modules.file_ops import write_file_data, get_diff_btwn_two_files, read_file_data, read_json_file_data, write_json_file_data
except ModuleNotFoundError:
    raise ModuleNotFoundError("Module pytube is not installed yet ....") from None


def check_if_video_already_exists(url_file_path: str, url: str, isPlaylist=False):
    """
    A function that checks if the video already exists by verifying against a config file.
    #TODO: Enhance to verify the whole playlist exists and if exists return the existing metadata.
    """
    url_file_data = read_json_file_data(url_file_path);
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
    # TODO: Use input validator module.
    user_AV_selection = input("A or V or AV: ")

    print(f"\nYou have choosen \"{user_AV_selection}\": ");

    downloadable_streams = [];

    # setting up the streams based on users input.
    if user_AV_selection == "A":
        downloadable_streams = video.streams.filter(only_audio=True);
    if user_AV_selection == "V":
        downloadable_streams = video.streams.filter(only_video=True).order_by('resolution').asc();
    if user_AV_selection == "AV":
        downloadable_streams = video.streams.filter(progressive=True);

    print ("\n")

    for a_stream in downloadable_streams:
        # gives the type of audio or video.
        mime_type = a_stream.mime_type.split("/")[1];
        # calculating the file size in mb and rounding off to last 2 digits.
        file_size =  str(round(a_stream.filesize*0.000001, 2)) + " MB"
        if user_AV_selection == "V":
            codec = list(a_stream.parse_codecs())[0];
            print(f"{a_stream.itag} | Resolution - {a_stream.resolution}; Type - {mime_type}; File Size - {file_size}; Codec - {codec}");
        elif user_AV_selection == "A":
            codec = list(a_stream.parse_codecs())[1];
            print(f"{a_stream.itag} | Type - {mime_type}; File Size - {file_size}; Codec - {codec}");
        else:
            codec = a_stream.parse_codecs();
            print(f"{a_stream.itag} | Resolution - {a_stream.resolution}; Type - {mime_type}; File Size - {file_size}; Codec - {codec}");

    # TODO: Use input validator module.
    itag_selected = input("\nEnter the record number from the above list: ");

    selected_stream = downloadable_streams.get_by_itag(itag_selected)

    # printing the meta data of the selected record.
    print("\nDetails of selected record: ")
    print("Includes Audio - ", selected_stream.includes_audio_track);
    print("Includes Video - ", selected_stream.includes_video_track);
    print("Resolution -", selected_stream.resolution);
    type_of_file = selected_stream.mime_type.split("/")[1];
    print(f"Type - {type_of_file}");
    file_size = round(selected_stream.filesize*0.000001, 2);
    print(f"File Size - {file_size} MB");

    # preparing meta data to insert into the json.
    metadata = dict()
    md_video_details = dict()
    md_video = dict()
    md_video_details["Title"] = video.title[0:25];
    md_video_details["URL"] = url;
    md_video_details["Includes Audo"] = selected_stream.includes_audio_track;
    md_video_details["Includes Video"] = selected_stream.includes_video_track
    md_video_details["Resolution"] = selected_stream.resolution;
    md_video_details["File Size"] = file_size
    md_video_details["Type"] = type_of_file
    md_video["Video"] = md_video_details
    metadata = read_json_file_data(os.path.dirname(__file__) + "/YTVD_metadata.json")
    if metadata is None:
        metadata = dict()
        metadata["Videos"] = list()
    metadata["Videos"].append(md_video["Video"])

    print("\nDownload started !!!")
    print("........................")
    selected_stream.download()
    print("........................")
    print("\nDownload complete !!!")

    ytvd_metadata_file = os.path.dirname(__file__) + "/YTVD_metadata.json"
    write_json_file_data(metadata, ytvd_metadata_file)


def download_playlist(url: str):
    """
    A function that downloads the video by looping through the given playlist.
    # TODO: More refinement to do.
    """
    playlist_data = Playlist(url)
    print(f"\nPlaylist - {playlist_data.title}")
    for video_url in playlist_data.video_urls:
        download_video(video_url);


def download_video(url: str):
    """
    A function to download a video by taking video URL as an input.
    It shows a popup if the video already exists. This existance will be verified
        against the metadata json that will be created while the script runs for first time.
    """
    ytvd_metadata_json = os.path.dirname(__file__) + "/YTVD_metadata.json"
    # logic to verify whether you have downloaded this video already using the script.
    video_exists = check_if_video_already_exists(ytvd_metadata_json, url, False)
    continue_download = "N";
    if video_exists is True:
        print("\nThis video already exists, do you wish to continue downloading?")
        # TODO: create an input validator module to verify given input.
        continue_download = input("\nYy or Ny: ")
        if continue_download == "Y":
            download_audio_video(url)
        else:
            print("\nDownloading None!!!")
    else:
        download_audio_video(url)


def youtube_downloader():
    """
    A function that downloads a video or playlist in a given path.
    This is the main funciton of the script.
    """
    # printing current date and time to the console.
    print(f"\nScript start time: {str(datetimeutils.datetime.now())}")
    print("Welcome to YTVd!!!\n");
    print("Enter the url of the video or playlist you want to download.");
    video_url = input("Video/Playlist URL: ");
    # determination logic of whether the url is a playlist or a video
    if "list" in video_url:
        download_playlist(video_url);
    else:
        download_video(video_url);

    print(f"\nScript end time{str(datetimeutils.datetime.now())}")
    print("Thank you!!!\n")


if __name__ == "__main__":
    print(f"\nScript: {__file__}\n")
    youtube_downloader()
