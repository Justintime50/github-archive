<div align="center">

# GitHub Archive

Powerful script to clone your entire GitHub instance or save it as an archive.

[![Build Status](https://travis-ci.com/Justintime50/github-archive.svg?branch=master)](https://travis-ci.com/Justintime50/github-archive)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

<img src="assets/showcase.gif">

</div>

## What Can it Do?

- Clone/pull personal repos (public and private)
- Clone/pull organization repos (public and private)
- Clone/pull personal gists (public and private)
- Iterate over 100's of repos and gists
- Can be configured to run on a schedule to automate pulling changes

### Configurable Settings

The power of GitHub Archive comes in its configuration. Maybe you only want to clone/pull your personal public repos or maybe you want to go all out and include private repos from you and all organizations you belong to including your gists. Customize the location repos are saved to, how long logs are kept for and the naming format they'll use. Iterate over 100's of repos and sit back while GitHub Archive does all the work.

- Personal repos (on/off)
- Organization repos (on/off)
- Personal Gists (on/off)
- Cloning (on/off)
- Pulling (on/off)
- Specify the number of repos to include (1 - ∞)
- Log retention life & filename scheme
- GitHub Archive location
- Which branch to pull from

## Install

This project requires that you have Python installed. Python comes built-in on macOS and Linux.

```bash
# Copy the configuration file and edit for your needs.
cp .config.example .config
``` 

**For Private Repos:** You must have an SSH key generated on your local machine and added to GitHub.

### Automating SSH Passphrase Prompt (Recommended)

To allow the script to run continuosly without requiring your SSH passphrase, you'll need to add your passphrase to the SSH agent. **NOTE:** Your SSH passphrase will be unloaded upon logout.

```bash
# This assumes you've saved your SSH keys to the default location
ssh-add
```

## Usage

GitHub Archive will clone any repo and gist that doesn't exist locally and pull those that do from the master branch of each repo and latest revision of each gist that you have access to - including organizations (if configured). You can run the script once, add an alias, or have it setup with a cron or Launch Agent and run occasionally to clone/pull any changes since it was last run.

**Merge Conflicts:** *Be aware that using GitHub Archive could lead to merge conflicts if you continually pull the same repos you work on without stashing or committing your changes. It is recommended to be used once for example on a new machine or setup as a separate archive from your development repositories. If you use GitHub Archive to pull in nighly changes from various repos, you should be religious about stashing or committing your changes or you will receive merge conflicts and the script may not complete running.*

### Run Script

```bash
./github-archive.sh
```

### Shell Alias

```bash
# If using Bash insted of ZSH, use ~/.bash_profile
echo alias github-archive="/path/to/github-archive.sh" >> ~/.zshrc
source ~/.zshrc

# Usage of alias
github-archive
```

### Launch Agent (Recommended on macOS)

Edit the path in the `plist` file to your script and logs as well as the time to execute, then setup the Launch Agent:

```bash
# Copy the plist to the Launch Agent directory
cp local.githubArchive.plist ~/Library/LaunchAgents

# Use `load/unload` to add/remove the script as a Launch Agent
launchctl load ~/Library/LaunchAgents/local.githubArchive.plist

# To `start/stop` the script from running, use the following
launchctl start local.githubArchive.plist
```

### Cron

```bash
crontab -e

0 1 * * * /path/to/github-archive.sh
```
