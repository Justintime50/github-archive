#!/bin/bash

# Import config and check if something is missing
# shellcheck disable=SC1090
source "${BASH_SOURCE%/*}/.config"
if [ -z "$USERNAME" ] || [ -z "$TOKEN" ] || [ -z "$PAGE" ] || [ -z "$DATE" ] || [ -z "$LOG_LIFE" ] || [ -z "$LOCATION" ] ; then
    echo "You have variables that have no values, please set them in the \".config\" before continuing."
    exit
fi

# Setup required directories
mkdir -p "$LOCATION"
mkdir -p "$LOCATION"/repos
mkdir -p "$LOCATION"/gists
mkdir -p "$LOCATION"/logs
cd "$LOCATION"/repos || exit

# Start archive
{
    # Clone all repos from the user's account
    mkdir -p "$LOCATION"/repos/"$USERNAME"
    cd "$LOCATION"/repos/"$USERNAME" || exit
    curl -u "$USERNAME":"$TOKEN" -s "https://api.github.com/users/$USERNAME/repos?page=$PAGE&per_page=100" |
    python -c $'import json, sys, os\nfor repo in json.load(sys.stdin): os.system("git clone " + repo["ssh_url"])'
    cd .. || exit

    # Clone all repos from the configured orgs you have access to
    for ORG in ${ORGS[*]} ; do
        mkdir -p "$LOCATION"/repos/"$ORG"
        cd "$LOCATION"/repos/"$ORG" || exit
        curl -u "$USERNAME":"$TOKEN" -s "https://api.github.com/orgs/$ORG/repos?page=$PAGE&per_page=100" |
        python -c $'import json, sys, os\nfor repo in json.load(sys.stdin): os.system("git clone " + repo["ssh_url"])'
        cd .. || exit
    done

    # Pull any changes from each repo in the archive
    DIRARRAY="$USERNAME $ORGS"
    for DIRARRAY in */ ; do
        printf '%s\n' "$DIRARRAY"
        cd "$DIRARRAY" || exit
        for DIR in */ ; do
            printf '%s\n' "$DIR"
            cd "$DIR" && git pull origin master
            cd .. || exit
        done
        cd .. || exit
    done

    # Clone all gists from the user's account
    cd "$LOCATION"/gists || exit
    curl -u "$USERNAME":"$TOKEN" -s "https://api.github.com/users/$USERNAME/gists?page=$PAGE&per_page=100" |
    python -c $'import json, sys, os\nfor repo in json.load(sys.stdin): os.system("git clone " + repo["html_url"])'

    # Pull any changes from each gist in the archive
    for DIR in */ ; do
        printf '%s\n' "$DIR"
        cd "$DIR" && git pull
        cd .. || exit
    done

    echo "Github Archive Complete!"
} 2>&1 | tee "$LOCATION"/logs/"$DATE".log

# Cleanup logs after being run
find "$LOCATION"/logs -mindepth 1 -mtime +"$LOG_LIFE" -delete
