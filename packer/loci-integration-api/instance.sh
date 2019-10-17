#!/bin/bash
cd /home/ec2-user/loci-integration-api/ && pwd && ls && docker-compose -f docker-compose.yml -f docker-compose.prod.yml  -f search/docker-compose.yml up 
