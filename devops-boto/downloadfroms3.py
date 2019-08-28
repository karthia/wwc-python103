import json
import boto3


def lambda_handler(event, context):
    # TODO implement

    sts_client = boto3.client('sts')

    assumed_role_object = sts_client.assume_role(
        RoleArn="<substitute iam role>",
        RoleSessionName="AssumeRoleSession1"
    )

    credentials = assumed_role_object['Credentials']

    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

    print("s3 resource created....\n")

    s3_resource.Object('<bucket name>', '<file name with prefix>').download_file(
        '<filename with path where file to be downloaded to>')

    print("s3 object downloaded....\n")

    with open('<file location in local, above mentioned>', 'r') as handle:
        parsed = json.load(handle)

    print("S3 object....\n")

    print(json.dumps(parsed, indent=4, sort_keys=True))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
