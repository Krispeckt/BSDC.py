from __future__ import annotations

from typing import TYPE_CHECKING

from disnake.ext.commands import Cog
from loguru import logger

from BSDC import BSDCClient

if TYPE_CHECKING:
    from disnake.ext.commands import Bot


class BSDC(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

        self.bsdc_client = BSDCClient(bot, "YOUR_TOKEN")

    async def cog_load(self) -> None:
        await self.bsdc_client.start_auto_post(self.on_success())

    def cog_unload(self) -> None:
        self.bsdc_client.stop_auto_post()

    async def on_success(self) -> None:
        logger.info("Successfully posted bot statistics to B.SDC monitoring.")


def setup(bot: Bot) -> None:
    return bot.add_cog(BSDC(bot))
