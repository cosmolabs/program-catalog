# importing requests module
import requests as request_api
from requests import Response

GITHUB_API_BASE = "https://api.github.com/"


def execute_request_api(uri: str):
    """Function for an api call that returns an api response by using the URI provided.

    Args:
        uri (str): universal resource identifier

    Returns:
        [Response]: the api response converted to json
    """        
    api_response: Response = request_api.get(url=uri)
    if not api_response.ok:
        print(f"\nApi call didn't worked. Returned {api_response}")
        exit(-1)
    else:
        # .json methods returns an array of dictionaries in json format.
        # you can use keys to retrieve values.
        return api_response.json()


def get_list_of_required_details_from_response(labels_dict: dict, api_response: Response):
    labels_list = []
    details_list = []
    # .keys returns all the keys that are available in the dictionary.
    for a_label_key in labels_dict.keys():
        labels_list.append(a_label_key)
        label_value: str = api_response.get(labels_dict.get(a_label_key))
        if type(label_value) is str :
            label_value_length = len(label_value)
            line_break_chars = 80
            a_new_line_char_at = line_break_chars
            while a_new_line_char_at < label_value_length:
                label_value = label_value[:a_new_line_char_at].strip() + "-\n-" + label_value[a_new_line_char_at:].strip()
                a_new_line_char_at = a_new_line_char_at + line_break_chars
        details_list.append(str(label_value).ljust(line_break_chars))
    return list(zip(labels_list, details_list))


def user_info(username: str):
    if not username is None and username != "":
        user_info_uri = GITHUB_API_BASE + f"users/{username}"
        api_response = execute_request_api(user_info_uri)
        required_labels_dict: dict = {'Name': "name", 'Username': "login", 'Avatar URL': "avatar_url", 
                                        'GitHub URL': "html_url", 'Create Date': "created_at", 
                                        'About': "bio", 'Email': "email", 'Update Date': "updated_at", 
                                        'Follwers': "followers_url", 'Followers Count': 'followers',
                                        'Follwing': "following_url", 'Subscriptions': "subscriptions_url", 
                                        'Repositories': "repos_url"}
        list_of_required_details = get_list_of_required_details_from_response(required_labels_dict, 
                                                                                api_response)
        return list_of_required_details    
    else:
        print(f"\nUsername shouldn't be null or empty.")
        exit(-1)
        return None
    
