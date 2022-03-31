from cgi import test
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
            self.emr_cluster_should_use_kms_for_s3_sse()
    
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
            issue_found = True
            cluster_id = cluster['Id']
            cluster_state = cluster['Status']['State']

            if cluster_state == "TERMINATING" or cluster_state == "TERMINATED" or cluster_state == "TERMINATED_WITH_ERRORS": pass
            else:
                response = self.aws_emr_client.describe_cluster(ClusterId=cluster_id)
                security_conf_name = response["Cluster"]["SecurityConfiguration"]
                security_conf = self.aws_emr_client.describe_security_configuration(Name=security_conf_name)
                security_conf = json.loads(security_conf)
                kms_key = security_conf.get("EncryptionConfiguration").get("AtRestEncryptionConfiguration").get("S3EncryptionConfiguration").get("AwsKmsKey")
                if kms_key:
                    key_details = self.aws_kms_client.describe_key(KeyId=kms_key)
                    if key_details["KeyMetadata"]["KeyManager"] == "CUSTOMER":
                        issue_found = False
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