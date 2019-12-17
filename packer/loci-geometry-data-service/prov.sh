#!/bin/bash
yum update -y
amazon-linux-extras install docker 
yum -y install git
curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
chmod +x /usr/bin/docker-compose
systemctl enable docker
systemctl start docker && sleep 5
usermod -a -G docker ec2-user
git clone --single-branch --branch master https://github.com/CSIRO-enviro-informatics/loci-geometry-data-service.git
mv /tmp/instance.sh  /var/lib/cloud/scripts/per-instance/instance.sh
chmod +x /var/lib/cloud/scripts/per-instance/instance.sh
printenv
echo -e "GSDB_HOSTNAME=10.0.1.201" > /home/ec2-user/loci-geometry-data-service/.env
echo -e "GSDB_PORT=25432" >> /home/ec2-user/loci-geometry-data-service/.env
cd /home/ec2-user/loci-geometry-data-service/ && pwd && ls && docker-compose -f docker-compose.yml up -d gservice
