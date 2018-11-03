# dev
# */10 * * * * (cd ~/lovenfrancist.github.io && exec python my_exam.py dev)

# staging
# */60 * * * * (cd ~/lovenfrancist.github.io && exec python my_exam.py staging)

*/5 * * * * (cd ~/lovenfrancist.github.io && exec poll_github.sh)
