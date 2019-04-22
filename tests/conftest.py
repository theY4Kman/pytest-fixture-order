import pkg_resources


###
# Manually include our plugin if it's not already installed
#
for entrypoint in pkg_resources.iter_entry_points('pytest11'):
    if entrypoint.name == 'fixture_order':
        break
else:
    pytest_plugins = [
        'pytest_fixture_order.plugin',
    ]
