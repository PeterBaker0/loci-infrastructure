from aws_cdk import(
    core as cdk,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_s3 as s3,
    aws_secretsmanager as sm
)

from typing import Optional
from time_api_infrastructure.user_data_tooling import generate_user_data

# If no other specs are provided, these will be
# used
DEFAULT_MACHINE_SPECS = ec2.InstanceType.of(
    instance_class=ec2.InstanceClass.BURSTABLE3,
    instance_size=ec2.InstanceSize.MEDIUM
)

# Specifies the locatino of the s3 bucket which holds
# the backed up PG database contents. This could take a
# while to restore on the instance if the data is moved
# into cold storage (after 90 days.)
BACKUP_ARN = "arn:aws:s3:::loci-change-over-time-db-backup"

# This is the secret key for the password which will be
# generated
DATABASE_SECRET_NAME = "loci-time-demo-db-password"


class DatabaseInfrastructure(cdk.Construct):
    def __init__(self, scope: cdk.Construct,
                 construct_id: str,
                 vpc: ec2.Vpc,
                 vpc_base_ip: str,
                 vpc_subnet_mask: str,
                 instance_ip: str,
                 machine_specs: Optional[ec2.InstanceType] = None,
                 **kwargs) -> None:

        # Super constructor
        super().__init__(scope, construct_id, **kwargs)

        # Establish default machine specs
        if not machine_specs:
            machine_specs = DEFAULT_MACHINE_SPECS

        # Generate user data for injection into ec2 instance
        # Configure user data
        prefix = "db_setup_scripts/"
        scripts = list(map(lambda x: prefix + x, [
            "retrieve_backup.sh",
            "db_password.sh",
            "setup_db.sh",
            "launch_db.sh"
        ]))
        user_data = generate_user_data(scripts, logging=True)

        # We now have a vpc and a subnet inside it, we can now create the instance
        # which will automatically create the EC2 and run appropriate scripting
        db_instance = ec2.Instance(
            scope=self,
            id="db_ec2_instance",
            instance_type=machine_specs,
            machine_image=ec2.MachineImage.lookup(
                name="ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20210223"
            ),
            vpc=vpc,
            instance_name="time_demo_db",
            private_ip_address=instance_ip,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            user_data=user_data,
            user_data_causes_replacement=True
        )

        # Expose for collecting variables
        self.instance = db_instance

        # Setup access for SSM
        db_instance.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore")
        )

        # Get the backup bucket
        backup_bucket = s3.Bucket.from_bucket_arn(self, "db_backup_bucket",
                                                  BACKUP_ARN)

        # Allow the instance to read from the bucket with its
        # implicit credentials
        # It will do the downloading when its ready in the script
        backup_bucket.grant_read(db_instance.grant_principal)

        # Establish an Elastic IP
        self.eip = ec2.CfnEIP(
            scope=self,
            id="dbEIP",
            instance_id=db_instance.instance_id
        )

        # Security policies

        CSIRO_IP_CIDRS = [
            ("140.79.0.0", 16),
            ("130.155.0.0", 16),
            ("152.83.0.0", 16),
            ("138.194.0.0", 16),
            ("140.253.0.0", 16),
            ("144.110.0.0", 16),
            ("130.116.0.0", 16)
        ]

        # Enable TCP on 5432 for CSIRO IP addresses
        PG_PORT = 5432
        for ip, mask in CSIRO_IP_CIDRS:
            db_instance.connections.allow_from(
                ec2.Peer.ipv4(str(ip) + "/" + str(mask)),
                ec2.Port.tcp(PG_PORT)
            )

        # Enable traffic within subnet of VPC
        db_instance.connections.allow_from(
            ec2.Peer.ipv4(f"{vpc_base_ip}/{vpc_subnet_mask}"),
            ec2.Port.tcp(PG_PORT)
        )

        # ICMP
        db_instance.connections.allow_from_any_ipv4(
            ec2.Port.icmp_ping(), "Ping health checks.")

        secret_generator = sm.SecretStringGenerator(
            include_space=False,
            exclude_punctuation=True,
            password_length=30,
            require_each_included_type=True
        )

        # Let's create a database password and store it as a secret
        self.db_password_secret = sm.Secret(
            scope=self,
            id="db_password_secret",
            description="Password dynamically generated to enable access to the loci time demo DB.",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            secret_name=DATABASE_SECRET_NAME,
            generate_secret_string=secret_generator
        )

        # We now have read access for the db instance, meaning its user
        # data scripting can pull the secret and update the password
        self.db_password_secret.grant_read(db_instance.grant_principal)
