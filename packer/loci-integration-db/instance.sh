#!/bin/bash
cd /home/ec2-user/loci-cache-scripts/docker/linksets/asgs2geofab/ && pwd && ls && source ../../../common/common.sh && docker-compose -f docker-compose.base.yml up -d 
