#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose
sudo ls -lah /usr/bin
sudo service docker start
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user
sudo docker-compose up -d 
