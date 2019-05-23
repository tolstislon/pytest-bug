import pytest
from .plugin import __version__

__all__ = ['__version__', 'bug']


def bug(*args, run: bool = False):
    return pytest.mark.bug(*args, run=run)
