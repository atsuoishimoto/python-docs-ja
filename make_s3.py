import boto3
import json

bucket_name = "test-pythondoc-ja-cloude1"
region = "ap-northeast-1"
index_document = "index.html"

s3 = boto3.client("s3", region_name=region)

s3.create_bucket(
    Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": region}
)

s3.put_public_access_block(
    Bucket=bucket_name,
    PublicAccessBlockConfiguration={
        "BlockPublicAcls": False,
        "IgnorePublicAcls": False,
        "BlockPublicPolicy": False,
        "RestrictPublicBuckets": False,
    },
)

policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*",
        }
    ],
}

s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))

s3_website = boto3.client("s3", region_name=region)
s3_website.put_bucket_website(
    Bucket=bucket_name,
    WebsiteConfiguration={"IndexDocument": {"Suffix": index_document}},
)

print(f"http://{bucket_name}.s3-website-{region}.amazonaws.com")
