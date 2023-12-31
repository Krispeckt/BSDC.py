from typing import TYPE_CHECKING

from disnake.ext.commands import Cog
from disnake.ext.tasks import loop

from disnake_sdc import SDCClient

if TYPE_CHECKING:
    from disnake.ext.commands import Bot


class SDC(Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

        self.sdc_client = SDCClient(
            bot=self.bot,
            sdc_token="YOUR_TOKEN_HERE",
            on_success=self.on_success
        )

    async def cog_load(self) -> None:
        await self.bot.wait_until_first_connect()
        self.sdc_post_task.start()

    def cog_unload(self) -> None:
        self.sdc_post_task.cancel()

    async def on_success(self) -> None:
        print("SUCCESS POSTED")

    @loop(minutes=50)
    async def sdc_post_task(self) -> None:
        await self.sdc_client.post()


def setup(bot: "Bot") -> None:
    return bot.add_cog(SDC(bot))
