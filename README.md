# pytest-bug

[![PyPI](https://img.shields.io/pypi/v/pytest-bug.svg?color=yellow&label=version)](https://pypi.org/project/pytest-bug/)
[![Build Status](https://travis-ci.com/tolstislon/pytest-bug.svg?branch=master)](https://travis-ci.com/tolstislon/pytest-bug)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-bug.svg)](https://pypi.org/project/pytest-bug/)
[![pytes_support](https://img.shields.io/badge/pytest-%3E%3D3.6.0-blue.svg)](https://github.com/pytest-dev/pytest/releases)
[![Downloads](https://pepy.tech/badge/pytest-bug)](https://pypi.org/project/pytest-bug/)


### Install

```bash
pip install pytest-bug
```


### Example

```python
import pytest


@pytest.mark.bug('C18', 'Critical bug')  # mark skip test
def test_one():
    assert False


@pytest.mark.bug('C39', 'Minor bug', run=True)  # mark xfail test if fail else pass
def test_two():
    assert False


@pytest.mark.bug('C41', 'Minor bug', run=True)
def test_three():
    assert True


@pytest.mark.bug('Bug all test')
class TestFour:

    def test_one(self):   # mark skip test
        assert False

    def test_two(self):    # mark skip test
        assert True


@pytest.mark.bug('Unstable tests', run=True)
class TestFive:

    def test_one(self): # mark xfail
        assert False

    def test_two(self): # pass
        assert True
```

```bash
$ pytest

======================== test session starts ========================
platform linux -- Python 3.x.y, pytest-x.y.z, py-x.y.z, pluggy-x.y.z
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
plugins: bug-x.y.z
collected 7 items

test_sample.py bfpbbfp

---------- Bugs skipped: 3 Bugs passed: 2 Bugs failed: 2 ----------
=================== 2 passed, 5 skipped in 0.10s ===================
```
Symbols:
* `b` - bug skip
* `f` - bug fail
* `p` - bug pass


##### verbosity
```bash
$ pytest -v

======================== test session starts ========================
platform linux -- Python 3.x.y, pytest-x.y.z, py-x.y.z, pluggy-x.y.z
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
plugins: bug-x.y.z
collected 7 items

test_sample.py::test_one BUG-SKIP                          [ 14%]
test_sample.py::test_two BUG-FAIL                          [ 28%]
test_sample.py::test_three BUG-PASS                        [ 42%]
test_sample.py::TestFour::test_one BUG-SKIP                [ 57%]
test_sample.py::TestFour::test_two BUG-SKIP                [ 71%]
test_sample.py::TestFive::test_one BUG-FAIL                [ 85%]
test_sample.py::TestFive::test_two BUG-PASS                [100%]

---------- Bugs skipped: 3 Bugs passed: 2 Bugs failed: 2 ----------
=================== 2 passed, 5 skipped in 0.10s ===================
```

Command line options:

| option | description |
| ------ | ------ |
| --bug-no-stats | Disabling summary statistics |                 
| --bug-pattern=REGEX | Run matching tests marked as bug |