import time
import interfaces
import boto3

class Tester(interfaces.TesterInterface):
    def __init__(self) -> None:
        self.aws_iam_client = boto3.client('iam')
        self.aws_iam_resource = boto3.resource('iam')
        self.user_id = boto3.client('sts').get_caller_identity().get('UserId')
        self.account_arn = boto3.client('sts').get_caller_identity().get('Arn')
        self.account_id = boto3.client('sts').get_caller_identity().get('Account') 

    def declare_tested_provider(self) -> str:
        return 'aws'

    def declare_tested_service(self) -> str:
        return 'iam'

    def run_tests(self) -> list:
        return \
            self.get_password_policy_has_14_or_more_char() + \
            self.get_hw_mfa_enabled_for_root_account()

    def get_password_policy_has_14_or_more_char(self):
        result = []
        test_name = "password_has_14_or_more_characters"
        response = self.aws_iam_client.get_account_password_policy()
        password_policy = response['PasswordPolicy']

        if password_policy['MinimumPasswordLength'] >= 14:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "password_policy@@" + self.account_id,
                "item_type": "password_policy_record",
                "test_name": test_name,
                "test_result": "no_issue_found"
            })
        else:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "password_policy@@" + self.account_id,
                "item_type": "password_policy_record",
                "test_name": test_name,
                "test_result": "issue_found"
            })
        
        return result
    
    def get_hw_mfa_enabled_for_root_account(self):
        result = []
        test_name = "hardware_mfa_enabled_for_root_account"

        response = self.aws_iam_client.get_account_summary()
        account_summary = response['SummaryMap']

        if account_summary['AccountMFAEnabled']:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "account_summary@@" + self.account_id,
                "item_type": "account_summary_record",
                "test_name": test_name,
                "test_result": "no_issue_found"
            })
        else:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "account_summary@@" + self.account_id,
                "item_type": "account_summary_record",
                "test_name": test_name,
                "test_result": "issue_found"
            })
        
        return result
