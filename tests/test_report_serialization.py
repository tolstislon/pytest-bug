import pytest
from _pytest.reports import TestReport

from pytest_bug.plugin import (
    MARK_BUG,
    FailBug,
    PassBug,
    SkipBug,
    pytest_report_from_serializable,
    pytest_report_to_serializable,
)


def _report() -> TestReport:
    return TestReport(
        nodeid="test_sample.py::test_one",
        location=("test_sample.py", 1, "test_one"),
        keywords={},
        outcome="passed",
        longrepr=None,
        when="call",
    )


@pytest.mark.parametrize("report_bug_cls", (SkipBug, FailBug, PassBug))
def test_round_trip(report_bug_cls: type):
    report = _report()
    setattr(report, MARK_BUG, report_bug_cls("BUG: comment"))

    data = pytest_report_to_serializable(report)
    assert data["$report_type"] == "TestReport"
    assert data[MARK_BUG] == {"type": report_bug_cls.__name__, "comment": "BUG: comment"}
    # the original report is left untouched for the other hooks of the worker
    assert isinstance(getattr(report, MARK_BUG), report_bug_cls)

    restored = pytest_report_from_serializable(data)
    assert isinstance(restored, TestReport)
    assert restored.nodeid == report.nodeid
    report_bug = getattr(restored, MARK_BUG)
    assert isinstance(report_bug, report_bug_cls)
    assert report_bug.comment == "BUG: comment"


def test_report_without_bug_uses_default_serialization():
    assert pytest_report_to_serializable(_report()) is None
    assert pytest_report_from_serializable({"$report_type": "TestReport", "nodeid": "x"}) is None
    assert pytest_report_from_serializable({MARK_BUG: {"type": "FailBug", "comment": "c"}}) is None
