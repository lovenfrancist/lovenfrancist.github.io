#!/bin/sh

/usr/bin/git remote update

UPSTREAM=${1:-'@{u}'}
LOCAL=$(/usr/bin/git rev-parse @)
REMOTE=$(/usr/bin/git rev-parse "$UPSTREAM")
BASE=$(/usr/bin/git merge-base @ "$UPSTREAM")
TAG=$(/usr/bin/git describe --abbrev=0 @)

if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date"
elif [ $LOCAL = $BASE ]; then
    echo "Need to pull"

    /usr/bin/git pull origin develop #TEMP develop to master
    /usr/bin/git fetch --tags

    NEWTAG=$(/usr/bin/git describe --abbrev=0 @)
    echo "TAG:$TAG"
    echo "NEWTAG:$NEWTAG"

    if [ "$TAG" == "$NEWTAG" ]; then
        echo "New commit. Deploying to DEV"
        # compile
        # update DEV domain
    else
        echo "New tag. Deploying to STAGING"
        # compile
        # update STAGING domain
    fi
elif [ $REMOTE = $BASE ]; then
    echo "Need to push"
else
    echo "Diverged"
fi
