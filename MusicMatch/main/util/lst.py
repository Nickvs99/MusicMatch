"""
Set of functions related to lists.
"""

def get_unique_items(list1, list2):
    """
    Returns a set of list1 and list2 without duplicates.
    Args:
        list1, list2
    Returns:
        set: All unique items
    """

    unique_values = set([])

    for item in list1:
        unique_values.add(item)

    for item in list2:
        unique_values.add(item)

    return unique_values

def get_shared_items(list1, list2):
    """
    Gets the items which are both in list1 and list2.
    Args:
        list1, list2

    Returns:
        set: Items which are both in list1 and list2.
    """

    items = set([])
    for item in list1:
        if item in list2:
            items.add(item)

    return items
