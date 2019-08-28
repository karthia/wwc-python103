import json
import boto3


def lambda_handler(event, context):
    # TODO implement

    data = b'Object from S3'

    # Get sts client to connect to AWS using IAM role
    sts_client = boto3.client('sts')

    # Assume role for AWS connection
    assumed_role_object = sts_client.assume_role(
        RoleArn="<iam role arn>",                # create IAM role with access to S3 and use here
        RoleSessionName="AssumeRoleSession1"     # role session name
    )

    credentials = assumed_role_object['Credentials']

    # S3 resource connection
    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

    print("s3 resource connection....\n")

    # Upload object into S3 bucket
    bucket = s3_resource.Bucket('<Bucket Name>')  #put bucket name that already exist in S3

    bucket.put_object(
        Key='<S3 file key with folder/prefix path>',   #put file name with path
        Body=data,
        ServerSideEncryption='AES256'
    )

    print("s3 object uploaded....\n")

    # Read the above uploaded object from S3 and print
    s3_resource.Object('<Bucket name>', '<Key with folder/prefix path').download_file(
        '/tmp/data.txt')           # use same bucket name and Key from above

    print("s3 object downloaded....\n")

    print("S3 object....\n")

    print(open('/tmp/data.txt').read())

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
