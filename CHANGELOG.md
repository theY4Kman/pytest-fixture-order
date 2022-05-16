# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [Unreleased]


## [0.1.4] — 2022-05-16
### Fixed
 - Resolve `scopenum_function` ImportErrors with pytest 7.x (see [GH#2](https://github.com/theY4Kman/pytest-fixture-order/issues/2); thank you, [@last-partizan](https://github.com/last-partizan)!)


## [0.1.3] — 2020-08-25
### Changed
 - Add compatibility for pytest versions up to ~6.0.0
 - Transferred ownership to @theY4Kman


## [0.1.2] — 2019-09-03
### Changed
 - The `order(index)`, `early`, and `late` markers are now explicitly registered, to avoid warnings from pytest.
 - The `combined` attribute is used to extract marker args/kwargs, to avoid warnings from pytest.
 - Compatibility with pytest ~5.0.0 and ~5.1.0 is now tested.


## [0.1.1] — 2019-04-22
### Fixed
 - Included README in package, for display on PyPI


## [0.1.0] - 2019-04-22
### Added
 - Introduced `@pytest.mark.order(index)`, `@pytest.mark.early` (where `index = -1`), and `@pytest.mark.late` (where `index = 1`) fixture markers to influence fixture evaluation order.
