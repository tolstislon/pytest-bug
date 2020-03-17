import pytest

pytestmark = pytest.mark.bug('file bug', run=True)


def test_one():
    assert False


def test_two():
    assert True
