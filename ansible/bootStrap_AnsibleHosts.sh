#!/bin/bash
#Bootstrap script to snip up ubuntu instances for ansible works
apt-get update -y
apt-get upgrade -y
useradd -mG admin sushil
echo "sushil:sushil123"|chpasswd
sed -i "s/PasswordAuthentication no/PasswordAuthentication yes/g" /etc/ssh/sshd_config
service sshd restart
apt install python -y
apt install sshpass