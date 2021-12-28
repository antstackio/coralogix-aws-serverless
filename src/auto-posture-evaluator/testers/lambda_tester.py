import time
from typing import List
import json
import interfaces
import boto3

class Tester(interfaces.TesterInterface):
    def __init__(self) -> None:
        self.aws_lambda_client = boto3.client('lambda')
        self.user_id = boto3.client('sts').get_caller_identity().get('UserId')
        self.account_arn = boto3.client('sts').get_caller_identity().get('Arn')
        self.account_id = boto3.client('sts').get_caller_identity().get('Account')
        self.functions = self._get_all_functions()

    def declare_tested_service(self) -> str:
        return 'lambda'

    def declare_tested_provider(self) -> str:
        return 'aws'

    def run_tests(self) -> list:
        return \
            self.get_lambda_publicly_accessible()

    def _get_all_functions(self) -> List:
        paginator = self.aws_lambda_client.get_paginator('list_functions')
        response_iterator = paginator.paginate(FunctionVersion='ALL')

        functions = []
        for response in response_iterator:
            functions.extend(response['Functions'])
        
        return functions

    def get_lambda_uses_latest_runtime(self) -> List:
        lambdas = self.functions

        for Lambda in lambdas:
            runtime = Lambda['Runtime']        
        return []
    
    def get_lambda_publicly_accessible(self) -> List:
        lambdas = self.functions
        test_name = "lambda_function_not_publicly_accessible"
        result = []
        function_arn_with_issue = []
        for Lambda in lambdas:
            try:
                policy = self.aws_lambda_client.get_policy(FunctionName=Lambda['FunctionName'])
                policy_json = json.loads(policy['Policy'])
                policy_statements = policy_json['Statement']

                for statement in policy_statements:
                    if (statement['Principal'] == '*' or statement['Principal']['AWS'] == '*') and not statement.has_key('Condition'):

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
            except Exception as e:
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
        pass