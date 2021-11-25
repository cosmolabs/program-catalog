#!/usr/bin/python

# imports
from typing import Optional, Any
# importing tabulate to frame a result grid
from requests import Response
from tabulate import tabulate
from os import path as io
from lib.github_api import *

"""

+----------------+---------------------------------------------------------------+
| Author:        | Ganesh Kuramsetti                                             |
+----------------+---------------------------------------------------------------+
| Script Name:   | github-userinfo                                               |
+----------------+---------------------------------------------------------------+
| Date Created:  | October 27, 2021                                              |
+----------------+---------------------------------------------------------------+
| Description:   | Gives an overview of a given user in GitHub using github API. |
+----------------+---------------------------------------------------------------+
| Language:      | Python                                                        |
+----------------+---------------------------------------------------------------+
| Prerequisites: | Python and rest are yet to determine.                         |
+----------------+---------------------------------------------------------------+
| Instructions:  | Will update later.                                            |
+----------------+---------------------------------------------------------------+
| Date Updated:  | Nov 21, 2021                                                  |
+----------------+---------------------------------------------------------------+

"""


def get_userdata_from_github(username: str):
    """
    A function that retrieves and returns the data from github for a given username.
    :rtype: object
    :param username: a string, any username from github.
    :return: an array of dictionaries
    """
    github_api_base = "https://api.github.com/"
    user_repos_link = github_api_base + f"users/{username}/repos"
    github_api_response: Response = request_api.get(user_repos_link)
    if not github_api_response.ok:
        print(f"\nApi call didn't worked. Returned {github_api_response}")
        exit(-1)
    else:
        # .json methods returns an array of dictionaries in json format.
        # you can use keys to retrieve values.
        user_repos: object = github_api_response.json()
        return user_repos
    

def frame_required_data_from_a_repo(user_repo) -> object:
    """
    A function that accepts a user repository and returns the required labels and it's detail.
    :param user_repo:
    :return: list of list (contains a label and it's corresponding detail.)
    """
    required_label_dict: dict = {'Repository': "name", 'Description': "description", 'SSH URL': "ssh_url",
                                 'HTML URL': "html_url", 'Create Date': "created_at", 'Watcher Count': "watchers_count",
                                 'Update Date': "updated_at"}
    labels_list = []
    details_list: list[Optional[Any]] = []
    # .keys returns all the keys that are available in the dictionary.
    for a_label_key in required_label_dict.keys():
        labels_list.append(a_label_key)
        label_value: str = user_repo.get(required_label_dict.get(a_label_key))
        details_list.append(str(label_value).ljust(65))
    return list(zip(labels_list, details_list))


def tabulate_repo_data(repo):
    """
    A function that returns a repo as a tabulated data.
    :param repo: framed github repository.
    :return:
    """
    return tabulate(repo, tablefmt="fancy_grid")


def add_contents_to_a_file(contents_to_be_added, file_path):
    """
    This function adds contents to a file. It's so smart, that it can identity if
    the file exists or not before adding and prompts user to create if it doesn't.

    Args:
        contents_to_be_added (string): The tabulated intro that has to be added to the file.
        file_path (string): The path to the file including file name to add the intro.
    """
    # Verifying whether a file exists or not and if it's valid file or not.
    if io.exists(file_path) and io.isfile(file_path):
        # * prepending the contents to the file by reading
        # * and joining the new content and the old content
        with open(file_path, "r") as file:
            existing_file_content = file.readlines()
            existing_file_content.insert(0, contents_to_be_added)
        with open(file_path, "w") as intro_file:
            intro_file_content = "".join(existing_file_content)
            intro_file.write(intro_file_content)
        print("\nAdded intro to the file!!")
    # To check if path entered is a directory.
    elif io.isdir(file_path):
        print("\nEntered path is not a valid file. No intro !!")
    else:
        create_file = input("\nFile doesn't exists. Do you want to create a new file (Y or N)?: ")
        if create_file.upper() == "Y":
            with open(file_path, "w+") as intro_file:
                intro_file.write(contents_to_be_added)
            print("\nAdded to the file!!")
        else:
            print("\nNothing!!")


def github_userinfo():
    username = input("What's the username in github? ")
    try:
        github_userdata = user_info(username)
        print(github_userdata)
        # repo_info = f"Username: {username};\n"
        # for a_repo in github_userdata:
        #     repo_data_in_required_fmt = frame_required_data_from_a_repo(a_repo)
        #     repo_data_tabulated = tabulate_repo_data(repo_data_in_required_fmt)
        #     repo_info = repo_info + "\n\n" + repo_data_tabulated
        # save_to_file = input("\nDo you want to save the data to a file? (Y or N): ")
        # # Asking user to output into standard output or to a file.
        # if save_to_file.upper() == "Y":
        #     file_path = input("\nEnter the path (including the file name): ")
        #     add_contents_to_a_file(repo_info, file_path)
        # elif save_to_file.upper() == "N":
        #     print(repo_info)
        # else:
        #     print('\nSelect Y or N, when asked for. Start over again!!')
    # ToDo: update the generic exception with actual exception.
    except Exception as ex:
        print("\nSome exception occurred during the api call.")
        print(f"\nStack trace: {ex}")
        exit(-1)


# Execute the below code block if this file run as a primary file.
if __name__ == '__main__':
    github_userinfo()
