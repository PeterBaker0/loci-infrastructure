from aws_cdk import(
    core as cdk,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_route53 as r53
)

from typing import Optional

DEFAULT_MACHINE_SPECS = ec2.InstanceType.of(
    instance_class=ec2.InstanceClass.BURSTABLE3,
    instance_size=ec2.InstanceSize.MEDIUM
)


def file_to_commands(file_path):
    return open(file_path, 'r').read().splitlines()


def generate_user_data(logging: bool = True):
    # Configure user data
    commands = [
        "setup_scripts/setup_docker.sh",
        "setup_scripts/setup_repo.sh",
        "setup_scripts/launch_service.sh"
    ]

    # We want to execute in bash
    bang = "#!/bin/bash -xe"

    # And log everything to /dev/console and /var/log/user-data.log
    # from https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-log-user-data/
    logging_header = "exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1"

    # Generate a list of commands from combining setup files
    combined = list(
        map(lambda f: str(open(f, 'r').read()), commands))
    combined.insert(0, bang)

    # Inject logging header if required
    if logging:
        combined.insert(1, logging_header)

    data = "\n".join(combined)

    # Return the created user data instance
    return ec2.UserData.custom(data)


class APIInfrastructure(cdk.Construct):
    def __init__(self, scope: cdk.Construct,
                 construct_id: str,
                 vpc: ec2.Vpc,
                 instance_ip: str,
                 machine_specs: Optional[ec2.InstanceType] = None,
                 **kwargs) -> None:

        # Super constructor
        super().__init__(scope, construct_id, **kwargs)

        # Establish default machine specs
        if not machine_specs:
            machine_specs = DEFAULT_MACHINE_SPECS

        # Generate user data for injection into ec2 instance
        user_data = generate_user_data(logging=True)

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
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            # init=api_cfn_config,
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
        app_eip = ec2.CfnEIP(
            scope=self,
            id="apiEID",
            instance_id=api_instance.instance_id
        )

        # Update the route53 record to reflect the elastic IP output
        # zone=r53.
        # r53.ARecord(self, ""

        # Security policies
        # HTTP
        api_instance.connections.allow_from_any_ipv4(
            ec2.Port.tcp(8080), "App HTTP traffic.")
        # ICMP
        api_instance.connections.allow_from_any_ipv4(
            ec2.Port.icmp_ping(), "Ping health checks.")
