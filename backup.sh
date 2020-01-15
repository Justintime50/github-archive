#!/bin/bash

# Import config and check if something is missing
source .config
if [ -z "$SCOPE" ] || [ -z "$USERNAME" ] || [ -z "$TOKEN" ] || [ -z "$PAGE" ] || [ -z "$DATE" ] || [ -z "$LOG_LIFE" ] || [ -z "$LOCATION" ] ; then
    echo "You have variables that have no values, please set them in the \".config\" before continuing."
    exit
fi

# Setup required directories
mkdir -p "$LOCATION"
mkdir -p "$LOCATION"/archive-logs
cd "$LOCATION" || exit

# Clone all repos you have access to
{
curl -u "$USERNAME":"$TOKEN" "https://api.github.com/$SCOPE/$USERNAME/repos?page=$PAGE&per_page=100" |
        grep -e 'git_ur[l]*' |
        cut -d \" -f 4 |
        xargs -L1 git clone

# Pull any changes
for DIR in */ ; do
    printf '%s\n' "$DIR"
    cd "$DIR" && git pull origin master
    cd ..
done
echo "Github Archive Complete!"
} 2>&1 | tee "$LOCATION"/archive-logs/"$DATE".log

# Cleanup after being run
find "$LOCATION"/archive-logs -mindepth 1 -mtime +"$LOG_LIFE" -delete
history -c
