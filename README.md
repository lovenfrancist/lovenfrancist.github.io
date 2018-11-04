
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
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod og-wx ~/.ssh/authorized_keys
```

## ssh-agent
These need to be executed every login to ssh, unless you edit the user's `~/.bash_profile`:

```bash
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_rsa
```

## install ansible

```bash
sudo apt-get update
sudo apt-get install software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt-get install ansible
```

# Playbook
Execute the playbook `my_exam_playbook.yaml` to provision the server where this project will run on (localhost). Use a non-root user with sudo privileges.

```bash
ansible-playbook -i inventory my_exam_playbook.yaml
```

# Python script
The Ansible playbook will already run the `my_exam.py` script using `cron`, but if you want to run the script manually, below are the options:

```bash
python my_exam.py dev
python my_exam.py staging
python my_exam.py build
python my_exam.py build /path/to/build/dir
```

# Shell script
The shell script `poll_github.sh`will check the github repo of the project to get new commits and tags.
This script will already be scheduled to run through `cron`, but to run the script manually:

```bash
./poll_github.sh
```
