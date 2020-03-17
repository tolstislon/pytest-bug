import pytest

pytestmark = pytest.mark.bug('skip file')


def test_one():
    assert False


def test_two():
    assert True
