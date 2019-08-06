from servererror.controllers import servererror_controller
from datetime import datetime
import pytest


@pytest.fixture
def error_fixture():
    return Exception('Server Error')


@pytest.fixture
def action_fixture():
    return 'test'


@pytest.fixture
def time_fixture():
    return datetime.now().timestamp()


@pytest.fixture
def data_fixture():
    return 'message'


@pytest.fixture
def request_fixture(action_fixture, time_fixture, data_fixture):
    return {
        'action': action_fixture,
        'time': time_fixture,
        'data': data_fixture
    }


def test_servererror_controller(request_fixture, error_fixture):
    try:
        servererror_controller(request_fixture)
    except Exception as err:
        return err == error_fixture
