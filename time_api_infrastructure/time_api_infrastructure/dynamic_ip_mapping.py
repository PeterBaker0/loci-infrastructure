
from aws_cdk import(
    core as cdk,
    aws_ec2 as ec2,
    aws_route53 as r53
)

from typing import Optional

DEFAULT_TTL = cdk.Duration.minutes(15)


class DynamicIPMapping(cdk.Construct):
    def __init__(self, scope: cdk.Construct,
                 construct_id: str,
                 zone_domain_name: str,
                 hosted_zone_id: str,
                 **kwargs) -> None:

        # Super constructor
        super().__init__(scope, construct_id, **kwargs)

        # Save some variables
        self.zone_domain_name = zone_domain_name

        # Pull the existing Hosted Zone based on the hosted_zone_id
        self.hz = r53.PublicHostedZone.from_hosted_zone_attributes(
            scope=self,
            id=construct_id + "_hosted_zone",
            hosted_zone_id=hosted_zone_id,
            zone_name=zone_domain_name
        )

    def add_instance(self,
                     id,
                     domain_prefix: str,
                     target_eip: ec2.CfnEIP,
                     comment: Optional[str] = None,
                     route_ttl: Optional[str] = DEFAULT_TTL):
        # Adds a new record to the hosted zone (or updates current one)
        record = r53.ARecord(
            scope=self,
            id=id,
            zone=self.hz,
            record_name=domain_prefix + self.zone_domain_name,
            comment=comment,
            ttl=route_ttl,
            # This is the only way to get the elastic IP to resolve
            # properly - no idea why this works?
            target=r53.RecordTarget.from_ip_addresses(target_eip.ref)
        )

    def add_static_website(self,
                           id: str,
                           unqualified_bucket_name: str,
                           comment: Optional[str] = None,
                           route_ttl: Optional[str] = DEFAULT_TTL,
                           region: Optional[str] = "ap-southeast-2"):
        
        # Work out the full qualified domain name
        full_domain_target = f"{unqualified_bucket_name}.{self.zone_domain_name}.s3-website-{region}.amazonaws.com"
        
        # Name of the record (desired URL) must be the qualified bucket name
        record_name = f"{unqualified_bucket_name}.{self.zone_domain_name}"
        
        # Create the record
        record = r53.CnameRecord(
            scope=self, 
            id=id,
            domain_name=full_domain_target,
            record_name=record_name,
            ttl=route_ttl,
            zone=self.hz, 
            comment=comment
        ) 
        
