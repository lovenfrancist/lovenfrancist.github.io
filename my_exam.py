import os
import sys
import time
import subprocess
import yaml
from string import Template

class MyExam:
    def __init__(self, env):
        self.env = env.lower()

    def add_post(self):
        # initialize variables
        post_body = subprocess.check_output("/usr/games/fortune", shell=True)
        post_title = ' '.join(post_body.split()[:5])
        post_date = time.strftime("%Y-%m-%d %H:%M:%S") + " +0000"
        newfile = time.strftime("%Y-%m-%d") + "-" + post_title + ".markdown"
        post_dict={ 'post_title':post_title, 'post_body':post_body, \
            'post_date':post_date, 'layout':'post' }

        # read, write to file
        with open(os.path.join(os.getcwd(), \
        "templates", "post.j2"), "rt") as post_template:
            with open(os.path.join(os.getcwd(), "_posts", newfile), "wt") as fout:
                src = Template( post_template.read() )
                fout.write(src.substitute(post_dict))

        print "Added new post: {0}".format(post_title)

    def bump_version(self):
        # get current version
        with open(os.path.join(os.getcwd(), "_config.yml"), "rt") as config:
            data = yaml.load(config)
            current_ver = data["description"].split(':')[1].strip()

        current_major = int(current_ver.split('.')[0])
        current_minor = int(current_ver.split('.')[1])
        current_revision = int(current_ver.split('.')[2])

        # bump
        if self.env == 'dev':
            new_ver = '.'.join([str(current_major), str(current_minor), str(current_revision + 1)])
        elif self.env == 'staging':
            new_ver = '.'.join([str(current_major), str(current_minor + 1), str(current_revision)])
        elif self.env == 'prod':
            new_ver = '.'.join([str(current_major + 1), str(current_minor), str(current_revision)])
        else:
            new_ver = current_ver

        # update config
        config_dict={ 'version':new_ver }
        with open(os.path.join(os.getcwd(), \
        "templates", "_config.yml.j2"), "rt") as config_template:
            with open(os.path.join(os.getcwd(), "_config.yml"), "wt") as fout:
                src = Template( config_template.read() )
                fout.write(src.substitute(config_dict))

        print "Bumped version to : {0}".format(new_ver)

    def compile_site(self):
        print subprocess.call(["~/gems/bin/bundle", "exec", \
        "~/gems/bin/jekyll", "build"], shell=True)

    def commit_code(self):
        print subprocess.call("/usr/bin/git remote set-url origin\
        git@github.com:lovenfrancist/lovenfrancist.github.io.git", shell=True)
        print subprocess.call("eval $(ssh-agent -s)", shell=True)
        print subprocess.call("ssh-add ~/.ssh/id_rsa", shell=True)

        print subprocess.call("/usr/bin/git add -A", shell=True)
        print subprocess.call("/usr/bin/git commit -m 'New Post {0}'"\
        .format(time.strftime("%Y-%m-%d %H:%M:%S")), shell=True)
        print subprocess.call("/usr/bin/git push origin \
        develop:develop", shell=True) #TEMP dev to master

if __name__ == '__main__':
    try:
        env = sys.argv[1]
    except IndexError:
        print "Parameter required. Usage: python my_exam.py [dev|staging]"
        sys.exit()
    else:
        if env.lower() not in ['dev', 'staging']:
            print "Invalid arguments. Usage: python my_exam.py [dev|staging]"
            sys.exit()

        # add new post
        myexam = MyExam(env)
        if env.lower() == 'dev':
            myexam.add_post()

        # bump version
        myexam.bump_version()

        # compile jekyll
        myexam.compile_site()

        # commit
        myexam.commit_code()
