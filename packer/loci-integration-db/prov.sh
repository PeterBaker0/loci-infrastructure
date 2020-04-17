#!/bin/bash
yum update -y
amazon-linux-extras install docker 
yum -y install git
curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
chmod +x /usr/bin/docker-compose
systemctl enable docker
systemctl start docker && sleep 5
usermod -a -G docker ec2-user
git clone --single-branch --branch master https://github.com/CSIRO-enviro-informatics/loci-cache-scripts.git
mv /tmp/instance.sh  /var/lib/cloud/scripts/per-boot/instance.sh
chmod +x /var/lib/cloud/scripts/per-boot/instance.sh
printenv
cd /home/ec2-user/loci-cache-scripts/docker/linksets/asgs2geofab/ && pwd && ls && source ../../../common/common.sh && docker-compose -f docker-compose.base.yml up -d postgis && docker-compose -f docker-compose.base.yml run linksets /bin/sh -c 'curl https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o ./wait-for-it.sh && chmod +x ./wait-for-it.sh && ./wait-for-it.sh postgis:5432 && sleep 10 && cd /app/mb2cc && python linksets_mb_cc_builder.py'
