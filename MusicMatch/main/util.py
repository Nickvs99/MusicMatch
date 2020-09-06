""" 
Some utility functions needed for all apps.
"""

import os
import json
from cryptography.fernet import Fernet

from django.contrib.messages import get_messages
from django.http import JsonResponse

def get_env_var(env_var_name):
    """Gets the enviroment variable. If the enviroment variable does not exist, raise an exception. """

    if not os.getenv(env_var_name):
        raise Exception(f"{env_var_name} is not set")
    return os.getenv(env_var_name)

def print_json(json_response):
    """ Prints the json response in a human readable form."""

    print(json.dumps(json_response, indent=4))

def print_dic(dic):
    """ Prints the items from dic on a new line for each. Makes it more human readable."""

    for key, value in dic.items():
        print(key, value)

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

    print(data["messages"])
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

def get_fernet_key():
    """ Returns the Fernet key in byte format."""

    return get_env_var("FERNET_KEY").encode()

def encrypt_message(message):
    """
    Encrypts a message.
    Args: message, str
    Returns: str
    """
    f = Fernet(get_env_var("FERNET_KEY"))

    return f.encrypt(message.encode()).decode("utf-8")

def decrypt_message(message):
    """
    Decrypts a message.
    Args: message, str
    Returns: str
    """
    f = Fernet(get_env_var("FERNET_KEY"))

    return f.decrypt(message.encode()).decode("utf-8")