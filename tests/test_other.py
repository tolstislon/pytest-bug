import re

import pytest

pytest_plugins = ("pytester",)


def test_item_attr(testdir: pytest.Testdir):
    testdir.makeconftest(
        """        
        def pytest_runtest_makereport(item):
            mark_bug = item._mark_bug
            assert mark_bug.comment == 'BUG: test'
        """
    )
    testdir.makepyfile(
        """
        import pytest
        
        @pytest.mark.bug('test', run=True)
        def test_one():
            assert True
            
        @pytest.mark.bug('test')
        def test_two():
            assert False
            
        @pytest.mark.bug('test', run=True)
        def test_three():
            assert False
        """
    )
    result = testdir.runpytest()
    assert result.ret == 0


def test_item_attr_no_comment(testdir: pytest.Testdir):
    testdir.makeconftest(
        """        
        def pytest_runtest_makereport(item):
            mark_bug = item._mark_bug
            assert mark_bug.comment == 'BUG: no comment'
        """
    )
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.bug(run=True)
        def test_one():
            assert True

        @pytest.mark.bug
        def test_two():
            assert False

        @pytest.mark.bug(run=True)
        def test_three():
            assert False
        """
    )
    result = testdir.runpytest()
    assert result.ret == 0


def test_report_item(testdir: pytest.Testdir):
    testdir.makeconftest(
        """
        def pytest_runtest_logreport(report):
            if report.when == 'call':
                mark_bug = report._mark_bug
                assert mark_bug.comment == 'BUG: test'
        """
    )
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.bug('test', run=True)
        def test_one():
            assert True

        @pytest.mark.bug('test')
        def test_two():
            assert False

        @pytest.mark.bug('test', run=True)
        def test_three():
            assert False
        """
    )
    result = testdir.runpytest()
    assert result.ret == 0


def test_report_item_no_comment(testdir: pytest.Testdir):
    testdir.makeconftest(
        """
        def pytest_runtest_logreport(report):
            if report.when == 'call':
                mark_bug = report._mark_bug
                assert mark_bug.comment == 'BUG: no comment'
        """
    )
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.bug(run=True)
        def test_one():
            assert True

        @pytest.mark.bug
        def test_two():
            assert False

        @pytest.mark.bug(run=True)
        def test_three():
            assert False
            
        @pytest.mark.bug(run=False)
        def test_four():
            assert False
        """
    )
    result = testdir.runpytest()
    assert result.ret == 0


def test_run_test_marked_as_bug(testdir: pytest.Testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.bug('test', run=True)
        def test_one():
            assert True

        @pytest.mark.bug('test')
        def test_two():
            assert False

        def test_three():
            assert False
        """
    )
    result = testdir.runpytest("-m bug")
    assert result.ret == 0
    outcomes = result.parseoutcomes()
    assert outcomes["passed"] == 1
    assert outcomes["deselected"] == 1
    assert outcomes["skipped"] == 1


def test_run_all_bugs(testdir: pytest.Testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.bug('test', run=True)
        def test_one():
            assert True

        @pytest.mark.bug('test')
        def test_two():
            assert False

        def test_three():
            assert False
        """
    )
    result = testdir.runpytest("--bug-all-run")
    result.assert_outcomes(skipped=1, passed=1, failed=1)
    stdout = result.stdout.str()
    assert re.search(r"-\sBugs passed: 1 Bugs failed: 1\s-", stdout)


def test_skip_all_bugs(testdir: pytest.Testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.bug('test', run=True)
        def test_one():
            assert True

        @pytest.mark.bug('test')
        def test_two():
            assert False

        def test_three():
            assert False
        """
    )
    result = testdir.runpytest("--bug-all-skip")
    result.assert_outcomes(skipped=2, failed=1)
    stdout = result.stdout.str()
    assert re.search(r"-\sBugs skipped: 2\s-", stdout)


def test_two_marks_comment(testdir: pytest.Testdir):
    testdir.makeconftest(
        """        
        def pytest_runtest_makereport(item):
            mark_bug = item._mark_bug
            assert mark_bug.comment == 'BUG: one, two'
        """
    )
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.bug('two', run=True)
        @pytest.mark.bug('one', run=True)
        def test_one():
            assert True

        @pytest.mark.bug('two')
        @pytest.mark.bug('one')
        def test_two():
            assert False

        @pytest.mark.bug('two', run=True)
        @pytest.mark.bug('one', run=True)
        def test_three():
            assert False
        """
    )
    result = testdir.runpytest()
    assert result.ret == 0


def test_several_marks_comment(testdir: pytest.Testdir):
    testdir.makeconftest(
        """        
        def pytest_runtest_makereport(item):
            mark_bug = item._mark_bug
            assert mark_bug.comment == 'BUG: bug1, bug2, bug3, bug4, bug5, bug6'
        """
    )
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.bug('bug6', run=True)
        @pytest.mark.bug('bug5', run=True)
        @pytest.mark.bug('bug4', run=True)
        @pytest.mark.bug('bug3', run=True)
        @pytest.mark.bug('bug2', run=True)
        @pytest.mark.bug('bug1', run=True)
        def test_one():
            assert True
        """
    )
    result = testdir.runpytest()
    assert result.ret == 0


def test_two_marks_run(testdir: pytest.Testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.bug('two', run=True)
        @pytest.mark.bug('one', run=True)
        def test_one():
            assert True

        @pytest.mark.bug('two')
        @pytest.mark.bug('one')
        def test_two():
            assert False

        @pytest.mark.bug('two', run=True)
        @pytest.mark.bug('one')
        def test_three():
            assert False
            
        @pytest.mark.bug('two', run=False)
        @pytest.mark.bug('one', run=True)
        def test_four():
            assert False
            
            
        @pytest.mark.bug
        @pytest.mark.bug('one', run=True)
        def test_five():
            assert False
        """
    )
    result = testdir.runpytest()
    assert result.ret == 0
    result.assert_outcomes(skipped=4, passed=1)
    stdout = result.stdout.str()
    assert re.search(r"\w+\.py pbbbb", stdout)
    assert re.search(r"-\sBugs skipped: 4 Bugs passed: 1\s-", stdout)
