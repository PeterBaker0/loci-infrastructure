
from aws_cdk import(
    core as cdk,
    aws_ec2 as ec2,
    aws_route53 as r53
)

from typing import Optional

# How long should the dns leases last, by default?
DEFAULT_TTL = cdk.Duration.minutes(15)


class DynamicIPMapping(cdk.Construct):
    def __init__(self, scope: cdk.Construct,
                 construct_id: str,
                 zone_domain_name: str,
                 hosted_zone_id: str,
                 **kwargs) -> None:
        """A construct which enables the dynamic subscription 
        of ec2 instances with elastic IPs and statically hosted 
        s3 buckets to a route53 hosted zone. 

        Args:
            scope (cdk.Construct): The surrounding CDK object.
            construct_id (str): The CDK id.
            zone_domain_name (str): The name of the hosted zone (domain name)
            hosted_zone_id (str): The hosted zone id (fixed)
        """

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
                     id: str,
                     domain_prefix: str,
                     target_eip: ec2.CfnEIP,
                     comment: Optional[str] = None,
                     route_ttl: Optional[str] = DEFAULT_TTL):
        """Given some information, links the elastic IP of an ec2 instance 
        to a specified domain prefix on the given hosted zone. 

        Args:
            id (str): The CDK id of the record you are creating (your choice)
            domain_prefix (str): The prefix (including the full stop) of the 
            target e.g. if you want api.example.com and the domain is example.com, 
            you should include "api."
            target_eip (ec2.CfnEIP): The elastic IP associated to the ec2 instance.
            comment (Optional[str], optional): A comment to tie to the record. 
            Defaults to None.
            route_ttl (Optional[str], optional): The time to live of the DNS result.
            Defaults to DEFAULT_TTL.
        """
        # Adds a new record to the hosted zone (or updates current one)
        r53.ARecord(
            scope=self,
            id=id,
            zone=self.hz,
            record_name=domain_prefix + self.zone_domain_name,
            comment=comment,
            ttl=route_ttl,
            # This is the only way to get the elastic IP to resolve
            # properly - no idea why this works?
            # I think cloud formation is BTS resolving the reference to the
            # newest IP. If you use the public_ip field of the ec2 instance, it is
            # not usually correct.
            target=r53.RecordTarget.from_ip_addresses(target_eip.ref)
        )

    def add_static_website(self,
                           id: str,
                           unqualified_bucket_name: str,
                           comment: Optional[str] = None,
                           route_ttl: Optional[str] = DEFAULT_TTL,
                           region: Optional[str] = "ap-southeast-2"):
        """Links a static s3 bucket website to the provided hosted zone.

        Args:
            id (str): The CDK id of the record (your choice)
            unqualified_bucket_name (str): The name of the bucket itself (without domain info.) E.g.
            if you had a bucket named api but it was part of the domain my.app.com just provide 
            api, even though the bucket's full name was forced to be api.my.app.com.
            comment (Optional[str], optional): Comment for the record. Defaults to None.
            route_ttl (Optional[str], optional): Time to live of DNS record. Defaults to DEFAULT_TTL.
            region (Optional[str], optional): The bucket region. Defaults to "ap-southeast-2".
        """

        # Work out the full qualified domain name
        full_domain_target = f"{unqualified_bucket_name}.{self.zone_domain_name}.s3-website-{region}.amazonaws.com"

        # Name of the record (desired URL) must be the qualified bucket name
        record_name = f"{unqualified_bucket_name}.{self.zone_domain_name}"

        # Create the record
        r53.CnameRecord(
            scope=self,
            id=id,
            domain_name=full_domain_target,
            record_name=record_name,
            ttl=route_ttl,
            zone=self.hz,
            comment=comment
        )
