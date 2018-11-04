
# lovenfrancist.github.io

# Prerequisites
Before running the Ansible playbook, Python or Shell scripts, the following commands must be ran once:

## download public and private keys for git ssh

```bash
wget -O ~/.ssh/id_rsa.pub https://s3-ap-southeast-1.amazonaws.com/isentia-exam/id_rsa.pub -q -o /dev/null
wget -O ~/.ssh/id_rsa https://s3-ap-southeast-1.amazonaws.com/isentia-exam/id_rsa -q -o /dev/null
```

## setup passwordless ssh for localhost

```bash
chmod 400 ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod og-wx ~/.ssh/authorized_keys
```

## ssh-agent
These need to be executed every login to ssh, unless you edit the user's `~/.bash_profile`:

```bash
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_rsa
```

To test, run:
```bash
ssh -T git@github.com
```
type `yes` then press enter key:

```bash
$ ssh -T git@github.com
The authenticity of host 'github.com (192.nn.253.nnn)' can't be established.
RSA key fingerprint is SHA256:nThbg6kXYZ0l7E1IGOCspRomTxdABCDviKw6E5SY8.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'github.com,192.nn.253.nnn' (RSA) to the list of known hosts.
Hi lovenfrancist! You've successfully authenticated, but GitHub does not provide shell access.
```

## install ansible (ubuntu)

```bash
sudo apt-get update
sudo apt-get install software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt-get install ansible
```

# Getting started
## Clone the repo
If you have not already done so, you will need to clone, or create a local copy, of the [lovenfrancist.github.io repo](https://github.com/lovenfrancist/lovenfrancist.github.io). For more on how to clone the repo, view [git clone help](https://git-scm.com/docs/git-clone).

```bash
git clone git@github.com:lovenfrancist/lovenfrancist.github.io.git
```

Once you have a local copy, run commands within the root of the project tree.

```bash
cd lovenfrancist.github.io/
```

## Playbook
Execute the playbook `my_exam_playbook.yaml` to provision the server where this project will run on (localhost). Use a non-root user with sudo privileges.

```bash
ansible-playbook -i inventory my_exam_playbook.yaml
```

## Python script
The Ansible playbook will already run the `my_exam.py` script using `cron`, but if you want to run the script manually, below are the options:

```bash
python my_exam.py dev
python my_exam.py staging
python my_exam.py build
python my_exam.py build /path/to/build/dir
```

## Shell script
The shell script `poll_github.sh`will check the github repo of the project to get new commits and tags.
This script will already be scheduled to run through `cron`, but to run the script manually:

```bash
./poll_github.sh
```

# Other info
## Build directories
The following are the default build directories for `dev/staging` environments and for `build` option:

```
/var/www/myexam.dev/html
/var/www/myexam.staging/html
/path/to/local/git/repo/_site
```

## Viewing the website
To view the static website, go to the server's hostname/IP address:

For dev:

    http://<hostname/IP address>:81
For staging:

    http://<hostname/IP address>
