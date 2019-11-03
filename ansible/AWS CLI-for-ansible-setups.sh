#Ami- ubuntu 16 : us-east-1 :-ami-04b9e92b5572fa0d1
# this is tested script :-->
#First create key pair -->
aws ec2 create-key-pair \
    --key-name  AnsibleKey\
    --query 'KeyMaterial' \
    --output text \
    --profile="SL" > AnsibleKey.pem

# aws ec2 delete-key-pair --key-name AnsibleKey --profile=SL

create security group:--
aws ec2 create-security-group \
    --group-name MySecurityGroup \
    --description "SG_Ansible_ssh_http" \
    --vpc-id vpc-bb47dcc1 \
    --profile=SL


Tag this SG->

aws ec2 create-tags \
    --resources sg-0ff67a4a8849eed0c \
    --tags 'Key="Name",Value=SG_Ansible_withSSH&HHTTP' \
    --profile=SL

ingress-->
#ssh --
aws ec2 authorize-security-group-ingress \
    --group-id sg-0ff67a4a8849eed0c \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0 \
    --profile=SL

#http:-
aws ec2 authorize-security-group-ingress \
    --group-id sg-0ff67a4a8849eed0c \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0 \
    --profile=SL
#ICMP -request :-
aws ec2 authorize-security-group-ingress \
    --group-id sg-0ff67a4a8849eed0c \
    --ip-permissions IpProtocol=icmp,FromPort=8,ToPort=-1,IpRanges='[{CidrIp=0.0.0.0/0}]' \
    --profile=SL

--verify security groups set up-->
aws ec2 describe-security-groups \
    --group-id sg-0ff67a4a8849eed0c \
    --profile=SL

aws ec2 run-instances \
    --image-id "ami-04b9e92b5572fa0d1" \
    --count 7 \
    --instance-type t2.micro \
    --key-name AnsibleKey \
    --security-group-ids "sg-0ff67a4a8849eed0c" \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value="AnibleHosts"}]' \
    --user-data file://UserData.sh \
    --profile=SL

    
aws ec2 describe-instances \
    --filter Name=tag:Name,Values=AnibleHosts\* \
    --query 'Reservations[*].Instances[*].{Instance:InstanceId,AZ:Placement.AvailabilityZone,PublicIPv4:PublicIpAddress,Name:Tags[?Key==`Name`]|[0].Value}' \
    --output table \
    --profile=SL



#NOw login to control node and set up /et/hosts file as per the host below:-

AnibleControlNode  |  3.89.124.87    
AnibleHosts-1      |  3.95.147.127   
AnibleHosts-2      |  3.95.160.142   
AnibleHosts-3      |  34.201.58.20 
AnibleHosts-4      |  34.205.71.164  
AnibleHosts-5      |  54.165.30.213  
AnibleHosts-6      |  184.72.202.248 
Later added new -->
AnibleHosts   |  3.85.62.255     |
AnibleHosts   |  3.86.77.95      |
AnibleHosts   |  3.88.210.79     |
AnibleHosts   |  52.87.236.11



vi /etc/hosts
3.89.124.87 	server00-pvt.sushiljadhav.com server00
3.95.147.127	client01-pvt.sushiljadhav.com client01
3.95.160.142   	client02-pvt.sushiljadhav.com client02
34.201.58.20 	client03-pvt.sushiljadhav.com client03
34.205.71.164  	client04-pvt.sushiljadhav.com client04
54.165.30.213  	client05-pvt.sushiljadhav.com client05
184.72.202.248 	client06-pvt.sushiljadhav.com client06
Added new servers:--
3.85.62.255 	client07-pvt.sushiljadhav.com client07
3.86.77.95    	client08-pvt.sushiljadhav.com client08
3.88.210.79 	client09-pvt.sushiljadhav.com client09
52.87.236.11	client10-pvt.sushiljadhav.com client10


ssh-keygen
sshpass -f<(printf "%s\n" sushil123) ssh-copy-id -o StrictHostKeyChecking=no sushil@client01-pvt.sushiljadhav.com
sshpass -f<(printf "%s\n" sushil123) ssh-copy-id -o StrictHostKeyChecking=no sushil@client02-pvt.sushiljadhav.com
sshpass -f<(printf "%s\n" sushil123) ssh-copy-id -o StrictHostKeyChecking=no sushil@client03-pvt.sushiljadhav.com
sshpass -f<(printf "%s\n" sushil123) ssh-copy-id -o StrictHostKeyChecking=no sushil@client03-pvt.sushiljadhav.com
sshpass -f<(printf "%s\n" sushil123) ssh-copy-id -o StrictHostKeyChecking=no sushil@client04-pvt.sushiljadhav.com
sshpass -f<(printf "%s\n" sushil123) ssh-copy-id -o StrictHostKeyChecking=no sushil@client05-pvt.sushiljadhav.com
sshpass -f<(printf "%s\n" sushil123) ssh-copy-id -o StrictHostKeyChecking=no sushil@client06-pvt.sushiljadhav.com

vi /var/tmp/setupkeys.sh
ssh-keygen -b 2048 -t rsa -f /tmp/sshkey -q -N ""
sshpass -f<(printf "%s\n" sushil123) ssh-copy-id -i /tmp/sshkey.pub  sushil@client01-pvt.sushiljadhav.com
sshpass -f<(printf "%s\n" sushil123) ssh-copy-id -i /tmp/sshkey.pub  sushil@client02-pvt.sushiljadhav.com
sshpass -f<(printf "%s\n" sushil123) ssh-copy-id -i /tmp/sshkey.pub  sushil@client03-pvt.sushiljadhav.com
sshpass -f<(printf "%s\n" sushil123) ssh-copy-id -i /tmp/sshkey.pub  sushil@client04-pvt.sushiljadhav.com
sshpass -f<(printf "%s\n" sushil123) ssh-copy-id -i /tmp/sshkey.pub  sushil@client05-pvt.sushiljadhav.com
sshpass -f<(printf "%s\n" sushil123) ssh-copy-id -i /tmp/sshkey.pub  sushil@client06-pvt.sushiljadhav.com

Or use following :-
ssh-copy-id -i /root/.ssh/id_rsa.pub  sushil@client01-pvt.sushiljadhav.com  --- worked 

Install ansible only on control host:-
apt update -y
apt upgrade -y 
apt install software-properties-common
apt-add-repository --yes --update ppa:ansible/ansible
apt install ansible -y

Now set up ansible inventory :- /etc/ansible/hosts :-

[all:vars]
ansible_user='sushil'           # Username for ssh connection
ansible_become='yes'             # Run commands as root user?
ansible_become_pass='sushil123' # Password for sudo user i.e. ansible_user password
ansible_become_method='sudo'     # How do I become root user? Use sudo.
ansible_python_interpreter=/usr/bin/python3

[all-servers]
client01-pvt.sushiljadhav.com
client02-pvt.sushiljadhav.com
client03-pvt.sushiljadhav.com
client04-pvt.sushiljadhav.com
client05-pvt.sushiljadhav.com
client06-pvt.sushiljadhav.com

[web-servers]
client01-pvt.sushiljadhav.com
client02-pvt.sushiljadhav.com
client03-pvt.sushiljadhav.com
client04-pvt.sushiljadhav.com

[db-servers]
client05-pvt.sushiljadhav.com
client06-pvt.sushiljadhav.com

Test ansible -->
ansible -m ping all-servers --become




#### Few practice commands >>

#Copy file from control node to web-servers:->
 ansible web-servers -m copy -a "src=test.html dest=/tmp mode='0644'"
 ansible web-servers -m command -a" cat /tmp/test.html"
 ansible all-servers -m command -a" cat /tmp/test.html"