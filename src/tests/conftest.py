from typing import Callable
import pytest
from httpx import AsyncClient
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry


BASE_URL = "http://api:8080"


@pytest.fixture
def async_client() -> AsyncClient:
    return AsyncClient(base_url=BASE_URL)


@pytest.fixture
def session_factory() -> Callable[[bool], Session]:
    def factory(with_retries=False) -> Session:
        session = Session()
        if with_retries:
            retries = 1
            retry = Retry(
                total=retries,
                read=retries,
                connect=retries,
                backoff_factor=0.2,
                status_forcelist=[],
            )
            adapter = HTTPAdapter(max_retries=retry)
        else:
            adapter = HTTPAdapter()  # no need for a custom adapter
        session.mount(BASE_URL, adapter)
        return session

    return factory