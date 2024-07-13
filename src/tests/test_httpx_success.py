from datetime import datetime, timedelta
import pytest
from httpx import AsyncClient, Response

from utils import remove_tc


@pytest.mark.asyncio
async def test_simple_request(async_client: AsyncClient) -> None:
    # ensure tc is removed
    remove_tc()
    
    response: Response = await async_client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_longrun_request(async_client: AsyncClient) -> None:
    # ensure tc is removed
    remove_tc()

    async_client.timeout = 2
    start = datetime.now()
    response: Response = await async_client.get("/longrun")
    end = datetime.now()
    assert response.status_code == 200
    content = response.json()
    assert content.get("message") == "Slow response"
    assert end - start >= timedelta(seconds=1)