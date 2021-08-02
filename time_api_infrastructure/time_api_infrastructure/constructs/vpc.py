from aws_cdk import(
    core,
    aws_ec2 as ec2
)
from typing import List


class ComputeVPC(core.Construct):
    def __init__(
            self,
            scope: core.Construct,
            id: str,
            cidr:str, 
            subnets:List,
            **kwargs):

        super().__init__(scope, id, **kwargs)

        # Establish vpc
        self.vpc = ec2.Vpc(self,
                           id + "_vpc", 
                           cidr=cidr,
                           subnet_configuration=subnets,
                           max_azs=1)