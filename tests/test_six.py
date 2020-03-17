from pytest_bug import bug

pytestmark = bug('file bug', run=True)


def test_one():
    assert False


def test_two():
    assert True
