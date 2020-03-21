import pytest

__version__ = '0.7.2'


def bug(*args, run=False):
    return pytest.mark.bug(*args, run=run)


__all__ = [
    '__version__',
    'bug'
]
