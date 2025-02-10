from discord.app_commands import guild_only
from discord.ext.commands import GroupCog
from models.client import Void
from private.cmd_batch import load_commands_base, load_subgroups


@guild_only()
class SomeCategory(GroupCog, group_name="some-category"):
    def __init__(self, /, client: Void) -> None:
        super().__init__()
        self.client: Void = client


async def setup(client: Void) -> None:
    basecog: SomeCategory = SomeCategory(client)

    await load_subgroups(client, basecog, __file__, __package__)
    await load_commands_base(client, basecog, __file__, __package__)
    await client.add_cog(basecog)
