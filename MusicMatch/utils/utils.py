""" 
Some utility functions needed for all apps.
"""

import os

def get_env_var(env_var_name):
    """ Gets the enviroment variable. If the enviroment variable does not exist, raise an exception. """

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

