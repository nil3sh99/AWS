# Overview

In this tutorial, you use CodePipeline to deploy code maintained in a CodeCommit repository to a single Amazon EC2 instance. Your pipeline is triggered when you push a change to the CodeCommit repository. The pipeline deploys your changes to an Amazon EC2 instance using CodeDeploy as the deployment service.



The pipeline has two stages:

A source stage (Source) for your CodeCommit source action.

A deployment stage (Deploy) for your CodeDeploy deployment action.

## Tutorial - 1 Steps

Objective:

I want to use the wizard to create a pipeline that uses CodeDeploy to deploy a sample application from an Amazon S3 bucket to Amazon EC2 instances running Amazon Linux. After using the wizard to create my two-stage pipeline, I want to add a third stage.

Steps involved:

1. Create an S3 storage bucket for the application (use sample windows application)
2. Create Amazon EC2 Windows instances and install the CodeDeploy agent
3. Create an application in CodeDeploy
   1. Create a deployment group in CodeDeploy
4. Create pipeline in CodePipeline
   1. Choose pipeline version type (only v2 are available to create from console now)
   2. Service role
      1. Create new service role OR
      2. Use an existing service role
   3. Add Source Stage
      1. Source provider
         1. In this case, because our application code lives in S3, so select AWS S3
         2. In cases where the code lives in CodeCommit, you have to select CodeCommit
   4. Change detection options allows the CodePipeline to use Amazon CloudWatch events to detect changes in the source bucket
   5. Skip the build stage
   6. Add deploy stage and choose CodeDeploy
      1. Select the application name as the application you created in step 3 and choose the deployment group that was created in step 3
   7. Create pipeline
5. Add another stage to the pipeline

## Tutorial - 2 Steps

**Step 1: Create a CodeCommit repository**

After creating a CodeCommit repository, a local repo in GitHub, GitLab is also created which is integrated with CodeCommit for update and pushing the code changes.

CodeCommit is a regional resource.

Now if you are logging into the account as a federated user, then CodeCommit won't allow the SSH option and AWS CLI manager is the only available option that users have. 

Workaround -> Create a new IAM user and assign required permissions (individually or better if a group exists) to that user.

Permission required: **AWSCodeCommitPowerUser**

Use these credentials to login as an IAM user instead of a federated user. 

Instructions -> https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-gc.html?icmpid=docs_acc_console_connect_np 

CodeCommit repo is cloned in this repo with name = MyDemoRepo
