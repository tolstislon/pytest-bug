import enum
import re

import pytest

from . import hooks

BUG = '_mark_bug'
COMMENT = '_bug_comment'


class MARKS(enum.Enum):
    SKIP = 'b'
    FAIL = 'f'
    PASS = 'p'
    UNKNOWN = 'u'


verbose = {
    MARKS.SKIP: 'BUG-SKIP',
    MARKS.PASS: 'BUG-PASS',
    MARKS.FAIL: 'BUG-FAIL'
}


class PyTestBug:

    def __init__(self, config):
        self.config = config
        self._skipped = 0
        self._failed = 0
        self._passed = 0
        self._all_run = False
        self._all_skip = False

    def _counter(self, mark):
        if mark is MARKS.SKIP:
            self._skipped += 1
        elif mark is MARKS.FAIL:
            self._failed += 1
        elif mark is MARKS.PASS:
            self._passed += 1

    def _bug_mark(self, *args, run=False, **kwargs):
        comment = [str(i) for i in args]
        comment.extend('{}={}'.format(key, value) for key, value in kwargs.items())
        if self._all_run:
            run = True
        elif self._all_skip:
            run = False
        return ', '.join(comment) if comment else 'no comment', run

    @staticmethod
    def _set_mark(obj, mark=MARKS.UNKNOWN):
        setattr(obj, BUG, mark)

    @staticmethod
    def _set_comment(obj, comment):
        setattr(obj, COMMENT, 'BUG: {}'.format(comment))

    @staticmethod
    def pytest_addhooks(pluginmanager):
        pluginmanager.add_hookspecs(hooks)

    def pytest_collection_modifyitems(self, items, config):
        self._all_run = config.getoption('--bug-all-run')
        self._all_skip = config.getoption('--bug-all-skip')
        for item in items:
            for i in item.iter_markers(name='bug'):
                comment, run = self._bug_mark(*i.args, **i.kwargs)
                self._set_comment(item, comment)
                if run:
                    config.hook.pytest_bug_run_before_set_mark(item=item, config=config)
                    self._set_mark(item)
                    config.hook.pytest_bug_run_after_set_mark(item=item, config=config)
                else:
                    self._set_mark(item, MARKS.SKIP)

        bug_pattern = config.getoption('--bug-pattern')
        if bug_pattern:
            selected_items = []
            for item in items:
                if hasattr(item, COMMENT):
                    comment = getattr(item, COMMENT)[5:]
                    if re.search(bug_pattern, comment, re.I):
                        selected_items.append(item)
            deselected_items = [i for i in items if i not in selected_items]
            config.hook.pytest_deselected(items=deselected_items)
            items[:] = selected_items

    def pytest_runtest_setup(self, item):
        mark = getattr(item, BUG, None)
        if mark and mark is MARKS.SKIP:
            pytest.skip(getattr(item, COMMENT, ''))

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item):
        outcome = yield
        report = outcome.get_result()
        mark = getattr(item, BUG, None)
        if mark:
            setattr(report, COMMENT, getattr(item, COMMENT, ''))
            if report.skipped:
                self._set_mark(report, MARKS.SKIP)
            if report.when == 'call':
                if report.passed:
                    self._set_mark(report, MARKS.PASS)
                elif report.failed:
                    report.outcome = "skipped"
                    report.wasxfail = 'skipped'
                    self._set_mark(report, MARKS.FAIL)

    def pytest_report_teststatus(self, report):
        mark = getattr(report, BUG, None)
        if mark:
            self._counter(mark)
            verb = verbose.get(mark, report.outcome.upper())
            return report.outcome, mark.value, verb

    def pytest_terminal_summary(self, terminalreporter):
        if not self.config.getoption('--bug-no-stats') and self.config.getini('bug_summary_stats'):
            text = []
            if self._skipped:
                text.append('Bugs skipped: {}'.format(self._skipped))
            if self._passed:
                text.append('Bugs passed: {}'.format(self._passed))
            if self._failed:
                text.append('Bugs failed: {}'.format(self._failed))
            if text:
                terminalreporter.write_sep('-', ' '.join(text))
