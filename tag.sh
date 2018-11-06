#!/usr/bin/env bash

/usr/bin/git remote set-url origin git@github.com:lovenfrancist/lovenfrancist.github.io.git
eval $(ssh-agent -s) && ssh-add ~/.ssh/id_rsa

/usr/bin/git add -A
/usr/bin/git commit -m 'New Post - '
/usr/bin/git push origin develop:develop

/usr/bin/git tag -a v0.22.85 -m, "v0.22.85"
/usr/bin/git push origin v0.22.85


