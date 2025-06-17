import re

import pytest

pytest_plugins = ("pytester",)


def test_func_and_class(testdir: pytest.Testdir):
    testdir.makepyfile(
        """
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
            """
    )
    result = testdir.runpytest("-v")
    assert result.ret == 0
    result.assert_outcomes(passed=2, skipped=5)
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py::test_one BUG-SKIP", stdout)
    assert re.search(r"\w+\.py::test_two BUG-FAIL", stdout)
    assert re.search(r"\w+\.py::test_three BUG-PASS", stdout)
    assert re.search(r"\w+\.py::TestFour::test_one BUG-SKIP", stdout)
    assert re.search(r"\w+\.py::TestFour::test_two BUG-SKIP", stdout)
    assert re.search(r"\w+\.py::TestFive::test_one BUG-FAIL", stdout)
    assert re.search(r"\w+\.py::TestFive::test_two BUG-PASS", stdout)
    assert re.search(r"-\sBugs skipped: 3 Bugs passed: 2 Bugs failed: 2\s-", stdout)


def test_module_run_true(testdir: pytest.Testdir):
    testdir.makepyfile(
        """
        import pytest

        pytestmark = pytest.mark.bug('file bug', run=True)

        def test_one():
            assert False

        def test_two():
            assert True
        """
    )
    result = testdir.runpytest("-v")
    assert result.ret == 0
    result.assert_outcomes(skipped=1, passed=1)
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py::test_one BUG-FAIL", stdout)
    assert re.search(r"\w+\.py::test_two BUG-PASS", stdout)
    assert re.search(r"-\sBugs passed: 1 Bugs failed: 1\s-", stdout)
