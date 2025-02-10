"""Global error handler for lazy peeps."""

from traceback import print_exc

from discord import Interaction
from discord.app_commands import (
    BotMissingPermissions,
    CheckFailure,
    CommandOnCooldown,
    MissingPermissions,
)
from private.embeds import EmbedTemplates as Et


async def lazy_error(
    interaction: Interaction,
    exc: CheckFailure | Exception,
) -> None:
    command = interaction.command
    try:
        await interaction.response.defer(ephemeral=True)
    except Exception:
        pass

    if isinstance(exc, BotMissingPermissions):
        actual_bmp: BotMissingPermissions = exc
        return await interaction.followup.send(
            embed=Et.Error("I'm missing permissions `" + f"{'`, `'.join(actual_bmp.missing_permissions)}`.".upper()),
            ephemeral=True,
        )
    elif isinstance(exc, MissingPermissions):
        actual_mp: MissingPermissions = exc
        return await interaction.followup.send(
            embed=Et.Error("You're missing permissions `" + f"{'`, `'.join(actual_mp.missing_permissions)}`.".upper()),
            ephemeral=True,
        )
    elif isinstance(exc, CheckFailure):
        if command.nsfw and not interaction.channel.nsfw:  # type: ignore
            return await interaction.followup.send(
                embed=Et.Error("This command can only be used in NSFW channels."),
                ephemeral=True,
            )
    elif isinstance(exc, CommandOnCooldown):
        return await interaction.followup.send(
            embed=Et.Error(f"This command is on cooldown. Try again in `{exc.retry_after:.2f}s`."),
            ephemeral=True,
        )

    await interaction.followup.send(embed=Et.Error(str(exc)), ephemeral=True)
    print_exc()
