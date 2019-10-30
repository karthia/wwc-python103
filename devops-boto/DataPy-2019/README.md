# IAAS - Python Boto

## Fargate Cluster creation steps

Assumption: We have created IAM roles needed for Lambda function execution. We have substituted VPC, Subnets and Security groups in the function code. You need to substitute Cluster, ALB and Target Group names.

1. Lambda Service screen (No function)
2. Click on 'Create Function' button
3. Enter name for the function
4. Select Python 3.7 (latest as of today)
5. Select existing IAM role and Lambda execution role - FGCluster-role-5i0kuqu2
   - Note: IAM policy JSON is in the github repo. You can create your own if you wish and use it to create Lambda Function
    https://raw.githubusercontent.com/womenwhocoderichmond/wwc-python103/master/devops-boto/DataPy-2019/IAMRoles/LambdaExecRole-Policy.json
6. Click 'Create'
7. Lambda function will be created and it will open designer view
8. Go to Code section and paste the code from 
   - https://raw.githubusercontent.com/womenwhocoderichmond/wwc-python103/master/devops-boto/DataPy-2019/FargateLambdas/FGClusterLambda.py
9. Update Cluster, ALB and TG names in the placeholder. Follow the comments in the program
10. Click 'Save'
11. Click on the 'Test' button and create test event by giving Event Name. Click 'Create'
12. CLick on 'Test' again to test the lambda code. It will create Cluster, ALB and Targetgroup.
13. Open Cluster, ALB and Target Group in other tabs and verify if resources are created.
14. Click on 'Add Trigger' and select 'API Gateway'
15. Select 'Create New API' in the drop down for API
16. Select 'Open' for Security. Caution: In production, you should confure with security
17. Click 'Add'
18. You will go back to Designer view.
19. Now you can try to trigger the Lambda through API Gateway using CURL through in command line
    - curl -X POST --http1.1 <API Gateway URL>

