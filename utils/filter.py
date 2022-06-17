import numpy as np

# TODO: add all the blending modes https://en.wikipedia.org/w/index.php?title=Blend_modes&oldid=747749280


def screen(a: list, b: list) -> list:
    '''
    https://en.wikipedia.org/w/index.php?title=Blend_modes&oldid=747749280#Screen
    '''
    # normalize
    max_a: float = np.max(a)
    max_b: float = np.max(b)
    max: float = max_a if max_a > max_b else max_b
    a_normalized: list = a / max
    b_normalized: list = b / max

    # do the function
    screen: list = 1 - ((1 - a_normalized) * (1 - b_normalized))

    # undo normalize
    return screen * max


def normal(a: list, b: list) -> list:
    # TODO: add alfa pass
    return b


def multiply(a: list, b: list) -> list:
    return np.multiply(a, b)
