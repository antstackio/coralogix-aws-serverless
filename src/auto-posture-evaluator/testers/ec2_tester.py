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
        all_inbound_permissions = self._get_all_inbound_permissions(self.instances)
        return \
            self.get_inbound_http_access(all_inbound_permissions) + \
            self.get_inbound_https_access(all_inbound_permissions) + \
            self.get_inbound_mongodb_access(all_inbound_permissions) + \
            self.get_inbound_mysql_access(all_inbound_permissions) + \
            self.get_inbound_mssql_access(all_inbound_permissions) + \
            self.get_inbound_ssh_access(all_inbound_permissions) + \
            self.get_inbound_rdp_access(all_inbound_permissions) + \
            self.get_inbound_postgresql_access(all_inbound_permissions) + \
            self.get_inbound_tcp_netbios_access(all_inbound_permissions) + \
            self.get_inbound_dns_access(all_inbound_permissions)
    
    def _get_all_instance_ids(self, instances):
        return list(map(lambda i: i.id, list(instances)))

    def _get_all_inbound_permissions(self, instances):
        all_inbound_permissions = []
        for instance in instances:
            security_groups = instance.security_groups
            for security_group in security_groups:
                inbound_permissions = self.aws_ec2_resource.SecurityGroup(security_group['GroupId']).ip_permissions
                for i in inbound_permissions:
                    i['instance'] = instance
                    all_inbound_permissions.append(i)
        return all_inbound_permissions

    def _get_inbound_port_access(self, all_inbound_permissions, target_port, test_name, protocol="tcp"):
        result = []
        instances = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] == target_port and permission['ToPort'] == target_port and permission['IpProtocol'] == protocol, all_inbound_permissions))))
        for i in instances:
            result.append({
               "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": i,
                "item_type": "ec2_instance",
                "test_name": test_name 
            })
        if len(result) == 0:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": None,
                "item_type": "ec2_instance",
                "test_name": test_name
            })
        return result

    def get_inbound_http_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_http_access_restricted"
        return self._get_inbound_port_access(all_inbound_permissions, 80, test_name)

    def get_inbound_https_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_https_access_restricted"
        return self._get_inbound_port_access(all_inbound_permissions, 443, test_name)
    
    def get_inbound_mongodb_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_mongodb_access_restricted"
        return self._get_inbound_port_access(all_inbound_permissions, 27017, test_name)
    
    def get_inbound_mysql_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_mysql_access_restricted"
        return self._get_inbound_port_access(all_inbound_permissions, 3306, test_name)
    
    def get_inbound_mssql_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_mssql_access_restricted"
        return self._get_inbound_port_access(all_inbound_permissions, 1433, test_name)

    def get_inbound_ssh_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_ssh_access_restricted"
        return self._get_inbound_port_access(all_inbound_permissions, 22, test_name)

    def get_inbound_rdp_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_rdp_access_restricted"
        return self._get_inbound_port_access(all_inbound_permissions, 3389, test_name)
    
    def get_inbound_postgresql_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_postgresql_access_restricted"
        return self._get_inbound_port_access(all_inbound_permissions, 5432, test_name)

    def get_inbound_tcp_netbios_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_tcp_netbios_access_restricted"
        return self._get_inbound_port_access(all_inbound_permissions, 139, test_name)

    def get_inbound_dns_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_dns_access_restricted"
        result = []
        target_port = 53
        instances = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] == target_port and permission['ToPort'] == target_port and (permission['IpProtocol'] == "tcp" or permission['IpProtocol'] == "udp"), all_inbound_permissions))))
        instances = set(instances)
        for i in instances:
            result.append({
               "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": i,
                "item_type": "ec2_instance",
                "test_name": test_name 
            })
        if len(result) == 0:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": None,
                "item_type": "ec2_instance",
                "test_name": test_name
            })
        return result

    def get_inbound_telnet_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_telnet_access_restricted"
        return self._get_inbound_port_access(all_inbound_permissions, 23, test_name)

    def get_inbound_cifs_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_cifs_access_restricted"
        return self._get_inbound_port_access(all_inbound_permissions, 445, test_name)
    
    def get_inbound_elasticsearch_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_elasticsearch_access_restricted"
        return self._get_inbound_port_access(all_inbound_permissions, 9200, test_name)
    
    def get_inbound_smtp_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_smtp_access_restricted"
        result = []
        port_25 = 25
        port_587 = 587
        port_2525 = 2525
        instances = []
        instances_25 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] == port_25 and permission['ToPort'] == port_25 and permission['IpProtocol'] == 'tcp', all_inbound_permissions))))
        instances.extend(instances_25)
        instances_587 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] == port_587 and permission['ToPort'] == port_587 and permission['IpProtocol'] == 'tcp', all_inbound_permissions))))
        instances.extend(instances_587)
        instances_2525 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] == port_2525 and permission['ToPort'] == port_2525 and permission['IpProtocol'] == 'tcp', all_inbound_permissions))))
        instances.extend(instances_2525)
        instances = set(instances)

        for i in instances:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": i,
                "item_type": "ec2_instance",
                "test_name": test_name 
            })
        if len(result) == 0:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": None,
                "item_type": "ec2_instance",
                "test_name": test_name
            })
        return result
