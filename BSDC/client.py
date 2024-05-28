from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Union, Coroutine, Awaitable

from aiohttp import ClientSession

from .exceptions import IsNotCoro, UnknownException, TaskNotFound

if TYPE_CHECKING:
    from disnake.ext.commands import Bot, InteractionBot

__all__ = (
    "BSDCClient",
)


class BSDCClient:
    __item: BSDCClient = None
    __slots__ = (
        '_bot',
        '_token',
        '_success_coro',
        '_session',
        '__task',
    )

    @classmethod
    def __set_item(cls, self: BSDCClient) -> None:
        cls.__item = self

    @classmethod
    def get_client(cls) -> BSDCClient | None:
        """
        Retrieves the singleton instance of BSDCClient.

        This method is a class method, so it can be called directly on the class (BSDCClient.get_client()).
        If the instance has not been created yet, it will raise an exception.

        Parameters:
        - None

        Returns:
        - BSDCClient | None: The singleton instance of BSDCClient or None if not created yet.

        Note:
        - This method is intended to be used to retrieve the singleton instance of BSDCClient.
        - It should not be used to create a new instance of BSDCClient.
        """
        return cls.__item

    def __init__(
            self,
            bot: Union[Bot, InteractionBot],
            token: str,
            on_success: Coroutine[None, None, any] | None = None
    ) -> None:
        self._bot = bot
        self._token = token

        if not token.startswith("SDC "):
            self._token = "SDC " + token

        if on_success and not asyncio.iscoroutinefunction(on_success):
            raise IsNotCoro

        self._session = ClientSession()
        self._success_coro = on_success
        self.__task = None

        self.__set_item(self)

    async def __schedule_task(self) -> None:
        while True:
            await self.post()
            if self._success_coro:
                await self._success_coro

            await asyncio.sleep(3600)

    async def start_auto_post(self, func: Coroutine[None, None, any] | None = None) -> None:
        """
        Starts the automatic posting of bot statistics to B.SDC monitoring.

        Parameters:
        - func (Coroutine[None, None, any] | None): A coroutine function to be executed after each successful post.
            If None, the default success coroutine will be used.

        Returns:
        - None

        Raises:
        - None

        Note:
        - This method cancels any existing scheduled tasks and starts a new one.
        - The bot statistics will be posted every 50 minutes.
        """
        await self._bot.wait_until_ready()

        if func:
            self._success_coro = func

        if self.__task:
            self.__task.cancel()

        self.__task = asyncio.create_task(self.__schedule_task())

    def stop_auto_post(self) -> None:
        """
        Cancels the scheduled task for automatic posting of bot statistics to B.SDC monitoring.

        Parameters:
        - None

        Returns:
        - None

        Raises:
        - TaskNotFound: If no scheduled task is found to cancel.

        Note:
        - This method should be called when the automatic posting of bot statistics is no longer needed.
        - It cancels the existing scheduled task, preventing further automatic posts.
        """
        if not self.__task:
            raise TaskNotFound

        self.__task.cancel()

    async def post(self) -> None:
        """
        Sends a POST request to the B.SDC monitoring to update the bot's statistics.

        Parameters:
        - None

        Returns:
        - None

        Raises:
        - UnknownException: If the response status is not 200.
        - WaitMore: If the time for the next request has not yet passed.
        """
        async with self._session.post(
                f"https://api.server-discord.com/v2/bots/{self._bot.user.id}/stats",
                headers={"Authorization": f"{self._token}"},
                data={
                    "shards": self._bot.shard_count or 1,
                    "servers": len(self._bot.guilds)
                }
        ) as response:
            if response.status != 200:
                raise UnknownException(f"Response status: {response.status}\n{response.text}")

            if self._success_coro:
                await self._success_coro
