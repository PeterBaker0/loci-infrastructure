#!/usr/bin/env python3
from time_api_infrastructure.configuration import DEPLOYMENT_REGION, DEPLOYMENT_ACCOUNT_ID
from time_api_infrastructure.time_api_infrastructure_stack import TimeApiInfrastructureStack

import aws_cdk.core as cdk

# Create base app in which to deploy the
# stack
app = cdk.App()

# Establish a target deployment
DEPLOYMENT_TARGET = {
    'account': DEPLOYMENT_ACCOUNT_ID,
    'region': DEPLOYMENT_REGION
}

# Deploy resources
TimeApiInfrastructureStack(app, "TimeApiInfrastructureStack",
                           env=DEPLOYMENT_TARGET
                           )
app.synth()
