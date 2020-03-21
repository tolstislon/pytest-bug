import re

pytest_plugins = ("pytester",)


def test_item_attr(testdir):
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


def test_item_attr_no_comment(testdir):
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


def test_report_item(testdir):
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


def test_report_item_no_comment(testdir):
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


def test_run_test_marked_as_bug(testdir):
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
    result = testdir.runpytest('-m bug')
    assert result.ret == 0
    outcomes = result.parseoutcomes()
    assert outcomes['passed'] == 1
    assert outcomes['deselected'] == 1
    assert outcomes['skipped'] == 1


def test_run_all_bugs(testdir):
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
    result = testdir.runpytest('--bug-all-run')
    result.assert_outcomes(skipped=1, passed=1, failed=1)
    stdout = result.stdout.str()
    assert re.search(r'-\sBugs passed: 1 Bugs failed: 1\s-', stdout)


def test_skip_all_bugs(testdir):
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
    result = testdir.runpytest('--bug-all-skip')
    result.assert_outcomes(skipped=2, failed=1)
    stdout = result.stdout.str()
    assert re.search(r'-\sBugs skipped: 2\s-', stdout)
