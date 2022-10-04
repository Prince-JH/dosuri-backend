import pytest


@pytest.fixture(scope='session')
def dummy_user():
    return {
        'task_always_eager': True
    }
