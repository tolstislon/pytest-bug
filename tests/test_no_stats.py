import re

import pytest

pytest_plugins = ("pytester",)

tests = """
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
        """


def test_disable_stats_option(testdir: pytest.Testdir):
    testdir.makepyfile(tests)
    result = testdir.runpytest("--bug-no-stats")
    assert result.ret == 0
    result.assert_outcomes(skipped=2, passed=1)
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py bfp", stdout)
    assert not re.search("Bugs", stdout)


def test_disable_stats_ini(testdir: pytest.Testdir):
    testdir.makeini(
        """
        [pytest]
        bug_summary_stats = false
        """
    )
    testdir.makepyfile(tests)
    result = testdir.runpytest()
    assert result.ret == 0
    result.assert_outcomes(skipped=2, passed=1)
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py bfp", stdout)
    assert not re.search("Bugs", stdout)


def test_disable_stats_option_enable_ini(testdir: pytest.Testdir):
    testdir.makeini(
        """
        [pytest]
        bug_summary_stats = true
        """
    )
    testdir.makepyfile(tests)
    result = testdir.runpytest("--bug-no-stats")
    assert result.ret == 0
    result.assert_outcomes(skipped=2, passed=1)
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py bfp", stdout)
    assert not re.search("Bugs", stdout)


def test_enable_ini(testdir: pytest.Testdir):
    testdir.makeini(
        """
        [pytest]
        bug_summary_stats = true
        """
    )
    testdir.makepyfile(tests)
    result = testdir.runpytest()
    assert result.ret == 0
    result.assert_outcomes(skipped=2, passed=1)
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py bfp", stdout)
    assert re.search(r"-\sBugs skipped: 1 Bugs passed: 1 Bugs failed: 1\s-", stdout)
