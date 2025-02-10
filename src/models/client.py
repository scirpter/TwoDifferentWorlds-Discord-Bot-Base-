from configparser import ConfigParser
from logging import info
from typing import Any
import urllib.parse
from aiopath import Path
from discord import Intents, Interaction
from discord.app_commands import Command
from discord.ext.commands import AutoShardedBot
from enhanced_str import es
from handler.lazy_error_handle import lazy_error
from models.command_analytics import CommandAnalyticsEngine
from private.cmd_batch import BASE_FILE_NAME
from tortoise import Tortoise

from .config import ConfigProvider
from .translator import TranslationEngine


class Void(AutoShardedBot):
    def __init__(self, **options: dict[str, Any]) -> None:
        self.config: ConfigParser = ConfigProvider().data

        super().__init__(
            command_prefix='$,lr"^b/::0LrGr</024`W%E54|B#sX>o,HGA9dq^Y~Grd?ka-S9W{%bN/',
            help_command=None,
            description="A Discord bot.",
            intents=Intents.all(),
            options=options,
        )
        self.analytics_engine: None | CommandAnalyticsEngine = None  # type: ignore
        self.translation_engine: TranslationEngine | None = None  # type: ignore
        self.db: Tortoise | None = None
        self.token: str = self.config.get("bot", "token")
        self.tree.on_error = lazy_error
        self.on_error = lazy_error  # type: ignore
        self.logical_file_pattern_excludes: list[str] = self.config.get("bot", "logical_file_pattern_excludes").split(
            " | "
        )

    async def setup_hook(self) -> None:
        database_url: str = (
            "mysql://"
            + self.config.get("database", "user")
            + ":"
            + urllib.parse.quote_plus(self.config.get("database", "password"))
            + "@"
            + self.config.get("database", "host")
            + ":"
            + self.config.get("database", "port")
            + "/"
            + self.config.get("database", "database")
            + "?maxsize=10"
        )
        await Tortoise.init(db_url=database_url, modules={"models": ["db.models"]})
        await Tortoise.generate_schemas()
        info("database init")

        self.analytics_engine: CommandAnalyticsEngine = CommandAnalyticsEngine(self)
        await self.analytics_engine.setup()
        info("analytics engine init")

        self.translation_engine: TranslationEngine = TranslationEngine(self)
        await self.translation_engine.cache_translations()
        await self.tree.set_translator(self.translation_engine)
        info("translation engine init")

        # async for file in Path("src/cache").iterdir():
        #     await file.unlink()
        # info("cleared cache")

        async for path in Path("src/commands").iterdir():
            if await path.is_dir():
                async for file in path.iterdir():
                    if (
                        await file.is_file()
                        and file.name.endswith(".py")
                        and not file.name.startswith("_")
                        and BASE_FILE_NAME[0] in file.stem
                    ):
                        await self.load_extension(f"commands.{path.name}.{file.stem}")
        info(f"loaded {len(self.cogs)} group(s)")
        await self.tree.sync()
        actual_cmds = [c for c in self.tree.walk_commands() if isinstance(c, Command)]
        info(f"synced {len(actual_cmds)} slash commands")

    async def on_app_command_completion(self, interaction: Interaction, command: Command[Any, ..., Any]) -> None:
        await self.analytics_engine.register(interaction, command)

    async def on_ready(self) -> None:
        info(f"{self.user.name} online. You're running on " + es("TwoDifferentWorlds").hexColor(0xFF1F7A).bold())
