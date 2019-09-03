"""
Wrapper around pytest which ignores some warnings pytest and its subdependencies
generate on older versions, which we have no control over.
"""
import warnings

# By default, treat warnings as errors
warnings.simplefilter('error')


# Ignore DeprecationWarnings about imp/importlib due to pytest's usage in
# earlier versions.
warnings.filterwarnings(
    action='ignore',
    message='the imp module is deprecated in favour of importlib.+',
    category=DeprecationWarning,
)

# Ignore an ImportWarning due to importlib/imp usage of earlier versions of pytest
# See https://github.com/pytest-dev/pytest/issues/3061
warnings.filterwarnings(
    action='ignore',
    message="can't resolve package from __spec__ or __package__, falling back on __name__ and __path__",
    category=ImportWarning,
)

# Ignore a DeprecationWarning from the attr package due to pytest's usage of it,
# in an earlier version
warnings.filterwarnings(
    action='ignore',
    message="The `convert` argument is deprecated in favor of `converter`.  It will be removed after 2019/01.",
    category=DeprecationWarning,
)


if __name__ == '__main__':
    import pytest
    pytest.main()
