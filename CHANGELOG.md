# CHANGELOG

## NEXT RELEASE

### Breaking Changes

* The `--user_clone` and `--user_pull` flags are now titled `--personal_clone` and `--personal_pull` as the new `--user_clone` and `--user_pull` flags are used for a list of specified users

### Features

* Adds the ability to specify a list of users via `GITHUB_ARCHIVE_USERS` to clone and pull repos for via the `--users_clone` and `--users_pull` flags (closes #20)

### Fixes

* Removed verbose logging of skipped actions (relegated them to the debugging logger). Added additional debug logging and user-readable logging related to API calls 
* Adds proper validation of the `GITHUB_ARCHIVE_ORGS` variable on startup
* Various code refactor, bug fixes, and optimizations

## v3.1.1 (2021-07-24)

* Removed `branch` flag and functionality as it was causing issues and inconsistencies when cloning/pulling and branches didn't match up. This became especially prevelant when repos started changing from `master` to `main`

## v3.1.0 (2020-12-16)

* Changed all classmethods to staticmethods
* Corrected a bug where org names may not have had whitespace stripped properly
* CLI arguments now have an explicit default of `False`, this shouldn't change behavior from previous versions
* CLI default argument for `branch` has been changed from `master` to `None` and is handled via logic now. If no branch is specified, the default repo branch will be used instead of blindly assuming that `master` is the default branch (closes #18)
* Revamped the entire test suite to use conftest, simplified boilerplate, etc

## v3.0.1 (2020-10-01)

* Fixed broken entrypoint after shifting code around

## v3.0.0 (2020-10-01)

* Refactored the entire codebase to be more pythonic, simpler, DRY, and documented (closes #15)
* Better error handling by raising errors where applicable and switching from a homegrown logger to the built-in Python logger (closes #12)
* Added unit tests and test coverage (closes #14)
* Added various additional configuration options
* Automated releasing on PyPi via Travis
* Various bug fixes throughout
* Better documentation on exactly what is possible with this tool
* Added a Makefile
* Adjusted most of the command and option names to be more uniform and explicit

## v2.1.2 (2020-08-14)

* Fixed the script's entrypoint (PyPi installs work again)

## v2.1.1 (2020-07-14)

* Fixed the long argument names which had underscores intead of hyphens
* Fixed a bug where threads were not waiting at the end of the script before printing the completion message

## v2.1.0 (2020-07-01)

* Replaced `requirements.txt` with `setup.py`
* Removed Launch Agent
* Set the default git pull behavior as `--ff-only` to avoid git message (closes #9)
* Increased default timeout for git operations from `120` seconds to `180` seconds
* Replaced the majority of environment variables with command line args making customization easier as "feature flags"
* Various bug fixes and minor improvements
* Removed log deletion functionality
* Published to Pypi

## v2.0.1 (2020-05-30)

* Fixed the Python program line in the launch agent plist

## v2.0.0 (2020-05-18)

* Rewrote the script in Python
* Added concurrency to clone/pull changes incredibly fast for large amounts of repos and gists
* Added even more custimization and control
* Uniform log naming, better logging details
* Added changelog

## v1.1.0 (2020)

* Added more customization options
* Allowed organization and gists to be cloned/pulled
* Allowed private repos to be cloned/pulled
* Bug fixes

## v1.0.0 (2019)

* Wrote the script in Bash with Python as dependency
* Added some customization options
