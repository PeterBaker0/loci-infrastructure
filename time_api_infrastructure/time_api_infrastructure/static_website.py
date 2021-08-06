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
        
        # Let's 
