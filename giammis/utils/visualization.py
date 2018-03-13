import numpy as np
import matplotlib.pyplot as plt


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


def plot_confusion_matrix(cm, classes, normalize=False, title="",
                          cmap=plt.cm.Blues, cluster_names=['First', 'Second']):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    accuracy = sum(cm.diagonal()) / sum([sum(row) for row in cm])
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    if title:
        plt.title(title + "\nAccuracy " + str(round(accuracy * 100, 2)) + "%")
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print "Normalized confusion matrix"
    else:
        print 'Confusion matrix, without normalization'

    print cm

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel(cluster_names[0] + ' cluster label')
    plt.xlabel(cluster_names[1] + ' cluster label')
    plt.tight_layout()
    pass
