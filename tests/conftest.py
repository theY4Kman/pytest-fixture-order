try:
    from importlib.metadata import entry_points
except ImportError:
    # For Python < 3.10
    from importlib_metadata import entry_points


###
# Manually include our plugin if it's not already installed
#
eps = entry_points()
if hasattr(eps, 'select'):
    # Python 3.10+
    selected = eps.select(group='pytest11')
else:
    # Python <3.10
    selected = eps.get('pytest11', [])

for entrypoint in selected:
    if entrypoint.name == 'fixture_order':
        break
else:
    pytest_plugins = [
        'pytest_fixture_order.plugin',
    ]
