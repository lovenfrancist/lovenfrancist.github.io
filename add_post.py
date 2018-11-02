import os
import datetime
import subprocess

post = subprocess.check_output("fortune", shell=True)
post_title = post.split()[:5]
post_title = ' '.join(post_title)
newfile = datetime.datetime.now().strftime("%Y-%m-%d") + "-" + post_title + ".markdown"

with open(os.path.join(os.getcwd(), \
"templates", "post.j2"), "rt") as post_template:
    with open(os.path.join(os.getcwd(), "_posts", newfile), "wt") as fout:
        for line in post_template:
            fout.write(line.replace('{{ post_title }}', post_title))
