import re
from typing import Dict, Tuple

import pytest

from . import hooks

MARK_BUG = "_mark_bug"
START_COMMENT = "BUG: "


class MarkBug:
    def __init__(self, comment: str = "no comment", run: bool = False):
        """
        :param comment: str
        :param run: bool
        """
        self.comment = "{}{}".format(START_COMMENT, comment)
        self.run = run


class ReportBug:
    letter = "u"  # type: str
    word = "BUG-UNKNOWN"  # type:str
    markup = {}  # type: Dict[str, bool]

    def __init__(self, comment):
        self.comment = comment


class SkipBug(ReportBug):
    letter = "b"
    word = "BUG-SKIP"
    markup = {"yellow": True}


class FailBug(ReportBug):
    letter = "f"
    word = "BUG-FAIL"
    markup = {"red": True}


class PassBug(ReportBug):
    letter = "p"
    word = "BUG-PASS"
    markup = {"green": True}


def pytest_addoption(parser):
    group = parser.getgroup("pytest-bug")
    group.addoption(
        "--bug-no-stats",
        action="store_true",
        help="Disabling summary statistics",
        default=False,
    )
    group.addoption(
        "--bug-pattern",
        action="store",
        metavar="REGEX",
        help="Run matching tests marked as bug",
    )
    group.addoption(
        "--bug-all-run",
        action="store_true",
        help="Includes all bugs in the run",
        default=False,
    )
    group.addoption(
        "--bug-all-skip",
        action="store_true",
        help="Disables all bugs in the run",
        default=False,
    )
    group.addoption(
        "--bug-skip-letter",
        action="store",
        metavar="LETTER",
        help="Set to output in console for skip-bug (default: b)",
    )
    group.addoption(
        "--bug-skip-word",
        action="store",
        metavar="WORLD",
        help="Set to output in console for skip-bug verbosity (default: BUG-SKIP)",
    )
    group.addoption(
        "--bug-fail-letter",
        action="store",
        metavar="LETTER",
        help="Set to output in console for fail-bug (default: f)",
    )
    group.addoption(
        "--bug-fail-word",
        action="store",
        metavar="WORLD",
        help="Set to output in console for fail-bug verbosity (default: BUG-FAIL)",
    )
    group.addoption(
        "--bug-pass-letter",
        action="store",
        metavar="LETTER",
        help="Set to output in console for pass-bug (default: p)",
    )
    group.addoption(
        "--bug-pass-word",
        action="store",
        metavar="WORLD",
        help="Set to output in console for fail-bug verbosity (default: BUG-PASS)",
    )

    # add ini params
    parser.addini(
        "bug_summary_stats",
        help="Display summary statistics",
        default=True,
        type="bool",
    )
    parser.addini(
        "bug_skip_letter", help="Set to output in console for skip-bug (default: b)",
    )
    parser.addini(
        "bug_skip_word",
        help="Set to output in console for skip-bug verbosity (default: BUG-SKIP)",
    )
    parser.addini(
        "bug_fail_letter", help="Set to output in console for fail-bug (default: f)",
    )
    parser.addini(
        "bug_fail_word",
        help="Set to output in console for fail-bug verbosity (default: BUG-FAIL)",
    )
    parser.addini(
        "bug_pass_letter", help="Set to output in console for pass-bug (default: p)",
    )
    parser.addini(
        "bug_pass_word",
        help="Set to output in console for fail-bug verbosity (default: BUG-PASS)",
    )


def pytest_addhooks(pluginmanager):
    pluginmanager.add_hookspecs(hooks)


def pytest_configure(config):
    bug = PyTestBug(config)
    config._bug = bug
    config.pluginmanager.register(bug)


class PyTestBug:
    def __init__(self, config):
        self.config = config
        self._skipped = 0
        self._failed = 0
        self._passed = 0
        self._all_run = config.getoption("--bug-all-run")
        self._all_skip = config.getoption("--bug-all-skip")

    def _counter(self, mark: ReportBug) -> None:
        """
        :param mark: Sub object ReportBug
        """
        if isinstance(mark, SkipBug):
            self._skipped += 1
        elif isinstance(mark, FailBug):
            self._failed += 1
        elif isinstance(mark, PassBug):
            self._passed += 1

    def _bug_mark(self, *args, run: bool = False, **kwargs) -> Tuple[str, bool]:
        """
        :param run: bool
        :return: Tuple[str, bool]
        """
        comment = [str(i) for i in args]
        comment.extend("{}={}".format(key, value) for key, value in kwargs.items())
        if self._all_run:
            run = True
        elif self._all_skip:
            run = False
        return ", ".join(comment) if comment else "no comment", run

    @staticmethod
    def pytest_configure(config):
        config.addinivalue_line("markers", "bug(*args, run: bool): Mark test as a bug")
        letter_skip = config.getoption("--bug-skip-letter") or config.getini(
            "bug_skip_letter"
        )
        if letter_skip:
            SkipBug.letter = letter_skip
        word_skip = config.getoption("--bug-skip-word") or config.getini(
            "bug_skip_word"
        )
        if word_skip:
            SkipBug.word = word_skip
        letter_fail = config.getoption("--bug-fail-letter") or config.getini(
            "bug_fail_letter"
        )
        if letter_fail:
            FailBug.letter = letter_fail
        word_fail = config.getoption("--bug-fail-word") or config.getini(
            "bug_fail_word"
        )
        if word_fail:
            FailBug.word = word_fail
        letter_pass = config.getoption("--bug-pass-letter") or config.getini(
            "bug_pass_letter"
        )
        if letter_pass:
            PassBug.letter = letter_pass
        word_pass = config.getoption("--bug-pass-word") or config.getini(
            "bug_pass_word"
        )
        if word_pass:
            PassBug.word = word_pass

    def pytest_collection_modifyitems(self, items, config):
        for item in items:
            bug_markers = tuple(item.iter_markers(name="bug"))
            if bug_markers:
                runs = []
                comments = []
                for i in bug_markers:
                    comment, run = self._bug_mark(*i.args, **i.kwargs)
                    runs.append(run)
                    comments.append(comment)
                mark_bug = MarkBug(comment=", ".join(comments), run=all(runs))
                config.hook.pytest_bug_set_mark(mark_bug=mark_bug, config=config)
                setattr(item, MARK_BUG, mark_bug)
                config.hook.pytest_bug_item_mark(item=item, config=config)

        bug_pattern = config.getoption("--bug-pattern")
        if bug_pattern:
            selected_items = []
            for item in items:
                mark_bug = getattr(item, MARK_BUG, None)
                if mark_bug is not None:
                    comment = mark_bug.comment[len(START_COMMENT):]
                    if re.search(bug_pattern, comment, re.I):
                        selected_items.append(item)
            config.hook.pytest_deselected(
                items=[i for i in items if i not in selected_items]
            )
            items[:] = selected_items

    @staticmethod
    def pytest_runtest_setup(item):
        mark_bug = getattr(item, MARK_BUG, None)
        if isinstance(mark_bug, MarkBug) and mark_bug.run is False:
            pytest.skip(mark_bug.comment)

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item):
        outcome = yield
        report = outcome.get_result()
        mark_bug = getattr(item, MARK_BUG, None)
        if isinstance(mark_bug, MarkBug):
            if report.skipped:
                setattr(report, MARK_BUG, SkipBug(mark_bug.comment))
            elif report.when == "call":
                if report.passed:
                    setattr(report, MARK_BUG, PassBug(mark_bug.comment))
                elif report.failed:
                    report.outcome, report.wasxfail = ("skipped", "skipped")
                    setattr(report, MARK_BUG, FailBug(mark_bug.comment))

    def pytest_report_teststatus(self, report):
        mark_bug = getattr(report, MARK_BUG, None)
        if isinstance(mark_bug, ReportBug):
            self._counter(mark_bug)
            self.config.hook.pytest_bug_report_teststatus(
                report=report, report_bug=mark_bug
            )
            return report.outcome, mark_bug.letter, (mark_bug.word, mark_bug.markup)

    def pytest_terminal_summary(self, terminalreporter):
        if not self.config.getoption("--bug-no-stats") and self.config.getini(
                "bug_summary_stats"
        ):
            text = []
            if self._skipped:
                text.append("Bugs skipped: {}".format(self._skipped))
            if self._passed:
                text.append("Bugs passed: {}".format(self._passed))
            if self._failed:
                text.append("Bugs failed: {}".format(self._failed))
            if text:
                terminalreporter.write_sep("-", " ".join(text))
