#!/bin/bash
yum update -y
amazon-linux-extras install docker 
yum -y install git
curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
chmod +x /usr/bin/docker-compose
systemctl enable docker
systemctl start docker && sleep 5
echo "vm.max_map_count=262144" >> /etc/sysctl.d/98-sysctl.conf
usermod -a -G docker ec2-user
git clone --single-branch --branch master https://github.com/CSIRO-enviro-informatics/loci-cors-proxy.git 
mv /tmp/instance.sh  /var/lib/cloud/scripts/per-instance/instance.sh
mv /tmp/wildcard-loci-cat.bundle.pem /home/ec2-user/loci-cors-proxy/certs/
mv /tmp/wildcard-loci-cat.pem /home/ec2-user/loci-cors-proxy/certs/
ls -la /home/ec2-user/loci-cors-proxy/certs/
chmod +x /var/lib/cloud/scripts/per-instance/instance.sh
