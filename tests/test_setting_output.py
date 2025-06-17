import re

import pytest

pytest_plugins = ("pytester",)

TESTS = """
        import pytest
        
        @pytest.mark.bug
        def test_one():
            assert Fail
        
        @pytest.mark.bug(run=True)
        def test_two():
            assert Fail
        
        @pytest.mark.bug(run=True)
        def test_three():
            assert True
        """


def test_set_options_letter(testdir: pytest.Testdir):
    testdir.makepyfile(TESTS)
    result = testdir.runpytest("--bug-skip-letter=q", "--bug-fail-letter=z", "--bug-pass-letter=r")
    assert result.ret == 0
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py qzr", stdout)
    assert re.search(r"-\sBugs skipped: 1 Bugs passed: 1 Bugs failed: 1\s-", stdout)


def test_set_options_word(testdir: pytest.Testdir):
    testdir.makepyfile(TESTS)
    result = testdir.runpytest("-v", "--bug-skip-word=FORGET", "--bug-fail-word=FUCK", "--bug-pass-word=YAHOO")
    assert result.ret == 0
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py::test_one FORGET", stdout)
    assert re.search(r"\w+\.py::test_two FUCK", stdout)
    assert re.search(r"\w+\.py::test_three YAHOO", stdout)
    assert re.search(r"-\sBugs skipped: 1 Bugs passed: 1 Bugs failed: 1\s-", stdout)


def test_set_ini_letter(testdir: pytest.Testdir):
    testdir.makeini(
        """
        [pytest]
        bug_skip_letter = q
        bug_fail_letter = z
        bug_pass_letter = r
        """
    )
    testdir.makepyfile(TESTS)
    result = testdir.runpytest()
    assert result.ret == 0
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py qzr", stdout)
    assert re.search(r"-\sBugs skipped: 1 Bugs passed: 1 Bugs failed: 1\s-", stdout)


def test_set_ini_word(testdir: pytest.Testdir):
    testdir.makeini(
        """
        [pytest]
        bug_skip_word = FORGET
        bug_fail_word = FUCK
        bug_pass_word = YAHOO
        """
    )
    testdir.makepyfile(TESTS)
    result = testdir.runpytest("-v")
    assert result.ret == 0
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py::test_one FORGET", stdout)
    assert re.search(r"\w+\.py::test_two FUCK", stdout)
    assert re.search(r"\w+\.py::test_three YAHOO", stdout)
    assert re.search(r"-\sBugs skipped: 1 Bugs passed: 1 Bugs failed: 1\s-", stdout)


def test_set_option_priority_letter(testdir: pytest.Testdir):
    testdir.makeini(
        """
        [pytest]
        bug_skip_letter = g
        bug_fail_letter = y
        bug_pass_letter = w
        """
    )
    testdir.makepyfile(TESTS)
    result = testdir.runpytest("--bug-skip-letter=q", "--bug-fail-letter=z", "--bug-pass-letter=r")
    assert result.ret == 0
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py qzr", stdout)
    assert re.search(r"-\sBugs skipped: 1 Bugs passed: 1 Bugs failed: 1\s-", stdout)


def test_set_option_priority_word(testdir: pytest.Testdir):
    testdir.makeini(
        """
        [pytest]
        bug_skip_word = SKIP_TEST
        bug_fail_word = FAIL_TEST
        bug_pass_word = PASS_TEST
        """
    )
    testdir.makepyfile(TESTS)
    result = testdir.runpytest("-v", "--bug-skip-word=FORGET", "--bug-fail-word=FUCK", "--bug-pass-word=YAHOO")
    assert result.ret == 0
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py::test_one FORGET", stdout)
    assert re.search(r"\w+\.py::test_two FUCK", stdout)
    assert re.search(r"\w+\.py::test_three YAHOO", stdout)
    assert re.search(r"-\sBugs skipped: 1 Bugs passed: 1 Bugs failed: 1\s-", stdout)
