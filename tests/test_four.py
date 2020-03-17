from pytest_bug import bug

pytestmark = bug('skip file')


def test_one():
    assert False


def test_two():
    assert True
