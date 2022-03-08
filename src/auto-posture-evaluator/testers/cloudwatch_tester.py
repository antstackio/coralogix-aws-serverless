import time
import interfaces
import boto3

class Tester(interfaces.TesterInterface):
    def __init__(self):
        self.aws_cloudwatch_client = boto3.client('cloudwatch')
        self.cache = {}
        self.user_id = boto3.client('sts').get_caller_identity().get('UserId')
        self.account_arn = boto3.client('sts').get_caller_identity().get('Arn')
        self.account_id = boto3.client('sts').get_caller_identity().get('Account')

    def declare_tested_service(self) -> str:
        return 'cloudwatch'

    def declare_tested_provider(self) -> str:
        return 'aws'

    def run_tests(self) -> list:
        return \
            self.get_unauthorized_api_calls_not_monitored() + \
            self.get_route_table_changes_not_monitored() + \
            self.get_console_sign_in_failure_alarm() + \
            self.get_s3_bucket_policy_changes_not_monitored() + \
            self.get_vpc_changes_not_monitored() + \
            self.get_organization_changes_not_monitored() + \
            self.get_usage_of_root_account_not_monitored() + \
            self.get_cloudtrail_configuration_changes_not_monitored() + \
            self.get_management_console_sign_in_without_mfa_not_monitored() + \
            self.get_cmk_configuration_change_not_monitored() + \
            self.get_network_gateway_changes_not_monitored() + \
            self.get_security_group_changes_not_monitored()

    def get_unauthorized_api_calls_not_monitored(self):
        test_name = "unauthorized_api_calls_not_monitored"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='SecurityGroupEventCount', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "no_issue_found"
            }]
        else:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]

    def get_route_table_changes_not_monitored(self):
        test_name = "route_table_changes_not_monitored"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='RouteTableEventCount', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "no_issue_found"
            }]
        else:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]

    def get_console_sign_in_failure_alarm(self):
        test_name = "console_sign_in_failure_alarm"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='ConsoleSignInFailureCount', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "no_issue_found"
            }]
        else:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]
    
    def get_s3_bucket_policy_changes_not_monitored(self):
        test_name = "s3_bucket_policy_changes_not_monitored"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='S3BucketEventCount', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "no_issue_found"
            }]
        else:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]

    def get_vpc_changes_not_monitored(self):
        test_name = "vpc_changes_not_monitored"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='VpcEventCount', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "no_issue_found"
            }]
        else:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]

    def get_organization_changes_not_monitored(self):
        test_name = "organization_changes_not_monitored"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='OrganizationEvents', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "no_issue_found"
            }]
        else:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]
    
    def get_usage_of_root_account_not_monitored(self):
        test_name = "usage_of_root_account_not_monitored"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='RootAccountUsageEventCount', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "no_issue_found"
            }]
        else:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]
    
    def get_cloudtrail_configuration_changes_not_monitored(self):
        test_name = "s3_bucket_policy_changes_not_monitored"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='CloudTrailEventCount', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "no_issue_found"
            }]
        else:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]

    def get_management_console_sign_in_without_mfa_not_monitored(self):
        test_name = "management_console_sign_in_without_mfa_not_monitored"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='ConsoleSignInWithoutMfaCount', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "no_issue_found"
            }]
        else:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]

    def get_cmk_configuration_change_not_monitored(self):
        test_name = "cmk_configuration_change_not_monitored"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='CMKEventCount', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "no_issue_found"
            }]
        else:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]
    
    def get_network_gateway_changes_not_monitored(self):
        test_name = "network_gateway_changes_not_monitored"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='GatewayEventCount', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "no_issue_found"
            }]
        else:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]
    
    def get_security_group_changes_not_monitored(self):
        test_name = "security_group_changes_not_monitored"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='SecurityGroupEventCount', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "no_issue_found"
            }]
        else:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]