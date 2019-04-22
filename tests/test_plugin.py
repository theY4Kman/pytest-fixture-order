from typing import Callable

import pytest


@pytest.fixture
def increment() -> Callable[[], int]:
    """Returns a method which increments a per-test counter
    """
    counter = 0

    def increment() -> int:
        nonlocal counter
        counter += 1
        return counter

    return increment


class DescribeBaseline:
    """Fixture evaluation behaviour when no marks are used

    Order of fixture evaluation ought to be the order of declaration.
    """

    @pytest.fixture
    def first(self, increment):
        return increment()

    @pytest.fixture
    def second(self, increment):
        return increment()

    def it_evaluates_based_on_declaration_order(self, first, second):
        assert first < second

    def it_evaluates_based_on_declaration_order_flipped(self, second, first):
        assert second < first


class DescribeLate:

    @pytest.fixture
    def normal(self, increment):
        return increment()

    @pytest.fixture
    @pytest.mark.late
    def late(self, increment):
        return increment()

    def it_evaluates_late_last(self, late, normal):
        assert normal < late


class DescribeEarly:

    @pytest.fixture
    def normal(self, increment):
        return increment()

    @pytest.fixture
    @pytest.mark.early
    def early(self, increment):
        return increment()

    def it_evaluates_early_first(self, normal, early):
        assert early < normal
