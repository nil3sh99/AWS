# Overview

In this tutorial, you will learn how to use AWS Step Functions to design and run a serverless workflow that coordinates multiple AWS Lambda functions. AWS Lambda is a compute service that lets you run code without provisioning or managing servers.

In our example, you are a developer who has been asked to create a serverless application to automate handling of support tickets in a call center. While you could have one Lambda function call the other, you worry that managing all of those connections will become challenging as the call center application becomes more sophisticated. Plus, any change in the flow of the application will require changes in multiple places, and you could end up writing the same code over and over again.

To solve this challenge, you decide to use AWS Step Functions. Step Functions is a serverless orchestration service that lets you easily coordinate multiple Lambda functions into flexible workflows that are easy to debug and change. Step Functions will keep your Lambda functions free of additional logic by triggering and tracking each step of your application for you.



**What is an IAM role?**

An IAM role is an identity you can create that has specific permissions with credentials that are valid for short durations. Roles can be assumed by entities that you trust.

**Step 1:** Create an AWS Identity and Access Management (IAM) role

AWS IAM is a web service that helps you securely control access to AWS resources. In this step, you will create an IAM role that allows Step Functions to access Lambda.

When you select AWS Step Function for your role, a default permission policy is recommended in the "Add Permissions" step. Continue with that.

Name the role as "step_functions_basic_execution".

**Step 2:** Create a state machine and serverless workflow

Your first step is to design a workflow that describes how you want support tickets to be handled in your call center. Workflows describe a process as a series of discrete tasks that can be repeated again and again.

You are able to sit down with the call center manager to talk through best practices for handling support cases. Using the visual workflows in Step Functions as an intuitive reference, you define the workflow together.

Then, you will design your workflow in AWS Step Functions. Your workflow will call one AWS Lambda function to create a support case, invoke another function to assign the case to a support representative for resolution, and so on. It will also pass data between Lambda functions to track the status of the support case as it's being worked on.

Amazon States Language is a JSON-based, structured language used to define your state machine.

A sample code has been given for the step function describing the workflow.

{

  "Comment": "A simple AWS Step Functions state machine that automates a call center support session.",

  "StartAt": "Open Case",

  "States": {

    "Open Case": {

    "Type": "Task",

    "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",

    "Next": "Assign Case"

    },

    "Assign Case": {

    "Type": "Task",

    "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",

    "Next": "Work on Case"

    },

    "Work on Case": {

    "Type": "Task",

    "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",

    "Next": "Is Case Resolved"

    },

    "Is Case Resolved": {

    "Type": "Choice",

    "Choices": [

    {

    "Variable": "$.Status",

    "NumericEquals": 1,

    "Next": "Close Case"

    },

    {

    "Variable": "$.Status",

    "NumericEquals": 0,

    "Next": "Escalate Case"

    }

    ]

    },

    "Close Case": {

    "Type": "Task",

    "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",

    "End": true

    },

    "Escalate Case": {

    "Type": "Task",

    "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",

    "Next": "Fail"

    },

    "Fail": {

    "Type": "Fail",

    "Cause": "Engage Tier 2 Support."

    }

  }

}


If you see in this code, the "FUNCTION_NAME" is not defined yet, which means the lambda function logic is not written. It's a skeleton workflow of the process.

![](https://file+.vscode-resource.vscode-cdn.net/var/folders/2s/2gmbx6wd23gcz0_vm1kwhws40000gp/T/TemporaryItems/NSIRD_screencaptureui_zx0Lln/Screenshot%202024-07-14%20at%207.49.21%E2%80%AFAM.png?version%3D1720964967938)


Now these lambdas need definiton and we have to tell the step function how to work.

Go to Lambdas in your console. 

While creating Lambda functions, we get following three options to deploy the logic in the function: 

* Author, write from scratch
* Blueprint, write from template
* Container Image

Furthermore, in the advanced settings, you also get an option to connect this lambda function with a VPC network (to access private resources during invocation), Enable tags, etc.

**NOTE: Make sure to deploy the lambda function when you write code in there.**

The logic for this example is written in node.js

**OpenCase code:**

exports.handler = (event, context, callback) => {    

    // Assign the support case and update the status message

    var myCaseID = event.Case;

    var myMessage = event.Message + "open case...";

    var result = {Case: myCaseID, Message: myMessage};

    callback(null, result);

};

**AssignCase code:**

exports.handler = (event, context, callback) => {    

    // Assign the support case and update the status message

    var myCaseID = event.Case;

    var myMessage = event.Message + "assigned...";

    var result = {Case: myCaseID, Message: myMessage};

    callback(null, result);

};

**WorkOnCaseFunction code:**

exports.handler = (event, context, callback) => {    

    // Generate a random number to determine whether the support case has been resolved, then return that value along with the updated message.

    var min = 0;

    var max = 1;

    var myCaseStatus = Math.floor(Math.random() * (max - min + 1)) + min;

    var myCaseID = event.Case;

    var myMessage = event.Message;

    if (myCaseStatus == 1) {

    // Support case has been resolved

    myMessage = myMessage + "resolved...";

    } else if (myCaseStatus == 0) {

    // Support case is still open

    myMessage = myMessage + "unresolved...";

    }

    var result = {Case: myCaseID, Status : myCaseStatus, Message: myMessage};

    callback(null, result);

};


**CloseCaseFunction code:**

exports.handler = (event, context, callback) => { 

    // Close the support case

    var myCaseStatus = event.Status;

    var myCaseID = event.Case;

    var myMessage = event.Message + "closed.";

    var result = {Case: myCaseID, Status : myCaseStatus, Message: myMessage};

    callback(null, result);

};

**EscalateCaseFunction code:**

exports.handler = (event, context, callback) => {    

    // Escalate the support case

    var myCaseID = event.Case;

    var myCaseStatus = event.Status;

    var myMessage = event.Message + "escalating.";

    var result = {Case: myCaseID, Status : myCaseStatus, Message: myMessage};

    callback(null, result);

};

**NOTE: Make sure to deploy the lambda function when you write code in there.**


Now go back to your StepFunction, and update the ARNs of the lambdas, it should look something like this:

{

  "Comment": "A simple AWS Step Functions state machine that automates a call center support session.",

  "StartAt": "Open Case",

  "States": {

    "Open Case": {

    "Type": "Task",

    "Resource": "arn:aws:lambda:ca-central-1:507638485545:function:OpenCaseFunction",

    "Next": "Assign Case"

    },

    "Assign Case": {

    "Type": "Task",

    "Resource": "arn:aws:lambda:ca-central-1:507638485545:function:AssignCaseFunction",

    "Next": "Work on Case"

    },

    "Work on Case": {

    "Type": "Task",

    "Resource": "arn:aws:lambda:ca-central-1:507638485545:function:WorkOnCaseFunction",

    "Next": "Is Case Resolved"

    },

    "Is Case Resolved": {

    "Type": "Choice",

    "Choices": [

    {

    "Variable": "$.Status",

    "NumericEquals": 1,

    "Next": "Close Case"

    },

    {

    "Variable": "$.Status",

    "NumericEquals": 0,

    "Next": "Escalate Case"

    }

    ]

    },

    "Close Case": {

    "Type": "Task",

    "Resource": "arn:aws:lambda:ca-central-1:507638485545:function:CloseCaseFunction",

    "End": true

    },

    "Escalate Case": {

    "Type": "Task",

    "Resource": "arn:aws:lambda:ca-central-1:507638485545:function:EscalateCaseFunction",

    "Next": "Fail"

    },

    "Fail": {

    "Type": "Fail",

    "Cause": "Engage Tier 2 Support."

    }

  }

}


**Step 5: Execute your workflow**

Your serverless workflow is now ready to be executed. A state machine execution is an instance of your workflow, and occurs each time a Step Functions state machine runs and performs its tasks. Each Step Functions state machine can have multiple simultaneous executions, which you can initiate from the Step Functions console (which is what you will do next), or by using AWS SDKs, Step Functions API actions, or the AWS CLI. An execution receives JSON input and produces JSON output.
