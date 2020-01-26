#!/bin/bash

# Import config and run some config checks
# shellcheck disable=SC1090,SC2153
source "${BASH_SOURCE%/*}/.config"
if [[ -z "$USERNAME" ]] || [[ -z "$TOKEN" ]] || [[ -z "$PAGES" ]] || [[ -z "$DATE" ]] || [[ -z "$LOG_LIFE" ]] || [[ -z "$LOCATION" ]] || [[ -z "$BRANCH" ]] || [[ -z "$USER_ON" ]] || [[ -z "$ORGS_ON" ]] || [[ -z "$GISTS_ON" ]] || [[ -z "$PER_PAGE" ]] || [[ -z "$CLONE_ON" ]] || [[ -z "$PULL_ON" ]] ; then
    # $ORGS is the only optional variable not checked for
    echo "ERROR: You have variables that have no values, please set them in the \".config\" file before continuing."
    exit
fi
if [[ "$PER_PAGE" -gt "100" ]] ; then
    echo "ERROR: PER_PAGE cannot be over 100 per Github's API limits. Please correct in your config and run again."
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
    if [[ "$CLONE_ON" == "enable" ]] ; then
        echo -e "Cloning personal repos..."
        for PAGE in ${PAGES[*]} ; do
            mkdir -p "$LOCATION"/repos/"$USERNAME"
            cd "$LOCATION"/repos/"$USERNAME" || exit
            curl -u "$USERNAME":"$TOKEN" -s "https://api.github.com/users/$USERNAME/repos?page=$PAGE&per_page=$PER_PAGE" |
            python -c $'import json, sys, os\nfor repo in json.load(sys.stdin): os.system("git clone " + repo["ssh_url"])'
            cd .. || exit
            echo -e "Personal repos cloned!\n"
        done

        # Clone all repos from the configured orgs you have access to
        if [[ "$ORGS_ON" == "enable" ]] ; then
            for PAGE in ${PAGES[*]} ; do
                for ORG in ${ORGS[*]} ; do
                    echo -e "Cloning $ORG repos..."
                    mkdir -p "$LOCATION"/repos/"$ORG"
                    cd "$LOCATION"/repos/"$ORG" || exit
                    curl -u "$USERNAME":"$TOKEN" -s "https://api.github.com/orgs/$ORG/repos?page=$PAGE&per_page=$PER_PAGE" |
                    python -c $'import json, sys, os\nfor repo in json.load(sys.stdin): os.system("git clone " + repo["ssh_url"])'
                    cd .. || exit
                    echo -e "$ORG repos cloned!\n"
                done
            done
            echo -e "Organization repos cloned!\n"
        fi
    fi

    # Setup dir and message if orgs are enabled
    if [[ "$ORGS_ON" == "enable" ]] ; then
        DIRARRAY="$USERNAME $ORGS"
        PULLMSG="Personal & organization repos pulled!\n"
    else
        DIRARRAY="$USERNAME"
        PULLMSG="Personal repos pulled!\n"
    fi

    # Pull any changes from each repo in the archive if enabled
    if [[ "$PULL_ON" == "enable" ]] ; then
        echo -e "Pulling existing repos..."
        for TOPDIR in ${DIRARRAY[*]} ; do
            printf '%s\n' "$TOPDIR"
            cd "$TOPDIR" || exit
            for DIR in */ ; do
                printf '%s\n' "$DIR"
                cd "$DIR" && git pull origin "$BRANCH"
                cd .. || exit
            done
            cd .. || exit
        done
        echo -e "$PULLMSG"
    fi

    # Clone all gists from the user's account
    if [[ "$GISTS_ON" == "enable" && "$CLONE_ON" == "enable" ]] ; then
        echo -e "Cloning personal gists..."
        for PAGE in ${PAGES[*]} ; do
            cd "$LOCATION"/gists || exit
            curl -u "$USERNAME":"$TOKEN" -s "https://api.github.com/users/$USERNAME/gists?page=$PAGE&per_page=$PER_PAGE" |
            python -c $'import json, sys, os\nfor repo in json.load(sys.stdin): os.system("git clone " + repo["html_url"])'
            echo -e "Personal gists cloned!\n"
        done

        # Pull any changes from each gist in the archive
        if [[ "$PULL_ON" == "enable" ]] ; then
            echo -e "Pulling existing gists..."
            for DIR in */ ; do
                printf '%s\n' "$DIR"
                cd "$DIR" && git pull
                cd .. || exit
            done
            echo -e "Personal gists pulled!\n"
        fi
    fi

    echo -e "Github Archive Complete!\n"
} 2>&1 | tee "$LOCATION"/logs/"$DATE".log

# Cleanup logs after being run
find "$LOCATION"/logs -mindepth 1 -mtime +"$LOG_LIFE" -delete
