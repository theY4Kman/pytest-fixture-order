from importlib import metadata

try:
    __version__ = metadata.version('pytest-fixture-order')
except metadata.PackageNotFoundError:
    __version__ = 'dev'
