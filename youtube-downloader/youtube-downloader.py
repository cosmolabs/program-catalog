#!/usr/bin/evn pythoni

import python_modules

try:
    from pytube import YouTube
    from python_modules.file_ops import write_file_data, get_diff_btwn_two_files, read_file_data
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

    video = YouTube(video_url)
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

    print("\nDetails of selected record: ")
    print("Includes Audio - ", selected_stream.includes_audio_track);
    print("Includes Video - ", selected_stream.includes_video_track);
    print("Resolution -", selected_stream.resolution);
    type_of_file = selected_stream.mime_type.split("/")[1];
    print(f"Type - {type_of_file}");
    file_size = round(selected_stream.filesize*0.000001, 2);
    print(f"File Size - {file_size} MB");

    print("\nDownload started !!!")
    selected_stream.download()
    print("\nDownload complete !!!")

    urlString = "- "+video_url + "|"

    write_file_data("/home/ganesh/Documents/YTVD_URLS", urlString)

if __name__ == "__main__":
    print("\nWelcome to YTVd!!!\n");
    print("Enter the url of the video you want to download.");
    video_url = input("Video URL: ");
    video_exists = check_if_video_already_exists("/home/ganesh/Documents/YTVD_URLS", video_url)
    continue_download = "N";
    if video_exists is True:
        print("\nThis video already exists, you want to continue downloading?")
        continue_download = input("\nY or N: ")
        if continue_download == "Y":
            download_audio_video(video_url)
        else:
            print("\nNot downloading!!!")
    else:
        download_audio_video(video_url)

    print("\nThank you!!!")
