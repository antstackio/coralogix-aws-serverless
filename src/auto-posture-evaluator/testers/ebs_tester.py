import time
from typing import Dict, List, Set
import boto3
import interfaces

class Tester(interfaces.TesterInterface):
    def __init__(self) -> None:
        self.aws_ec2_client = boto3.client('ec2')
        self.aws_ec2_resource = boto3.resource('ec2')
        self.user_id = boto3.client('sts').get_caller_identity().get('UserId')
        self.account_arn = boto3.client('sts').get_caller_identity().get('Arn')
        self.account_id = boto3.client('sts').get_caller_identity().get('Account')

    def declare_tested_service(self) -> str:
        return 'ebs'

    def declare_tested_provider(self) -> str:
        return 'aws'
    
    def run_tests(self) -> list:
        return self.get_volume_is_not_encrypted()
    
    def get_volume_is_not_encrypted(self) -> List:
        result = []
        test_name = "volume_is_not_encrypted"
        volumes = []
        can_paginate = self.aws_ec2_client.can_paginate('describe_volumes')
        
        if can_paginate:
            paginator = self.aws_ec2_client.get_paginator('describe_volumes')
            response_iterator = paginator.paginate(PaginationConfig={'PageSize': 50})
            for page in response_iterator:
                volumes.extend(page['Volumes'])
        else:
            response = self.aws_ec2_client.describe_volumes()
            volumes.extend(response['Volumes'])

        for volume in volumes:
            volume_id = volume['VolumeId']
            if not volume['Encrypted']:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": volume_id,
                    "item_type": "ebs_volume",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
            else:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": volume_id,
                    "item_type": "ebs_volume",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })
        
        return result

    def get_volume_attached_to_ec2(self):
        result = []
        test_name = "volume_attached_to_ec2"
        volumes = []
        can_paginate = self.aws_ec2_client.can_paginate('describe_volumes')
        
        if can_paginate:
            paginator = self.aws_ec2_client.get_paginator('describe_volumes')
            response_iterator = paginator.paginate(PaginationConfig={'PageSize': 50})
            for page in response_iterator:
                volumes.extend(page['Volumes'])
        else:
            response = self.aws_ec2_client.describe_volumes()
            volumes.extend(response['Volumes'])

        for volume in volumes:
            volume_id = volume['VolumeId']
            attachments = volume['Attachments']
            if len(attachments) > 0:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": volume_id,
                    "item_type": "ebs_volume",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
            else:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": volume_id,
                    "item_type": "ebs_volume",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })
        
        return result