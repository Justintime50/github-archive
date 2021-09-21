<div align="center">

# GitHub Archive

A powerful tool to concurrently clone or pull user and org repos and gists to create a GitHub archive.

[![Build Status](https://github.com/Justintime50/github-archive/workflows/build/badge.svg)](https://github.com/Justintime50/github-archive/actions)
[![Coverage Status](https://coveralls.io/repos/github/Justintime50/github-archive/badge.svg?branch=main)](https://coveralls.io/github/Justintime50/github-archive?branch=main)
[![PyPi](https://img.shields.io/pypi/v/github-archive)](https://pypi.org/project/github-archive)
[![Licence](https://img.shields.io/github/license/justintime50/GitHub-archive)](LICENSE)

<img src="https://raw.githubusercontent.com/justintime50/assets/main/src/github-archive/showcase.png" alt="Showcase">

</div>

GitHub Archive is a powerful tool to concurrently clone or pull repositories or gists from GitHub with incredible flexibility. It's the perfect tool for spinning up a new dev environment, keeping a local copy of your GitHub instance, or quickly pulling in projects from your favorite users and organizations.

### Configurable Settings

The power of GitHub Archive comes in its configuration. Maybe you only want to clone or pull your personal public repos or maybe you want to go all out and include private repos from you and all organizations you belong to along with your gists. 

## Install

```bash
# Install tool
pip3 install github-archive

# Install locally
make install

# Get Makefile help
make help
``` 

## Usage

```
Usage:
    github-archive --users justintime50 --clone

Options:
    -h, --help            show this help message and exit
    -t TOKEN, --token TOKEN
                            Provide your GitHub token to authenticate with the GitHub API and gain access to private repos and gists.
    -u USERS, --users USERS
                            Pass a comma separated list of users to get repos for.
    -o ORGS, --orgs ORGS  Pass a comma separated list of orgs to get repos for.
    -g GISTS, --gists GISTS
                            Pass a comma separated list of users to get gists for.
    -s STARS, --stars STARS
                            Pass a comma separated list of users to get starred repos for.
    -v, --view            Pass this flag to view git assets (dry run).
    -c, --clone           Pass this flag to clone git assets.
    -p, --pull            Pass this flag to pull git assets.
    -f, --forks           Pass this flag to include forked git assets.
    -l LOCATION, --location LOCATION
                            The location where you want your GitHub Archive to be stored.
    -ht, --https          Use HTTPS URLs instead of SSH.
    -to TIMEOUT, --timeout TIMEOUT
                            The number of seconds before a git operation times out.
    -th THREADS, --threads THREADS
                            The number of concurrent threads to run.
```

### Automating SSH Passphrase Prompt (Recommended)

To allow the script to run continuosly without requiring your SSH passphrase, you'll need to add your passphrase to the SSH agent. **NOTE:** Your SSH passphrase will be unloaded upon logout.

```bash
# This assumes you've saved your SSH keys to the default location
ssh-add
```

### Notes

**SSH Key:** By default, you must have an SSH key generated on your local machine and added to your GitHub account as this tool uses the `ssh_url` to clone/pull. If you'd like to instead use the `git_url` to clone/pull, you can pass the `--https` flag which will authenticate with your username and password.

**Merge Conflicts:** Be aware that using GitHub Archive could lead to merge conflicts if you do not commit or stash your changes if using these repos as active development repos instead of simply an archive or one-time clone.

**Access**: GitHub Archive can only clone or pull git assets that the authenticated user has access to. This means that private repos from another user or org that you don't have access to will not be able to be cloned or pulled.

## Development

```bash
# Lint the project
make lint

# Run tests
make test

# Run test coverage
make coverage

# Run the tool locally
venv/bin/python github_archive/cli.py --help
```
