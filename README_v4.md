<div align="center">

# GitHub Archive

A powerful tool to concurrently clone or pull user and org repos and gists to create a GitHub archive.

[![Build Status](https://github.com/Justintime50/github-archive/workflows/build/badge.svg)](https://github.com/Justintime50/github-archive/actions)
[![Coverage Status](https://coveralls.io/repos/github/Justintime50/github-archive/badge.svg?branch=main)](https://coveralls.io/github/Justintime50/github-archive?branch=main)
[![PyPi](https://img.shields.io/pypi/v/github-archive)](https://pypi.org/project/github-archive)
[![Licence](https://img.shields.io/github/license/justintime50/GitHub-archive)](LICENSE)

<img src="assets/showcase.png" alt="Showcase">

</div>

GitHub Archive will clone any repo and gist that doesn't exist locally and pull those that do from the main branch of each repo and latest revision of each gist that you have access to - including organizations (if configured).

## What Can it Do?

* Clone/pull personal repos (public and private)
* Clone/pull organization repos (public and private)
* Clone/pull personal gists (public and private)
* Iterate over infinite number of repos and gists concurrently
* Great use case: Run on a schedule to automate pulling changes or keep a local backup of all your repos

### Configurable Settings

The power of GitHub Archive comes in its configuration. Maybe you only want to clone/pull your personal public repos or maybe you want to go all out and include private repos from you and all organizations you belong to including your gists. Iterate over all your repos concurrently and sit back while GitHub Archive does the work.

* Personal repos cloning/pulling
* Organization repos cloning/pulling
* Gists cloning/pulling
* List of organizations to include
* A host of environment variables to tweak GitHub Archive even further to meet your needs

## Install

```bash
# Install tool
pip3 install github-archive

# Install locally
make install

# Get Makefile help
make help
``` 

### Automating SSH Passphrase Prompt (Recommended)

To allow the script to run continuosly without requiring your SSH passphrase, you'll need to add your passphrase to the SSH agent. **NOTE:** Your SSH passphrase will be unloaded upon logout.

```bash
# This assumes you've saved your SSH keys to the default location
ssh-add
```

## Usage

**SSH Key:** You must have an SSH key generated on your local machine and added to your GitHub account as this tool uses the `ssh_url` to clone/pull. 

**Merge Conflicts:** Be aware that using GitHub Archive could lead to merge conflicts if you do not commit or stash your changes if using these repos as active development repos instead of simply an archive or one-time clone.

**Access**: GitHub Archive can only clone or pull repos that the authenticated user has access to. That means that private repos from another user or orgs that you don't have access to will not be able to be cloned or pulled.

```
Usage:
    github-archive --users justintime50 --clone

Options:
    -h, --help            show this help message and exit
    -v, --view            Pass this flag to view git assets (dry run).
    -c, --clone           Pass this flag to clone git assets.
    -p, --pull            Pass this flag to pull git assets.
    -u USERS, --users USERS
                            Pass a comma separated list of users to get repos for.
    -o ORGS, --orgs ORGS  Pass a comma separated list of orgs to get repos for.
    -g GISTS, --gists GISTS
                            Pass a comma separated list of users to get gists for.
    -s STARS, --stars STARS
                            Pass a comma separated list of users to get starred repos for.
    -to TIMEOUT, --timeout TIMEOUT
                            The number of seconds before a git operation times out.
    -th THREADS, --threads THREADS
                            The number of concurrent threads to run.
    -t TOKEN, --token TOKEN
                            Provide your GitHub token to authenticate with the GitHub API and gain access to private repos and gists.
    -l LOCATION, --location LOCATION
                            The location where you want your GitHub Archive to be stored.
```

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
