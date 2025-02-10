from typing import Any

from discord import Embed
from private.ansi import TextColor, ansi
from private.consts import DARK_MIDNIGHT_HEX, EXPLOSION_EMOJI, RED_HEX


class EmbedTemplates:
    class AIO(Embed):
        def __init__(
            self,
            /,
            description: str | None = None,
            *,
            props: dict[str, Any] | None = None,
            **kwargs: ...,
        ) -> None:
            if props is None:
                props = {}

            super().__init__(
                color=DARK_MIDNIGHT_HEX,
                description=description,
                **kwargs,  # type: ignore
            )

            self.set_footer(
                text=props.get("footer", ""),
                icon_url=props.get("footer_icon"),
            )
            self.set_image(url=props.get("image"))
            self.set_thumbnail(url=props.get("thumbnail"))

            for field in props.get("fields", []):
                self.add_field(**field)

    class Simple(Embed):
        def __init__(self, t: str) -> None:
            super().__init__(
                color=DARK_MIDNIGHT_HEX,
                description=t,
            )

    class Error(Embed):
        def __init__(self, t: str) -> None:
            super().__init__(
                color=RED_HEX,
                description=f"### {EXPLOSION_EMOJI} Es gab einen Fehler beim Ausführen der Anfrage.\n\n{ansi(text_color=TextColor.RED, text=t)}",
            )

    class Success(Embed):
        def __init__(self, t: str) -> None:
            super().__init__(
                color=DARK_MIDNIGHT_HEX,
                description=t,
            )
