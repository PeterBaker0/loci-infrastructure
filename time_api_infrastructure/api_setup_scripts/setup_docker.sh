# Update repos
sudo yum update -y

# Get docker
sudo amazon-linux-extras install docker -y

# Start docker
sudo service docker start

# Enable non sudo docker booting
sudo usermod -a -G docker ec2-user

# Get docker compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make executable
sudo chmod +x /usr/local/bin/docker-compose