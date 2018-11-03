#!/bin/sh

/usr/bin/git remote update

UPSTREAM=${1:-'@{u}'}
LOCAL=$(/usr/bin/git rev-parse @)
REMOTE=$(/usr/bin/git rev-parse "$UPSTREAM")
BASE=$(/usr/bin/git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date"
elif [ $LOCAL = $BASE ]; then
    echo "Need to pull"
    /usr/bin/git pull origin develop #TEMP develop to master
    /usr/bin/git fetch --tags
    TAG=$(/usr/bin/git describe @)
    echo "TAG:$TAG"
elif [ $REMOTE = $BASE ]; then
    echo "Need to push"
else
    echo "Diverged"
fi
