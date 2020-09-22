"""
Set of functions related to dictionaries.
"""

def get_total_dict_value(dictionary):
    """
    Returns the sum of all values in a dictionary.
    Args: dictionary, value has to be an int
    Returns: int
    """

    total = 0
    for value in dictionary.values():
        total += value

    return total

def sort_dict_value(dictionary):
    """
    Sort a dictionary based on the values from high to low.
    Args: dictionary, value has to be an integer or float
    Returns: sorted dictionary
    """

    return dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))

def get_unique_keys(dict1, dict2):
    """
    Get the total number of unique keys in the dictionaries.
    Args:
        dict1, dict2: dict
    Returns:
        int: Total number of unique keys
    """

    key_count = len(dict1);

    for key in dict2.keys():
        if key not in dict1:
            key_count += 1
    
    return key_count

def get_shared_keys(dict1, dict2):
    """
    Get the total number of shared keys across both dictionaries.
    Args:
        dict1, dict2: dict
    Returns:
        int: Total number of shared keys
    """
    key_count = 0;

    for key in dict2.keys():
        if key in dict1:
            key_count += 1
    
    return key_count

def get_dict_comparison(dict1, dict2):
    """ 
    Compares two dictionaries based on their keys and values
    Args:
        dict1, dict2: dict{key: string, value: int/float}
    Returns:
        list_coparison: list[string, list[float, float]], sorted decreasingly 
            based on the values from dict1 and dict2
    """

    user1_total = get_total_dict_value(dict1)
    user2_total = get_total_dict_value(dict2)

    # Create an dictionary where a dict key has a certain comparison value
    dict_comparison = {}
    for key in dict1:
        if key in dict2:
            user1_count = dict1[key]
            user2_count = dict2[key]
            dict_comparison[key] = (user1_count / user1_total) * (user2_count / user2_total)
    
    # sort the dictionary based on the comparison value
    dict_comparison = sort_dict_value(dict_comparison)

    # replace comparison value with the initial 
    for key in dict_comparison:
        dict_comparison[key] = [dict1[key], dict2[key]]

    return dict_comparison
