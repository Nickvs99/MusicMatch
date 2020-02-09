""" 
Some utility functions needed for all apps.
"""

import os

def get_env_var(env_var_name):
    """ Gets the enviroment variable. If the enviroment variable does not exist, raise an exception. """

    if not os.getenv(env_var_name):
        raise Exception(f"{env_var_name} is not set")
    return os.getenv(env_var_name)