from pytest_bug import bug


@bug('skip')
def test_one():
    assert False


@bug('fail', run=True)
def test_two():
    assert False


@bug('pass', run=True)
def test_three():
    assert True


@bug('skip class')
class TestFour:

    def test_one(self):
        assert False

    def test_two(self):
        assert True


@bug('class', run=True)
class TestFive:

    def test_one(self):
        assert False

    def test_two(self):
        assert True
