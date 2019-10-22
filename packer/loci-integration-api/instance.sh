#!/bin/bash
cd /home/ec2-user/loci-integration-api/ && pwd && ls && while [ ! -d "/certs" ];  do sleep 2; done; docker-compose -f docker-compose.yml -f docker-compose.prod.yml -f docker-compose.es.yml up -d 
