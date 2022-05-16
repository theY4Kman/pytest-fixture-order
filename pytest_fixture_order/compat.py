from _pytest.fixtures import FixtureDef


try:
    from pytest import version_tuple as pytest_version_tuple
except ImportError:  # pytest<7.0
    import pytest
    pytest_version_tuple = tuple(int(part) for part in pytest.__version__.split('.'))


try:
    from _pytest.mark import Mark
except ImportError:  # pytest<=4.0
    from _pytest.mark import MarkInfo as Mark


try:
    from _pytest.scope import Scope

    scope_ordering = list(reversed(Scope))

    scopenum_function = scope_ordering.index(Scope.Function)

    def get_scopenum(fixturedef: FixtureDef):
        return scope_ordering.index(Scope(fixturedef.scope))

except ImportError:  # pytest<7.0
    from _pytest.fixtures import scopenum_function

    def get_scopenum(fixturedef: FixtureDef):
        return fixturedef.scopenum
