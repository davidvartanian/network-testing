from datetime import datetime, timedelta
import pytest
from httpx import AsyncClient, ConnectError, ConnectTimeout, ReadTimeout

from utils import apply_tc, remove_tc


@pytest.mark.asyncio
async def test_timeout_request(async_client: AsyncClient) -> None:
    async_client.timeout = 0.5
    start = datetime.now()
    with pytest.raises(ReadTimeout):
        await async_client.get("/longrun")
    end = datetime.now()
    assert end - start < timedelta(seconds=1)


@pytest.mark.asyncio
async def test_network_failure(async_client: AsyncClient) -> None:
    """
    Since httpx doesn't use urllib's retry mechanism, it's easy to test by turning network traffic on and off.
    """
    timeout = 0.5
    async_client.timeout = timeout
    
    # make network traffic fail
    apply_tc()
    
    start = datetime.now()
    with pytest.raises(ConnectTimeout):
        await async_client.get("/")
    end = datetime.now()
    
    # This proves that, when the network fails to provide the response, the request waits until the specified timeout.
    assert end - start >= timedelta(seconds=timeout)
