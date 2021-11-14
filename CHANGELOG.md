# CHANGELOG

## v4.2.0 (2021-11-13)

* Uses `woodchips` for logging and removes internal logging logic from the package
* Refactors git commands to not change directories but instead run commands with the `-C` flag to invoke it in the directory we want

## v4.1.1 (2021-11-02)

* Fixes a bug that wouldn't allow for gist cloning/pulling because of a bad "forks" check on a gist GitHub object
* Adds a missing check to ensure that at least one CLI argument was passed (closes #40)
* No longer invoke a shell while using the subprocess module. Git operations should now be more stable across operating systems

## v4.1.0 (2021-09-19)

* Adds a new `--https` flag which will authenticate via HTTPS instead of the default `SSH`
* Fixes a bug where using the `--stars` flag would not properly run due to a missing parameter. This parameter wasn't actually being used anymore and has been removed. Tests were beefed up for this function to protect against this happening again

## v4.0.0 (2021-08-24)

### Breaking Changes

* Reworks the entire app config to use CLI flags solely instead of a mix of CLI flags and env variables, additionally, most flags have changed names and functionality. See the README for new usage instructions or run `github-archive --help` (closes #30)
* Repos or gists that fail to clone or pull will now be completely removed so that they can be retried from scratch on the next run of the tool. This was an especially important change for bad clones as the tool would previously leave an empty initialized git folder even if the clone failed which would not possess the actual git repo yet. In this state, you could not properly pull new changes because the content of the repo hadn't properly been cloned yet
* Bumps required Python version from 3.6 to 3.7

### Features

* Adds a new `--users` flag which can be used to clone or pull git assets for a list of comma separated users (closes #20)
* Adds a new `--threads` flag which can specify the number of concurrent threads to run at once, default is `10` (closes #22)
* Adds a new `--view` flag which allows you to "dry run" the application, seeing the entire list of repos and gists based on the input provided (closes #25)
* Adds a new `--stars` flag which you can pass a comma separated list of users to and GitHub Archive will retrieve all of their starred repos which you can then view, clone, or pull (closes #26)
* Adds a new `--forks` flag which will include forks for whatever lists and operations you provide, default is `False` (closes #17))

### Fixes

* Removed verbose logging of skipped actions and "Already up to date" messages. Added additional logging related to API calls
* Added proper validation and type checking of variables and environment on startup
* Various code refactors, bug fixes, and optimizations
* Bumped the default git operation timeout from `180 seconds` to `300 seconds` to assist with cloning or pulling larger repos (closes #22)
* Removes `mock` library in favor of builtin `unittest.mock` library

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
