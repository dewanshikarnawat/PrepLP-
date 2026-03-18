import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="https://s3.us-west-002.backblazeb2.com",
    aws_access_key_id="00405c5ad4850b8000000000a",
    aws_secret_access_key="K004XXXXXXXXXXXXXXX",
    region_name="us-west-002",
)

s3.put_object(
    Bucket="Study-Material-Exchange",
    Key="boto3-test.txt",
    Body=b"hello"
)

print("UPLOAD OK")
