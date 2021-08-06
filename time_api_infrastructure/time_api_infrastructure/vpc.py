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
            subnets:List[ec2.SubnetConfiguration],
            **kwargs):
        """Produces a basic VPC which suits this application
        with the given params.

        Args:
            scope (core.Construct): The CDK construct.
            id (str): The CDK id of this construct.
            cidr (str): The CIDR block for the VPC.
            subnets (List(ec2.SubnetConfiguration)): 
            The list of subnets included.
        """
        super().__init__(scope, id, **kwargs)

        # Establish vpc
        self.vpc = ec2.Vpc(self,
                           id + "_vpc", 
                           cidr=cidr,
                           subnet_configuration=subnets,
                           # No need for availability zones
                           # right now.
                           max_azs=1)