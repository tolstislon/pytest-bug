import pytest


@pytest.mark.bug('skip')
def test_one():
    assert False


@pytest.mark.bug('fail', run=True)
def test_two():
    assert False


@pytest.mark.bug('pass', run=True)
def test_three():
    assert True


@pytest.mark.bug('skip class')
class TestFour:

    def test_one(self):
        assert False

    def test_two(self):
        assert True


@pytest.mark.bug('class', run=True)
class TestFive:

    def test_one(self):
        assert False

    def test_two(self):
        assert True
