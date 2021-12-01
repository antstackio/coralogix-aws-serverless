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
            self.get_inbound_https_access(self.instances) + \
            self.get_inbound_mongodb_access(self.instances) + \
            self.get_inbound_mysql_access(self.instances) + \
            self.get_inbound_mssql_access(self.instances)
    
    def _get_inbound_port_access(self, instances, target_port, test_name):
        result = []
        for instance in instances:
            # get security group of that instance 
            security_groups = instance.security_groups
            all_inbound_permissions = []
            for security_group in security_groups:
                inbound_permissions = self.aws_ec2_resource.SecurityGroup(security_group['GroupId']).ip_permissions
                for i in inbound_permissions:
                    all_inbound_permissions.append(i)

            https_port_access = list(filter(lambda permission: permission['FromPort'] == target_port and permission['ToPort'] == target_port, all_inbound_permissions))
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

    def get_inbound_http_access(self, instances):
        test_name = "ec2_inbound_http_access_restricted"
        return self._get_inbound_port_access(instances, 80, test_name)

    def get_inbound_https_access(self, instances):
        test_name = "ec2_inbound_https_access_restricted"
        return self._get_inbound_port_access(instances, 443, test_name)
    
    def get_inbound_mongodb_access(self, instances):
        test_name = "ec2_inbound_mongodb_access_restricted"
        return self._get_inbound_port_access(instances, 27017, test_name)
    
    def get_inbound_mysql_access(self, instances):
        test_name = "ec2_inbound_mysql_access_restricted"
        return self._get_inbound_port_access(instances, 3306, test_name)
    
    def get_inbound_mssql_access(self, instances):
        test_name = "ec2_inbound_mssql_access_restricted"
        return self._get_inbound_port_access(instances, 1433, test_name)

print(Tester().run_tests())