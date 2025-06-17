import pytest

pytest_plugins = ("pytester",)

TESTS = """
import pytest

@pytest.mark.bug('C345 Invalid value', run=True)
def test_one():
    assert True

@pytest.mark.bug('C346', 'Invalid type', run=True)
def test_two():
    assert True
    
@pytest.mark.bug('Critical bug', issue='476', run=True)
def test_three():
    assert True

@pytest.mark.bug('All is bad')
def test_four():
    assert True
    
def test_five():
    assert False
    
@pytest.mark.bug(2671, 'No Value', run=True)
def test_six():
    assert True
"""


def test_search_start(testdir: pytest.Testdir):
    testdir.makepyfile(TESTS)
    result = testdir.runpytest(r"--bug-pattern=^C34\d")
    assert result.ret == 0
    outcomes = result.parseoutcomes()
    assert outcomes["passed"] == 2
    assert outcomes["deselected"] == 4


def test_search_word(testdir: pytest.Testdir):
    testdir.makepyfile(TESTS)
    result = testdir.runpytest(r"--bug-pattern=Invalid")
    assert result.ret == 0
    outcomes = result.parseoutcomes()
    assert outcomes["passed"] == 2
    assert outcomes["deselected"] == 4


def test_search_words(testdir: pytest.Testdir):
    testdir.makepyfile(TESTS)
    result = testdir.runpytest(r"--bug-pattern=Invalid type")
    assert result.ret == 0
    outcomes = result.parseoutcomes()
    assert outcomes["passed"] == 1
    assert outcomes["deselected"] == 5


def test_search_ignore_case(testdir: pytest.Testdir):
    testdir.makepyfile(TESTS)
    result = testdir.runpytest(r"--bug-pattern=invalid type")
    assert result.ret == 0
    outcomes = result.parseoutcomes()
    assert outcomes["passed"] == 1
    assert outcomes["deselected"] == 5


def test_search_ignore_case2(testdir: pytest.Testdir):
    testdir.makepyfile(TESTS)
    result = testdir.runpytest(r"--bug-pattern=CrItIcAl bUg")
    assert result.ret == 0
    outcomes = result.parseoutcomes()
    assert outcomes["passed"] == 1
    assert outcomes["deselected"] == 5


def test_search_or(testdir: pytest.Testdir):
    testdir.makepyfile(TESTS)
    result = testdir.runpytest(r"--bug-pattern=(C345|C346)")
    assert result.ret == 0
    outcomes = result.parseoutcomes()
    assert outcomes["passed"] == 2
    assert outcomes["deselected"] == 4


def test_search_any(testdir: pytest.Testdir):
    testdir.makepyfile(TESTS)
    result = testdir.runpytest(r"--bug-pattern=.*")
    assert result.ret == 0
    outcomes = result.parseoutcomes()
    assert outcomes["passed"] == 4
    assert outcomes["deselected"] == 1
    assert outcomes["skipped"] == 1


def test_search_kwargs(testdir: pytest.Testdir):
    testdir.makepyfile(TESTS)
    result = testdir.runpytest(r"--bug-pattern=issue=476")
    assert result.ret == 0
    outcomes = result.parseoutcomes()
    assert outcomes["passed"] == 1
    assert outcomes["deselected"] == 5


def test_search_int(testdir: pytest.Testdir):
    testdir.makepyfile(TESTS)
    result = testdir.runpytest(r"--bug-pattern=2671")
    assert result.ret == 0
    outcomes = result.parseoutcomes()
    assert outcomes["passed"] == 1
    assert outcomes["deselected"] == 5
