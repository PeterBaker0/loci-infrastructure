from aws_cdk import(
    core as cdk,
    aws_s3 as s3
)

class StaticWebsite(cdk.Construct):
    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 website_name: str,
                 **kwargs) -> None:
        """Produces the resources required for a static 
        website hosting. This is just an s3 bucket with the
        appropriate permissions.

        Args:
            scope (cdk.Construct): The CDK scope.
            construct_id (str): The CDK id of this construct.
            website_name (str): The full name of the bucket which 
            should include the full domain e.g. if you want your 
            bucket to be for an api, on the subdomain example.com, 
            you could have a target url of api.subdomain.example. You 
            should name the bucket whatever the domain is, e.g. the bucket
            should be "api.subdomain.example". 
        """

        # Super constructor
        super().__init__(scope, construct_id, **kwargs)

        # Let's make an s3 bucket
        self.bucket = s3.Bucket(
            self,
            id="static_website_bucket_" + website_name,
            bucket_name=website_name,
            public_read_access=True,
            website_index_document="index.html",

            # Make sure bucket is cleaned up when the stack is
            # destroyed
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )
