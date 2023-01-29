import re
from typing import Dict, Tuple, List

import pytest
from _pytest.config import Config, PytestPluginManager
from _pytest.config.argparsing import Parser
from _pytest.python import Function
from _pytest.reports import TestReport
from _pytest.terminal import TerminalReporter

from . import hooks

MARK_BUG = "_mark_bug"
START_COMMENT = "BUG: "
ORT_GROUP = "pytest-bug"


class Metavar:
    LETTER = "LETTER"
    WORLD = "WORLD"
    REGEX = "REGEX"


class MarkBug:
    def __init__(self, comment: str = "no comment", run: bool = False):
        """
        :param comment: str
        :param run: bool
        """
        self.comment = f"{START_COMMENT}{comment}"
        self.run = run


class ReportBug:
    letter: str = "u"
    word: str = "BUG-UNKNOWN"
    markup: Dict[str, bool] = {}

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


def pytest_addoption(parser: Parser):
    group = parser.getgroup(ORT_GROUP)

    def _add_option(name: str, help_text: str, default: str, metavar: str) -> None:
        op_name = f"--{name.replace('_', '-')}"
        group.addoption(
            op_name,
            action="store",
            metavar=metavar,
            help=f"{help_text} (default: {default})",
            dest=name,
        )
        parser.addini(
            name=name, help=f"{help_text} (default: {default})", default=default
        )

    group.addoption(
        "--bug-no-stats",
        action="store_true",
        help="Disabling summary statistics",
        default=False,
        dest="bug_summary_stats",
    )
    group.addoption(
        "--bug-pattern",
        action="store",
        metavar=Metavar.REGEX,
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
    _add_option(
        name="bug_skip_letter",
        help_text="Set to output in console for skip-bug",
        default=SkipBug.letter,
        metavar=Metavar.LETTER,
    )
    _add_option(
        name="bug_skip_word",
        help_text="Set to output in console for skip-bug verbosity",
        default=SkipBug.word,
        metavar=Metavar.WORLD,
    )
    _add_option(
        name="bug_fail_letter",
        help_text="Set to output in console for fail-bug",
        default=FailBug.letter,
        metavar=Metavar.LETTER,
    )
    _add_option(
        name="bug_fail_word",
        help_text="Set to output in console for fail-bug verbosity",
        default=FailBug.word,
        metavar=Metavar.WORLD,
    )
    _add_option(
        name="bug_pass_letter",
        help_text="Set to output in console for pass-bug",
        default=PassBug.letter,
        metavar=Metavar.LETTER,
    )
    _add_option(
        name="bug_pass_word",
        help_text="Set to output in console for fail-bug verbosity",
        default=PassBug.word,
        metavar=Metavar.WORLD,
    )

    parser.addini(
        "bug_summary_stats",
        help="Display summary statistics",
        default=True,
        type="bool",
    )


def pytest_addhooks(pluginmanager: PytestPluginManager):
    pluginmanager.add_hookspecs(hooks)


def pytest_configure(config: Config):
    bug = PyTestBug(config)
    config._bug = bug
    config.pluginmanager.register(bug)


class PyTestBug:
    def __init__(self, config: Config):
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
        comment.extend(f"{key}={value}" for key, value in kwargs.items())
        if self._all_run:
            run = True
        elif self._all_skip:
            run = False
        return ", ".join(comment) if comment else "no comment", run

    def _get_value(self, key: str) -> str:
        return self.config.getoption(key) or self.config.getini(key)

    def pytest_configure(self, config: Config):
        config.addinivalue_line("markers", "bug(*args, run: bool): Mark test as a bug")
        SkipBug.letter = self._get_value("bug_skip_letter")
        SkipBug.word = self._get_value("bug_skip_word")
        FailBug.letter = self._get_value("bug_fail_letter")
        FailBug.word = self._get_value("bug_fail_word")
        PassBug.letter = self._get_value("bug_pass_letter")
        PassBug.word = self._get_value("bug_pass_word")

    def pytest_collection_modifyitems(self, items: List[Function], config: Config):
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
                    comment = mark_bug.comment[len(START_COMMENT) :]
                    if re.search(bug_pattern, comment, re.I):
                        selected_items.append(item)
            config.hook.pytest_deselected(
                items=[i for i in items if i not in selected_items]
            )
            items[:] = selected_items

    @staticmethod
    def pytest_runtest_setup(item: Function):
        mark_bug = getattr(item, MARK_BUG, None)
        if isinstance(mark_bug, MarkBug) and mark_bug.run is False:
            pytest.skip(mark_bug.comment)

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item: Function):
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

    def pytest_report_teststatus(self, report: TestReport):
        mark_bug = getattr(report, MARK_BUG, None)
        if isinstance(mark_bug, ReportBug):
            self._counter(mark_bug)
            self.config.hook.pytest_bug_report_teststatus(
                report=report, report_bug=mark_bug
            )
            return report.outcome, mark_bug.letter, (mark_bug.word, mark_bug.markup)

    def pytest_terminal_summary(self, terminalreporter: TerminalReporter):
        if not self.config.getoption("bug_summary_stats") and self.config.getini(
            "bug_summary_stats"
        ):
            text = []
            if self._skipped:
                text.append(f"Bugs skipped: {self._skipped}")
            if self._passed:
                text.append(f"Bugs passed: {self._passed}")
            if self._failed:
                text.append(f"Bugs failed: {self._failed}")
            if text:
                terminalreporter.write_sep("-", " ".join(text))
