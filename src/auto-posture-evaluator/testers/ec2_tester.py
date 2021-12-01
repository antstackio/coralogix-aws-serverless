import json
import time
import boto3
import botocore.exceptions
import interfaces

class Tester(interfaces.TesterInterface):
    def __init__(self) -> None:
        self.aws_ec2_client = boto3.client('ec2')
        self.aws_ec2_resource = boto3.resource('ec2')
        self.user_id = boto3.client('sts').get_caller_identity().get('UserId')
        self.account_arn = boto3.client('sts').get_caller_identity().get('Arn')
        self.account_id = boto3.client('sts').get_caller_identity().get('Account')
        self.instances = self.aws_ec2_resource.instances.all()

    def declare_tested_service(self) -> str:
        return 'ec2'

    def declare_tested_provider(self) -> str:
        return 'aws'

    def run_tests(self) -> list:
        return \
            self.get_inbound_http_access(self.instances) + \
            self.get_inbound_https_access(self.instances)

    def get_inbound_http_access(self, instances):
        test_name = "ec2_inbound_http_access_restricted"
        result = []
        for instance in instances:
            # get security group of that instance 
            security_groups = instance.security_groups
            all_inbound_permissions = []
            for security_group in security_groups:
                inbound_permissions = self.aws_ec2_resource.SecurityGroup(security_group['GroupId']).ip_permissions
                for i in inbound_permissions:
                    all_inbound_permissions.append(i)

            http_port_access = list(filter(lambda permission: permission['FromPort'] == 80 and permission['ToPort'] == 80, all_inbound_permissions))
            if len(http_port_access) == 0:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": instance.id,
                    "item_type": "ec2",
                    "test_name": test_name
                })
            else:
                pass
        if len(result) == 0:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": None,
                "item_type": "ec2",
                "test_name": test_name
            })
        return result

    def get_inbound_https_access(self, instances):
        test_name = "ec2_inbound_https_access_restricted"
        result = []
        for instance in instances:
            # get security group of that instance 
            security_groups = instance.security_groups
            all_inbound_permissions = []
            for security_group in security_groups:
                inbound_permissions = self.aws_ec2_resource.SecurityGroup(security_group['GroupId']).ip_permissions
                for i in inbound_permissions:
                    all_inbound_permissions.append(i)

            https_port_access = list(filter(lambda permission: permission['FromPort'] == 443 and permission['ToPort'] == 443, all_inbound_permissions))
            if len(https_port_access) == 0:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": instance.id,
                    "item_type": "ec2",
                    "test_name": test_name
                })
            else:
                pass
        if len(result) == 0:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": None,
                "item_type": "ec2",
                "test_name": test_name
            })
        return result
