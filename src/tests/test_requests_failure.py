from datetime import datetime, timedelta
import pytest
from requests import Session
from requests.exceptions import ReadTimeout, ConnectTimeout

from utils import PatchedMakeRequest, apply_tc, remove_tc


def test_timeout_request(session_factory) -> None:
    session_without_retry: Session = session_factory(with_retries=False)
    # ensure tc is off
    remove_tc()
    timeout = 0.5
    start = datetime.now()
    with pytest.raises(ReadTimeout):
        session_without_retry.get("http://api:8080/longrun", timeout=timeout)
    end = datetime.now()
    
    # This proves that network errors makes the request hang until the configured timeout.
    # In this particular case, the request time could be equal or very close to the timeout because there's no retry.
    assert end - start >= timedelta(seconds=timeout)


def test_network_error_retry_success(session_factory) -> None:
    """
    This only works in the test context because HTTPConnectionPool._make_request has been monkey-patched to apply and remove tc.
    """
    # this context manager will make only the first attempt fail
    with PatchedMakeRequest():
        session_with_retries: Session = session_factory(with_retries=True)
        timeout = 0.5
        start = datetime.now()
        response = session_with_retries.get("http://api:8080", timeout=timeout)
        end = datetime.now()
    assert response.status_code == 200

    # This proves that network errors makes the request hang until the configured timeout.
    # In this case, the difference is greater than the expected timeout because of the successful retry after the failure.
    assert end - start > timedelta(seconds=timeout)


def test_network_error_failure(session_factory) -> None:
    session_without_retry = session_factory(with_retries=False)
    apply_tc()
    with pytest.raises(ConnectTimeout):
        session_without_retry.get("http://api:8080", timeout=0.1)
