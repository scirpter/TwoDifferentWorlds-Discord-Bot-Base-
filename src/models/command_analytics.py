from __future__ import annotations

from typing import TYPE_CHECKING, Any
from discord.app_commands import Command
from discord import Interaction


if TYPE_CHECKING:
    from models.client import Void


class CommandAnalyticsEngine:
    def __init__(self, client: Void) -> None:
        self.client: Void = client

    async def setup(self) -> None:
        ...

    async def get_command_data(self, command_full_name: str, /) -> dict[str, Any]:
        ...

    async def add_command_entry_if_not_exists(self, command_full_name: str, /) -> None:
        ...

    async def register(self, interaction: Interaction, command: Command) -> None:  # type: ignore
        ...
