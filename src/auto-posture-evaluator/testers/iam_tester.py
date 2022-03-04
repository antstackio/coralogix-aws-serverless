import os
import time
import jmespath
import interfaces
import boto3
import botocore
import datetime as dt
from datetime import datetime
class Tester(interfaces.TesterInterface):
    def __init__(self) -> None:
        self.aws_iam_client = boto3.client('iam')
        self.aws_iam_resource = boto3.resource('iam')
        self.user_id = boto3.client('sts').get_caller_identity().get('UserId')
        self.account_arn = boto3.client('sts').get_caller_identity().get('Arn')
        self.account_id = boto3.client('sts').get_caller_identity().get('Account')
        self.iam_user_credentials_unuse_threshold = os.environ.get('AUTOPOSTURE_IAM_CREDENTIALS_UNUSE_THRESHOLD')
        self.password_maximum_age_policy = os.environ.get('AUTOPOSTURE_PASSWORD_MAX_AGE_POLICY')
        self.password_length_threshold_policy = os.environ.get('AUTOPOSTURE_PASSWORD_LENGTH_THRESHOLD_POLICY')
        self.access_key_maximum_age = os.environ.get('AUTOPOSTURE_ACCESS_KEY_MAX_AGE')

    def declare_tested_provider(self) -> str:
        return 'aws'

    def declare_tested_service(self) -> str:
        return 'iam'

    def run_tests(self) -> list:
        return \
            self.get_password_policy_has_14_or_more_char() + \
            self.get_hw_mfa_enabled_for_root_account() + \
            self.get_mfa_enabled_for_root_account() + \
            self.get_policy_does_not_have_user_attached() + \
            self.get_access_keys_rotated_every_90_days() + \
            self.get_server_certificate_will_expire() + \
            self.get_expired_ssl_tls_certtificate_removed() + \
            self.get_password_expires_in_90_days() + \
            self.get_password_policy_requires_lowercase() + \
            self.get_password_policy_requires_uppercase() + \
            self.get_password_policy_requires_symbols() + \
            self.get_password_policy_requires_numbers() + \
            self.get_support_role_for_aws_support() + \
            self.get_priviledged_user_has_admin_permissions() + \
            self.get_password_reuse_policy() + \
            self.get_no_access_key_for_root_account() + \
            self.get_mfa_enabled_for_all_iam_users() + \
            self.get_role_uses_trused_principals() + \
            self.get_access_keys_are_not_created_during_initial_setup() + \
            self.get_policy_with_admin_privilege_not_created() + \
            self.get_iam_user_credentials_unused_for_45_days()

    def get_password_policy_has_14_or_more_char(self):
        result = []
        test_name = "password_has_14_or_more_characters"
        try:
            response = self.aws_iam_client.get_account_password_policy()
            password_policy = response['PasswordPolicy']

            password_length_threshold = int(self.password_length_threshold_policy) if self.password_length_threshold_policy else 14
            
            if password_policy['MinimumPasswordLength'] >= password_length_threshold:
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
        except self.aws_iam_client.exceptions.NoSuchEntityException as e:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "no_password_policy@@" + self.account_id,
                "item_type": "password_policy_record",
                "test_name": test_name,
                "test_result": "issue_found"
            })
        return result
    
    def get_hw_mfa_enabled_for_root_account(self):
        result = []
        test_name = "hardware_mfa_enabled_for_root_account"

        response = self.aws_iam_client.list_virtual_mfa_devices(AssignmentStatus='Assigned')
        virtual_devices = response['VirtualMFADevices']
        
        if len(virtual_devices) > 0:
            for device in virtual_devices:
                serial_number = device['SerialNumber']
                root_account_device = serial_number.split('/')[-1]

                if root_account_device == 'root-account-mfa-device':
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
        else:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "no_mfa_device@@" + self.account_id,
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
            response_iterator = paginator.paginate(PaginationConfig={'PageSize': 50})

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

    def get_access_keys_rotated_every_90_days(self):
        result = []
        test_name = "access_keys_are_rotated_every_90_days_or_less"

        paginator = self.aws_iam_client.get_paginator('list_users')
        response_iterator = paginator.paginate()
        users = []
        for page in response_iterator:
            users.extend(page['Users'])
        access_keys_max_age = int(self.access_key_maximum_age) if self.access_key_maximum_age else 90
        if len(users) > 0:
            for user in users:
                user_name = user['UserName']
                response = self.aws_iam_client.list_access_keys(UserName=user_name)
                access_keys = response['AccessKeyMetadata']
                old_access_keys = 0
                
                for key in access_keys:
                    create_date = key['CreateDate']
                    current_date = datetime.now(tz=dt.timezone.utc)
                    time_diff = (current_date - create_date).days
                    
                    if time_diff > access_keys_max_age:
                        old_access_keys += 1
                    else: pass
                if old_access_keys > 0:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": user_name,
                        "item_type": "iam_user",
                        "test_name": test_name,
                        "test_result": "issue_found"
                    })
                else:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": user_name,
                        "item_type": "iam_user",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
        else:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "no_iam_user@@" + self.account_id,
                "item_type": "iam_user",
                "test_name": test_name,
                "test_result": "no_issue_found"
            })
        
        return result

    def get_server_certificate_will_expire(self):
        result = []
        test_name = "server_certificate_will_expire_within_30_days"

        paginator = self.aws_iam_client.get_paginator('list_server_certificates')
        response_iterator = paginator.paginate()
        certificates = []
        for page in response_iterator:
            certificates.extend(page['ServerCertificateMetadataList'])

        if len(certificates) > 0:
            
            for certificate in certificates:
                certificate_id = certificate['ServerCertificateId']
                expiration_date = certificate['Expiration']
                current_date = datetime.date(datetime.now())
                time_diff = (expiration_date - current_date).days

                if time_diff < 0:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": certificate_id,
                        "item_type": "iam_server_certificate",
                        "test_name": test_name,
                        "test_result": "issue_found"
                    })
                elif time_diff <= 30:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": certificate_id,
                        "item_type": "iam_server_certificate",
                        "test_name": test_name,
                        "test_result": "issue_found"
                    })
                else:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": certificate_id,
                        "item_type": "iam_server_certificate",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
        else:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": None,
                "item_type": "iam_server_certificate",
                "test_name": test_name,
                "test_result": "no_issue_found"
            })
        
        return result

    def get_expired_ssl_tls_certtificate_removed(self):
        result = []
        test_name = "all_expired_ssl_tls_certificate_removed"

        paginator = self.aws_iam_client.get_paginator('list_server_certificates')
        response_iterator = paginator.paginate()
        certificates = []
        for page in response_iterator:
            certificates.extend(page['ServerCertificateMetadataList'])

        if len(certificates) > 0:
            for certificate in certificates:
                certificate_id = certificate['ServerCertificateId']
                expiration_date = certificate['Expiration']
                current_date = datetime.date(datetime.now())
                time_diff = (expiration_date - current_date).days

                if time_diff < 0:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": certificate_id,
                        "item_type": "iam_server_certificate",
                        "test_name": test_name,
                        "test_result": "issue_found"
                    })
                else:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": certificate_id,
                        "item_type": "iam_server_certificate",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
        else:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "no_server_certificate@@" + self.account_id,
                "item_type": "iam_server_certificate",
                "test_name": test_name,
                "test_result": "no_issue_found"
            })

        return result

    def get_password_expires_in_90_days(self):
        result = []
        test_name = "policy_is_set_expire_passwords_within_90_days_or_less"

        try:
            response = self.aws_iam_client.get_account_password_policy()
            password_policy = response['PasswordPolicy']
            
            password_maximum_age_policy = int(self.password_maximum_age_policy) if self.password_maximum_age_policy else 90
            expire_passwords = password_policy.get('ExpirePasswords')
            if expire_passwords:
                max_password_age = password_policy['MaxPasswordAge']
                if max_password_age <= password_maximum_age_policy:
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
        except self.aws_iam_client.exceptions.NoSuchEntityException as e:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "no_password_policy@@" + self.account_id,
                "item_type": "password_policy_record",
                "test_name": test_name,
                "test_result": "issue_found"
            })
        return result

    def get_password_policy_requires_lowercase(self):
        result = []
        test_name = "password_requires_one_or_more_lowercase_characters"
        
        try:
            response = self.aws_iam_client.get_account_password_policy()
            password_policy = response['PasswordPolicy']

            if password_policy['RequireLowercaseCharacters']:
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
        except self.aws_iam_client.exceptions.NoSuchEntityException as e:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "no_password_policy@@" + self.account_id,
                "item_type": "password_policy_record",
                "test_name": test_name,
                "test_result": "issue_found"
            })
        return result

    def get_password_policy_requires_uppercase(self):
        result = []
        test_name = "password_requires_one_or_more_uppercase_characters"

        try:
            response = self.aws_iam_client.get_account_password_policy()
            password_policy = response['PasswordPolicy']

            if password_policy['RequireUppercaseCharacters']:
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
        except self.aws_iam_client.exceptions.NoSuchEntityException as e:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "no_password_policy@@" + self.account_id,
                "item_type": "password_policy_record",
                "test_name": test_name,
                "test_result": "issue_found"
            })
        return result
    
    def get_password_policy_requires_symbols(self):
        result = []
        test_name = "password_requires_one_or_more_symbols"
        try:
            response = self.aws_iam_client.get_account_password_policy()
            password_policy = response['PasswordPolicy']

            if password_policy['RequireSymbols']:
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
        except self.aws_iam_client.exceptions.NoSuchEntityException as e:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "no_password_policy@@" + self.account_id,
                "item_type": "password_policy_record",
                "test_name": test_name,
                "test_result": "issue_found"
            })
        return result

    def get_password_policy_requires_numbers(self):
        result = []
        test_name = "password_requires_one_or_more_numbers"

        try:
            response = self.aws_iam_client.get_account_password_policy()
            password_policy = response['PasswordPolicy']

            if password_policy['RequireNumbers']:
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
        except self.aws_iam_client.exceptions.NoSuchEntityException as e:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "no_password_policy@@" + self.account_id,
                "item_type": "password_policy_record",
                "test_name": test_name,
                "test_result": "issue_found"
            })
        return result

    def get_support_role_for_aws_support(self):
        result = []
        policies = []
        test_name = "support_role_to_manage_incidents_with_AWS_support"

        paginator = self.aws_iam_client.get_paginator('list_policies')
        response_iterator = paginator.paginate(PaginationConfig={'PageSize': 50})

        for page in response_iterator:
            policies.extend(page['Policies'])

        policy_dict =  { 'policies' : policies }
        response = jmespath.search("policies[?PolicyName == 'AWSSupportAccess'].Arn[]", policy_dict)
        policy_arn = response[0]
        if len(response) > 0:
            response = self.aws_iam_client.list_entities_for_policy(
                PolicyArn=policy_arn,
                EntityFilter='Role'
            )
            support_role =  response['PolicyRoles']
            if len(support_role) > 0:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": "support_role@@" + self.account_id,
                    "item_type": "iam_support_role",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })
            else:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": "support_role@@" + self.account_id,
                    "item_type": "iam_support_role",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
        else:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "support_role@@" + self.account_id,
                "item_type": "iam_support_role",
                "test_name": test_name,
                "test_result": "issue_found"
            })
        
        return result

    def get_priviledged_user_has_admin_permissions(self):
        result = []
        test_name = "priviledged_user_has_admin_permissions"

        paginator = self.aws_iam_client.get_paginator('list_users')
        response_iterator = paginator.paginate()
        users = []
        for page in response_iterator:
            users.extend(page['Users'])
        
        if len(users) > 0:
            for user in users:
                user_name = user['UserName']
                response = self.aws_iam_client.list_user_policies(UserName=user_name)
                policy_names = response['PolicyNames']
                admin_access = False
                for policy in policy_names:
                    if policy == 'AdministratorAccess':
                        admin_access = True
                        result.append({
                            "user": self.user_id,
                            "account_arn": self.account_arn,
                            "account": self.account_id,
                            "timestamp": time.time(),
                            "item": user_name,
                            "item_type": "iam_user",
                            "test_name": test_name,
                            "test_result": "issue_found"
                        })
                        break
                if not admin_access:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": user_name,
                        "item_type": "iam_user",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
        else:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "no_iam_user@@" + self.account_id,
                "item_type": "iam_user",
                "test_name": test_name,
                "test_result": "no_issue_found"
            })
        
        return result

    def get_password_reuse_policy(self):
        result = []
        test_name = "password_policy_prevents_password_reuse"

        try:
            response = self.aws_iam_client.get_account_password_policy()
            password_policy = response['PasswordPolicy']
            password_reuse_prevetion = password_policy.get('PasswordReusePrevention')

            if password_reuse_prevetion is not None:
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
        except self.aws_iam_client.exceptions.NoSuchEntityException as e:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "no_password_policy@@" + self.account_id,
                "item_type": "password_policy_record",
                "test_name": test_name,
                "test_result": "issue_found"
            })
        return result

    def get_no_access_key_for_root_account(self):
        result = []
        test_name = "no_root_account_access_key_exists"

        response = self.aws_iam_client.get_account_summary()
        root_access_key_present = response['SummaryMap']['AccountAccessKeysPresent']
        
        if root_access_key_present:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "root_account@@" + self.account_id,
                "item_type": "iam_root_account",
                "test_name": test_name,
                "test_result": "issue_found"
            })
        else:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "root_account@@" + self.account_id,
                "item_type": "iam_root_account",
                "test_name": test_name,
                "test_result": "no_issue_found"
            })
        
        return result

    def get_mfa_enabled_for_all_iam_users(self):
        result = []
        users = []
        test_name = "mfa_is_enabled_for_all_iam_users_with_console_password"

        paginator = self.aws_iam_client.get_paginator('list_users')
        response_paginator = paginator.paginate()
        
        for page in response_paginator:
            users.extend(page['Users'])
        
        if len(users) > 0:
            for user in users:
                user_name = user['UserName']
                paginator = self.aws_iam_client.get_paginator('list_mfa_devices')
                response_paginator = paginator.paginate(UserName=user_name)
                mfa_devices = []
            
                for page in response_paginator:
                    mfa_devices.extend(page['MFADevices'])
            
                if len(mfa_devices) > 0:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": user_name,
                        "item_type": "iam_user",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
                else: 
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": user_name,
                        "item_type": "iam_user",
                        "test_name": test_name,
                        "test_result": "issue_found"
                    })
        else:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "no_iam_user@@" + self.account_id,
                "item_type": "iam_user",
                "test_name": test_name,
                "test_result": "no_issue_found"
            })
        return result

    def get_role_uses_trused_principals(self):
        result = []
        policies = []
        test_name = "role_uses_trusted_principals"

        paginator = self.aws_iam_client.get_paginator('list_policies')
        response_iterator =  paginator.paginate(PaginationConfig={'PageSize': 50})

        for page in response_iterator:
            policies.extend(page['Policies'])
        
        for policy in policies:
            policy_id = policy['PolicyId']
            policy_arn = policy['Arn']

            response = self.aws_iam_client.list_entities_for_policy(PolicyArn=policy_arn)
            policy_users = response['PolicyUsers']
            policy_groups = response['PolicyGroups']
            policy_roles = response['PolicyRoles']
            if (len(policy_groups) > 0 or len(policy_roles) > 0) and len(policy_users) == 0:
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
            else:
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

        return result

    def get_access_keys_are_not_created_during_initial_setup(self):
        result = []
        test_name = "access_keys_are_not_created_for_IAM_user_during_initial_setup"
        users = []
        paginator = self.aws_iam_client.get_paginator('list_users')
        response_iterator = paginator.paginate()

        for page in response_iterator:
            users.extend(page['Users'])
        
        if len(users) > 0:
            for user in users:
                user_name = user['UserName']
                user_created_at = user['CreateDate']
                response = self.aws_iam_client.list_access_keys(UserName = user_name)
                access_key_metadata = response['AccessKeyMetadata']

                if len(access_key_metadata) > 0:
                    for access_key in access_key_metadata:
                        access_key_created_at = access_key['CreateDate']
                        access_key_status = access_key['Status']

                        issue_with_access_key = False
                        if access_key_status == 'Active':
                            user_created_at = datetime.strptime(datetime.strftime(user_created_at, '%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')
                            access_key_created_at = datetime.strptime(datetime.strftime(access_key_created_at, '%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')

                            if user_created_at == access_key_created_at:
                                issue_with_access_key = True
                                break
                            else: pass
                        else: pass

                    if issue_with_access_key:
                        result.append({
                            "user": self.user_id,
                            "account_arn": self.account_arn,
                            "account": self.account_id,
                            "timestamp": time.time(),
                            "item": user_name,
                            "item_type": "iam_user",
                            "test_name": test_name,
                            "test_result": "issue_found"
                        })
                    else:
                        result.append({
                            "user": self.user_id,
                            "account_arn": self.account_arn,
                            "account": self.account_id,
                            "timestamp": time.time(),
                            "item": user_name,
                            "item_type": "iam_user",
                            "test_name": test_name,
                            "test_result": "no_issue_found"
                        })
                else:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": user_name,
                        "item_type": "iam_user",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
        else:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "no_iam_user@@" + self.account_id,
                "item_type": "iam_user",
                "test_name": test_name,
                "test_result": "no_issue_found"
            })
        return result

    def get_policy_with_admin_privilege_not_created(self):
        result = []
        policies = []
        test_name = "policy_with_admin_privilege_not_created"

        paginator = self.aws_iam_client.get_paginator('list_policies')
        response_iterator =  paginator.paginate(PaginationConfig={'PageSize': 50})

        for page in response_iterator:
            policies.extend(page['Policies'])
        
        for policy in policies:
            policy_id = policy['PolicyId']
            policy_arn = policy['Arn']
            version_id = policy['DefaultVersionId']

            response = self.aws_iam_client.get_policy_version(PolicyArn=policy_arn, VersionId=version_id)
            policy_document = response['PolicyVersion']['Document']['Statement']

            for policy in policy_document:
                if(type(policy) is not dict or not policy.get('Action')): continue
                if ((policy.get('Resource') and (policy['Resource']=='*' and policy['Action']=='*')) \
                    or (type(policy['Action']) is str and policy['Action']=='*:*') \
                    or (type(policy['Action']) is list and any([True if action=='*:*' else False for action in policy['Action']]))):
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

    def get_iam_user_credentials_unused_for_45_days(self):
        result = []
        users = []
        test_name = "iam_user_credentials_unused_for_45_days_or_more"

        paginator = self.aws_iam_client.get_paginator('list_users')
        response_iterator = paginator.paginate()

        for page in response_iterator:
            users.extend(page['Users'])
        
        credentials_unuse_threshold = int(self.iam_user_credentials_unuse_threshold) if self.iam_user_credentials_unuse_threshold else 45
        
        if len(users) > 0:
            for user in users:
                user_name = user['UserName']
                password_last_used = user.get('PasswordLastUsed')
                if password_last_used is not None:
                    current_date = datetime.now(tz=dt.timezone.utc)
                    time_diff = (current_date - password_last_used).days
                    if time_diff >= credentials_unuse_threshold:
                        result.append({
                           "user": self.user_id,
                            "account_arn": self.account_arn,
                            "account": self.account_id,
                            "timestamp": time.time(),
                            "item": user_name,
                            "item_type": "iam_user",
                            "test_name": test_name,
                            "test_result": "issue_found" 
                        })
                    else:
                        result.append({
                            "user": self.user_id,
                            "account_arn": self.account_arn,
                            "account": self.account_id,
                            "timestamp": time.time(),
                            "item": user_name,
                            "item_type": "iam_user",
                            "test_name": test_name,
                            "test_result": "no_issue_found"
                        })
                else:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": user_name,
                        "item_type": "iam_user",
                        "test_name": test_name,
                        "test_result": "no_issue_found" 
                    })
        else:
            result.append({
               "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": "no_iam_user@@" + self.account_id,
                "item_type": "iam_user",
                "test_name": test_name,
                "test_result": "no_issue_found" 
            })
        
        return result
