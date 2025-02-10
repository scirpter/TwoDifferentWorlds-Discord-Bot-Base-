from enum import Enum


class Format(Enum):
    NORMAL = 0
    BOLD = 1
    UNDERLINE = 4


class TextColor(Enum):
    NORMAL = 0
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37


class BackgroundColor(Enum):
    NONE = 0
    FIREFLY_DARK_BLUE = 40
    ORANGE = 41
    MARBLE_BLUE = 42
    GREYISH_TURQUOISE = 43
    GRAY = 44
    INDIGO = 45
    LIGHT_GRAY = 46
    WHITE = 47


def ansi(
    *,
    format: Format = Format.BOLD,
    text_color: TextColor = TextColor.MAGENTA,
    background_color: BackgroundColor = BackgroundColor.NONE,
    text: str = "",
) -> str:
    return (
        f"```ansi\n\u001b[{format.value};{text_color.value}"
        + ("" if background_color == BackgroundColor.NONE else f";{background_color.value}")
        + f"m{text}\x1b[0m```"
    )
