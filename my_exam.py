import os
import sys
import time
import subprocess
import yaml
from string import Template

class MyExam:
    def __init__(self, env):
        self.env = env.lower()
        self.myexam_path = os.path.dirname(os.path.realpath(__file__))

    def add_post(self):
        # initialize variables
        post_body = subprocess.check_output("/usr/games/fortune", shell=True)
        post_title = ' '.join(post_body.split()[:5])
        post_title = post_title.replace('"', '')
        post_title = post_title.replace("'", '')
        post_title = post_title.replace("?", '')
        post_title = post_title.replace(".", '')
        post_date = time.strftime("%Y-%m-%d %H:%M:%S") + " +0000"
        newfile = time.strftime("%Y-%m-%d") + "-" + post_title + ".markdown"
        post_dict={ 'post_title':post_title, 'post_body':post_body, \
            'post_date':post_date, 'layout':'post' }

        # read, write to file
        with open(os.path.join(self.myexam_path, \
        "templates", "post.j2"), "rt") as post_template:
            with open(os.path.join(self.myexam_path, "_posts", newfile), "wt") as fout:
                src = Template( post_template.read() )
                fout.write(src.substitute(post_dict))

        print "Added new post: {0}".format(post_title)

    def bump_version(self):
        # get current version
        with open(os.path.join(self.myexam_path, "_config.yml"), "rt") as config:
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
        with open(os.path.join(self.myexam_path, \
        "templates", "_config.yml.j2"), "rt") as config_template:
            with open(os.path.join(self.myexam_path, "_config.yml"), "wt") as fout:
                src = Template( config_template.read() )
                fout.write(src.substitute(config_dict))

        self.new_ver = new_ver
        print "Bumped version to : {0}".format(new_ver)

    def compile_site(self, build_dir=''):
        print "Compiling at: {0}".format(build_dir)

        if os.path.isdir(build_dir):
            print subprocess.check_output("bundle exec \
            jekyll build -d {0}".format(build_dir), shell=True)
            print "Compiled at: {0}".format(build_dir)
        else:
            if env.lower() == 'dev':
                build_dir = '/var/www/myexam.dev/html'
            elif env.lower() == 'staging':
                build_dir = '/var/www/myexam.staging/html'

            if os.path.isdir(build_dir):
                print subprocess.check_output("bundle exec \
                jekyll build -d {0}".format(build_dir), shell=True)
                print "Compiled at: {0}".format(build_dir)
            else:
                print subprocess.check_output("bundle exec \
                jekyll build", shell=True)
                print "Compiled at: {0}".format(build_dir)

        print subprocess.check_output("sudo nginx -s reload", shell=True)
        print subprocess.check_output("sudo service nginx restart", shell=True)

    def commit_code(self):
        print "Commiting code"
        print subprocess.check_output("/usr/bin/git remote set-url origin\
        git@github.com:lovenfrancist/lovenfrancist.github.io.git", shell=True)
        print subprocess.check_output("eval $(ssh-agent -s) && \
        ssh-add ~/.ssh/id_rsa", shell=True)
        # print subprocess.check_output("ssh-add ~/.ssh/id_rsa", shell=True)

        print subprocess.check_output("/usr/bin/git add -A", shell=True)
        print subprocess.check_output("/usr/bin/git commit -m 'New Post {0}'"\
        .format(time.strftime("%Y-%m-%d %H:%M:%S")), shell=True)

        # tag
        if self.env == 'staging':
            print subprocess.check_output("/usr/bin/git tag -a v{0} -m, 'v{0}'"\
            .format(self.new_ver), shell=True)

            print subprocess.check_output("/usr/bin/git push origin v{0}"\
            .format(self.new_ver), shell=True)

        # push
        print subprocess.check_output("/usr/bin/git push origin \
        develop:develop", shell=True) #TEMP dev to master


if __name__ == '__main__':
    try:
        try:
            env = sys.argv[1]
        except IndexError:
            print "Parameter required. Usage: python my_exam.py [dev|staging|build]\
             [environment directory (optional)]"
            sys.exit()

        if env.lower() not in ['dev', 'staging', 'build']:
            print "Invalid arguments. Usage: python my_exam.py [dev|staging|build]\
             [environment directory (optional)]"
            sys.exit()

        # add new post
        myexam = MyExam(env)
        if env.lower() == 'dev':
            myexam.add_post()

        # bump version
        if env.lower() in ['dev', 'staging']:
            myexam.bump_version()

    #     # compile jekyll
    #     try:
    #         myexam.compile_site(sys.argv[2])
    #     except IndexError:
    #         myexam.compile_site()
    #
    #     # commit
    #     if env.lower() in ['dev', 'staging']:
    #         myexam.commit_code()
    except Exception, e:
        print(sys.exc_info()[0])
