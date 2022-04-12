import os
import time
import interfaces

from slack_sdk import WebClient

class Tester(interfaces.TesterInterface):
    def __init__(self):
        self.slack_client = WebClient(token=os.environ.get("SLACK_USER_TOKEN"))
        self.team_info = self.slack_client.team_info()
        self.team_id = self.team_info["team"]["id"]

    def declare_tested_service(self) -> str:
        return 'slack'

    def declare_tested_provider(self) -> str:
        return 'slack'

    def run_tests(self) -> list:
        return self.get_public_file_sharing_enabled() + \
               self.get_apps_with_no_privacy_policy() + \
               self.get_apps_with_no_description()

    def get_public_file_sharing_enabled(self):
        test_name = "public_file_sharing_enabled"
        response = self.slack_client.files_list(team_id=self.team_id)
        result = []
        for file in response["files"]:
            if file["public_url_shared"]:
                result.append({
                    "timestamp": time.time(),
                    "account": self.team_id,
                    "item": file["id"],
                    "item_type": "file",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
            else:
                result.append({
                    "timestamp": time.time(),
                    "account": self.team_id,
                    "item": file["id"],
                    "item_type": "file",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
        return result
    
    def get_apps_with_no_privacy_policy(self):
        test_name = "apps_with_no_privacy_policy"
        response = self.slack_client.admin_apps_approved_list(team_id=self.team_id)
        result = []
        for app in response['approved_apps']:
            if not app['app']['privacy_policy_url']:
                result.append({
                    "timestamp": time.time(),
                    "account": self.team_id,
                    "item": app["app"]["id"],
                    "item_type": "app",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
            else:
                result.append({
                    "timestamp": time.time(),
                    "account": self.team_id,
                    "item": app["app"]["id"],
                    "item_type": "app",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })
        return result

    def get_apps_with_no_description(self):
        test_name = "apps_with_no_description"
        response = self.slack_client.admin_apps_approved_list(team_id=self.team_id)
        result = []
        for app in response['approved_apps']:
            if not app['app']['description']:
                result.append({
                    "timestamp": time.time(),
                    "account": self.team_id,
                    "item": app["app"]["id"],
                    "item_type": "app",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
            else:
                result.append({
                    "timestamp": time.time(),
                    "account": self.team_id,
                    "item": app["app"]["id"],
                    "item_type": "app",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })
        return result