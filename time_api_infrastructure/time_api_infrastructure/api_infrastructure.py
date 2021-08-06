from aws_cdk import(
    core as cdk,
    aws_ec2 as ec2,
    aws_iam as iam
)

from typing import Optional
from time_api_infrastructure.user_data_tooling import generate_user_data

# If no other specs are provided, these will be
# used
DEFAULT_MACHINE_SPECS = ec2.InstanceType.of(
    instance_class=ec2.InstanceClass.BURSTABLE3,
    instance_size=ec2.InstanceSize.MEDIUM
)

class APIInfrastructure(cdk.Construct):
    def __init__(self, scope: cdk.Construct,
                 construct_id: str,
                 vpc: ec2.Vpc,
                 instance_ip: str,
                 machine_specs: Optional[ec2.InstanceType] = None,
                 **kwargs) -> None:
        """Defines primarily an ec2 instance which hosts the api application 
        and produces associated relationships/permissions/resources.

        Args:
            scope (cdk.Construct): The surrounding scope.
            construct_id (str): The CDK id of the object.
            vpc (ec2.Vpc): The existing VPC to place this instance into.
            instance_ip (str): The private IP for this instance.
            machine_specs (Optional[ec2.InstanceType], optional): Manually specify the 
            specs of the instance. Defaults to t3.medium.
        """

        # Super constructor
        super().__init__(scope, construct_id, **kwargs)

        # Establish default machine specs
        if not machine_specs:
            machine_specs = DEFAULT_MACHINE_SPECS

        # Generate user data for injection into ec2 instance
        # Configure user data
        prefix = "api_setup_scripts/"
        scripts = list(map(lambda x: prefix + x, [
            "setup_docker.sh",
            "setup_repo.sh",
            "app_env.sh",
            "launch_service.sh"
        ]))
        user_data = generate_user_data(scripts, logging=True)

        # We now have a vpc and a subnet inside it, we can now create the instance
        # which will automatically create the
        api_instance = ec2.Instance(
            scope=self,
            id="api_ec2_instance",
            instance_type=machine_specs,
            machine_image=ec2.MachineImage.latest_amazon_linux(
                # use the Amazon Linux AMI v2
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
            ),
            vpc=vpc,
            instance_name="time_api_host",
            private_ip_address=instance_ip,
            # Links to public subnets on this vpc (might need to adjust
            # if there are multiple subnets on your vpc)
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            user_data=user_data,
            user_data_causes_replacement=True
        )

        # Expose for collecting variables
        self.instance = api_instance

        # Setup access for SSM
        api_instance.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore")
        )

        # Establish an Elastic IP
        self.eip = ec2.CfnEIP(
            scope=self,
            id="apiEIP",
            instance_id=api_instance.instance_id
        )

        # Security policies
        # HTTP
        api_instance.connections.allow_from_any_ipv4(
            ec2.Port.tcp(8080), "App HTTP traffic.")
        # ICMP
        api_instance.connections.allow_from_any_ipv4(
            ec2.Port.icmp_ping(), "Ping health checks.")
