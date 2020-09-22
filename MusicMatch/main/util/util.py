import os
import re

from django.contrib.messages import get_messages
from django.http import JsonResponse

def get_env_var(env_var_name):
    """Gets the enviroment variable. If the enviroment variable does not exist, raise an exception. """

    if not os.getenv(env_var_name):
        raise Exception(f"{env_var_name} is not set")
    return os.getenv(env_var_name)

def JsonResponseWrapper(request, data):
    """ 
    Wrapper around django's JsonResponse function. 
    Adds the django messages to the data dict and returns it.
    Args:
        dict: data
    Returns:
        dict
    """

    data["messages"] = parse_messages(get_messages(request))

    return JsonResponse(data)

def parse_messages(messages):
    """
    Extract the tag and message from all the messages.
    Args:
        messages: django's FallbackStorage
    Returns:
        list: [{"tag": tag, "message", message}, {...}]
    """

    parsed_messages = []
    for message in messages:
        parsed_messages.append({"tag": message.tags, "message": message.message})

    return parsed_messages

def remove_chars(string):
    """
    Returns a string where all the forbidden windows path chars are removed.
    """
    return re.sub(r'[\\/:*?"<>|]', '', str(string))
    