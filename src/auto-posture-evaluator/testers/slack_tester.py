import os
import time
import interfaces

from slack_sdk import WebClient

class Tester(interfaces.TesterInterface):
    def __init__(self):
        self.slack_client = WebClient(token=os.environ.get("SLACK_USER_TOKEN"))
        self.account_id = None#tbd
    
    def declare_tested_service(self) -> str:
        return 'slack'

    def declare_tested_provider(self) -> str:
        return 'slack'

    def run_tests(self) -> list:
        return self.get_public_file_sharing_enabled()

    def get_public_file_sharing_enabled(self):
        test_name = "public_file_sharing_enabled"
        response = self.slack_client.files_list()
        result = []
        for file in response["files"]:
            if file["public_url_shared"]:
                result.append({
                    "timestamp": time.time(),
                    "account": self.account_id,
                    "item": file["id"],
                    "item_type": "file",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
            else:
                result.append({
                    "timestamp": time.time(),
                    "account": self.account_id,
                    "item": file["id"],
                    "item_type": "file",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
        return result
