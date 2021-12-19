'''
This python script is to compare the difference between all the dot files I have.
'''
#!/usr/bin/python

#importing libraries
import json
import os
import importlib.util
from python_modules.file_ops import get_files_from_dir_and_its_sub_dir, get_file_differences, compare_two_files, write_file_data


def dotfiles_comparision(git_folder_path, home_folder_path, is_email_required, excluded_sub_dirs):
    script_path = os.path.dirname(__file__)
    RESULT = []    
    # Get all the files from given git folder 
    all_dot_files_in_git_folder = get_files_from_dir_and_its_sub_dir(git_folder_path, excluded_sub_dirs)    
    for a_dot_file in all_dot_files_in_git_folder:
        git_file_path = a_dot_file
        home_file_path = git_file_path.replace(git_folder_path, home_folder_path)        
        is_diff_exist = compare_two_files(git_file_path,home_file_path)
        if is_diff_exist != -1 and is_diff_exist == 1:
            diff_data = get_file_differences(git_file_path, home_file_path)
            os.makedirs(script_path + "/" + "diff/", exist_ok=True)
            file_path_to_write_diff_data = script_path + "/" + "diff/" + os.path.basename(git_file_path) + ".html"
            write_file_data(file_path_to_write_diff_data, diff_data)
            RESULT.append(f"Written diff file for {git_file_path}"\
                            f" and {home_file_path} to {file_path_to_write_diff_data}\n")
        else:
            RESULT.append(f"No diff b/w for {git_file_path} and {home_file_path}\n")
    print(RESULT)


#sending the result in an email
# USER_NAME = "rigel"
# for an_email in json_config["emaildetails"]:
#     if an_email["user_name"] == USER_NAME:
#         email_credentials = {}
#         email_credentials["user_id"] = an_email["user_id"]
#         email_credentials["user_passwd"] = an_email["user_passwd"]
# from_email = email_credentials["user_id"]
# to_email = email_credentials["user_id"]
# SUBJECT = "Dot File Comparisions."
# CONTENT = "".join(RESULT)
# email_message = email_ops.prepare_email_data(from_email, to_email, SUBJECT, CONTENT)
# email_ops.send_email(email_credentials, email_message)
# print(f"sent email to {USER_NAME}")

exclude_dirs = list()
exclude_dirs.append("awesome")
exclude_dirs.append(".git")
exclude_dirs.append(".vscode-oss")
exclude_dirs.append(".fonts")
dotfiles_comparision("/home/ganesh/gitrepos/configfiles", "/home/ganesh", False, exclude_dirs)