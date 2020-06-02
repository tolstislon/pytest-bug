"""Plugin hooks"""


def pytest_bug_set_mark(mark_bug, config):  # pragma: no cover
    """
    Called set mark
    :param mark_bug: MarkBug
    :param config: Base pytest config
    """


def pytest_bug_item_mark(item, config):  # pragma: no cover
    """
    Called after set mark
    :param item: pytest item
    :param config: Base pytest config
    """


def pytest_bug_report_teststatus(report, report_bug):  # pragma: no cover
    """
    Called before output
    :param report: Base pytest report
    :param report_bug: SkipBug or FailBug or PassBug
    """
