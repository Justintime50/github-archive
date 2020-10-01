# CHANGELOG

## 3.0.0 (2020-10-01)

* Refactored the entire codebase to be more pythonic, simpler, DRY, and documented (closes #15)
* Better error handling by raising errors where applicable and switching from a homegrown logger to the built-in Python logger (closes #12)
* Added unit tests and test coverage (closes #14)
* Added various additional configuration options
* Automated releasing on PyPi via Travis
* Various bug fixes throughout
* Better documentation on exactly what is possible with this tool
* Added a Makefile
* Adjusted most of the command and option names to be more uniform and explicit

## 2.1.2 (2020-8-14)

* Fixed the script's entrypoint (PyPi installs work again)

## 2.1.1 (2020-07-14)

* Fixed the long argument names which had underscores intead of hyphens
* Fixed a bug where threads were not waiting at the end of the script before printing the completion message

## 2.1.0 (2020-07-01)

* Replaced `requirements.txt` with `setup.py`
* Removed Launch Agent
* Set the default git pull behavior as `--ff-only` to avoid git message (closes #)
* Increased default timeout for git operations from `120` seconds to `180` seconds
* Replaced the majority of environment variables with command line args making customization easier as "feature flags"
* Various bug fixes and minor improvements
* Removed log deletion functionality
* Published to Pypi

## 2.0.1 (2020-05-30)

* Fixed the Python program line in the launch agent plist

## 2.0.0 (2020-05-18)

* Rewrote the script in Python
* Added concurrency to clone/pull changes incredibly fast for large amounts of repos and gists
* Added even more custimization and control
* Uniform log naming, better logging details
* Added changelog

## 1.1.0 (2020)

* Added more customization options
* Allowed organization and gists to be cloned/pulled
* Allowed private repos to be cloned/pulled
* Bug fixes

## 1.0.0 (2019)

* Wrote the script in Bash with Python as dependency
* Added some customization options
