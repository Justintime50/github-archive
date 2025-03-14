# CHANGELOG

## v6.3.0 (2025-03-13)

- Adds new `languages` CLI flag allowing filtering via a comma-separated list of GitHub languages for repos (cannot be used with include/exclude) - (closes #59)
- Forking repos is now a threaded operation like all other operations instead of sequential

## v6.2.0 (2025-03-13)

- Forking gists is now a threaded operation like all other operations instead of sequential
- Corrects two log messages that incorrectly mentioned `starred` resources when they should have been `org/user` resources

## v6.1.2 (2023-08-27)

- Expand paths for user-supplied `--location` strings. This now allows for spaces in paths and proper expansion of home directories (eg: `~`)

## v6.1.1 (2023-08-26)

- Fixes PyGithub pinned version to ensure `Auth` is available

## v6.1.0 (2023-08-24)

- Allows the tool to be run without passing any authentication flags (previously, to use unauthenticated, you'd have to at least pass the `--https` flag)
- Removes constraint that required `--token` and `--https` to be mutually exclusive (you can now authenticate with other tools such as Git Credential Manager instead of only SSH)
- Adds `--version` CLI flag

## v6.0.0 (2023-06-30)

- Drops support for Python 3.7
- Updates dependencies

## v5.0.3 (2023-05-15)

- Fixes a syntax error that led to not being able to remove the authenticated user from the user's list so their git assets weren't included twice (fixes #55)

## v5.0.2 (2023-03-25)

- Overhauls subprocess error handling so output is no longer clobbered
- No longer inserts newlines (which were often formatted incorrectly) when a log entry was for a new section or action

## v5.0.1 (2022-12-07)

- Fixes a bug that tries removing the authenticated user from a list so we don't double dip git operations even when there is no authenticated user (eg: using the `--https` flag)
- Fixes a bug that allowed users to use both the `--token` and `--https` when it should only be one or the other

## v5.0.0 (2022-10-19)

- Adds a new `--fork` CLI arg which adds support to fork the repos or gists specified via `users`, `orgs`, `stars`, or `gists`
- Removed various shorthand CLI args to avoid confusion and improved help message output for CLI args (updated docs as well)
  - Breaking Change Note: The previous `-f` flag that would include forks when cloning or pulling repos/gists is now associated with the `--fork` CLI arg which will actually fork repos to your account. The `--forks` (plural) CLI flag no longer has a shorthand option
- Namespaces for various functions changed for better project organization. As this project is intended to be used as a CLI tool and not a library, the impact should be minimal

## 4.5.1 (2022-09-15)

- Clarifies default location of github-archive in help output

## v4.5.0 (2022-02-22)

- Switches from the `threading` package to the `concurrent.futures` package allowing us to return values from each individual thread (in this case, the names of failed git assets)
  - Fixes a long-standing bug where git repos that failed to clone would remain in the archive on Windows. This meant that recloning was impossible due to the repo existing and pulling was not possible because the repo wasn't yet fully initialized. The tool now has a proper cleanup step after everything has run that is compatible with both Unix and Windows environments (closes #38)
- Adds `--log_level` to allow the user to specify a custom log level
- Small adjustment to `include` and `exclude` help verbage used to be more clear they are optional filters

## v4.4.0 (2022-02-18)

- Adds an `--include` and `--exclude` CLI flag that accepts a comma-separated list of repo names to either include or exclude. If neither are passed, no filtering will occur (closes #43)

## v4.3.0 (2021-12-16)

- Adds the ability to specify a custom base_url for GitHub (useful for enterprise GitHub users with a custom hostname, closes #41)

## v4.2.2 (2021-11-29)

- Adds `mypy` and fixes typing errors

## v4.2.1 (2021-11-25)

- Bumps `woodchips` to use the new implementation (also fixes a bug where we were creating a new `woodchips.Logger` class each time we called the logger instead of reusing the same logger instance)
- Adds missing `__all__` variable for importing
- Added Python type hinting

## v4.2.0 (2021-11-13)

- Uses `woodchips` for logging and removes internal logging logic from the package
- Refactors git commands to not change directories but instead run commands with the `-C` flag to invoke it in the directory we want

## v4.1.1 (2021-11-02)

- Fixes a bug that wouldn't allow for gist cloning/pulling because of a bad "forks" check on a gist GitHub object
- Adds a missing check to ensure that at least one CLI argument was passed (closes #40)
- No longer invoke a shell while using the subprocess module. Git operations should now be more stable across operating systems

## v4.1.0 (2021-09-19)

- Adds a new `--https` flag which will authenticate via HTTPS instead of the default `SSH`
- Fixes a bug where using the `--stars` flag would not properly run due to a missing parameter. This parameter wasn't actually being used anymore and has been removed. Tests were beefed up for this function to protect against this happening again

## v4.0.0 (2021-08-24)

### Breaking Changes

- Reworks the entire app config to use CLI flags solely instead of a mix of CLI flags and env variables, additionally, most flags have changed names and functionality. See the README for new usage instructions or run `github-archive --help` (closes #30)
- Repos or gists that fail to clone or pull will now be completely removed so that they can be retried from scratch on the next run of the tool. This was an especially important change for bad clones as the tool would previously leave an empty initialized git folder even if the clone failed which would not possess the actual git repo yet. In this state, you could not properly pull new changes because the content of the repo hadn't properly been cloned yet
- Bumps required Python version from 3.6 to 3.7

### Features

- Adds a new `--users` flag which can be used to clone or pull git assets for a list of comma separated users (closes #20)
- Adds a new `--threads` flag which can specify the number of concurrent threads to run at once, default is `10` (closes #22)
- Adds a new `--view` flag which allows you to "dry run" the application, seeing the entire list of repos and gists based on the input provided (closes #25)
- Adds a new `--stars` flag which you can pass a comma separated list of users to and GitHub Archive will retrieve all of their starred repos which you can then view, clone, or pull (closes #26)
- Adds a new `--forks` flag which will include forks for whatever lists and operations you provide, default is `False` (closes #17))

### Fixes

- Removed verbose logging of skipped actions and "Already up to date" messages. Added additional logging related to API calls
- Added proper validation and type checking of variables and environment on startup
- Various code refactors, bug fixes, and optimizations
- Bumped the default git operation timeout from `180 seconds` to `300 seconds` to assist with cloning or pulling larger repos (closes #22)
- Removes `mock` library in favor of builtin `unittest.mock` library

## v3.1.1 (2021-07-24)

- Removed `branch` flag and functionality as it was causing issues and inconsistencies when cloning/pulling and branches didn't match up. This became especially prevelant when repos started changing from `master` to `main`

## v3.1.0 (2020-12-16)

- Changed all classmethods to staticmethods
- Corrected a bug where org names may not have had whitespace stripped properly
- CLI arguments now have an explicit default of `False`, this shouldn't change behavior from previous versions
- CLI default argument for `branch` has been changed from `master` to `None` and is handled via logic now. If no branch is specified, the default repo branch will be used instead of blindly assuming that `master` is the default branch (closes #18)
- Revamped the entire test suite to use conftest, simplified boilerplate, etc

## v3.0.1 (2020-10-01)

- Fixed broken entrypoint after shifting code around

## v3.0.0 (2020-10-01)

- Refactored the entire codebase to be more pythonic, simpler, DRY, and documented (closes #15)
- Better error handling by raising errors where applicable and switching from a homegrown logger to the built-in Python logger (closes #12)
- Added unit tests and test coverage (closes #14)
- Added various additional configuration options
- Automated releasing on PyPi via Travis
- Various bug fixes throughout
- Better documentation on exactly what is possible with this tool
- Added a Makefile
- Adjusted most of the command and option names to be more uniform and explicit

## v2.1.2 (2020-08-14)

- Fixed the script's entrypoint (PyPi installs work again)

## v2.1.1 (2020-07-14)

- Fixed the long argument names which had underscores intead of hyphens
- Fixed a bug where threads were not waiting at the end of the script before printing the completion message

## v2.1.0 (2020-07-01)

- Replaced `requirements.txt` with `setup.py`
- Removed Launch Agent
- Set the default git pull behavior as `--ff-only` to avoid git message (closes #9)
- Increased default timeout for git operations from `120` seconds to `180` seconds
- Replaced the majority of environment variables with command line args making customization easier as "feature flags"
- Various bug fixes and minor improvements
- Removed log deletion functionality
- Published to Pypi

## v2.0.1 (2020-05-30)

- Fixed the Python program line in the launch agent plist

## v2.0.0 (2020-05-18)

- Rewrote the script in Python
- Added concurrency to clone/pull changes incredibly fast for large amounts of repos and gists
- Added even more custimization and control
- Uniform log naming, better logging details
- Added changelog

## v1.1.0 (2020)

- Added more customization options
- Allowed organization and gists to be cloned/pulled
- Allowed private repos to be cloned/pulled
- Bug fixes

## v1.0.0 (2019)

- Wrote the script in Bash with Python as dependency
- Added some customization options
