import colorsys

_START = "#3F7EA6"  # "#12223E"
_END = "#A63860"  # "#F9D366"


def hex_to_rgb(hex_string):
    """
    :param hex_string: "#FFFFFF" -> [255,255,255]
    """
    # Pass 16 to the integer function for change of base
    return [int(hex_string[i:i + 2], 16) for i in range(1, 6, 2)]


def rgb_to_hex(rgb):
    """
    :param rgb: [255,255,255] -> "#FFFFFF"
    """
    # Components need to be integers for hex to make sense
    rgb = [int(x) for x in rgb]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
                        "{0:x}".format(v) for v in rgb])


def normalize_rgb(rgb):
    return [c / 255 for c in rgb]


def rgb_to_normalized_rgba(rgb, alpha=1.0):
    return normalize_rgb(rgb) + [alpha]


def rgb_to_rgba(rgb, alpha=1.0):
    return rgb + [alpha]


def linear_gradient(start, finish, n=10):
    """
    returns a gradient list of (n) colors between two hex colors.

    :param start: full six-digit color string, including the hashtag ("#FFFFFF")
    :param finish: full six-digit color string, including the hashtag ("#000000")
    :param n: amount of generated colors (including start_hex and finish_hex)
    """
    # Initialize a list of the output colors with the starting color
    hex_list = [start]
    # Calculate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
            start[j] + (float(t)/(n-1))*(finish[j]-start[j])
            for j in range(3)
        ]
        # Add it to our list of output colors
        hex_list.append(curr_vector)

    return hex_list


def gradient(rgb_to_x, x_to_rgb, start, finish, n=10):
    start = rgb_to_x(start[0], start[1], start[2])
    finish = rgb_to_x(finish[0], finish[1], finish[2])
    colors = linear_gradient(start, finish, n)

    return [list(x_to_rgb(c[0], c[1], c[2])) for c in colors]


def expanse_cmap(n=10, alpha=1.0, mode='color'):
    from matplotlib.colors import ListedColormap

    return ListedColormap(expanse_colors(n, alpha, mode), N=n)


def expanse_colors(n=10, alpha=1.0, mode='color'):
    start = normalize_rgb(hex_to_rgb(_START))
    finish = normalize_rgb(hex_to_rgb(_END))
    if mode == 'hsv':
        colors = gradient(colorsys.rgb_to_hsv, colorsys.hsv_to_rgb, start, finish, n)
    elif mode == 'hls':
        colors = gradient(colorsys.rgb_to_hls, colorsys.hls_to_rgb, start, finish, n)
    elif mode == 'yiq':
        colors = gradient(colorsys.rgb_to_yiq, colorsys.yiq_to_rgb, start, finish, n)
    else:
        colors = linear_gradient(start, finish, n)

    return [rgb_to_rgba(rgb, alpha) for rgb in colors]
