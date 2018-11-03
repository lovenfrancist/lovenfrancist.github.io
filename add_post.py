import os
import datetime
import subprocess
from string import Template

post_body = subprocess.check_output("fortune", shell=True)
post_title = ' '.join(post_body.split()[:5])
post_date = datetime.datetime.now().strftime("%Y-%m-%d")
newfile = post_date + "-" + post_title + ".markdown"
post_dict={ 'post_title':post_title, 'post_body':post_body, 'post_date':post_date }

with open(os.path.join(os.getcwd(), \
"templates", "post.j2"), "rt") as post_template:
    with open(os.path.join(os.getcwd(), "_posts", newfile), "wt") as fout:
        src = Template( post_template.read() )
        fout.write(src.substitute(post_dict))
