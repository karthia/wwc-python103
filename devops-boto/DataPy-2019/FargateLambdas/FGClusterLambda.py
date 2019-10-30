import json
import boto3
import os

#BOT_TOKEN = os.environ["BOT_TOKEN"]

## Instructions are given within ## comment. Please substitute values.
## You can also substitute subnets, security groups and vpc. But we have pre-populated for you to work in WWC AWS Account
## Caution: This cluster is wide open to internet traffic. In production, you should have more secured infrastructure

def lambda_handler(event, context):

    # Cluster and ALB function calls
    create_wwc_cluster()
    create_wwc_alb_tg()

    # Slack trigger or URL trigger;
    # case of Slack trigger, there will be challenge data so that slack can understans that API is executed successfully.
    # If it is triggered through CURL URL, Else part will be executed
    if "challenge" in event:
        return event["challenge"]
    else:
        return "200 OK"
    #return {
    #    'statusCode': 200,
    #    'body': json.dumps('Hello from Lambda!')
    #}

#Cluster Creation
def create_wwc_cluster():

    client = boto3.client('ecs')
    ## SUbstitute cluster name as you wish in the place holder <cluster name> ##
    response = client.create_cluster(clusterName='<Cluster Name>')

#ALB, Listener and Default TG creation orchestrator
def create_wwc_alb_tg():

    client = boto3.client('elbv2')

    # function call to create alb
    alb_arn = create_alb(client)

    # function call to create default tg
    tg_arn = create_wwc_dftg(client)

    # function call to create Listener to link ALB to default TG
    response = create_listener(client,tg_arn,alb_arn)

#ALB creation
def create_alb(client):

    ## Substitute ALB name as you wish in the placeholder <ALB Name> ##
    response = client.create_load_balancer(
    Name='<ALB Name>',
    Subnets=[
        'subnet-48fac014','subnet-4d3e3a63'
    ],
    SecurityGroups=[
        'sg-13d04a40','sg-0cd1292545de29b06'
    ],
    Scheme='internet-facing',
    Tags=[
        {
            'Key': 'ALBName',
            'Value': 'FG ALB'
        }
    ]
    )
    alb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
    return alb_arn

#Default Target Group Creation
def create_wwc_dftg(client):

    ## Substitute Default Target Group name as you wish in the placeholder <TG Name> ##
    response = client.create_target_group(
    Name='<TG Name>',
    Protocol='HTTP',
    Port=80,
    VpcId='vpc-24f2b85e',
    TargetType='ip'
    )
    tg_arn = response['TargetGroups'][0]['TargetGroupArn']
    return tg_arn

#ALB Listener Creation
def create_listener(client,tg_arn,alb_arn):

    response = client.create_listener(
    LoadBalancerArn=alb_arn,
    Protocol='HTTP',
    Port=8080,
    #SslPolicy='ELBSecurityPolicy-TLS-1-2-2017-01',
    #Certificates=[
    #   {
     #       'CertificateArn': 'xxxx'
     #   }
    #],
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': tg_arn
        }
    ]
    )
    return response
