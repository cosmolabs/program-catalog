#!/usr/bin/python
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
| Date Updated:  | October 27, 2021                                              |
+----------------+---------------------------------------------------------------+

"""

# importing requests module
import requests as reqApi
# importing tabulate to frame a result grid
from tabulate import tabulate as tab


BASE_URI = "https://api.github.com/"


#  Function which pull repository information by accepting username.
def get_repositories_info_tabulated(username: str):
    try:
        url = BASE_URI + f"users/{username}/repos"
        response = reqApi.get(url)
        if not response.ok:
            print(f"\nApi call didn't worked. Returned {response}")
            exit(-1)
        else:
            user_repo_list = response.json()    # returns a list of dictionaries
            required_list = []            
            # Framing a list of dictionaries with only the required keys.
            for a_repo in user_repo_list:
                # * Python IDE helps in writing the declaration as literal
                required_details = {"Repository": a_repo.get("name"), "Description": a_repo.get("description"),
                                    "SSH URL": a_repo.get("ssh_url"), "HTML URL": a_repo.get("html_url"),
                                    "Create Date": a_repo.get("created_at"),
                                    "Watchers Count": a_repo.get("watchers_count"),
                                    "Update Date": a_repo.get("updated_at")}
                required_list.append(required_details)
            # * More tabulate details can be found in https://pypi.org/project/tabulate/
            return tab(required_list, headers="keys", showindex="always", tablefmt="grid")
    # ToDo: update the generic exception with actual exception that has to be caught during web api calls.
    except Exception as ex:
        print("\nSome exception occurred during the api call.")
        print(f"\nStack trace: {ex}")
        exit(-1)


def github_userinfo():
    USERNAME = input("What's the username in github? ")
    return get_repositories_info_tabulated(USERNAME)

# Execute the below code block if this file run as a primary file.
if __name__ == '__main__':
    print(github_userinfo())
