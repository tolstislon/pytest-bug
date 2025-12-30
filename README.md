# pytest-bug

[![PyPI](https://img.shields.io/pypi/v/pytest-bug.svg?color=%2301a001&label=pypi)](https://pypi.org/project/pytest-bug/)
[![Downloads](https://pepy.tech/badge/pytest-bug)](https://pepy.tech/project/pytest-bug)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-bug.svg)](https://pypi.org/project/pytest-bug/)
[![pytes_support](https://img.shields.io/badge/pytest-%3E%3D9.0.0-blue.svg)](https://github.com/pytest-dev/pytest/releases)
[![Build Pypi](https://github.com/tolstislon/pytest-bug/actions/workflows/python-publish.yml/badge.svg)](https://github.com/tolstislon/pytest-bug/actions/workflows/python-publish.yml)

[Pytest](https://github.com/pytest-dev/pytest) plugin for marking tests as a bug

Installation
----

```bash
pip install pytest-bug
```

### Example

```python
import pytest


@pytest.mark.bug("C18", "Critical bug")  # mark skip test
def test_one():
    assert False


@pytest.mark.bug("C39", "Minor bug", run=True)  # mark xfail test if fail else pass
def test_two():
    assert False


@pytest.mark.bug("C41", "Minor bug", run=True)
def test_three():
    assert True


@pytest.mark.bug("Bug all tests")
class TestFour:

    def test_one(self):  # mark skip test
        assert False

    def test_two(self):  # mark skip test
        assert True


@pytest.mark.bug("Unstable tests", run=True)
class TestFive:

    def test_one(self):  # mark xfail
        assert False

    def test_two(self):  # pass
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

Options:

| option                   | description                                                         | config                   |
|--------------------------|---------------------------------------------------------------------|--------------------------|
| --bug-no-stats           | Disabling summary statistics                                        | bug_summary_stats (bool) |                
| --bug-pattern=REGEX      | Run matching tests marked as bug                                    | -                        |
| --bug-all-run            | Includes all bugs in the run                                        | -                        |
| --bug-all-skip           | Disables all bugs in the run                                        | -                        |
| --bug-skip-letter=LETTER | Set to output in console for skip-bug (default: b)                  | bug_skip_letter (string) |
| --bug-fail-letter=LETTER | Set to output in console for fail-bug (default: f)                  | bug_fail_letter (string) |
| --bug-pass-letter=LETTER | Set to output in console for pass-bug (default: p)                  | bug_pass_letter (string) |
| --bug-skip-word=WORLD    | Set to output in console for skip-bug verbosity (default: BUG-SKIP) | bug_skip_word (string)   |
| --bug-fail-word=WORLD    | Set to output in console for fail-bug verbosity (default: BUG-FAIL) | bug_fail_word (string)   |
| --bug-pass-word=WORLD    | Set to output in console for fail-bug verbosity (default: BUG-PASS) | bug_pass_word (string)   |

#### Contributions are very welcome.

###### Getting started

* python 3.12
* pipenv 2023.11.15+

1. Clone the repository
    ```bash
    git clone https://github.com/tolstislon/pytest-bug.git
    cd pytest-bug
   ```
2. Install dev dependencies
    ```bash
    pipenv install --dev
    pipenv shell
   ```
3. Run ruff format
    ```bash
    pipenv run format
   ```
4. Run ruff check
    ```bash
    pipenv run check
   ```
5. Run the tests
    ```bash
    pipenv run tests
   ```
