#!/bin/bash
sudo apt update
sudo apt install git -y
sudo apt install ansible -y
git clone https://github.com/jaykwapong/awswordpress.git
cd awswordpress
ansible-galaxy collection install community.general
ansible-playbook playbook.yml