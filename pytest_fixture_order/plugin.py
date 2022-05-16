from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .compat import Mark, get_scopenum, scopenum_function

if TYPE_CHECKING:
    from pytest import Config, Metafunc

# Default ordering number for fixtures without an explicitly defined ordering
DEFAULT_ORDER = 0

# Default ordering numbers for early/late
DEFAULT_EARLY_ORDER = -1
DEFAULT_LATE_ORDER = 1


def pytest_configure(config: Config):
    markers = [
        f'order(index): mark a fixture to be evaluated in a certain order',
        f'early: mark a fixture to be evaluated earlier than others (order index {DEFAULT_EARLY_ORDER})',
        f'late: mark a fixture to be evaluated later than others (order index {DEFAULT_LATE_ORDER})',
    ]

    for marker in markers:
        config.addinivalue_line('markers', marker)


def pytest_generate_tests(metafunc: Metafunc):
    reorder_fixtures(metafunc)


def reorder_fixtures(metafunc: Metafunc):
    """Allows fixtures to change the order they're executed in

    Simply apply the `late` or `early` mark to them:

        @pytest.mark.late
        @pytest.fixture
        def load_me_last():
            do_stuff()

        @pytest.mark.early
        @pytest.fixture
        def load_me_first():
            do_other_stuff()

    NOTE: ordering respects scope — i.e. marking a function-scoped fixture with
          @pytest.mark.early will still mean it's evaluated after session-,
          module-, and class-scoped fixtures.

    """

    # This will be filled with 4-tuples (scope_index, order, original_order, name)
    ordering = []

    # NOTE: _arg2fixturedefs will not include fixtures only defined by
    #       parametrization. were we only to enumerate _arg2fixturedefs, pytest
    #       would yell: function uses no argument '<argname>'
    #
    for original_order, fixturename in enumerate(metafunc.fixturenames):
        fixturedefs = metafunc._arg2fixturedefs.get(fixturename)

        # If no fixturedefs are found, this argument is defined by
        # parametrization only
        if not fixturedefs:
            scopenum = scopenum_function
            order = DEFAULT_ORDER
            ordering.append((scopenum, order, original_order, fixturename))
            continue

        for fixturedef in fixturedefs:
            order = DEFAULT_ORDER

            if get_fixture_mark(fixturedef, 'early'):
                order = DEFAULT_EARLY_ORDER

            if get_fixture_mark(fixturedef, 'late'):
                order = DEFAULT_LATE_ORDER

            # NOTE: the explicit @pytest.mark.order fixture overrules early/late
            order_mark = get_fixture_mark(fixturedef, 'order')
            if order_mark:
                if hasattr(order_mark, "combined"):
                    args, kwargs = order_mark.combined.args, order_mark.combined.kwargs
                else:
                    args, kwargs = order_mark.args, order_mark.kwargs

                ###
                # Support @pytest.mark.order(12)
                #
                if args:
                    order = args[0]

                ###
                # Support @pytest.mark.order(index=12)
                #
                elif 'index' in kwargs:
                    order = kwargs['index']

            ordering.append((get_scopenum(fixturedef), order, original_order, fixturename))

    ordered_fixturenames = []
    encountered_fixturenames = set()

    for scope_index, order, original_order, argname in sorted(ordering):
        if argname not in encountered_fixturenames:
            encountered_fixturenames.add(argname)
            ordered_fixturenames.append(argname)

    # NOTE: This list MUST be in-place edited —
    #       if reassigned, pytest will not see our changes.
    metafunc.fixturenames[:] = ordered_fixturenames


def get_fixture_mark(fixturedef, mark_name) -> Optional[Mark]:
    """Return info for a marker applied to a fixture

    Due to the way pytest collects fixtures, marks must be placed below
    @pytest.fixture — which is to say, they must be applied BEFORE @pytest.fixture.

    NOTE: markers on fixtures are UNSUPPORTED by pytest. the ability to apply
          markers to fixtures could disappear in any version.
    """
    fixturefunc = fixturedef.func

    if hasattr(fixturefunc, 'pytestmark'):
        marks = fixturefunc.pytestmark
        for mark in marks:
            if mark.name == mark_name:
                return mark

    return getattr(fixturefunc, mark_name, None)
