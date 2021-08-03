from aws_cdk import(
    core as cdk,
    aws_ec2 as ec2
)

from time_api_infrastructure.constructs.vpc import ComputeVPC
from time_api_infrastructure.api_infrastructure import APIInfrastructure


class TimeApiInfrastructureStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # CIDR for the VPC
        cidr = "10.0.0.0/24"

        # Setting up subnets
        # In our case all elements are publically exposed
        # and therefore we can have only a single public endpoint
        subnets = [
            ec2.SubnetConfiguration(
                name="api_db_subnet",
                subnet_type=ec2.SubnetType.PUBLIC,
                cidr_mask=24
            )
        ]

        # Setup the VPC
        compute_vpc = ComputeVPC(
            scope=self,
            id="time_demo_network",
            cidr=cidr,
            subnets=subnets
        )
        
        # Create API infrastructure 
        api_infrastructure = APIInfrastructure(
            self, 
            "api_infrastructure",
            compute_vpc.vpc,
            "10.0.0.27"
        )