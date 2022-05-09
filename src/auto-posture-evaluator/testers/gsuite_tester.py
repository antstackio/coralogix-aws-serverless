from datetime import datetime
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
        self.inactive_user_threshold = os.environ.get("AUTOPOSTURE_GSUITE_USER_INACTIVE_THRESHOLD")
        self.SCOPES = {}
    def declare_tested_provider(self) -> str:
        return "google"
    
    def declare_tested_service(self) -> str:
        return "gsuite"
    
    def run_tests(self) -> list:
        return \
            self.detect_single_super_admin_account() + \
            self.detect_2step_verification_enforced() + \
            self.detect_2step_verification_enforcement_for_all_users() + \
            self.detect_users_authenticating_with_imap() + \
            self.detect_users_authenticating_with_pop() + \
            self.detect_automatic_mail_forwarding()
    
    def _get_user_id(self):
        credentials = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT)
        people_service = build('people', 'v1', credentials=credentials)
        result = people_service.people().get(resourceName='people/me', personFields='metadata').execute()
        resource_name = result['resourceName']
        user_id = resource_name.split('/')[-1]

        return user_id
    def _get_google_workspace_users(self):
        SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

        credentials = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT, scopes=SCOPES, subject='admin@cparanoid.com')
        service = build('admin', 'directory_v1', credentials=credentials)
        response = service.users().list(customer='my_customer', orderBy='email').execute()

        users = response['users']
        return users

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

    def detect_2step_verification_enforced(self):
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

    def detect_2step_verification_enforcement_for_all_users(self):
        result = []
        test_name = "two_step_verification_enforcement_for_all_users"
        
        SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

        credentials = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT, scopes=SCOPES, subject='admin@cparanoid.com')
        service = build('admin', 'directory_v1', credentials=credentials)
        response = service.users().list(customer='my_customer', orderBy='email').execute()

        users = response['users']

        for user in users:
            user_primary_email = user['primaryEmail']
            if user['isEnforcedIn2Sv'] and user['isEnrolledIn2Sv']:
                result.append(self._append_gsuite_test_result(user_primary_email, "google_user", test_name, "no_issue_found"))
            else:
                result.append(self._append_gsuite_test_result(user_primary_email, "google_user", test_name, "issue_found"))
        
        return result

    def detect_users_authenticating_with_imap(self):
        result = []
        test_name = "users_authenticating_with_imap"
        users = self._get_google_workspace_users()
        user = users[0]

        user_id = user['id']
        user_primary_email = user['primaryEmail']
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        credentials = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT, scopes=SCOPES, subject=user_primary_email)
        gmail_service = build('gmail', 'v1', credentials=credentials)
        response =gmail_service.users().settings().getImap(userId=user_id).execute()
        imap_enabled = response['enabled']
        if imap_enabled:
            result.append(self._append_gsuite_test_result('gmail_iamp_settings', 'google_workspace_settings', test_name, "issue_found"))
        else:
            result.append(self._append_gsuite_test_result('gmail_iamp_settings', 'google_workspace_settings', test_name, "no_issue_found"))

        return result

    def detect_users_authenticating_with_pop(self):
        result = []
        test_name = "users_authenticating_with_pop"
        users = self._get_google_workspace_users()
        user = users[0]

        SCOPES = ['https://www.googleapis.com/auth/admin.directory.user', 'https://www.googleapis.com/auth/gmail.readonly']

        user_id = user['id']
        user_primary_email = user['primaryEmail']
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        credentials = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT, scopes=SCOPES, subject=user_primary_email)
        gmail_service = build('gmail', 'v1', credentials=credentials)
        response =gmail_service.users().settings().getPop(userId=user_id).execute()
        
        access_winow = response['accessWindow']
        if access_winow == 'disabled':
            result.append(self._append_gsuite_test_result('gmail_pop_settings', 'google_workspace_settings', test_name, "no_issue_found"))
        else: 
            result.append(self._append_gsuite_test_result('gmail_pop_settings', 'google_workspace_settings', test_name, "issue_found"))
        
        return result

    def detect_automatic_mail_forwarding(self):
        result = []
        test_name = "automatic_forwarding"
        users = self._get_google_workspace_users()
        user = users[0]

        user_id = user['id']
        user_primary_email = user['primaryEmail']
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        credentials = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT, scopes=SCOPES, subject=user_primary_email)
        gmail_service = build('gmail', 'v1', credentials=credentials)
        response =gmail_service.users().settings().getAutoForwarding(userId=user_id).execute()
        
        auto_forwarding_enabled = response['enabled']
        if not auto_forwarding_enabled:
            result.append(self._append_gsuite_test_result("gmail_auto_forwarding_settings", "google_workspace_settings", test_name, "not_issue_found"))
        else:
            result.append(self._append_gsuite_test_result("gmail_auto_forwarding_settings", "google_workspace_settings", test_name, "issue_found"))
        
        return result

    def detect_inactive_user(self):
        result = []
        test_name = "inactive_gsuite_user"
        users = self._get_google_workspace_users()
        inactive_user_threshold = int(self.inactive_user_threshold) if self.inactive_user_threshold else 30
        for user in users:
            last_login = user['lastLoginTime']
            user_primary_email = user['primaryEmail']
            last_login_obj = datetime.strptime(last_login, '%Y-%m-%dT%H:%M:%S.000Z').date()
            current_date_obj = datetime.now().date()
            diff = (current_date_obj - last_login_obj).days
            
            if diff >= inactive_user_threshold:
                result.append(self._append_gsuite_test_result(user_primary_email, "user_email", test_name, "issue_found"))
            else: result.append(self._append_gsuite_test_result(user_primary_email, "user_email", test_name, "no_issue_found"))

        return result
