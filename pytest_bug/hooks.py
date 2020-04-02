"""Plugin hooks"""


def pytest_bug_item_mark(mark_bug, config):
    """
    Called set mark
    :param mark_bug: MarkBug
    :param config: Base pytest config
    """


def pytest_bug_report_teststatus(report, report_bug):
    """
    Called before output
    :param report: Base pytest report
    :param report_bug: SkipBug or FailBug or PassBug
    """
