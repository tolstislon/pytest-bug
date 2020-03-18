pytest_plugins = ("pytester",)


def test_item_attr(testdir):
    testdir.makeconftest(
        """        
        def pytest_runtest_makereport(item):
            assert hasattr(item, '_mark_bug')
            assert hasattr(item, '_bug_comment') 
            assert item._bug_comment == 'BUG: test'
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


def test_report_item(testdir):
    testdir.makeconftest(
        """
        def pytest_runtest_logreport(report):
            if report.when == 'call':
                assert hasattr(report, '_mark_bug')
                assert hasattr(report, '_bug_comment')
                assert report._bug_comment == 'BUG: test'
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
