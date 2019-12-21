# Github Archive

[![Build Status](https://travis-ci.org/Justintime50/github-archive.svg?branch=master)](https://travis-ci.org/Justintime50/github-archive)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

Backup and clone your entire Github instance to a local machine.

## Setup

Edit the variables in the `backup.sh` to setup your user, log life, pagination, and scope.

## Usage

This script is intended to either be used to grab an archive of your entire Github instance or to be setup with a Cron to run daily to pull in any changes to keep a local copy of your Github repos.

It will pull/clone from the master branch of each repo.

**Single Use**
```bash
./backup.sh
```

**Cron**
```bash
crontab -e

0 1 * * * ~/github-archive/backup.sh
```
