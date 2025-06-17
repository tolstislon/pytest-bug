"""Pytest bug plugin."""

import pytest


def bug(*args, run: bool = False) -> pytest.Mark:
    """
    Mark test as a bug.

    :param run: Test run bool.
    :return: MarkGenerator.
    """
    return pytest.mark.bug(*args, run=run)


__all__ = ["bug"]
