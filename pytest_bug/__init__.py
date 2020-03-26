import pytest


def bug(*args, run=False):
    return pytest.mark.bug(*args, run=run)


__all__ = [
    'bug'
]
