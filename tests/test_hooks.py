import re

import pytest

pytest_plugins = ("pytester",)


def test_pytest_bug_set_mark(testdir: pytest.Testdir):
    testdir.makeconftest(
        """
        import pytest
        
        def pytest_bug_set_mark(mark_bug, config):
            mark_bug.comment = mark_bug.comment.replace('BUG', 'FEATURE')
            mark_bug.run = True
            
        def pytest_runtest_makereport(item):
            mark_bug = item._mark_bug
            assert mark_bug.comment == 'FEATURE: comment'
        """
    )
    testdir.makepyfile(
        """
        import pytest
        
        @pytest.mark.bug('comment')
        def test_one():
            assert True
        """
    )

    result = testdir.runpytest()
    assert result.ret == 0
    result.assert_outcomes(passed=1)


def test_pytest_bug_report_teststatus(testdir: pytest.Testdir):
    testdir.makeconftest(
        """
        import pytest

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

    result = testdir.runpytest()
    assert result.ret == 0
    result.assert_outcomes(passed=1)
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py 1", stdout)
