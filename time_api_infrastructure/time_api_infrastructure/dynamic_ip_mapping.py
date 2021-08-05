
from aws_cdk import(
    core as cdk,
    aws_route53 as r53
)

from typing import Optional

DEFAULT_TTL = cdk.Duration.minutes(15)

class DynamicIPMapping(cdk.Construct):
    def __init__(self, scope: cdk.Construct,
                 construct_id: str,
                 hosted_zone_id: str,
                 zone_domain_name: str,
                 full_domain_name: str,
                 ip: str,
                 route_ttl: Optional[cdk.Duration] = DEFAULT_TTL,
                 route_comment: Optional[str] = None,
                 **kwargs) -> None:

        # Super constructor
        super().__init__(scope, construct_id, **kwargs)

        # Pull the existing Hosted Zone based on the hosted_zone_id
        hz = r53.PublicHostedZone.from_hosted_zone_attributes(
            scope=self,
            id=construct_id + "_hz",
            hosted_zone_id=hosted_zone_id,
            zone_name=zone_domain_name
        )

        # Adds a new record to the existing hosted zone (or updates current one)
        record = r53.ARecord(
            scope=self,
            id=construct_id + "_a_record",
            zone=hz,
            record_name=full_domain_name,
            comment=route_comment,
            target=r53.RecordTarget.from_ip_addresses(ip),
            ttl=route_ttl
        )
