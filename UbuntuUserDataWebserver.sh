#!/bin/bash
apt-get update -y
apt-get install apache2 -y
apt-get install curl -y
systemctl start apache2
systemctl enable apache2
ip=$(curl http://169.254.169.254/latest/meta-data/hostname)
cd /var/www/html
echo "<html> <h1> Welcome to Webserver - $ip !! </h1> </html>" > index.html