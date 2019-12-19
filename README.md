# Github Archive

[![Build Status](https://travis-ci.org/Justintime50/github-archive.svg?branch=master)](https://travis-ci.org/Justintime50/github-archive)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

Backup and clone your entire Github instance to a local machine.

## Setup

Change the Username in the `backup.sh` file to your username. The script will ask for your password each time.

## Usage

This script is intended to either be used to grab an archive of your entire Github instance or to be setup with a Cron to run daily to pull in any changes to keep a local copy of your Github repos.

It will pull/clone from the master branch of each repo.

```bash
./backup.sh
```
