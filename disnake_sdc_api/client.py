import asyncio
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Union, Callable

from aiohttp import ClientSession

from .exceptions import IsNotCoro, WaitMore, UnknownException

if TYPE_CHECKING:
    from disnake.ext.commands import Bot, AutoShardedBot

__all__ = (
    "SDCClient",
)


class SDCClient:
    __slots__ = ('_bot', '_token', 'time_for_request', '_success_coro')

    def __init__(
            self, bot: Union["Bot", "AutoShardedBot"],
            sdc_token: str, on_success: Callable
    ) -> None:
        self._bot = bot
        self._token = sdc_token

        if not sdc_token.startswith("SDC "):
            self._token = "SDC " + sdc_token

        if asyncio.iscoroutinefunction(on_success):
            raise IsNotCoro

        self._success_coro = on_success
        self.time_for_request = 0

    async def post(self) -> None:
        await self._bot.wait_until_first_connect()

        if self.time_for_request < datetime.now().timestamp():
            async with ClientSession() as session:
                async with session.post(
                    f"https://api.server-discord.com/v2/bots/{self._bot.user.id}/stats",
                    headers={"Authorization": f"{self._token}"},
                    data={
                        "shards": self._bot.shard_count or 1, "servers": len(self._bot.guilds)
                    }
                ) as response:
                    if response.status != 200:
                        raise UnknownException(f"Response status: {response.status}\n{response.text}")
                    await self._success_coro()
            self.time_for_request = (datetime.now() + timedelta(minutes=40)).timestamp()
            return

        raise WaitMore
