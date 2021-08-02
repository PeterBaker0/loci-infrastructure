#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from time_api_infrastructure.time_api_infrastructure_stack import TimeApiInfrastructureStack


app = core.App()

DEFAULT_REGION = 'ap-southeast-2'
ACCOUNT_ID = "077917336704"  # LOCI Account
DEPLOYMENT_TARGET = {
    'account': ACCOUNT_ID,
    'region': DEFAULT_REGION
}

TimeApiInfrastructureStack(app, "TimeApiInfrastructureStack",
                           env=DEPLOYMENT_TARGET
                           )

app.synth()
