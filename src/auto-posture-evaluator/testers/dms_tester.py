import time
import boto3
import interfaces

class Tester(interfaces.TesterInterface):
    def __init__(self) -> None:
        self.user_id = boto3.client('sts').get_caller_identity().get('UserId')
        self.account_arn = boto3.client('sts').get_caller_identity().get('Arn')
        self.account_id = boto3.client('sts').get_caller_identity().get('Account')
        self.aws_dms_client = boto3.client('dms')
        self.dms_instances = self._get_dms_instances()

    def declare_tested_provider(self) -> str:
        return "aws"
    
    def declare_tested_provider(self) -> str:
        return "dms"

    def run_tests(self) -> list:
        return \
            self.get_replication_instances_have_auto_minor_version_upgrade_enabled() + \
            self.get_multi_az_is_enabled()
    
    def _get_dms_instances(self):
        dms_instances = []

        paginator = self.aws_dms_client.get_paginator('describe_replication_instances')
        response_iterator = paginator.paginate()
        for page in response_iterator:
            dms_instances.extend(page["ReplicationInstances"])
        
        return dms_instances

    def _append_ems_test_result(self, item, item_type, test_name, issue_status):
        return {
            "user": self.user_id,
            "account_arn": self.account_arn,
            "account": self.account_id,
            "timestamp": time.time(),
            "item": item,
            "item_type": item_type,
            "test_name": test_name,
            "test_result": issue_status
        }
    
    def get_replication_instances_have_auto_minor_version_upgrade_enabled(self):
        test_name = "replication_instances_should_have_auto_minor_version_upgrade"
        result = []

        replication_instances = self.dms_instances
        for instance in replication_instances:
            instance_identifier = instance['ReplicationInstanceIdentifier']
            auto_minor_version_upgrade = instance['AutoMinorVersionUpgrade']

            if auto_minor_version_upgrade:
                result.append(self._append_ems_test_result(instance_identifier, "dms_replication_instance", test_name, "no_issue_found"))
            else:
                result.append(self._append_ems_test_result(instance_identifier, "dms_replication_instance", test_name, "issue_found"))

        return result

    def get_multi_az_is_enabled(self):
        test_name = "replication_instance_should_use_multi_AZ_deployment"
        result = []

        replication_instances = self.dms_instances
        for instance in replication_instances:
            instance_identifier = instance['ReplicationInstanceIdentifier']
            multi_az = instance['MultiAZ']

            if multi_az:
                result.append(self._append_ems_test_result(instance_identifier, "dms_replication_instance", test_name, "no_issue_found"))
            else:
                result.append(self._append_ems_test_result(instance_identifier, "dms_replication_instance", test_name, "issue_found"))
            
        return result
