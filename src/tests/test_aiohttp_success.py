from typing import Callable

import pytest
from aiohttp import ClientResponse, ClientSession

from utils import remove_tc


@pytest.mark.asyncio
async def test_simple_request(aiohttp_factory: Callable[[], ClientSession]) -> None:
    # ensure tc is removed
    remove_tc()

    aiohttp_client = aiohttp_factory()

    async with aiohttp_client:
        response: ClientResponse = await aiohttp_client.get("/")
    assert response.status == 200
