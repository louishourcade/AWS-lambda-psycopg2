# Deploy AWS Step Functions that supports partial runs

[Psycopg](https://pypi.org/project/psycopg2/) is the most popular PostgresSQL database adapter for Python. It enables developers 
to write a Python application that interacts with a PostgreSQL database.

Among the compute options developers might want to include in their application, there is [AWS Lambda](https://aws.amazon.com/lambda/).
AWS Lambda is a serverless, event-driven compute service that lets developers run code for any type of application or
backend service without provisioning or managing servers. Lambda natively supports Python, Java, Go, PowerShell, Node.js, C#, and Ruby code, and provides a Runtime API 
allowing developers to use any additional programming languages to author functions.

By default, when you create a new function with a Python runtime (either Python3.9, 3.8, or 3.7), the Lambda environment is created
from an [AWS-provided base image for Lambda](https://github.com/aws/aws-lambda-base-images).

When using Lambda, you will sooner or later need to use libraries not included in the base images for Lambda. For example, if you
need to use [pandas](https://pypi.org/project/pandas/) and [psycopg2](https://pypi.org/project/psycopg2/), your script will start with:

```bash
import pandas as pd
import psycopg2
```

If you run this in your Lambda function with the Python default image, you will hit this error:

```bash
Unable to import module 'lambda_function': No module named 'pandas'
```

To resolve this, you need to bundle your libraries in a custom package, and then find a way to attach the package to Lambda. There are multiple ways to do it, including:
* Deploying your Lambda function [from a .zip file archive](https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-zip.html)
* Deploying your Lambda function [from a custom container image](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html#gettingstarted-package-images)
* Creating a [Lambda Layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html) and attaching it to your Lambda function

In this article, we focus on the first two. Adding the `pandas` library to your Lambda function is relatively straightforward. You just have to create a new folder in your
Linux machine, put the Lambda script together with the `pandas` library and its dependencies in the folder, zip it, and provide it as a source for your Lambda function.

However, this does not work for `psycopg2`. In this article, we illustrate the error that you will get when trying to use `psycopg2` in your Lambda function created from
a .zip file, and we will see how to use `psycopg2` in your Lambda function created from a custom container image.

## Solution overview

To illustrate the challenges developers might face when using the `psycopg2` library in Lanbda, we will deploy two Lambda functions:
* One Lambda function with the Python3.8 runtime **created from a .zip file**. The `psycopg2` and `libraries` are installed in this .zip folder with [pip](https://pypi.org/project/pip/).
* One Lambda function with the Python3.8 runtime **created from a Dockerfile**. The dockerfile installs the `psycopg2` and `pandas` libraries into the Lambda image.

![lambdas](assets/img/lambdas_img.PNG)

With these two Lambda functions, we illustrate that installing the `pandas` library and its dependencies in a zip file is enough for your Lambda script to run.
This is however not the case for the `psycopg2` for reasons we will detail in [Run the Lambda function created from the .zip file](#zip). We then see that developers can overcome this limitation by creating their Lambda functions
from custom containers.

## Code deployment

#### Pre-requisites

For this deployment, you will need:
* An AWS account with sufficient permissions to deploy AWS resources packaged in this code.
* aws-cdk: installed globally (npm install -g aws-cdk) 
* git client
* python3.8

#### Clone the repository

Clone the GitHub repository on your machine:

```bash
git clone https://github.com/louishourcade/AWS-lambda-psycopg2.git
cd AWS-lambda-psycopg2
```

#### Configure your deployment

Edit the `app.py` file with information about your AWS account:

```python
aws_acccount = "AWS_ACCOUNT_ID"
region = "AWS_REGION"
```

This is the AWS environment where the resources will be deployed.

#### Bootstrap your AWS account

If not already done, you need to [bootstrap your AWS environment](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html) before deploying this CDK application.

Run the commands below with the AWS credentials of your AWS account:

```bash
cdk bootstrap aws://<tooling-account-id>/<aws-region>
```

#### Deploy the CDK application

Now that your AWS account is bootstrapped, and that you configured your deployment, you can deploy the CDK application with the following command:

```bash
cdk deploy AWSLambdaPyscopg2
```

Confirm the deployment in the terminal, wait until the CloudFormation stack is deployed, and you're done 🎉

## Test partial retries on the state machine

#### Explanations about the resources deployed

#### Run the Lambda function created from the .zip file <a name="zip"></a>

#### Run the Lambda function created from the Dockerfile

## Conclusion
