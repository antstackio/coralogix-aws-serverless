import time
import interfaces
import boto3
import botocore.exceptions

class Tester(interfaces.TesterInterface):
    def __init__(self):
        self.aws_cloudwatch_client = boto3.client('cloudwatch')
        self.aws_cloudformation_client = boto3.client('cloudformation')
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
            self.get_security_group_changes_not_monitored() + \
            self.get_network_acl_changes_not_monitored() + \
            self.get_aws_config_configuration_changes_not_monitored() + \
            self.get_iam_policy_changes_not_monitored() + \
            self.get_enable_aws_cloudformation_stack_notifications()

    def get_unauthorized_api_calls_not_monitored(self):
        test_name = "unauthorized_api_calls_not_monitored"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='SecurityGroupEventCount', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "SecurityGroupEventCount",
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
                "item": "SecurityGroupEventCount",
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
                "item": "RouteTableEventCount",
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
                "item": "RouteTableEventCount",
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
                "item": "ConsoleSignInFailureCount",
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
                "item": "ConsoleSignInFailureCount",
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
                "item": "S3BucketEventCount",
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
                "item": "S3BucketEventCount",
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
                "item": "VpcEventCount",
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
                "item": "VpcEventCount",
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
                "item": "OrganizationEvents",
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
                "item": "OrganizationEvents",
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
                "item": "RootAccountUsageEventCount",
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
                "item": "RootAccountUsageEventCount",
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
                "item": "CloudTrailEventCount",
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
                "item": "CloudTrailEventCount",
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
                "item": "ConsoleSignInWithoutMfaCount",
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
                "item": "ConsoleSignInWithoutMfaCount",
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
                "item": "CMKEventCount",
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
                "item": "CMKEventCount",
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
                "item": "GatewayEventCount",
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
                "item": "GatewayEventCount",
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
                "item": "SecurityGroupEventCount",
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
                "item": "SecurityGroupEventCount",
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]
    
    def get_network_acl_changes_not_monitored(self):
        test_name = "network_acl_changes_not_monitored"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='NetworkAclEventCount', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "NetworkAclEventCount",
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
                "item": "NetworkAclEventCount",
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]
    
    def get_aws_config_configuration_changes_not_monitored(self):
        test_name = "aws_config_configuration_changes_not_monitored"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='ConfigEventCount', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "ConfigEventCount",
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
                "item": "ConfigEventCount",
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]

    def get_iam_policy_changes_not_monitored(self):
        test_name = "iam_policy_changes_not_monitored"
        alarms = self.aws_cloudwatch_client.describe_alarms_for_metric(MetricName='IAMPolicyEventCount', Namespace='CloudTrailMetrics')
        if len(alarms['MetricAlarms']) > 0:
            return [{
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "IAMPolicyEventCount",
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
                "item": "IAMPolicyEventCount",
                "item_type": "cloudwatch_alarm",
                "test_name": test_name,
                "test_result": "issue_found"
            }]

    def get_enable_aws_cloudformation_stack_notifications(self):
        test_name = "enable_aws_cloudformation_stack_notifications"
        stacks = self.aws_cloudformation_client.list_stacks()
        result = []
        for stack in stacks['StackSummaries']:
            stack_name = stack['StackName']
            issue_detected = False
            try:
                stack_info = self.aws_cloudformation_client.describe_stacks(StackName=stack_name)
                notif_arns = stack_info['Stacks'][0]['NotificationARNs']
                if not notif_arns or len(notif_arns) == 0:
                    issue_detected = True
            except botocore.exceptions.ClientError as ex:
                if ex.response['Error']['Code'] == 'ValidationError':
                    issue_detected = True
                else:
                    raise ex
            
            if issue_detected:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": stack_name,
                    "item_type": "cloudformation_stack",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
            else:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": stack_name,
                    "item_type": "cloudformation_stack",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })

        return result