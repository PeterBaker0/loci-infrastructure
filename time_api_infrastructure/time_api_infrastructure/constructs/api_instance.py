
from aws_cdk import(
    core,
    aws_ec2 as ec2
)
from typing import Optional


class EC2Instance(core.Construct):
    def __init__(
            self,
            scope: core.Construct,
            id: str,
            size: Optional[ec2.InstanceSize] = ec2.InstanceSize.MICRO,
            machine_type: Optional[ec2.InstanceClass] = ec2.InstanceClass.STANDARD5,
            **kwargs):

        super().__init__(scope, id, **kwargs)

