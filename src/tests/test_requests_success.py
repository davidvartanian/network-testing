from datetime import datetime, timedelta
from typing import Callable

from requests import Session

from utils import remove_tc


def test_simple_request(session_factory: Callable[[bool], Session]) -> None:
    session_without_retry: Session = session_factory(False)
    # ensure tc is off
    remove_tc()

    response = session_without_retry.get("http://api:8080", timeout=0.5)
    assert response.status_code == 200


def test_longrun_request(session_factory: Callable[[bool], Session]) -> None:
    session_without_retry: Session = session_factory(False)
    # ensure tc is off
    remove_tc()

    start = datetime.now()
    response = session_without_retry.get("http://api:8080/longrun", timeout=2)
    end = datetime.now()
    assert response.status_code == 200
    content = response.json()
    assert content.get("message") == "Slow response"
    assert end - start >= timedelta(seconds=1)
