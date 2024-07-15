from datetime import datetime, timedelta
from typing import Callable

import pytest
from aiohttp import ClientSession, ClientTimeout

from utils import apply_tc


@pytest.mark.asyncio
async def test_timeout_request(
    aiohttp_factory: Callable[[ClientTimeout | None], ClientSession]
) -> None:
    timeout = 0.5
    client_timeout = ClientTimeout(total=timeout)
    aiohttp_client = aiohttp_factory(client_timeout)

    async with aiohttp_client:
        start = datetime.now()
        with pytest.raises(TimeoutError):
            await aiohttp_client.get("/longrun")
        end = datetime.now()
    assert end - start < timedelta(seconds=1)


@pytest.mark.asyncio
async def test_network_failure(
    aiohttp_factory: Callable[[ClientTimeout | None], ClientSession]
) -> None:
    """
    Since httpx doesn't use urllib's retry mechanism, it's easy to test by turning network traffic on and off.
    """
    timeout = 0.5
    client_timeout = ClientTimeout(total=timeout)
    aiohttp_client = aiohttp_factory(client_timeout)

    # make network traffic fail
    apply_tc()

    async with aiohttp_client:
        start = datetime.now()
        with pytest.raises(TimeoutError):
            await aiohttp_client.get("/")
        end = datetime.now()

    # This proves that, when the network fails to provide the response, the request waits until the specified timeout.
    assert end - start >= timedelta(seconds=timeout)
