from typing import Callable

import pytest

from pytest_fixture_order.compat import pytest_version_tuple


IS_PYTEST3 = (3,) < pytest_version_tuple < (4,)


@pytest.fixture(scope='session')
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

    @pytest.fixture(scope='class')
    def class_first(self, increment):
        return increment()

    @pytest.fixture(scope='class')
    def class_second(self, increment):
        return increment()

    @pytest.fixture(scope='module')
    def module_first(self, increment):
        return increment()

    @pytest.fixture(scope='module')
    def module_second(self, increment):
        return increment()

    if not IS_PYTEST3:
        @pytest.fixture(scope='package')
        def package_first(self, increment):
            return increment()

        @pytest.fixture(scope='package')
        def package_second(self, increment):
            return increment()

    # pytest 3 did not include package scope
    else:
        @pytest.fixture()
        def package_first(self, increment):
            return increment()

        @pytest.fixture()
        def package_second(self, increment):
            return increment()

    @pytest.fixture(scope='session')
    def session_first(self, increment):
        return increment()

    @pytest.fixture(scope='session')
    def session_second(self, increment):
        return increment()

    def it_evaluates_based_on_declaration_order(self, first, second):
        assert first < second

    def it_evaluates_based_on_declaration_order_flipped(self, second, first):
        assert second < first

    def it_respects_scope_ordering(
        self,
        first, second,
        class_first, class_second,
        module_first, module_second,
        package_first, package_second,
        session_first, session_second,
    ):
        encountered_order = [
            (first, 'first'),
            (second, 'second'),
            (class_first, 'class_first'),
            (class_second, 'class_second'),
            (module_first, 'module_first'),
            (module_second, 'module_second'),
            (package_first, 'package_first'),
            (package_second, 'package_second'),
            (session_first, 'session_first'),
            (session_second, 'session_second'),
        ]
        if IS_PYTEST3:
            encountered_order = [
                (value, name)
                for value, name in encountered_order
                if not name.startswith('package')
            ]
        encountered_order.sort(key=lambda t: t[0])

        expected = [
            'session_first',
            'session_second',
            'package_first',
            'package_second',
            'module_first',
            'module_second',
            'class_first',
            'class_second',
            'first',
            'second',
        ]
        if IS_PYTEST3:
            expected = [
                name
                for name in expected
                if not name.startswith('package')
            ]
        actual = [name for value, name in encountered_order]
        assert expected == actual


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


class DescribeOrder:

    @pytest.fixture
    def normal(self, increment):
        return increment()

    @pytest.fixture
    @pytest.mark.order(-1)
    def early(self, increment):
        return increment()

    @pytest.fixture
    @pytest.mark.order(index=1)
    def late(self, increment):
        return increment()

    @pytest.fixture
    @pytest.mark.order(index=5)
    def latest(self, increment):
        return increment()

    def it_evaluates_in_correct_order(self, normal, early, late, latest):
        assert early < normal < late < latest
