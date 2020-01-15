<div align="center">

# Github Archive

[![Build Status](https://travis-ci.org/Justintime50/github-archive.svg?branch=master)](https://travis-ci.org/Justintime50/github-archive)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

Backup and clone your entire Github instance.

<img src="assets/showcase.gif">

</div>

## Install

1. Run `cp .config.example .config` and edit the values to your liking.
1. For private repos, you must have an SSH key generated on your local machine and added to Github.

### Automating SSH Key Prompt on macOS (optional)

To allow the script to run continuosly without user intervention, you'll need to add your SSH key to the SSH agent.

```bash
ssh-add -K ~/.ssh/id_rsa
```

## Usage

This script is intended to grab an archive of your entire Github instance or to be setup with a cron to run occasionally and pull in any changes to keep a local copy of your Github repos.

Github Archive will pull/clone from the master branch of each repo that you have access to including organizations.

**Single Use**
```bash
./backup.sh
```

**Cron Example**
```bash
crontab -e

0 1 * * * ~/github-archive/backup.sh
```
