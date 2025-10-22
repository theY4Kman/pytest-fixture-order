from importlib import metadata


###
# Manually include our plugin if it's not already installed
#

eps = metadata.entry_points()
if hasattr(eps, 'select'):
    scripts = eps.select(group='pytest11')
else:
    scripts = eps.get('pytest11', ())

for script in scripts:
    if script.name == 'fixture_order':
        break
else:
    pytest_plugins = [
        'pytest_fixture_order.plugin',
    ]
