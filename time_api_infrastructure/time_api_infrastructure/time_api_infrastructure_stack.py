from aws_cdk import(
    core as cdk,
    aws_ec2 as ec2,
)
from database_infrastructure import DatabaseInfrastructure

from time_api_infrastructure.vpc import ComputeVPC
from time_api_infrastructure.api_infrastructure import APIInfrastructure
from time_api_infrastructure.static_website import StaticWebsite


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

        # Create DB infrastructure
        db_infrastructure = DatabaseInfrastructure(
            self,
            "db_infrastructure",
            compute_vpc.vpc,
            "10.0.0.28"
        )

        # Create the static website hosting
        time_demo_website_name = "timedemo"
        demo_website = StaticWebsite(
            scope=self,
            construct_id="time_demo_website",
            website_name=time_demo_website_name
        )

        """
        =======
        OUTPUTS
        =======
        """
        # Grab the public ip address of the api EC2 instance
        self.api_ip_output = cdk.CfnOutput(
            self,
            "api_pub_ip_output",
            export_name="apiPublicAddress",
            value=api_infrastructure.instance.instance_public_ip
        )

        # Grab the public ip address of the db EC2 instance
        self.db_ip_output = cdk.CfnOutput(
            self,
            "db_pub_ip_output",
            export_name="dbPublicAddress",
            value=db_infrastructure.instance.instance_public_ip
        )

        # can know where to send the files
        self.bucket_name_output = cdk.CfnOutput(
            scope=self,
            id=time_demo_website_name + "_bucket_name",
            value=demo_website.bucket.bucket_name,
            export_name=time_demo_website_name + "-bucket-name"
        )

        # Export the SSM instance ID for debugging connection
        self.api_instance_id = cdk.CfnOutput(
            self,
            "api_instance_id_output",
            export_name="apiInstanceId",
            value=api_infrastructure.instance.instance_id
        )
