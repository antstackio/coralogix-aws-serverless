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
        all_vpcs = self._get_all_vpc_ids(self.instances)
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
            self.get_inbound_dns_access(all_inbound_permissions) + \
            self.get_inbound_elasticsearch_access(all_inbound_permissions) + \
            self.get_inbound_smtp_access(all_inbound_permissions) + \
            self.get_inbound_telnet_access(all_inbound_permissions) + \
            self.get_inbound_rpc_access(all_inbound_permissions) + \
            self.get_inbound_ftp_access(all_inbound_permissions) + \
            self.get_inbound_udp_netbios(all_inbound_permissions) + \
            self.get_inbound_cifs_access(all_inbound_permissions) + \
            self.get_outbound_access_to_all_ports(all_vpcs) + \
            self.get_vpc_default_security_group_restrict_traffic(all_vpcs) + \
            self.get_inbound_oracle_access(all_inbound_permissions) + \
            self.get_inbound_icmp_access(all_inbound_permissions) + \
            self.get_security_group_allows_ingress_from_anywhere(all_inbound_permissions)
    
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
                    i['security_group'] = security_group
                    all_inbound_permissions.append(i)
        return all_inbound_permissions

    def _get_inbound_port_access(self, all_inbound_permissions, target_port, test_name, protocol="tcp"):
        result = []
        instances = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] <= target_port and permission['ToPort'] >= target_port and permission['IpProtocol'] == protocol, all_inbound_permissions))))
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
        result = []
        instances = []
        NAMERESPORT = 137
        SESSIONPORT = 139
        instancse_137 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] <= NAMERESPORT and permission['ToPort'] >= NAMERESPORT and permission['IpProtocol'] == 'tcp', all_inbound_permissions))))
        instances.extend(instancse_137)
        instancse_139 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] <= SESSIONPORT and permission['ToPort'] >= SESSIONPORT and permission['IpProtocol'] == 'tcp', all_inbound_permissions))))
        print(f"{test_name} - {instances}")
        instances.extend(instancse_139)
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

    def get_inbound_dns_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_dns_access_restricted"
        result = []
        target_port = 53
        instances = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] <= target_port and permission['ToPort'] >= target_port and (permission['IpProtocol'] == "tcp" or permission['IpProtocol'] == "udp"), all_inbound_permissions))))
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
        result = []
        instances = []

        instances_137_to_138 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] == 137 and permission['ToPort'] == 138 and permission['IpProtocol'] == 'udp', all_inbound_permissions))))
        instances.extend(instances_137_to_138)
        instancse_137 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] == 137 and permission['ToPort'] == 137 and permission['IpProtocol'] == 'udp', all_inbound_permissions))))
        instances.extend(instancse_137)
        instancse_138 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] == 138 and permission['ToPort'] == 138 and permission['IpProtocol'] == 'udp', all_inbound_permissions))))
        instances.extend(instancse_138)
        instancse_139 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] == 139 and permission['ToPort'] == 139 and permission['IpProtocol'] == 'tcp', all_inbound_permissions))))
        instances.extend(instancse_139)
        instancse_445 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] == 445 and permission['ToPort'] == 445 and permission['IpProtocol'] == 'tcp', all_inbound_permissions))))
        instances.extend(instancse_445)
        instancse_3020 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] == 3020 and permission['ToPort'] == 3020 and permission['IpProtocol'] == 'tcp', all_inbound_permissions))))
        instances.extend(instancse_3020)

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
    
    def get_inbound_elasticsearch_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_elasticsearch_access_restricted"
        results = []
        instances = []
        PORT9200 = 9200
        PORT9300 = 9300
        instances_9200 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] <= PORT9200 and permission['ToPort'] >= PORT9200 and permission['IpProtocol'] == 'tcp', all_inbound_permissions))))
        instances.extend(instances_9200)
        instances_9300 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] <= PORT9300 and permission['ToPort'] >= PORT9300 and permission['IpProtocol'] == 'tcp', all_inbound_permissions))))
        instances.extend(instances_9300)

        instances = set(instances)

        for i in instances:
            results.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": i,
                "item_type": "ec2_instance",
                "test_name": test_name
            })
        
        if len(results) == 0:
            results.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": None,
                "item_type": "ec2_instance",
                "test_name": test_name
            })
    
        return results
    
    def get_inbound_smtp_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_smtp_access_restricted"
        result = []
        PORT25 = 25
        PORT587 = 587
        instances = []
        instances_25 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] <= PORT25 and permission['ToPort'] >= PORT25 and permission['IpProtocol'] == 'tcp', all_inbound_permissions))))
        instances.extend(instances_25)
        instances_587 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] <= PORT587 and permission['ToPort'] >= PORT587 and permission['IpProtocol'] == 'tcp', all_inbound_permissions))))
        instances.extend(instances_587)
        
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

    def get_inbound_rpc_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_rpc_access_restricted"
        return self._get_inbound_port_access(all_inbound_permissions, 135, test_name)

    def get_inbound_ftp_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_ftp_access_restricted"
        result = []
        instances = []
        DATAPORT = 20
        COMMANDPORT = 21
        instances_20 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] <= DATAPORT and permission['ToPort'] >= DATAPORT and permission['IpProtocol'] == 'tcp', all_inbound_permissions))))
        instances.extend(instances_20)
        instances_21 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] <= COMMANDPORT and permission['ToPort'] >= COMMANDPORT and permission['IpProtocol'] == 'tcp', all_inbound_permissions))))
        instances.extend(instances_21)

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

    def get_inbound_udp_netbios(self, all_inbound_permissions):
        test_name = "ec2_inbound_udp_netbios_access_restricted"
        result = []
        instances = []
        NAMERESPORT = 137
        DATAGRAMPORT = 138
        
        instancse_137 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] <= NAMERESPORT and permission['ToPort'] >= NAMERESPORT and permission['IpProtocol'] == 'udp', all_inbound_permissions))))
        instances.extend(instancse_137)
        instancse_138 = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['FromPort'] <= DATAGRAMPORT and permission['ToPort'] >= DATAGRAMPORT and permission['IpProtocol'] == 'udp', all_inbound_permissions))))
        instances.extend(instancse_138)
        
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

    def _get_all_vpc_ids(self, instances):
        vpc_ids = []
        for instance in instances:
            vpc_ids.append(instance.vpc_id)
        vpc_ids = set(vpc_ids)
        return vpc_ids

    def get_outbound_access_to_all_ports(self, all_vpcs):
        test_name = "ec2_outbound_access_to_all_ports_restricted"
        result = []
        security_groups = []
        effective_security_group = []
        for vpc in all_vpcs:
            vpc = self.aws_ec2_resource.Vpc(vpc)
            security_groups.extend(vpc.security_groups.all())

        for security_group in security_groups:
            outbound_permissions = security_group.ip_permissions_egress
            for outbound_permission in outbound_permissions:
                if outbound_permission['IpProtocol'] == '-1':
                    effective_security_group.append(security_group.id)
        
        effective_security_group = set(effective_security_group)
        for i in effective_security_group:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": i,
                "item_type": "ec2_security_group",
                "test_name": test_name
            })

        if len(result) == 0:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": None,
                "item_type": "ec2_security_group",
                "test_name": test_name
            })

        return result 

    def get_vpc_default_security_group_restrict_traffic(self, all_vpcs):
        test_name = "vpc_default_security_group_restrict_all_traffic"
        result = []

        for vpc in all_vpcs:
            vpc = self.aws_ec2_resource.Vpc(vpc)
            security_groups = vpc.security_groups.all()

            for security_group in security_groups:
                if security_group.group_name == "default":
                    inbound_permissions = security_group.ip_permissions
                    outbound_permissions = security_group.ip_permissions_egress
                    if (len(inbound_permissions) == 1 and len(outbound_permissions) == 1) and (inbound_permissions[0]['IpProtocol'] == '-1' and outbound_permissions[0]['IpProtocol'] == '-1'):
                        result.append({
                            "user": self.user_id,
                            "account_arn": self.account_arn,
                            "account": self.account_id,
                            "timestamp": time.time(),
                            "item": vpc.id,
                            "item_type": "aws_vpc",
                            "test_name": test_name
                        })
                else:
                    continue
        if len(result) == 0:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": None,
                "item_type": "aws_vpc",
                "test_name": test_name
            })
        return result
    
    def get_inbound_oracle_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_oracle_access_restricted"
        return self._get_inbound_port_access(all_inbound_permissions, 1521, test_name)

    def get_inbound_icmp_access(self, all_inbound_permissions):
        test_name = "ec2_inbound_icmp_access_restricted"
        result = []
        instances = list(map(lambda i: i['instance'].id, list(filter(lambda permission: permission['IpProtocol'] == "icmp", all_inbound_permissions))))
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

    def get_security_group_allows_ingress_from_anywhere(self, all_inbound_permissions):
        test_name = "security_group_allows_ingress_to_remote_administration_ports_from_anywhere"
        result = []
        security_groups = []
        for i in all_inbound_permissions:
            if (i['FromPort'] == 22 and i['ToPort'] == 22) or (i['FromPort'] == 3389 and i['ToPort'] == 3389):
                if len(i['IpRanges']) == 1 and i['IpRanges'][0]['CidrIp'] == '0.0.0.0/0':
                    security_groups.append(i['security_group']['GroupId'])
            else:
                continue
        
        if len(security_groups) == 0:
            result.append({
                "user": self.user_id,
                "account_arn": self.account_arn,
                "account": self.account_id,
                "timestamp": time.time(),
                "item": None,
                "item_type": "ec2_security_group",
                "test_name": test_name
            })
        else:
            security_groups = set(security_groups)
            for s in security_groups:
                result.append({
                    "user": self.user_id,
                    "account_arn": self.account_arn,
                    "account": self.account_id,
                    "timestamp": time.time(),
                    "item": s,
                    "item_type": "ec2_security_group",
                    "test_name": test_name
                })
        return result
