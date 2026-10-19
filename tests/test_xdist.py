import re

import pytest

pytest_plugins = ("pytester",)

pytest.importorskip("xdist")

TESTS = """
    import pytest

    @pytest.mark.bug('skip')
    def test_skip():
        assert False

    @pytest.mark.bug('fail', run=True)
    def test_fail():
        assert False

    @pytest.mark.bug('pass', run=True)
    def test_pass():
        assert True

    def test_plain():
        assert True
    """


@pytest.mark.parametrize("workers", ("1", "2"))
def test_xdist_reports(testdir: pytest.Testdir, workers: str):
    """Reports with ReportBug survive the worker -> controller transfer; the summary is built on the controller."""
    testdir.makepyfile(TESTS)
    result = testdir.runpytest_subprocess("-n", workers, "-v")
    assert result.ret == 0
    result.assert_outcomes(passed=2, skipped=2)
    stdout = result.stdout.str()
    assert "INTERNALERROR" not in stdout
    assert re.search(r"BUG-SKIP .*::test_skip", stdout)
    assert re.search(r"BUG-FAIL .*::test_fail", stdout)
    assert re.search(r"BUG-PASS .*::test_pass", stdout)
    assert "Bugs skipped: 1 Bugs passed: 1 Bugs failed: 1" in stdout


def test_xdist_report_teststatus_hook(testdir: pytest.Testdir):
    """The restored ReportBug reaches pytest_bug_report_teststatus on the controller."""
    testdir.makeconftest(
        """
        def pytest_bug_report_teststatus(report, report_bug):
            report_bug.letter = '1'
        """
    )
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.bug('comment', run=True)
        def test_one():
            assert True
        """
    )
    result = testdir.runpytest_subprocess("-n", "1")
    assert result.ret == 0
    result.assert_outcomes(passed=1)
    assert re.search(r"^1 +\[100%\]", result.stdout.str(), re.MULTILINE)
