import aws_cdk as cdk
from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    aws_lambda as aws_lambda,
    aws_stepfunctions as sf,
    aws_stepfunctions_tasks as tasks,
    aws_glue as aws_glue,
    aws_s3_deployment as s3deploy,
    Duration
)

class LambdaStack(cdk.Stack):

    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda function that gets data from public API
        lambda_role = iam.Role(
            self,
            "LambdaRole",
            role_name=f"lambda-execution-role-{self.region}",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_managed_policy_arn(self,"LambdaAccessPolicy","arn:aws:iam::aws:policy/AdministratorAccess"),
            ]
        )

        # Deploy Lambda function from a zip file
        lambda_zip = aws_lambda.Function(
            self,
            "LambdaPsycopg2Zip",
            function_name="lambda-from-zip",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.from_asset("Constructs/lambda/lambda_deploy.zip"),
            handler='lambda_code.handler',
            role=lambda_role,
            timeout=Duration.seconds(10)
        )

        # Deploy Lambda function from a Docker file
        lambda_docker = aws_lambda.DockerImageFunction(
            self,
            'LambdaPsycopg2Docker',
            function_name="lambda-from-docker",
            code=aws_lambda.DockerImageCode.from_image_asset(
                directory="Constructs",
                cmd=['lambda_code.handler']
            ),
            role=lambda_role,
            timeout=Duration.seconds(10)
        )