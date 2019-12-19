#!/bin/bash

# Clone all repos
mkdir -p "$HOME"/github-archive
cd "$HOME"/github-archive || exit
CNTX="users"; NAME="Justintime50"; PAGE=1
curl -u "Justintime50" "https://api.github.com/$CNTX/$NAME/repos?page=$PAGE&per_page=100" |
        grep -e 'git_ur[l]*' |
        cut -d \" -f 4 |
        xargs -L1 git clone

# Pull any changes
for dir in * ; do
    printf '%s\n' "$dir"
    cd "$dir" && git pull origin master
    cd ..
done
