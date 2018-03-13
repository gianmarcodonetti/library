def merge_dictionaries(list_of_dict, keys_to_remove=None):
    """Given a list of dictionaries, merge them in a single one, with priorities on the last ones.

    Args:
        list_of_dict (list):
        keys_to_remove (list):

    Returns:
        dict: The union of the list of dictionaries
    """
    if keys_to_remove is None:
        keys_to_remove = []
    merged_dict = {}
    for d in list_of_dict:
        merged_dict.update(d)
    for key_to_remove in keys_to_remove:
        try:
            merged_dict.pop(key_to_remove)
        except KeyError:  # the key you're trying to remove is not inside the merged dictionary
            pass
    return merged_dict


def keep_only_x_keys(x, keys):
    """

    Args:
        x (dict):
        keys (list):

    Returns:
        dict:
    """
    return {k: x[k] for k in keys}


def pipe_functions(functions, zero_value):
    """Pipe a list of functions to a starting value.

    Args:
        functions (list): A sorted list of functions.
        zero_value (Any): The initial value, the first to be passed to the list of functions.

    Returns:
        Any: The input zero value modified in cascade from all the given functions.
    """
    return reduce(lambda res, f: f(res), functions, zero_value)


def percentage_levels_round_up(x, levels):
    """Given a float value between 0.0 and 1.0, assign it to the ceil nearest value in levels list.

    Args:
        x (float):
        levels (list): list of float between 0.0 and 1.0, must be sorted decreasingly

    Returns:
        float: floor nearest value to x in levels list
    """
    if sorted(levels, reverse=True) != levels:
        raise ValueError("Levels are not sorted... {}".format(levels))
    if x > levels[1]:
        return levels[0]
    return min(level for level in levels if level >= x)


def identity_func(x):
    return x
