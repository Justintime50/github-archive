#!/bin/bash

# Declare variables
#######################################################################
SCOPE="users"                   # either "users" or "orgs"
USERNAME=""                     # your username or organization name
TOKEN=""                        # this is either your password or a token if 2FA is enabled
PAGE="1"                        # pagination for repos, currently 100 is the max per page per Github's limits
DATE=$(date +'%m-%d-%Y')        # date format you'd like your logs saved in
LOG_LIFE="30"                   # number of days logs will be retained for
LOCATION="$HOME/github-archive" # where your archive will be housed
#######################################################################

if [ -z "$SCOPE" ] || [ -z "$USERNAME" ] || [ -z "$TOKEN" ] || [ -z "$PAGE" ] || [ -z "$DATE" ] || [ -z "$LOG_LIFE" ] || [ -z "$LOCATION" ] ; then
    echo "You have variables that have no values, please set them before continuing."
    exit
fi

# Setup required directories
mkdir -p "$LOCATION"
mkdir -p "$LOCATION"/archive-logs
cd "$LOCATION" || exit

# Clone all repos
{
curl -u "$USERNAME":"$TOKEN" "https://api.github.com/$SCOPE/$USERNAME/repos?page=$PAGE&per_page=100" |
        grep -e 'git_ur[l]*' |
        cut -d \" -f 4 |
        xargs -L1 git clone

# Use the following to clone private repos. NOTE: This method is not automated as it requires the RSA passphrase for each repository.
# curl -u "$USERNAME":"$TOKEN" -s "https://api.github.com/$SCOPE/$USERNAME/repos?page=$PAGE&per_page=100" | 
# python -c $'import json, sys, os\nfor repo in json.load(sys.stdin): os.system("git clone " + repo["ssh_url"])'

# Pull any changes
for DIR in */ ; do
    printf '%s\n' "$DIR"
    cd "$DIR" && git pull origin master
    cd ..
done
} 2>&1 | tee "$LOCATION"/archive-logs/"$DATE".log

# Cleanup after being run
find "$LOCATION"/archive-logs -mindepth 1 -mtime +"$LOG_LIFE" -delete
history -c
