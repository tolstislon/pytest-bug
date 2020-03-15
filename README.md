# pytest-bug

[![PyPI](https://img.shields.io/pypi/v/pytest-bug.svg?color=yellow&label=version)](https://pypi.org/project/pytest-bug/)
[![Build Status](https://travis-ci.com/tolstislon/pytest-bug.svg?branch=master)](https://travis-ci.com/tolstislon/pytest-bug)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-bug.svg)](https://pypi.org/project/pytest-bug/)
[![pytes_support](https://img.shields.io/badge/pytest-%3E%3D3.6.0-blue.svg)](https://pypi.org/project/pytest-bug/)
[![Downloads](https://pepy.tech/badge/pytest-bug)](https://pypi.org/project/pytest-bug/)

```python
import pytest


@pytest.mark.bug('skip')
def test_one():
    assert False


@pytest.mark.bug('fail', run=True)
def test_two():
    assert False


@pytest.mark.bug('pass', run=True)
def test_three():
    assert True


@pytest.mark.bug('skip class')
class TestFour:

    def test_one(self):
        assert False

    def test_two(self):
        assert True


@pytest.mark.bug('class', run=True)
class TestFive:

    def test_one(self):
        assert False

    def test_two(self):
        assert True
```

```
$ pytest

======================== test session starts ========================
platform linux -- Python 3.x.y, pytest-5.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 1 item

test_sample.py bspbbsp

---------- Bugs skipped: 3 Bugs passed: 2 Bugs failed: 2 ----------
=================== 2 passed, 5 skipped in 0.10s ===================
```