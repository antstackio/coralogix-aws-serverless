import time
import boto3
import interfaces
import json

class Tester(interfaces.TesterInterface):
    def __init__(self) -> None:
        self.user_id = boto3.client('sts').get_caller_identity().get('UserId')
        self.account_arn = boto3.client('sts').get_caller_identity().get('Arn')
        self.account_id = boto3.client('sts').get_caller_identity().get('Account')
        self.aws_emr_client = boto3.client('emr')
        self.aws_kms_client = boto3.client('kms')
        self.emr_clusters = self._get_all_emr_clusters()

    def declare_tested_provider(self) -> str:
        return "aws"

    def declare_tested_service(self) -> str:
        return "emr"
    
    def run_tests(self) -> list:
        return \
            self.emr_cluster_should_have_a_security_configuration() + \
            self.emr_cluster_should_use_kerberos_authentication() + \
            self.emr_in_transit_and_at_rest_encryption_enabled() + \
            self.emr_cluster_should_use_kms_for_s3_sse() + \
            self.emr_cluster_should_upload_logs_to_s3() + \
            self.emr_cluster_should_have_local_disk_encryption() + \
            self.emr_cluster_should_have_encryption_in_transit_enabled() + \
            self.emr_cluster_should_use_kms_for_s3_cse()
    
    def _get_all_emr_clusters(self):
        clusters = []
        paginator = self.aws_emr_client.get_paginator('list_clusters')
        response_iterator = paginator.paginate()

        for page in response_iterator:
            clusters.extend(page['Clusters'])
            
        return clusters
    
    def emr_cluster_should_have_a_security_configuration(self):
        result = []
        test_name = "emr_cluster_should_have_a_security_configuration"

        clusters = self._get_all_emr_clusters()

        for cluster in clusters:
            cluster_id = cluster['Id']
            cluster_state = cluster['Status']['State']

            if cluster_state == "TERMINATING" or cluster_state == "TERMINATED" or cluster_state == "TERMINATED_WITH_ERRORS": pass
            else:
                response = self.aws_emr_client.describe_cluster(ClusterId=cluster_id)
                cluster_info = response['Cluster']
                security_config = cluster_info.get("SecurityConfiguration")

                if security_config is not None:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": cluster_id,
                        "item_type": "emr_cluster",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
                else:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": cluster_id,
                        "item_type": "emr_cluster",
                        "test_name": test_name,
                        "test_result": "issue_found"
                    })
        
        return result

    def emr_cluster_should_use_kerberos_authentication(self):
        result = []
        test_name = "emr_cluster_should_use_keberos_authentication"

        clusters = self._get_all_emr_clusters()

        for cluster in clusters:
            cluster_id = cluster['Id']
            cluster_state = cluster['Status']['State']

            if cluster_state == "TERMINATING" or cluster_state == "TERMINATED" or cluster_state == "TERMINATED_WITH_ERRORS": pass
            else:
                response = self.aws_emr_client.describe_cluster(ClusterId=cluster_id)
                cluster_info = response['Cluster']

                kerberos_attrs = cluster_info.get('KerberosAttributes')

                if kerberos_attrs is not None:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": cluster_id,
                        "item_type": "emr_cluster",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
                else:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": cluster_id,
                        "item_type": "emr_cluster",
                        "test_name": test_name,
                        "test_result": "issue_found"
                    })
        
        return result
    
    def emr_in_transit_and_at_rest_encryption_enabled(self):
        result = []
        test_name = "emr_in_transit_and_at_rest_encryption_enabled"

        clusters = self._get_all_emr_clusters()

        for cluster in clusters:
            cluster_id = cluster['Id']
            cluster_state = cluster['Status']['State']

            if cluster_state == "TERMINATING" or cluster_state == "TERMINATED" or cluster_state == "TERMINATED_WITH_ERRORS": pass
            else:
                response = self.aws_emr_client.describe_cluster(ClusterId=cluster_id)
                cluster_info = response['Cluster']

                security_conf = cluster_info.get('SecurityConfiguration')

                if security_conf is not None:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": cluster_id,
                        "item_type": "emr_cluster",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
                else:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": cluster_id,
                        "item_type": "emr_cluster",
                        "test_name": test_name,
                        "test_result": "issue_found"
                    })
        
        return result

    def emr_cluster_should_use_kms_for_s3_sse(self):
        result = []
        test_name = "emr_cluster_should_use_kms_for_s3_sse"

        clusters = self._get_all_emr_clusters()

        for cluster in clusters:
            cluster_id = cluster['Id']
            cluster_state = cluster['Status']['State']

            if cluster_state == "TERMINATING" or cluster_state == "TERMINATED" or cluster_state == "TERMINATED_WITH_ERRORS": pass
            else:
                response = self.aws_emr_client.describe_cluster(ClusterId=cluster_id)
                security_conf_name = response["Cluster"]["SecurityConfiguration"]
                security_conf = self.aws_emr_client.describe_security_configuration(Name=security_conf_name)
                security_conf = json.loads(security_conf)
                security_conf = security_conf["SecurityConfiguration"]
                if security_conf.get("EncryptionConfiguration").get("AtRestEncryptionConfiguration").get("S3EncryptionConfiguration").get("EncryptionMode")=="SSE-KMS":
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": cluster_id,
                        "item_type": "emr_cluster",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
                else:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": cluster_id,
                        "item_type": "emr_cluster",
                        "test_name": test_name,
                        "test_result": "issue_found"
                    })
        return result
    
    def emr_cluster_should_have_local_disk_encryption_with_cmk(self):
        test_name = "emr_cluster_should_have_local_disk_encryption_with_cmk"
        result = []

        clusters = self._get_all_emr_clusters()

        for cluster in clusters:
            issue_found = False
            cluster_id = cluster['Id']
            cluster_state = cluster['Status']['State']

            if cluster_state == "TERMINATING" or cluster_state == "TERMINATED" or cluster_state == "TERMINATED_WITH_ERRORS": pass
            else:
                response = self.aws_emr_client.describe_cluster(ClusterId=cluster_id)
                security_conf_name = response["Cluster"]["SecurityConfiguration"]
                security_conf = self.aws_emr_client.describe_security_configuration(Name=security_conf_name)
                security_conf = json.loads(security_conf)
                security_conf = security_conf["SecurityConfiguration"]
                kms_key = security_conf.get("EncryptionConfiguration").get("AtRestEncryptionConfiguration").get("S3EncryptionConfiguration").get("AwsKmsKey")
                if kms_key:
                    kms_response = self.aws_kms_client.list_aliases(KeyId=kms_key)
                    for alias in kms_response['Aliases']:
                        if alias['AliasName'] == 'alias/aws/emr':
                            issue_found = True
                            break
                else:
                    issue_found = True
            if issue_found:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": cluster_id,
                    "item_type": "emr_cluster",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
            else:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": cluster_id,
                    "item_type": "emr_cluster",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })
        return result
    
    def emr_cluster_should_upload_logs_to_s3(self):
        result = []
        test_name = "emr_cluster_should_upload_logs_to_s3"

        clusters = self.emr_clusters

        for cluster in clusters:
            cluster_id = cluster['Id']
            response = self.aws_emr_client.describe_cluster(ClusterId=cluster_id)
            cluster_obj = response['Cluster']

            log_uri = cluster_obj.get("LogUri")

            if log_uri is not None:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": cluster_id,
                    "item_type": "emr_cluster",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })
            else:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": cluster_id,
                    "item_type": "emr_cluster",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
        
        return result

    def emr_cluster_should_have_local_disk_encryption(self):
        test_name = "emr_cluster_should_have_local_disk_encryption"
        result = []

        clusters = self._get_all_emr_clusters()

        for cluster in clusters:
            cluster_id = cluster['Id']
            cluster_state = cluster['Status']['State']

            if cluster_state == "TERMINATING" or cluster_state == "TERMINATED" or cluster_state == "TERMINATED_WITH_ERRORS": pass
            else:
                response = self.aws_emr_client.describe_cluster(ClusterId=cluster_id)
                security_conf_name = response["Cluster"]["SecurityConfiguration"]
                security_conf = self.aws_emr_client.describe_security_configuration(Name=security_conf_name)
                security_conf = json.loads(security_conf)
                security_conf = security_conf["SecurityConfiguration"]
                local_encryption = security_conf.get("EncryptionConfiguration").get("AtRestEncryptionConfiguration").get("LocalDiskEncryptionConfiguration")
                if local_encryption:
                    result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": cluster_id,
                    "item_type": "emr_cluster",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                    })
                else:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": cluster_id,
                        "item_type": "emr_cluster",
                        "test_name": test_name,
                        "test_result": "issue_found"
                    })
        return result

    def emr_cluster_should_have_encryption_in_transit_enabled(self):
        test_name = "emr_cluster_should_have_encryption_in_transit_enabled"
        result = []
        clusters = self._get_all_emr_clusters()

        for cluster in clusters:
            cluster_id = cluster['Id']
            cluster_state = cluster['Status']['State']

            if cluster_state == "TERMINATING" or cluster_state == "TERMINATED" or cluster_state == "TERMINATED_WITH_ERRORS": pass
            else:
                response = self.aws_emr_client.describe_cluster(ClusterId=cluster_id)
                security_conf_name = response["Cluster"]["SecurityConfiguration"]
                security_conf = self.aws_emr_client.describe_security_configuration(Name=security_conf_name)
                security_conf = json.loads(security_conf)
                security_conf = security_conf["SecurityConfiguration"]
                encryption_enabled = security_conf.get("EncryptionConfiguration").get("EnableInTransitEncryption")
                if encryption_enabled:
                    result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": cluster_id,
                    "item_type": "emr_cluster",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                    })
                else:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": cluster_id,
                        "item_type": "emr_cluster",
                        "test_name": test_name,
                        "test_result": "issue_found"
                    })
        return result
    
    def emr_cluster_should_use_kms_for_s3_cse(self):
        result = []
        test_name = "emr_cluster_should_use_kms_for_s3_cse"

        clusters = self.emr_clusters

        for cluster in clusters:
            cluster_id = cluster['Id']
            cluster_state = cluster['Status']['State']

            if cluster_state == "TERMINATING" or cluster_state == "TERMINATED" or cluster_state == "TERMINATED_WITH_ERRORS": pass
            else:
                response = self.aws_emr_client.describe_cluster(ClusterId=cluster_id)
                cluster_obj = response['Cluster']
                security_configuration = cluster_obj.get('SecurityConfiguration')

                if security_configuration is not None:
                    response = self.aws_emr_client.describe_security_configuration(Name=security_configuration)
                    security_configuration_details = json.loads(response['SecurityConfiguration'])

                    if security_configuration_details.get("EncryptionConfiguration").get("AtRestEncryptionConfiguration").get("S3EncryptionConfiguration").get("EncryptionMode") == "CSE-KMS":
                        result.append({
                            "user": self.user_id,
                            "account_arn": self.account_arn,
                            "account": self.account_id,
                            "timestamp": time.time(),
                            "item": cluster_id,
                            "item_type": "emr_cluster",
                            "test_name": test_name,
                            "test_result": "no_issue_found"
                        })
                    else:
                        result.append({
                            "user": self.user_id,
                            "account_arn": self.account_arn,
                            "account": self.account_id,
                            "timestamp": time.time(),
                            "item": cluster_id,
                            "item_type": "emr_cluster",
                            "test_name": test_name,
                            "test_result": "issue_found"
                        })
                else: pass

        return result
