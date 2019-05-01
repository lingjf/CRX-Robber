# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased] - 2019-05-01
(Poikilos)
### Changed
* Rename project.
* Change newlines to LF for linux.
* Simplify README.md.
* Shorten function names.
* Allow filename instead of URL.
  - Make functions more functional (take param, return result).
* Conform to PEP8.
* Return nonzero on error.
* Convert to Python 3.
* Compare None properly.
* Correctly handle result of fcrx.read(1) (in `rb` mode).
* Correctly read crx v3 (only try to read signature_key_length if v2)
