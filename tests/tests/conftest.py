"""Module contains pytest fixtures used to interact with simple_app service/container"""
import pytest

import service


@pytest.fixture(scope='function')
def simple_app():
    """
    Return SimpleApp service object used to interact with SimpleApp service running in CUT.

    This fixture will handle setup/teardown for all interactions with service.
    """
    with service.SimpleApp() as simple_app_service:
        yield simple_app_service
