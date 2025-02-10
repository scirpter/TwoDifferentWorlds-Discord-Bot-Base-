import sys
from asyncio import AbstractEventLoop, new_event_loop
from logging import INFO
from logging import basicConfig as basicLogConfig
from typing import NoReturn
from enhanced_str import clearConsole, es
from models.client import Void
from private.common import get_config_hex


def main() -> NoReturn:
    loop.run_until_complete(client.start(client.config.get("bot", "token")))
    sys.exit(0)


if __name__ == "__main__":
    clearConsole()

    client: Void = Void()

    bracket_color: int = get_config_hex(client.config, "logging", "bracket_color")
    in_bracket_text_color: int = get_config_hex(client.config, "logging", "in_bracket_text_color")
    text_color: int = get_config_hex(client.config, "logging", "text_color")
    basicLogConfig(
        level=INFO,
        format=f"{es('[').hexColor(bracket_color)}"
        f"{es('%(asctime)s').hexColor(in_bracket_text_color)}"
        f"{es(']').hexColor(bracket_color)} "
        f"{es('[').hexColor(bracket_color)}"
        f"{es('%(levelname)s').hexColor(in_bracket_text_color)}"
        f"{es(']').hexColor(bracket_color)} "
        f"{es('[').hexColor(bracket_color)}"
        f"{es('%(name)s').hexColor(in_bracket_text_color)}"
        f"{es(']').hexColor(bracket_color)} "
        f"{es('%(message)s').hexColor(text_color)}",
    )

    loop: AbstractEventLoop = new_event_loop()
    main()
