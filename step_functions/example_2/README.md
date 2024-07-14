# Overview

In this tutorial, you will learn how to use AWS Step Functions to handle workflow runtime errors. AWS Step Functions is a serverless orchestration service that lets you easily coordinate multiple Lambda functions into flexible workflows that are easy to debug and easy to change. AWS Lambda is a compute service that lets you run code without provisioning or managing servers.

Lambda functions can occasionally fail, such as when an :

* unhandled exception is raised,
* when they run longer than the configured timeout, or
* when they run out of memory.

Writing and maintaining error-handling logic in every one of your Lambda functions to handle situations such as API throttling or socket timeouts can be time-intensive and complicated, especially for distributed applications. Embedding this code in each Lambda function creates dependencies between them, and it can be difficult to maintain all of those connections as things change.

To avoid this, and to reduce the amount of error-handling code you write, you can use AWS Step Functions to create a serverless workflow that supports function error handling. Regardless of whether the error is a function exception created by the developer (such as, file not found) or unpredicted (such as, out of memory), you can configure Step Functions to respond with conditional logic based on the type of error that occurred. By separating your workflow logic from your business logic in this way, you can modify how your workflow responds to errors without changing the business logic of your Lambda functions.

## Objectives

* design and run a serverless workflow using AWS Step Functions to handle errors
* create an AWS Lambda function, which will mock calls to a RESTful API and return various response codes and exceptions
* create a state machine with Retry and Catch capabilities that responds with different logic depending on the exception raised.

## Steps

Step 1: Create a Lambda Function to mock an API

The Lambda function raises exceptions to simulate responses from a fictitious API, depending on the error code that you provide as input in the event parameter.

Check the lambda_function.py file in this repo for the lambda function.

Step 2: Create an AWS Identity and Access Management (IAM) role

AWS Step Functions can run code and access other AWS resources (for example, data stored in Amazon S3 buckets). To maintain security, you must grant Step Functions access to these resources using AWS Identity and Access Management (IAM).

Step 3: Create a Step Functions state machine

Now that you’ve created your simple Lambda function that mocks an API response, you can create a Step Functions state machine to call the API and handle exceptions.

In this step, you will use the Step Functions console to create a state machine that uses a Task state with a **Retry and Catch** field to handle the various API response codes. You will use a Task state to invoke your mock API Lambda function, which will return the API status code you provide as input into your state machine.

To see the State machine code, check the state_machine.py file in this directory.


Step 4: Execution

Start the execution of the code, by providing this as a sample input (status code).

Note that in the python code, this value is passed to the lambda_handler() function, and it takes event as one of the argument.

Now, check the lambda_function.py file, and see that the "statuscode" is taken as an input from the event, and saved in another variable which is compared in multiple if else in the lambda function.

/1

{

    "statuscode": "200"

}

/2

{

    "statuscode": "429"

}
