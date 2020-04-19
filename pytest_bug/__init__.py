import pytest


def bug(*args, run: bool = False):
    """
    Mark test as a bug
    :param run: test run bool
    :return: MarkGenerator
    """
    return pytest.mark.bug(*args, run=run)


__all__ = ["bug"]
