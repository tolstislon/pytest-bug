import enum

import pytest

from . import hooks

BUG = '_mark_bug'
COMMENT = '_bug_comment'


class MARKS(enum.Enum):
    SKIP = 'b'
    FAIL = 'f'
    PASS = 'p'
    UNKNOWN = 'u'


def bug_mark(*args, run=False, **kwargs):
    comment = [str(i) for i in args]
    comment.extend(f'{key}={value}' for key, value in kwargs.items())
    return ', '.join(comment) if comment else 'no comment', run


class PyTestBug:

    def __init__(self, config):
        self.config = config
        self._skipped = 0
        self._failed = 0
        self._passed = 0

    def counter(self, mark):
        if mark is MARKS.SKIP:
            self._skipped += 1
        elif mark is MARKS.FAIL:
            self._failed += 1
        elif mark is MARKS.PASS:
            self._passed += 1

    @staticmethod
    def set_mark(obj, mark=MARKS.UNKNOWN):
        setattr(obj, BUG, mark)

    @staticmethod
    def set_comment(obj, comment):
        if comment:
            setattr(obj, COMMENT, 'BUG: %s' % str(comment))

    @staticmethod
    def pytest_addhooks(pluginmanager):
        pluginmanager.add_hookspecs(hooks)

    def pytest_runtest_setup(self, item):
        for i in item.iter_markers(name='bug'):
            comment, run = bug_mark(*i.args, **i.kwargs)
            self.set_comment(item, comment)
            if run:
                self.config.hook.pytest_bug_run_before_set_mark(item=item, config=self.config)
                self.set_mark(item)
                self.config.hook.pytest_bug_run_after_set_mark(item=item, config=self.config)
            else:
                self.set_mark(item, MARKS.SKIP)
                pytest.skip(comment)

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item):
        outcome = yield
        report = outcome.get_result()
        mark = getattr(item, BUG, None)
        if mark:
            self.set_comment(report, getattr(item, COMMENT))
            if report.skipped:
                self.set_mark(report, MARKS.SKIP)
            if report.when == 'call':
                if report.passed:
                    self.set_mark(report, MARKS.PASS)
                elif report.failed:
                    report.outcome = "skipped"
                    report.wasxfail = 'skipped'
                    self.set_mark(report, MARKS.FAIL)

    def pytest_report_teststatus(self, report):
        mark = getattr(report, BUG, None)
        if mark:
            self.counter(mark)
            return report.outcome, mark.value, report.outcome.upper()

    def pytest_terminal_summary(self, terminalreporter):
        text = []
        if self._skipped:
            text.append(f'Bugs skipped: {self._skipped}')
        if self._passed:
            text.append(f'Bugs passed: {self._passed}')
        if self._failed:
            text.append(f'Bugs failed: {self._failed}')
        if text:
            terminalreporter.write_sep('-', ' '.join(text))
