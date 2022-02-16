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
            self.get_hw_mfa_enabled_for_root_account() + \
            self.get_mfa_enabled_for_root_account() + \
            self.get_policy_does_not_have_user_attached()

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
    
    def get_mfa_enabled_for_root_account(self):
        result = []
        test_name = "mfa_is_enabled_for_root_account"

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
    
    def get_policy_does_not_have_user_attached(self):
        result = []
        test_name = "policy_does_not_have_a_user_attached_to_it"
        policies = []
        can_paginate = self.aws_iam_client.can_paginate('list_policies')
        if can_paginate:
            paginator = self.aws_iam_client.get_paginator('list_policies')
            response_iterator = paginator.paginate(Scope='Local', PaginationConfig={'PageSize': 50})

            for page in response_iterator:
                policies.extend(page['Policies'])
        else:
            response = self.aws_iam_client.list_policies()
            policies.extend(response['Policies'])

        for policy in policies:
            policy_id = policy['PolicyId']
            policy_arn = policy['Arn']
            response = self.aws_iam_client.list_entities_for_policy(PolicyArn=policy_arn,EntityFilter='User')
            
            attached_users = response['PolicyUsers']
            if len(attached_users) > 0:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": policy_id,
                    "item_type": "iam_policy",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
            else:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": policy_id,
                    "item_type": "iam_policy",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })

        return result
