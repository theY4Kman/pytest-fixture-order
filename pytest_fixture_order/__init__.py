from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version('pytest-fixture-order')
except PackageNotFoundError:
    __version__ = 'dev'
