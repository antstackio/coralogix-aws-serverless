import os
import time
import interfaces
from google.oauth2 import service_account
from googleapiclient.discovery import build

class Tester(interfaces.TesterInterface):
    def __init__(self) -> None:
        self.ACCOUNT_ADMIN_EMAIL = os.environ.get("AUTOPOSTURE_GSUITE_ADMIN_EMAIL")
        self.SERVICE_ACCOUNT = "service_account.json"
        self.user_id = self._get_user_id()

        self.SCOPES = {}
    def declare_tested_provider(self) -> str:
        return "google"
    
    def declare_tested_service(self) -> str:
        return "gsuite"
    
    def run_tests(self) -> list:
        return \
            self.detect_single_super_admin_account() + \
            self.detect_2sv_verification_enforced()
    
    def _get_user_id(self):
        credentials = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT)
        people_service = build('people', 'v1', credentials=credentials)
        result = people_service.people().get(resourceName='people/me', personFields='metadata').execute()
        resource_name = result['resourceName']
        user_id = resource_name.split('/')[-1]

        return user_id

    def _append_gsuite_test_result(self, item, item_type, test_name, issue_status):
        return {
            "user": self.user_id,
            "timestamp": time.time(),
            "item": item,
            "item_type": item_type,
            "test_name": test_name,
            "test_result": issue_status
        }
    
    def detect_single_super_admin_account(self):
        result = []
        test_name = "single_super_admin_account"

        SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']
        credentials = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT, scopes=SCOPES, subject='admin@cparanoid.com')
        service = build('admin', 'directory_v1', credentials=credentials)
        response = service.users().list(customer='my_customer', orderBy='email').execute()
        
        users = response['users']
        admin_users = list(filter(lambda user: user['isAdmin'] == True, users))
        
        if len(admin_users) > 1:
            result.append(self._append_gsuite_test_result("user", "google_admin", test_name, "issue_found"))
        else:
            result.append(self._append_gsuite_test_result("user", "google_admin", test_name, "no_issue_found"))
        
        return result

    def detect_2sv_verification_enforced(self):
        result = []
        test_name = "two_step_verification_admin_enforcement"

        SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

        credentials = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT, scopes=SCOPES, subject='admin@cparanoid.com')
        service = build('admin', 'directory_v1', credentials=credentials)
        response = service.users().list(customer='my_customer', orderBy='email').execute()
        
        user = response['users'][0]

        if user['isEnforcedIn2Sv']:
            result.append(self._append_gsuite_test_result("user_2sv", "google_security", test_name, "no_issue_found"))
        else:
            result.append(self._append_gsuite_test_result("user_2sv", "google_security", test_name, "issue_found"))
        
        return result
