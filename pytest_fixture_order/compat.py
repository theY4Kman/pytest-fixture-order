from _pytest.fixtures import FixtureDef


try:
    from _pytest.mark import Mark
except ImportError:
    from _pytest.mark import MarkInfo as Mark

try:
    from _pytest.scope import Scope

    scope_ordering = list(reversed(Scope))

    scopenum_function = scope_ordering.index(Scope.Function)

    def get_scopenum(fixturedef: FixtureDef):
        return scope_ordering.index(Scope(fixturedef.scope))

except ImportError:
    from _pytest.fixtures import scopenum_function

    def get_scopenum(fixturedef: FixtureDef):
        return fixturedef.scopenum
