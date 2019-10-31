# IAAS - Python Boto

## Fargate Cluster creation steps:

Assumption: We have created IAM roles needed for Lambda function execution. We have substituted VPC, Subnets and Security groups in the function code. You need to substitute Cluster, ALB and Target Group names.

You have AWS console access for WWC account. Please login and select Lambda service.

1. Lambda Service screen (No function) will open
<img width="1360" alt="WWC-LambdaScreen" src="https://user-images.githubusercontent.com/53320397/67826779-1119e100-faa4-11e9-9b35-97eab3c7bb8e.png">

2. Click on 'Create Function' button
3. Enter name for the function
4. Select Python 3.7 (latest as of today)
5. Select existing IAM role and Lambda execution role - FGCluster-role-5i0kuqu2
   - Note: IAM policy JSON is in the github repo. You can create your own if you wish and use it to create Lambda Function
    https://raw.githubusercontent.com/womenwhocoderichmond/wwc-python103/master/devops-boto/DataPy-2019/IAMRoles/LambdaExecRole-Policy.json
6. Click 'Create'
7. Lambda function will be created and it will open designer view
<img width="1312" alt="WWC-LambdaFunction" src="https://user-images.githubusercontent.com/53320397/67826879-6d7d0080-faa4-11e9-8343-bea55f7850d7.png">

8. Go to Code section and paste the code from 
   - https://raw.githubusercontent.com/womenwhocoderichmond/wwc-python103/master/devops-boto/DataPy-2019/FargateLambdas/FGClusterLambda.py
9. Update Cluster, ALB and TG names in the placeholder. Follow the comments in the program
10. Click 'Save'
11. Click on the 'Test' button and create test event by giving Event Name. Click 'Create'
12. CLick on 'Test' again to test the lambda code. It will create Cluster, ALB and Targetgroup.
13. Open Cluster, ALB and Target Group in individual tabs and verify if resources are created.
14. Click on 'Add Trigger' and select 'API Gateway'
15. Select 'Create New API' in the drop down for API
16. Select 'Open' for Security. Caution: In production, you should confure with security
17. Click 'Add'
<img width="857" alt="WWC-APITrigger" src="https://user-images.githubusercontent.com/53320397/67827007-dd8b8680-faa4-11e9-82b2-a76b12d713e8.png">

18. You will go back to Designer view
19. Go to ALB tab and delete your ALB (Action > delete)
20. Go to TG tab and delete your TG (Action > delete)
21. Go to ECS and delete cluster
19. Now you can try to trigger the Lambda through API Gateway using CURL in command line or MAC terminal
    - curl -X POST --http1.1 "Add API Gateway URL from LAMbda function API Gateway section"
    
## Fargate Service creation and deployment steps:

Docker image is managed in AWS ECR. We use already existing image. We have used NGINX web server. ECR Docker image push and web application information is provided below. We have substituted vpc, subnets, security groups, IAM role and image URL. Please substitute Cluster name (the one you created in step 1), ALB name (the one you created in the Cluster step), TG name and Service name where you see placeholder like <Enter name>.

1. Go to Lambda function
2. Click 'Create Function' button and create function for service as mentioned in the Cluster section
3. Lambda designer view will open
4. Paste service code from the link in the code section
   - xxxxxx
5. Please substitute values as mentioned in the code
6. Click 'Save'
7. Click 'Test', create Test Event and test the function (as you did in the Cluster section.
8. This will create Service/task under the Cluster, Target group and ALB listener.
9. Go to ECS, click on the cluster. You will see Service.
10. Click on the service. You will see Target group name. Navigate to Task tab, you will see Task inrunning state. Navigate to Events tab, you will see event details. Finally, it should show task in steady state.
11. In details tab, click TG. TG will open in another tab. Go to targets. You will see service in healthy state.
12. From decription tab, look for ALB and click to open in another tab.
13. In ALB screen, go to listener tab. You will see newly created target group is a high priority one to which traffic is forwarded. This is the one pointing to the docker image (web application) that we deployed
14. Validate if you are able to access the web application through ALB
    - http://<Your ALB DNS from ALB screen>:8080/index.html
15. Now, all are looking good. Go to ALB > Listener, delete the TG listener that we created. Go To TG, delete the TG that we created. Go to ECS and delete the service (NOT the cluster).
16. Now create API gateway like we created for cluster.
17. You can trigger service creation and deployment using CURL from command line or Mac terminal.

## Web Application:
We have used NGINX server and simpler HTML application. Please refer to the Dockerfile and application detail here
- ......

## ECR repository creation and Image push:
###Prerequisite:
   Need Docker desktop and AWS CLI to create image and push the image to ECR. Need Credentials (Access Key ID and Access key) for your IAM user. Create token again and save it.
   IAM user's policy needs ecr:GetAuthorizationToken access to allow user to push image into ECR from local.

1. Use Windows Powershell or Mac terminal to run aws configure with user credential and get STS token for CLI access
2. Follow instructions below to push docker image to ECR.
   - https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html
3. For Docker image creation and docker resources. Visit: https://docs.docker.com/   
   



