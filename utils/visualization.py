import numpy as np


# TODO unittest
def from_rgba_to_rgb(rgba_color_string):
    """

    Args:
        rgba_color_string (str):

    Returns:
        str:
    """
    return ','.join(rgba_color_string.replace('a', '').split(',')[:-1]) + ')'


def from_rgb_to_rgba(rgb_color_string, alpha=1.0):
    """

    Args:
        rgb_color_string (str):
        alpha (float):

    Returns:
        str:
    """
    return rgb_color_string.split('(')[0] + 'a(' + rgb_color_string.split('(')[1].split(')')[0] + ',{})'.format(alpha)


def rgb_lighter(color, white_percentage):
    """

    Args:
        color (3-tuple): Assumes color is rgb between (0, 0, 0) (black) and (255, 255, 255) (white)
        white_percentage (float):

    Returns:
        3-tuple:
    """
    color = np.array(color)
    white = np.array([255, 255, 255])
    vector = white - color
    return color + vector * white_percentage


def from_rgb_to_hex(rgb_tuple):
    """

    Args:
        rgb_tuple (list):

    Returns:
        str: hex representation of the input rgb color
    """
    return '#%02x%02x%02x' % tuple(x for x in rgb_tuple)
