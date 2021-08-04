from aws_cdk import(
    core as cdk,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_s3 as s3,
    aws_secretsmanager as sm
)

from typing import Optional

DEFAULT_MACHINE_SPECS = ec2.InstanceType.of(
    instance_class=ec2.InstanceClass.BURSTABLE3,
    instance_size=ec2.InstanceSize.MEDIUM
)

BACKUP_ARN = "arn:aws:s3:::loci-change-over-time-db-backup"
DATABASE_SECRET_NAME = "loci-time-demo-db-password"


def file_to_commands(file_path):
    return open(file_path, 'r').read().splitlines()


def generate_user_data(logging: bool = True):
    # Configure user data
    prefix = "db_setup_scripts/"
    scripts = list(map(lambda x : prefix + x, [
        "retrieve_backup.sh",
        "db_password.sh",
        "setup_db.sh",
        "launch_db.sh"
    ]))

    # We want to execute in bash
    bang = "#!/bin/bash -xe"

    # And log everything to /dev/console and /var/log/user-data.log
    # from https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-log-user-data/
    logging_header = "exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1"

    # Generate a list of commands from combining setup files
    combined = list(
        map(lambda f: str(open(f, 'r').read()), scripts))
    combined.insert(0, bang)

    # Inject logging header if required
    if logging:
        combined.insert(1, logging_header)

    data = "\n".join(combined)

    # Return the created user data instance
    return ec2.UserData.custom(data)


class DatabaseInfrastructure(cdk.Construct):
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
        db_eip = ec2.CfnEIP(
            scope=self,
            id="dbEIP",
            instance_id=db_instance.instance_id
        )

        # Update the route53 record to reflect the elastic IP output
        # zone=r53.
        # r53.ARecord(self, ""

        # Security policies
        # TCP port 5432 for PG from everywhere
        db_instance.connections.allow_from(
            ec2.Peer.ipv4("0.0.0.0/0"),
            ec2.Port.tcp(5432)
        )

        # ICMP
        db_instance.connections.allow_from_any_ipv4(
            ec2.Port.icmp_ping(), "Ping health checks.")

        # Let's create a database password and store it as a secret
        db_password_secret = sm.Secret(
            scope = self,
            id = "db_password_secret", 
            description = "Password dynamically generated to enable access to the loci time demo DB.",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            secret_name=DATABASE_SECRET_NAME
        )
        
        # We now have read access for the db instance, meaning its user 
        # data scripting can pull the secret and update the password 
        db_password_secret.grant_read(db_instance.grant_principal)
