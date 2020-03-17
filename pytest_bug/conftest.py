from .plugin import PyTestBug


def pytest_addoption(parser):
    bug = parser.getgroup('pytest-bug')
    bug.addoption('--bug-no-stats', action='store_true', help='Disabling summary statistics', default=False)
    parser.addini('bug_summary_stats', help='Display summary statistics', default=True, type="bool")


def pytest_configure(config):
    config.addinivalue_line("markers", "bug(*args, run: bool): Mark test as a bug")
    config.pluginmanager.register(PyTestBug(config), name="pytest-bug-instance")
