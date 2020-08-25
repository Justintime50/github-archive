<div align="center">

# GitHub Archive

A powerful script to concurrently clone your entire GitHub instance or save it as an archive.

[![Build Status](https://travis-ci.com/Justintime50/github-archive.svg?branch=master)](https://travis-ci.com/Justintime50/github-archive)
[![Coverage Status](https://coveralls.io/repos/github/Justintime50/github-archive/badge.svg?branch=master)](https://coveralls.io/github/Justintime50/github-archive?branch=master)
[![PyPi](https://img.shields.io/pypi/v/github-archive)](https://pypi.org/project/github-archive)
[![Licence](https://img.shields.io/github/license/justintime50/GitHub-archive)](https://opensource.org/licenses/mit-license.php)

<img src="assets/showcase.gif" alt="Showcase">

</div>

## What Can it Do?

- Clone/pull personal repos (public and private)
- Clone/pull organization repos (public and private)
- Clone/pull personal gists (public and private)
- Iterate over infinite number of repos and gists concurrently
- Great use case: Run on a schedule to automate pulling changes or keep a local backup of all your repos

### Configurable Settings

The power of GitHub Archive comes in its configuration. Maybe you only want to clone/pull your personal public repos or maybe you want to go all out and include private repos from you and all organizations you belong to including your gists. Iterate over all your repos concurrently and sit back while GitHub Archive does the work.

- Personal repos (on/off)
- Organization repos (on/off)
- Personal Gists (on/off)
- Cloning (on/off)
- Pulling (on/off)
- What organizations you'd like included
- GitHub Archive location
- Which branch to clone/pull from

## Install

```bash
pip3 install github-archive
``` 

**For Private Repos:** You must have an SSH key generated on your local machine and added to your GitHub account as this tool uses the `ssh_url` to clone/pull. 

### Automating SSH Passphrase Prompt (Recommended)

To allow the script to run continuosly without requiring your SSH passphrase, you'll need to add your passphrase to the SSH agent. **NOTE:** Your SSH passphrase will be unloaded upon logout.

```bash
# This assumes you've saved your SSH keys to the default location
ssh-add
```

## Usage

GitHub Archive will clone any repo and gist that doesn't exist locally and pull those that do from the master branch of each repo and latest revision of each gist that you have access to - including organizations (if configured). **Merge Conflicts:** *Be aware that using GitHub Archive could lead to merge conflicts if you do not commit or stash your changes if using these repos as active development repos instead of simply an archive or one-time clone.*

By default, you only need to specify your GitHub token and GitHub Archive will clone/pull your personal repos for you. See below for customization options.

```
Basic Usage:
    GITHUB_ARCHIVE_TOKEN=123... github_archive --user-clone --user-pull

Advanced Usage:
    GITHUB_ARCHIVE_TOKEN=123... GITHUB_ARCHIVE_ORGS="org1, org2" GITHUB_ARCHIVE_LOCATION="~/custom_location" \
    github-archive -uc -up -gc -gp -oc -op -b develop

Options:
    -uc, --user-clone   Clone personal repos (default: on)
    -up, --user-pull    Pull personal repos (default: on)
    -gc, --gists-clone  Clone personal gists (default: off)
    -gp, --gists-pull   Pull personal gists (default: off)
    -oc, --orgs-clone   Clone organization repos (default: off)
    -op, --orgs-pull    Pull organization repos (defaulf: off)
    -b, --branch        The branch to clone/pull from (default "master")
    -h, --help          Show usage info on for this tool

Environment variables
    GITHUB_ARCHIVE_TOKEN - expects a string
    GITHUB_ARCHIVE_ORGS - expects a string of comma separated orgs. eg: "org1, org2"
    GITHUB_ARCHIVE_LOCATION - expects a string of an explicit location on your machine. eg: "~/custom_location"
```

## Development

Install project with dev depencencies:

```bash
pip3 install -e ."[dev]"
```

Lint the project:

```bash
pylint githubarchive/*.py
```

## Legacy Script

GitHub Archive was initially built with Bash partly because I was into shell scripting at the time and partly because I wanted to keep the script as dependency free as possible. Even still, the Bash script depended on Python. As Python will soon be removed from macOS by default, I decided to rewrite the script in pure Python for two reasons - 1) Once Python is no longer built-in, users would need to install Python anyway making the pure Bash script broken out of the box and 2) Rewriting allowed me to take full advantage of the power of Python. One large benefit of doing this was adding concurrency which is great for users with dozens or hundreds of repos across various organizations. Additional logging and stability improvements were also made.

If you'd like to use or view the legacy script, check out the `src/legacy` folder.
