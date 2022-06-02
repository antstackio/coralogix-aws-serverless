import time
from typing import List
import json
import re
import interfaces
import boto3
import requests


class Tester(interfaces.TesterInterface):
    def __init__(self) -> None:
        self.aws_lambda_client = boto3.client('lambda')
        self.user_id = boto3.client('sts').get_caller_identity().get('UserId')
        self.account_arn = boto3.client('sts').get_caller_identity().get('Arn')
        self.account_id = boto3.client('sts').get_caller_identity().get('Account')
        self.functions = self._get_all_functions()
        self.SUPPORTED_LAMBDA_RUNTIME = "https://cgx-s3-nsm-logshipper-config.s3.eu-west-1.amazonaws.com/acceptable-lambda-runtime-versions.json"

    def declare_tested_service(self) -> str:
        return 'lambda'

    def declare_tested_provider(self) -> str:
        return 'aws'

    def run_tests(self) -> list:
        return \
            self.get_lambda_publicly_accessible() + \
            self.get_lambda_has_access_to_vpc_resources() + \
            self.get_lambda_uses_latest_runtime()

    def _get_all_functions(self) -> List:
        paginator = self.aws_lambda_client.get_paginator('list_functions')
        response_iterator = paginator.paginate(FunctionVersion='ALL')

        functions = []
        for response in response_iterator:
            functions.extend(response['Functions'])

        return functions

    def get_lambda_uses_latest_runtime(self) -> List:
        lambdas = self.functions
        test_name = "aws_lambda_uses_latest_runtime"
        response = requests.get(self.SUPPORTED_LAMBDA_RUNTIME)
        supported_versions_repo = response.json()
        result = []
        for Lambda in lambdas:
            runtime = Lambda['Runtime']
            language = re.split(r"\d+.\d+|\d+.\w", runtime)[0]
            version = runtime.split(language)[-1]
            versions = supported_versions_repo[language]
            if version in versions:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": Lambda['FunctionArn'],
                    "item_type": "aws_lambda",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })
            else:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": Lambda['FunctionArn'],
                    "item_type": "aws_lambda",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
        return result

    def get_lambda_publicly_accessible(self) -> List:
        lambdas = self.functions
        test_name = "aws_lambda_function_not_publicly_accessible"
        result = []
        function_arn_with_issue = []
        for Lambda in lambdas:
            try:
                policy = self.aws_lambda_client.get_policy(FunctionName=Lambda['FunctionName'])
                policy_json = json.loads(policy['Policy'])
                policy_statements = policy_json['Statement']
                for statement in policy_statements:
                    if (statement['Principal'] == '*' or statement['Principal']['AWS'] == '*') and 'Condition' not in statement:

                        function_arn_with_issue.append(Lambda['FunctionArn'])
                    else:
                        result.append({
                            "user": self.user_id,
                            "account_arn": self.account_arn,
                            "account": self.account_id,
                            "timestamp": time.time(),
                            "item": Lambda['FunctionArn'],
                            "item_type": "aws_lambda",
                            "test_name": test_name,
                            "test_result": "no_issue_found"
                        })
            except Exception:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": Lambda['FunctionArn'],
                    "item_type": "aws_lambda",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })
        function_arn_with_issue = set(function_arn_with_issue)
        for arn in function_arn_with_issue:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": arn,
                "item_type": "aws_lambda",
                "test_name": test_name,
                "test_result": "issue_found"
            })

        return result

    def get_lambda_has_access_to_vpc_resources(self) -> List:
        test_name = "aws_lambda_has_access_to_vpc_resources"
        result = []
        lambdas = self.functions

        for i in lambdas:
            if "VpcConfig" in i:
                vpc_info = i['VpcConfig']
                # check vpc id, subnet and security group
                if (vpc_info['VpcId'] is not None or vpc_info['VpcId'] != '') and len(vpc_info['SubnetIds']) > 0 and len(vpc_info['SecurityGroupIds']) > 0:
                    # has issue
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": i['FunctionArn'],
                        "item_type": "aws_lambda",
                        "test_name": test_name,
                        "test_result": "issue_found"
                    })
                else:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": i['FunctionArn'],
                        "item_type": "aws_lambda",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
            else:
                # no issue
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": i['FunctionArn'],
                    "item_type": "aws_lambda",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })

        return result
