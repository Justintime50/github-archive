<div align="center">

# GitHub Archive

A powerful tool to concurrently clone, pull, or fork user and org repos and gists to create a GitHub archive.

[![Build Status](https://github.com/Justintime50/github-archive/workflows/build/badge.svg)](https://github.com/Justintime50/github-archive/actions)
[![Coverage Status](https://coveralls.io/repos/github/Justintime50/github-archive/badge.svg?branch=main)](https://coveralls.io/github/Justintime50/github-archive?branch=main)
[![PyPi](https://img.shields.io/pypi/v/github-archive)](https://pypi.org/project/github-archive)
[![Licence](https://img.shields.io/github/license/justintime50/GitHub-archive)](LICENSE)

<img src="https://raw.githubusercontent.com/justintime50/assets/main/src/github-archive/showcase.png" alt="Showcase">

</div>

GitHub Archive is a powerful tool to concurrently clone, pull, or fork repositories or gists from GitHub with incredible flexibility. It's the perfect tool for spinning up a new dev environment, keeping a local copy of your GitHub instance, or quickly pulling in projects from your favorite users and organizations.

The power of GitHub Archive comes in its configuration. Maybe you only want to clone or pull your personal public repos or maybe you want to go all out and include private repos from you and all organizations you belong to along with your gists. GitHub Archive can do it all.

## Install

```bash
# Install tool
pip3 install github-archive

# Install locally
make install
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
    -f, --fork            Pass this flag to fork git assets.
    --include INCLUDE     Pass a comma separated list of repos to filter what is included in the Archive.
    --exclude EXCLUDE     Pass a comma separated list of repos to filter what is excluded from the Archive.
    --forks               Pass this flag to include forked git assets (when cloning or pulling).
    --location LOCATION   The location where you want your GitHub Archive to be stored. Default: /Users/USERNAME/github-archive
    --https               Use HTTPS URLs instead of SSH.
    --timeout TIMEOUT     The number of seconds before a git operation times out. Default: 300
    --threads THREADS     The number of concurrent threads to run. Default: 10
    --base_url BASE_URL   The base URL of your GitHub instance (useful for enterprise users with custom hostnames). Default: https://api.github.com
    --log_level {error,critical,warning,info,debug}
                            The log level used for the tool. Default: info
```

### Automating SSH Passphrase Prompt (Recommended)

To allow the script to run continuosly without requiring your SSH passphrase, you'll need to add your passphrase to the SSH agent. **NOTE:** Your SSH passphrase will be unloaded upon logout.

```bash
# This assumes you've saved your SSH keys to the default location
ssh-add
```

### Notes

**SSH Key:** By default, you must have an SSH key generated on your local machine and added to your GitHub account as this tool uses the `ssh_url` to clone/pull. If you'd like to instead use the `git_url` to clone/pull, you can pass the `--https` flag which currently requires no authentication. Without using a token/SSH, you will not be able to interact with private git assets. Additionally, GitHub has a hard limit of 60 requests per hour - using the `--https` option may quickly burn through that unauthenticated limit if you have a large GitHub instance to archive.

**Merge Conflicts:** Be aware that using GitHub Archive could lead to merge conflicts if you do not commit or stash your changes if using these repos as active development repos instead of simply an archive or one-time clone.

**Access**: GitHub Archive can only clone or pull git assets that the authenticated user has access to. This means that private repos from another user or org that you don't have access to will not be able to be cloned or pulled.

## Development

```bash
# Get a comprehensive list of development tools
make help

# Run the tool locally
venv/bin/python github_archive/cli.py --help
```
