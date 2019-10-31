import json
import boto3

def lambda_handler(event, context):

    # Describe listener
    service_orchestrater()
    #create_wwc_alb_tg()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def service_orchestrater():

    client = boto3.client('elbv2')

    # Create Target Group with health check
    tg_arn = create_wwc_tg(client)
    print (tg_arn)

    # Describe ALB by using ALB name
    alb_arn = describe_alb(client)
    print(alb_arn)

    # Describe Listener by using ALB Arn
    listener_arn = describe_listener(client,alb_arn)
    print(listener_arn)

    response = create_listener_rule(client,listener_arn,tg_arn)
    print(response)

    ecsclient = boto3.client('ecs')
    task_def_arn = register_task_def(ecsclient)
    print(task_def_arn)

    create_service(ecsclient,alb_arn,tg_arn,task_def_arn)

#Target Group Creation
def create_wwc_tg(client):

    ## Substite values
    response = client.create_target_group(
    Name='<Substitute your TG name>',
    Protocol='HTTP',
    Port=80,
    VpcId='vpc-24f2b85e',
    TargetType='ip',
    HealthCheckProtocol='HTTP',
    HealthCheckPort='80',
    HealthCheckEnabled=True,
    HealthCheckPath='/index.html',
    HealthCheckIntervalSeconds=56,
    HealthCheckTimeoutSeconds=55,
    HealthyThresholdCount=2,
    UnhealthyThresholdCount=4,
    Matcher={
        'HttpCode': '200-299'
    }
    )
    tg_arn = response['TargetGroups'][0]['TargetGroupArn']
    return tg_arn

#Describe ALB
def describe_alb(client):

    ## Substitute values
    alb_response = client.describe_load_balancers(
    Names=[
        '<Substitute ALB name that you used in Cluster creation section>'
    ]
    )
    alb_arn = alb_response['LoadBalancers'][0]['LoadBalancerArn']
    return alb_arn

#Describe Listener
def describe_listener(client,alb_arn):
    listener_response = client.describe_listeners(
    LoadBalancerArn=alb_arn
    )
    listener_arn = listener_response['Listeners'][0]['ListenerArn']
    return listener_arn

#ALB Listener Rule Creation
def create_listener_rule(client,listener_arn,tg_arn):
    response = client.create_rule(
    ListenerArn=listener_arn,
    Conditions=[
        {
            'Field': 'path-pattern',
            'Values': [
                '/index*',
            ]
        }
    ],
    Priority=1,
    Actions=[
        {
            'Type': 'forward',
            'TargetGroupArn': tg_arn
        }
    ]
    )
    return response

#Register task definition
def register_task_def(ecsclient):

    ## Substitute Values Carefully. multiple places
    response =  ecsclient.register_task_definition(
    family='<Substitute service name as you wish>',
    taskRoleArn='arn:aws:iam::896599253871:role/FargateRole',
    executionRoleArn='arn:aws:iam::896599253871:role/FargateRole',
    networkMode='awsvpc',
    containerDefinitions=[
        {
            'name': '<service name as mentioned above>',
            'image': '896599253871.dkr.ecr.us-east-1.amazonaws.com/wwc-python:v1',
            'cpu': 128,
            'memory': 1024,
            'memoryReservation': 512,
            'portMappings': [
                {
                    'containerPort': 80,
                    'protocol': 'tcp'
                }
            ],
            'essential': True,
            'environment': [
                {
                    'name': 'SERVICE_NAME',
                    'value': '<put same service name you mentioned above>'
                }
            ]
        }
    ],
    requiresCompatibilities=[
        'FARGATE'
    ],
    cpu='1024',
    memory='2048',
    tags=[
        {
            'key': 'Task',
            'value': '<taskname as your wish>'
        },
        {
            'key': 'Contact',
            'value': '<Your name or something that you can understand>'
        }
    ]
    )
    return response['taskDefinition']['taskDefinitionArn']

#Create Service
def create_service(client,alb_arn,tg_arn,task_def_arn):
    print("create service called....")
    response = client.create_service(
    cluster='<Cluster name from last lambda>',
    serviceName='<Service name from above>',
    taskDefinition=task_def_arn,
    loadBalancers=[
        {
            'targetGroupArn': tg_arn,
            'containerName': '<same as service>',
            'containerPort': 80
        }
    ],
    desiredCount=1,
    launchType='FARGATE',
    deploymentConfiguration={
        'maximumPercent': 200,
        'minimumHealthyPercent': 50
    },
    networkConfiguration={
        'awsvpcConfiguration': {
            'subnets': [
                'subnet-4d3e3a63','subnet-48fac014'
            ],
            'securityGroups': [
                'sg-13d04a40','sg-0cd1292545de29b06'
            ],
            'assignPublicIp': 'ENABLED'
        }
    }
)
