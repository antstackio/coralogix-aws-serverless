import time
from typing import List
import interfaces
import boto3

class Tester(interfaces.TesterInterface):
    def __init__(self) -> None:
        self.user_id = boto3.client('sts').get_caller_identity().get('UserId')
        self.account_arn = boto3.client('sts').get_caller_identity().get('Arn')
        self.account_id = boto3.client('sts').get_caller_identity().get('Account')
        self.aws_elbs_client = boto3.client('elb')
        self.aws_elbsv2_client = boto3.client('elbv2')
        self.elbs = self._get_all_elb()
        self.elbsv2 = self._get_all_elbv2()

    def declare_tested_service(self) -> str:
        return "elb"

    def declare_tested_provider(self) -> str:
        return "aws"

    def run_tests(self) -> list:
        pass
    
    def _get_all_elbv2(self) -> List:
        elbs = self.aws_elbsv2_client.describe_load_balancers()
        return elbs['LoadBalancers']
    
    def _get_all_elb(self) -> List:
        elbs = self.aws_elbs_client.describe_load_balancers()
        return elbs['LoadBalancerDescriptions']
    
    def get_elbv2_internet_facing(self) -> List: 
        elbs = self.elbsv2
        test_name = "elbv2_is_not_internet_facing"
        result = []

        for elb in elbs:
            if elb['Scheme'] == 'internet-facing':
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": elb['LoadBalancerArn'],
                    "item_type": "aws_elbv2",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
            else:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": elb['LoadBalancerArn'],
                    "item_type": "aws_elbv2",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })
        
        return result
    
    def get_elb_generating_access_log(self) -> List:
        elbs = self.elbs
        test_name = "elb_is_generating_access_log"
        result = []

        for elb in elbs:
            load_balancer_name = elb['LoadBalancerName']
            response = self.aws_elbs_client.describe_load_balancer_attributes(LoadBalancerName=load_balancer_name)
            if response['LoadBalancerAttributes']['AccessLog']['Enabled']:
                # no issue
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": load_balancer_name,
                    "item_type": "aws_elb",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })
            else:
                # issue
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": load_balancer_name,
                    "item_type": "aws_elb",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
        
        return result
    
    def get_alb_using_secure_listener(self) -> List:
        test_name = "alb_is_using_secure_listeners"
        elbs = self.elbsv2
        result = []

        for elb in elbs:
            # check elbv2 type and only let ALB pass
            if elb['Type'] == "application":
                load_balancer_arn = elb['LoadBalancerArn']
                response = self.aws_elbsv2_client.describe_listeners(LoadBalancerArn=load_balancer_arn)
                listeners = response['Listeners']
                secure_listener_count = 0
                for listener in listeners:
                    if listener['Protocol'] == "HTTPS":
                        secure_listener_count += 1
                
                if secure_listener_count == len(listeners):
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": load_balancer_arn,
                        "item_type": "aws_elbv2",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
                else:
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": load_balancer_arn,
                        "item_type": "aws_elbv2",
                        "test_name": test_name,
                        "test_result": "issue_found"
                    })
            else:
                continue
        
        return result
    
    def get_elbv2_generating_access_log(self) -> List:
        test_name = "elbv2_is_generating_access_logs"
        result = []
        elbs = self.elbsv2

        for elb in elbs:
            elb_arn = elb['LoadBalancerArn']
    
            elb_type = elb['Type']
            if elb_type == 'application' or elb_type == 'network':
                elb_attributes = self.aws_elbsv2_client.describe_load_balancer_attributes(LoadBalancerArn=elb_arn)
                attributes = elb_attributes['Attributes']
                for i in attributes:
                    if i['Key'] == 'access_logs.s3.enabled':
                        if i['Value'] == 'false':
                            result.append({
                            "user": self.user_id,
                            "account_arn": self.account_arn,
                            "account": self.account_id,
                            "timestamp": time.time(),
                            "item": elb_arn,
                            "item_type": "aws_elbv2",
                            "test_name": test_name,
                            "test_result": "issue_found"
                            })
                        else:
                            result.append({
                            "user": self.user_id,
                            "account_arn": self.account_arn,
                            "account": self.account_id,
                            "timestamp": time.time(),
                            "item": elb_arn,
                            "item_type": "aws_elbv2",
                            "test_name": test_name,
                            "test_result": "no_issue_found"
                            })
                    else: pass
            else:
                pass
        return result

    def get_elb_listeners_using_tls(self) -> List:
        test_name = "elb_listeners_using_tls_v1.2"
        result = []
        elbs = self.elbs

        for elb in elbs:
            elb_name = elb['LoadBalancerName']
            listeners = elb['ListenerDescriptions']
            secure_listeners_count = 0
            for listener in listeners:
                policy_names = listener['PolicyNames']
                
                if len(policy_names) > 0:
                    response = self.aws_elbs_client.describe_load_balancer_policies(PolicyNames=policy_names, LoadBalancerName=elb_name)
                    policy_descriptions = response['PolicyDescriptions']
                    print(policy_descriptions)
                    found_tls_v12_count = 0
                        # look into policy attrs
                    for policy_description in policy_descriptions:
                        policy_attrs = policy_description['PolicyAttributeDescriptions']
                        for attr in policy_attrs:
                            if attr['AttributeName'] == 'Protocol-TLSv1.2' and attr['AttributeValue'] == 'true':
                                found_tls_v12_count += 1
                                break
                    if found_tls_v12_count == len(policy_descriptions):
                        secure_listeners_count += 1
                else: pass            
            if secure_listeners_count == len(listeners):
                # secure
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": elb_name,
                    "item_type": "aws_elb",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })
            else:
                # issue found
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": elb_name,
                    "item_type": "aws_elb",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
        return result

    def get_elb_listeners_securely_configured(self) -> List:
        test_name = "elb_listeners_securely_configurd"
        result = []

        elbs = self.elbs

        for elb in elbs:
            listeners = elb['ListenerDescriptions']
            loab_balancer_name = elb['LoadBalancerName']
            for i in listeners:
                listener = i['Listener']
                if listener['InstanceProtocol'] == 'HTTPS' and listener['Protocol'] == 'HTTPS':
                    # secure
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": loab_balancer_name,
                        "item_type": "aws_elb",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
                elif listener['InstanceProtocol'] == 'SSL' and listener['Protocol'] == 'SSL':
                    # secure
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": loab_balancer_name,
                        "item_type": "aws_elb",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
                elif listener['InstanceProtocol'] == 'HTTPS' and listener['Protocol'] == 'SSL':
                    # secure
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": loab_balancer_name,
                        "item_type": "aws_elb",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
                elif listener['InstanceProtocol'] == 'SSL' and listener['Protocol'] == 'HTTPS':
                    # secure
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": loab_balancer_name,
                        "item_type": "aws_elb",
                        "test_name": test_name,
                        "test_result": "no_issue_found"
                    })
                else:
                    # insecure
                    result.append({
                        "user": self.user_id,
                        "account_arn": self.account_arn,
                        "account": self.account_id,
                        "timestamp": time.time(),
                        "item": loab_balancer_name,
                        "item_type": "aws_elb",
                        "test_name": test_name,
                        "test_result": "issue_found"
                    })
        
        return result
