<div align="center">

# GitHub Archive

A powerful script to concurrently clone your entire GitHub instance or save it as an archive.

[![Build Status](https://travis-ci.com/Justintime50/github-archive.svg?branch=master)](https://travis-ci.com/Justintime50/github-archive)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

<img src="assets/showcase.gif">

</div>

## What Can it Do?

- Clone/pull personal repos (public and private)
- Clone/pull organization repos (public and private)
- Clone/pull personal gists (public and private)
- Iterate over infinite number of repos and gists concurrently
- Great use case: Run on a schedule to automate pulling changes or keep a local backup of all your repos

### Configurable Settings

The power of GitHub Archive comes in its configuration. Maybe you only want to clone/pull your personal public repos or maybe you want to go all out and include private repos from you and all organizations you belong to including your gists. Customize the location repos are saved to, how long logs are kept for. Iterate over 100's of repos concurrently and sit back while GitHub Archive does all the work.

- Personal repos (on/off)
- Organization repos (on/off)
- Personal Gists (on/off)
- Cloning (on/off)
- Pulling (on/off)
- What organizations you'd like included
- Log retention life
- GitHub Archive location
- Which branch to pull from

## Install

```bash
# Install dependencies
pip3 install -r requirements.txt

# Copy the environment file and edit for your needs.
cp .env.example .env
``` 

**For Private Repos:** You must have an SSH key generated on your local machine and added to your GitHub account.

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
python3 github-archive.py
```

### Shell Alias

```bash
# If using Bash insted of ZSH, use ~/.bash_profile
echo alias github-archive="/path/to/github-archive.py" >> ~/.zshrc
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

0 1 * * * /path/to/github-archive.py
```

## Legacy Script

GitHub Archive was initially built with Bash partly because I was into shell scripting at the time and partly because I wanted to keep the script as dependency free as possible. Even still, the Bash script depended on Python. As Python will soon be removed from macOS by default, I decided to rewrite the script in pure Python for two reasons - 1) Once Python is no longer built-in, users would need to install Python anyway making the pure Bash script broken out of the box and 2) Rewriting allowed me to take full advantage of the power of Python. One large benefit of doing this was adding concurrency which is great for users with dozens or hundreds of repos across various organizations. Additional logging and stability improvements were also made.

If you'd like to use or view the legacy script, check out the `src/legacy` folder.
