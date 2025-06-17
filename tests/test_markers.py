import re

import pytest

pytest_plugins = ("pytester",)

PARAMETRIZE = (("import pytest", "pytest.mark."), ("from pytest_bug import bug", ""))


@pytest.mark.parametrize(("test_import", "test_mark"), PARAMETRIZE)
def test_mark_func_and_class(testdir: pytest.Testdir, test_import: str, test_mark: str):
    testdir.makepyfile(
        f"""
        {test_import}

        @{test_mark}bug('skip')
        def test_one():
            assert False

        @{test_mark}bug('fail', run=True)
        def test_two():
            assert False

        @{test_mark}bug('pass', run=True)
        def test_three():
            assert True

        @{test_mark}bug('skip class')
        class TestFour:

            def test_one(self):
                assert False

            def test_two(self):
                assert True

        @{test_mark}bug('class', run=True)
        class TestFive:

            def test_one(self):
                assert False

            def test_two(self):
                assert True
        """
    )
    result = testdir.runpytest()
    assert result.ret == 0
    result.assert_outcomes(passed=2, skipped=5)
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py bfpbbfp", stdout)
    assert re.search(r"-\sBugs skipped: 3 Bugs passed: 2 Bugs failed: 2\s-", stdout)


@pytest.mark.parametrize(("test_import", "test_mark"), PARAMETRIZE)
def test_mark_module_no_run(testdir: pytest.Testdir, test_import: str, test_mark: str):
    testdir.makepyfile(
        f"""
        {test_import}
        
        pytestmark = {test_mark}bug('skip file')
        
        def test_one():
            assert False
        
        def test_two():
            assert True
        """
    )
    result = testdir.runpytest()
    assert result.ret == 0
    result.assert_outcomes(skipped=2)
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py bb", stdout)
    assert re.search(r"-\sBugs skipped: 2\s-", stdout)


@pytest.mark.parametrize(("test_import", "test_mark"), PARAMETRIZE)
def test_mark_module_run_true(testdir: pytest.Testdir, test_import: str, test_mark: str):
    testdir.makepyfile(
        f"""
        {test_import}
        
        pytestmark = {test_mark}bug('file bug', run=True)
        
        def test_one():
            assert False
        
        def test_two():
            assert True
        """
    )
    result = testdir.runpytest()
    assert result.ret == 0
    result.assert_outcomes(skipped=1, passed=1)
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py fp", stdout)
    assert re.search(r"-\sBugs passed: 1 Bugs failed: 1\s-", stdout)
