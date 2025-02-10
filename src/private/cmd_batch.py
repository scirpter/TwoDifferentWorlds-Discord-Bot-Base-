from __future__ import annotations

from importlib import import_module
from importlib.util import find_spec
from types import ModuleType
from typing import TYPE_CHECKING

from aiopath import Path
from discord.ext.commands import Cog, Group, GroupCog


if TYPE_CHECKING:
    from models.client import Void


f = "index"
BASE_FILE_NAME: tuple[str, str] = (f, f + ".py")


async def load_commands_base(client: Void, basecog: GroupCog | Cog, _file: str, _pkg: str | None) -> None:
    """Automatically load all commands in `./*`."""
    excludes: list[str] = client.logical_file_pattern_excludes + [BASE_FILE_NAME[1]]

    async for path in Path(_file).parent.iterdir():
        if path.name.endswith(".py") and not path.name.startswith("_") and path.name not in excludes:
            module: ModuleType = import_module(f".{path.stem}", _pkg)
            if find_spec(f"{_pkg}.{path.stem}"):
                _setup = getattr(module, "setup", None)
                if callable(_setup):
                    await _setup(basecog)  # type: ignore


async def load_commands_sub(client: Void, basecog: GroupCog | Cog, subgroup: Group, __file: str, __pkg: str) -> None:  # type: ignore
    """Automatically load all commands in `./*/*`."""
    excludes: list[str] = client.logical_file_pattern_excludes + [BASE_FILE_NAME[1]]

    async for path in Path(__file).parent.iterdir():
        if (
            await path.is_file()
            and path.name.endswith(".py")
            and not path.name.startswith("_")
            and path.name not in excludes
        ):
            module: ModuleType = import_module(f".{path.stem}", __pkg)
            if find_spec(f"{__pkg}.{path.stem}"):
                _setup = getattr(module, "setup", None)
                if callable(_setup):
                    await _setup(basecog, subgroup)  # type: ignore


async def load_subgroups(client: Void, basecog: GroupCog | Cog, _file: str, _pkg: str | None) -> None:
    """Automatically load all subgroups, e.g. `./*/index.py`."""
    excludes: list[str] = client.logical_file_pattern_excludes

    async for path in Path(_file).parent.iterdir():
        if await path.is_dir():
            async for file in path.iterdir():
                if (
                    await file.is_file()
                    and file.name.endswith(".py")
                    and not file.name.startswith("_")
                    and BASE_FILE_NAME[0] in file.stem
                    and file.name not in excludes
                ):
                    module: ModuleType = import_module(f".{path.name}.{file.stem}", _pkg)
                    if find_spec(f"{_pkg}.{path.name}.{file.stem}"):
                        _setup = getattr(module, "setup", None)
                        if callable(_setup):
                            await _setup(basecog)  # type: ignore
