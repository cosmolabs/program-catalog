'''
    This python script is to compare the difference between all the dot files I have.
'''
#!/usr/bin/python

#importing libraries
import json
import os
import importlib.util
from python_modules.file_ops import get_files_from_dir_and_its_sub_dir, get_diff_btwn_two_files, compare_two_files, write_file_data, read_json_file_data
from python_modules.email_ops import prepare_email_data, send_email


def compare_two_folders(first_folder_path, second_folder_path, is_email_required, excluded_sub_dirs):
    compare_script_path = os.path.dirname(__file__)
    RESULT = []    
    # Get all the files from given git folder 
    all_file_paths_in_first_folder = get_files_from_dir_and_its_sub_dir(first_folder_path, excluded_sub_dirs)
    for a_first_folder_file_path in all_file_paths_in_first_folder:
        a_temp_path = a_first_folder_file_path
        a_second_folder_file_path = a_temp_path.replace(first_folder_path, second_folder_path)
        is_diff_exist = compare_two_files(a_first_folder_file_path,a_second_folder_file_path)
        if is_diff_exist != -1 and is_diff_exist == 1:
            diff_data = get_diff_btwn_two_files(a_first_folder_file_path, a_second_folder_file_path)
            os.makedirs(compare_script_path + "/" + "diff/", exist_ok=True)
            file_path_to_write_diff_data = compare_script_path + "/" + "diff/" + os.path.basename(a_first_folder_file_path) + ".html"
            write_file_data(file_path_to_write_diff_data, diff_data)
            RESULT.append(f"\nWritten diff file for {a_first_folder_file_path}"\
                            f" and {a_second_folder_file_path} to {file_path_to_write_diff_data}\n")
        else:
            # RESULT.append(f"\nNo diff b/w for {a_first_folder_file_path} and {a_second_folder_file_path}\n")
    print(RESULT)
    if is_email_required is True:
        #sending the result in an email
        USER_NAME = "rigel"
        json_config = read_json_file_data("/home/ganesh/gitrepos/program_catalog/compare/helper.json")
        for an_email in json_config["emaildetails"]:
            if an_email["user_name"] == USER_NAME:
                email_credentials = {}
                email_credentials["user_id"] = an_email["user_id"]
                email_credentials["user_passwd"] = an_email["user_passwd"]
                from_email = email_credentials["user_id"]
                to_email = email_credentials["user_id"]
                SUBJECT = "Dot File Comparisions."
                CONTENT = "".join(RESULT)
                email_message = prepare_email_data(from_email, to_email, SUBJECT, CONTENT)
                send_email(email_credentials, email_message)
                print(f"Sent email to {USER_NAME}")

if __name__ == '__main__':
    json_config = read_json_file_data("/home/ganesh/gitrepos/program_catalog/compare/helper.json")
    exclude_dirs = list()
    for an_exclude_dir in json_config["excluded_dirs"]:
        exclude_dirs.append(an_exclude_dir)
    compare_two_folders(json_config["gitpath"], json_config["homepath"], True, exclude_dirs)
