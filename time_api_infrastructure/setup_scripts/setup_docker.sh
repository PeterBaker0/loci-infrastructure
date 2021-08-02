# Update package repo
sudo yum update -y

# Install docker
sudo amazon-linux-extras install docker

# Start service
sudo service docker start

# Add the ec2-user user to docker group
sudo usermod -a -G docker ec2-user

# Let's also setup docker compose 
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# And enable execution 
sudo chmod +x /usr/local/bin/docker-compose
