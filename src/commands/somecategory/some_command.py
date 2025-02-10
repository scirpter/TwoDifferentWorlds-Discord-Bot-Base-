from discord import Interaction
from discord.app_commands import Command, describe
from discord.app_commands.checks import has_permissions
from commands.somecategory.index import SomeCategory


class SomeCommand(Command):
    def __init__(self, basecog: SomeCategory) -> None:
        super().__init__(
            name="some-command",
            description="This is a description",
            callback=self.callback,
        )
        self.basecog: SomeCategory = basecog

    @has_permissions(administrator=True)
    @describe(some_argument="This is a description for /some-argument")
    async def callback(self, interaction: Interaction, some_argument: str) -> None:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(f"Do something with {some_argument}!")


async def setup(basecog: SomeCategory) -> None:
    basecog.app_command.add_command(SomeCommand(basecog))
