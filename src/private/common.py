import sys
from configparser import ConfigParser
from datetime import datetime, timezone, timedelta
from logging import error
import pytz
from typing import TYPE_CHECKING
from discord import Guild, Interaction, Member, Role
from discord.app_commands import Command, Group
from discord.ext.commands import GroupCog


if TYPE_CHECKING:
    from models.client import Void


def is_valid_hex_string(hex_string: str, /) -> bool:
    try:
        int(hex_string, 16)
    except ValueError:
        return False
    return True


def money_to_short_money(money: int, /) -> str:
    if money >= 1_000_000_000:
        return f"{money / 1_000_000_000:.2f}B"
    if money >= 1_000_000:
        return f"{money / 1_000_000:.2f}M"
    if money >= 1_000:
        return f"{money / 1_000:.2f}K"
    return str(money)


def current_utc_and(days: int, hours: int, minutes: int, /) -> datetime:
    return datetime.now(pytz.utc) + timedelta(days=days, hours=hours, minutes=minutes)


async def to_proper_ts(timestamp: float, /) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%a, %b %d, %Y %I:%M %p UTC")


def get_config_hex(config: ConfigParser, section: str, key: str) -> int:
    return int(config.get(section, key), 16)


def get_config_int_list(config: ConfigParser, section: str, key: str) -> list[int]:
    return [int(x) for x in config.get(section, key).split(" | ")]


def is_bot_administrator(config: ConfigParser, user_id: int, /) -> bool:
    return user_id in get_config_int_list(config, "bot", "administrators")


def get_full_command_name(command: Command) -> str:  # type: ignore
    base: Group | None = command.root_parent
    sub: Group | GroupCog | None = command.parent
    command_name: str = command.name
    full: str = f"{'' if not base else ' ' + base.qualified_name}{'' if not sub else sub.name}{command_name}"
    return full


async def is_server_patreon_subbed(interaction: Interaction, /) -> bool:
    client: Void = interaction.client  # type: ignore
    support_server: Guild | None = client.get_guild(int(client.config.get("bot", "support_server_id")))

    if not support_server:
        error("support server not found. please configure the bot properly.")
        sys.exit(1)

    if interaction.user not in support_server.members:
        return False

    if interaction.guild.owner == interaction.user:
        # check if the interaction.user has the patreon role in the support server
        patreon_role: Role | None = support_server.get_role(int(client.config.get("bot", "patreon_role_id")))
        if not patreon_role:
            error("Patreon role not found. Please update the config.")
            raise Exception(
                "Patreon role not found from given client "
                "configuration (PATREON_ROLE_ID). "
                "Please wait for a fix by the bot owners."
            )

        support_server_user: Member | None = support_server.get_member(interaction.user.id)
        if patreon_role not in support_server_user.roles:
            return False
        return True
    return False
