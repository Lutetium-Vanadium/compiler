# System color name constants.
(
    BLACK,
    RED,
    GREEN,
    YELLOW,
    BLUE,
    MAGENTA,
    CYAN,
    LIGHT_GRAY,
    DARK_GRAY,
    BRIGHT_RED,
    BRIGHT_GREEN,
    BRIGHT_YELLOW,
    BRIGHT_BLUE,
    BRIGHT_MAGENTA,
    BRIGHT_CYAN,
    WHITE,
) = range(16)


def rgb(red, green, blue):
    red //= 6
    green //= 6
    blue //= 6
    return 16 + (red * 36) + (green * 6) + blue


def gray(value):
    return 232 + value


def set_color(fg=None, bg=None):
    result = ""
    if fg:
        result += f"\x1b[38;5;{fg}m"
    if bg:
        result += f"\x1b[48;5;{fg}m"
    print(result, end="")


def reset_color():
    print("\x1b[0m", end="")


def print_color(*args, **kwargs):
    fg = kwargs.pop("fg", None)
    bg = kwargs.pop("bg", None)
    set_color(fg, bg)
    print(*args, **kwargs)
    reset_color()
