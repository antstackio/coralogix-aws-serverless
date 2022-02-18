import interfaces
import boto3
import time

class Tester(interfaces.TesterInterface):
    def __init__(self) -> None:
        self.aws_kms_client = boto3.client('kms')
        self.user_id = boto3.client('sts').get_caller_identity().get('UserId')
        self.account_arn = boto3.client('sts').get_caller_identity().get('Arn')
        self.account_id = boto3.client('sts').get_caller_identity().get('Account') 
    def declare_tested_provider(self) -> str:
        return 'aws'

    def declare_tested_service(self) -> str:
        return 'kms'

    def run_tests(self) -> list:
        return \
            self.get_rotation_for_cmks_is_enabled()
    
    def get_rotation_for_cmks_is_enabled(self):
        result = []
        test_name = "rotation_for_cmks_is_enabled"
        keys = []
        can_paginate = self.aws_kms_client.can_paginate('list_keys')
        if can_paginate:
            paginator = self.aws_kms_client.get_paginator('list_keys')
            response_iterator = paginator.paginate(PaginationConfig={'PageSize': 50})

            for page in response_iterator:
                keys.extend(page['Keys'])
        else:
            response = self.aws_kms_client.list_keys()
            keys.extend(response['Keys'])

        for key in keys:
            key_id = key['KeyId']
            key_arn = key['KeyArn']
            response = self.aws_kms_client.get_key_rotation_status(KeyId = key_id)
            rotation_status = response['KeyRotationEnabled']
            if rotation_status:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": key_id,
                    "item_type": "kms_policy",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })
            else:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": key_id,
                    "item_type": "kms_policy",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
        return result
