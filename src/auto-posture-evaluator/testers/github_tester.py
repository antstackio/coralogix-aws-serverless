import json
from operator import le
import os
import time
from urllib import response
import requests
import interfaces
from datetime import date, datetime

class Tester(interfaces.TesterInterface):
    def __init__(self):
        self.github_authorization_token = os.environ.get('AUTOPOSTURE_GITHUB_TOKEN')
        self.github_organizations = os.environ.get('AUTOPOSTURE_GITHUB_ORGANIZATIONS')
        self.tests = {
            "users_without_mfa": {
                "method": self.get_users_without_mfa,
                "result_item_type": "github_user"
            },
            "forking_enabled_repos": {
                "method": self.get_forkable_repositories,
                "result_item_type": "github_repository"
            },
            "too_many_admin_users_per_org": {
                "method": self.check_for_too_many_admin_users,
                "result_item_type": "github_organization"
            },
            "two_factor_authentication_is_enforced":{
                "method": self.get_2fa_authentication_enforced,
                "result_item_type": "github_organization"
            },
            "base_permissions_not_set_to_admin":{
                "method": self.get_base_permission_not_admin,
                "result_item_type": "github_organization"
            },
            "members_can_not_create_public_repositories": {
                "method": self.get_members_can_not_create_public_repos,
                "result_item_type": "github_organization"
            },
            "organization's_domains_are_not_verified": {
                "method": self.get_org_domains_are_not_verified,
                "result_item_type": "github_organization"
            },
            "github_pages_is_disabled": {
                "method": self.get_github_pages_disabled,
                "result_item_type": "github_repository"
            },
            "members_without_signing_gpg_keys": {
                "method": self.get_members_without_gpg_keys,
                "result_item_type": "github_organization"
            },
            "code_security_alerts_are_enabled": {
                "method": self.get_code_security_alerts_are_enabled,
                "result_item_type": "github_repository"
            },
        }
        self.request_headers = {
            "Authorization": "token " + self.github_authorization_token,
            "Accept": "application/vnd.github.v3+json"
        }

    def declare_tested_service(self) -> str:
        return 'github'

    def declare_tested_provider(self) -> str:
        return 'github'

    def run_tests(self) -> list:
        results = []
        organizations_list = self.get_organizations_list(self.github_organizations)
        for test_name in self.tests.keys():
            for organization in organizations_list:
                raw_results = self.tests[test_name]["method"](organization)
                if len(raw_results) > 0:
                    for item in raw_results:
                        if item["issue"]:
                            results.append({
                                "timestamp": time.time(),
                                "account": organization,
                                "item": item["item"],
                                "item_type": self.tests[test_name]["result_item_type"],
                                "test_name": test_name,
                                "test_result": "issue_found"
                            })
                        else:
                            results.append({
                                "timestamp": time.time(),
                                "account": organization,
                                "item": item["item"],
                                "item_type": self.tests[test_name]["result_item_type"],
                                "test_name": test_name,
                                "test_result": "no_issue_found"})

        return results

    def get_organizations_list(self, organizations):
        if organizations is not None:
            return str(organizations).split(',')
        else:
            raw_results = requests.get(headers=self.request_headers, url='https://api.github.com/user/orgs')
            raw_results_obj = raw_results.json()
            result = []
            for organization in raw_results_obj:
                result.append(organization["login"])
            return result

    def get_users_without_mfa(self, organization):
        result = []
        raw_api_result_all_users = requests.get(headers=self.request_headers, url='https://api.github.com/orgs/' + organization + '/members')
        raw_api_result_all_users_obj = raw_api_result_all_users.json()
        raw_api_result_2fa_disabled = requests.get(headers=self.request_headers, url='https://api.github.com/orgs/' + organization + '/members?filter=2fa_disabled')
        raw_api_result_2fa_disabled_obj = raw_api_result_2fa_disabled.json()
        for user in raw_api_result_all_users_obj:
            if user["login"] in [u.login for u in raw_api_result_2fa_disabled_obj]:
                result.append({"item": user["login"] + "@@" + organization, "issue": True})
            else:
                result.append({"item": user["login"] + "@@" + organization, "issue": False})

        return result

    def get_forkable_repositories(self, organization):
        result = []
        raw_api_result = requests.get(headers=self.request_headers, url='https://api.github.com/orgs/' + organization + '/repos')
        raw_api_result_obj = raw_api_result.json()
        for repo in raw_api_result_obj:
            if repo["allow_forking"]:
                result.append({"item": repo["name"], "issue": True})
            else:
                result.append({"item": repo["name"], "issue": False})

        return result

    def check_for_too_many_admin_users(self, organization):
        result = []
        org_admins = []
        raw_api_result = requests.get(headers=self.request_headers, url='https://api.github.com/orgs/' + organization + '/members?role=admin')
        raw_api_result_obj = raw_api_result.json()
        for user in raw_api_result_obj:
            org_admins.append(user["login"])
        if len(org_admins) > 15:
            result.append({"item": organization, "issue": True})
        else:
            result.append({"item": organization, "issue": False})

        return result

    def get_2fa_authentication_enforced(self, organization):
        result = []
        raw_api_response = requests.get(headers=self.request_headers, url='https://api.github.com/orgs/' + organization)
        raw_api_response_obj = raw_api_response.json()

        if raw_api_response_obj['two_factor_requirement_enabled']:
            result.append({"item": organization, "issue": False})
        else:
            result.append({"item": organization, "issue": True})
        
        return result

    def get_base_permission_not_admin(self, organization):
        result = []
        raw_api_response = requests.get(headers=self.request_headers, url='https://api.github.com/orgs/' + organization)
        raw_api_response_obj = raw_api_response.json()

        if raw_api_response_obj['default_repository_permission'].lower() == 'admin':
            result.append({"item": organization, "issue": True})
        else:
            result.append({"item": organization, "issue": False})
        
        return result

    def get_members_can_not_create_public_repos(self, organization):
        result = []
        raw_api_response = requests.get(headers=self.request_headers, url='https://api.github.com/orgs/' + organization)
        org_details = raw_api_response.json()

        if org_details['members_can_create_public_repositories']:
            result.append({"item": organization, "issue": True})
        else:
            result.append({"item": organization, "issue": False})
        
        return result

    def get_org_domains_are_not_verified(self, organization):
        result = []
        raw_api_response = requests.get(headers=self.request_headers, url='https://api.github.com/orgs/' + organization)
        org_details =  raw_api_response.json()
        if org_details['is_verified']:
            result.append({"item": organization, "issue": False})
        else:
            result.append({"item": organization, "issue": True})
        
        return result

    def get_github_pages_disabled(self, organization):
        result = []
        raw_api_response = requests.get(headers=self.request_headers, url="https://api.github.com/orgs/" + organization + "/repos")
        repos_details = raw_api_response.json()
        
        for repo in repos_details:
            repo_name = repo['name']
            has_pages = repo['has_pages']
            if has_pages:
                result.append({"item": repo_name, "issue": True})
            else:
                result.append({"item": repo_name, "issue": False})
        
        return result
    
    def get_members_without_gpg_keys(self, organization):
        result = []
        raw_api_response = requests.get(headers=self.request_headers, url='https://api.github.com/orgs/' + organization + '/members')
        org_members = raw_api_response.json()
        
        members_with_gpg_keys_count = 0
        for member in org_members:
            username = member['login']
            response = requests.get(headers=self.request_headers, url='http://api.github.com/users/' + username + '/gpg_keys')
            user_gpg_keys = response.json()
            if len(user_gpg_keys) > 0:
                members_with_gpg_keys_count += 1
            else: pass

        if members_with_gpg_keys_count == len(org_members):
            result.append({"item": organization, "issue": False})
        else:
            result.append({"item": organization, "issue": True})

        return result
    
    def get_code_security_alerts_are_enabled(self, organization):
        result = []
        raw_api_response = requests.get(headers=self.request_headers, url="https://api.github.com/orgs/" + organization + "/repos")
        repos_details = raw_api_response.json()

        for repo in repos_details:
            repo_name = repo['name']
            owner = repo['owner']['login']
            raw_response = requests.get(headers=self.request_headers, url="https://api.github.com/repos/" + owner + "/" + repo_name + "/vulnerability-alerts")
            response_code = raw_response.status_code
            
            if response_code == 204:
                result.append({"item": repo_name, "issue": False})
            else:
                result.append({"item": repo_name, "issue": True})
        
        return result
