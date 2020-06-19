import colorsys
from matplotlib.colors import ListedColormap

_START = '#12223E'
_END = '#D1A94D'


def hex_to_rgb(hex_string: str) -> list:
    """
    :param hex_string: "#FFFFFF"
    :return: "#FFFFFF" -> [255,255,255]
    """
    # Pass 16 to the integer function for change of base
    return [int(hex_string[i:i + 2], 16) for i in range(1, 6, 2)]


def rgb_to_hex(rgb: list) -> str:
    """
    :param rgb: [255,255,255]
    :return: [255,255,255] -> "#FFFFFF"
    """
    # Components need to be integers for hex to make sense
    rgb = [int(x) for x in rgb]
    return '#' + ''.join(['0{0:x}'.format(v) if v < 16 else
                          '{0:x}'.format(v) for v in rgb])


def normalize_rgb(rgb: list) -> list:
    """
    :param rgb: [255,255,255]
    :return: [255,255,255] -> [1.0, 1.0, 1.0]
    """
    return [c / 256 for c in rgb]


def _linear_gradient(start, finish, n=10):
    """
    returns a gradient list of (n) colors between two hex colors.

    :param start: full six-digit color string, including the hashtag ("#FFFFFF")
    :param finish: full six-digit color string, including the hashtag ("#000000")
    :param n: amount of generated colors (including start_hex and finish_hex)
    """
    # Initialize a list of the output colors with the starting color
    hex_list = [start]
    # Calculate a color at each evenly spaced value of t from 1 to n
    for pos in range(1, n):
        # Interpolate RGB vector for color at the current value of pos and add it to our list of output colors
        hex_list.append([start[j] + (float(pos) / (n - 1)) * (finish[j] - start[j]) for j in range(3)])

    return hex_list


def _gradient(rgb_to_x, x_to_rgb, start: list, finish: list, n: int = 10) -> list:
    """
    Universal function for colorsys rgb_to_x and x_to_rgb functions.

    Converts the given rgb values start and finish to hls, hsv or yiq values and applies a linear gradient on them.
    Afterwards, reconverts the produced values back to rgb.

    :param rgb_to_x: function that converts three rgb parameter to a tuple of x
    :param x_to_rgb: function that converts three x parameter to a tuple of rgb
    :param start: normalized rgb value
    :param finish: normalized rgb value
    :param n: amount of colors produced by this functions
    :return: n normalized rgb values
    """
    start = rgb_to_x(start[0], start[1], start[2])
    finish = rgb_to_x(finish[0], finish[1], finish[2])
    colors = _linear_gradient(start, finish, n)

    return [list(x_to_rgb(c[0], c[1], c[2])) for c in colors]


def expanse_cmap(n: int = 256, alpha: float = 1.0, mode: str = 'color') -> ListedColormap:
    """
    Creates a color map for a matplotlib color scale.

    :param n: amount of colors to produce
    :param alpha: normalized opacity
    :param mode: color mode ('color', 'hsv', 'hls', 'yiq')
    :return: a ListedColormap with the produced rgba values
    """

    return ListedColormap(expanse_colors(n, alpha, mode), N=n)


def expanse_colors(n: int = 256, alpha: float = 1.0, mode: str = 'color') -> list:
    """
    Creates a list of normalized rgba values between the colors defined by _START and _END.

    :param n: amount of colors to produce
    :param alpha: normalized opacity
    :param mode: color mode ('color', 'hsv', 'hls', 'yiq')
    :return: a list with the produced rgba values
    """
    n = min(n, 256)
    start = normalize_rgb(hex_to_rgb(_START))
    finish = normalize_rgb(hex_to_rgb(_END))
    if mode == 'hsv':
        colors = _gradient(colorsys.rgb_to_hsv, colorsys.hsv_to_rgb, start, finish, n)
    elif mode == 'hls':
        colors = _gradient(colorsys.rgb_to_hls, colorsys.hls_to_rgb, start, finish, n)
    elif mode == 'yiq':
        colors = _gradient(colorsys.rgb_to_yiq, colorsys.yiq_to_rgb, start, finish, n)
    else:
        colors = _linear_gradient(start, finish, n)

    return [rgb + [alpha] for rgb in colors]
