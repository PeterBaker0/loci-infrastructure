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

        # Let's setup the inbound rules to enable API hosting on this IP/port
        api_hosting_group = ec2.SecurityGroup(
            scope=self,
            id="time_api_hosting_group",
            vpc=compute_vpc.vpc,
            allow_all_outbound=True,
            description="Enables HTTP api communication on port 8080.",
            security_group_name="time_api_hosting_group"
        )

        api_hosting_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(8080),
            description="Enable HTTP connection through TCP on port 8080 and SSH on 22."
        )

        api_hosting_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.icmp_ping(),
            description="Enable ping responses."
        )
        
        api_hosting_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="Enable SSH access."
        )

        ## Create a restart handle
        restart_handle = ec2.InitServiceRestartHandle()

        ## Let's create a cloud formation init script
        api_setup_config = ec2.InitConfig(
            [
                # Pull the integration api source code
                ec2.InitSource.from_git_hub(
                    target_directory="~/api_source/",
                    owner="CSIRO-enviro-informatics",
                    repo="loci-integration-api",
                    ref_spec="+refs/heads/master:refs/remotes/origin/timework"
                )])
        #        # Upload the docker setup file
        #        ec2.InitFile.from_file_inline(
        #            target_file_name="setup_docker.sh",
        #            source_file_name="setup_scripts/setup_docker.sh",
        #            mode="000555"  # Read and execute, no writing
        #        ),
        #        # Setup docker and docker-compose and restart
        #        ec2.InitCommand.shell_command(
        #            shell_command="./setup_docker.sh",
        #            service_restart_handles=[restart_handle]
        #        ),

        #        # Not yet confident on deployment strategy for
        #        # the main application, just move in for now
        #        ec2.InitCommand.shell_command(
        #            shell_command="cd ~/api_source/ && echo \"ready\"",
        #        )
        #    ]
        #)

        ## Setup the API ec2 instance with a custom setup script
        api_cfn_config = ec2.CloudFormationInit.from_config(api_setup_config)
        
        # SSH key name
        ssh_key_name = "loci-cdk-api-key"

        # We now have a vpc and a subnet inside it, we can now create the instance
        # which will automatically create the
        api_instance = ec2.Instance(
            scope=self,
            id="api_ec2_instance",
            instance_type=ec2.InstanceType.of(
                instance_class=ec2.InstanceClass.BURSTABLE3,
                instance_size=ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=compute_vpc.vpc,
            instance_name="time_api_host",
            private_ip_address="10.0.0.27",
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=api_hosting_group,
            init=api_cfn_config,
            key_name=ssh_key_name
        )
        
        # Not working since we don't have access to another VPC's security 
        # protocol
        # SSH CSIRO Group access
        #ssh_group_id = "sg-0edbeef80e6f3e977"
        #ssh_group = ec2.SecurityGroup.from_security_group_id(
        #    scope=self,
        #    id="CSIRO_ssh_group",
        #    security_group_id=ssh_group_id
        #)
        #api_instance.add_security_group(ssh_group)

        # Grab the public ip address of the EC2 instance
        self.api_ip_output = cdk.CfnOutput(
            self,
            "api_pub_ip_output",
            export_name="apiPublicAddress",
            value=api_instance.instance_public_ip
        )
