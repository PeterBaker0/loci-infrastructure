from aws_cdk import(
    core as cdk,
    aws_ec2 as ec2
)

from time_api_infrastructure.constructs.vpc import ComputeVPC


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

        # We now have a vpc and a subnet inside it, we can now create the instance
        # which will automatically create the
        api_instance = ec2.Instance(
            scope=self,
            id="api_ec2_instance",
            instance_type=ec2.InstanceType.of(
                instance_class=ec2.InstanceClass.STANDARD5,
                instance_size=ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=compute_vpc.vpc,
            instance_name="time_api_host",
            private_ip_address="10.0.0.27",
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
        )
