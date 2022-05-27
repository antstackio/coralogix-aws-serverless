import requests
import json
import time


class Tester:

    def __init__(self):  # cookies might expire after a certain period
        # permanent solution for this is web scraping
        self.enterprise_id = 'els1489b'
        self.cookies = {
            'd': 'xoxd-rBL2RqsGXeXZlkxniNuypM8VN0UV1FeKVWW12wIzfXUOU0bLMurHWS0zbC%2FPugAcdoD3E5r6piNwBpI8FULqOGLciB5WKlp4mYdmH1LA714jaAAHeGnzSN%2BnEp5A0zSdbL2qUnaQnKjoJD6C5l%2Fa882a4%2BLwLu8upVvmLqaWZkZwNPAPBfuwbCrpMA%3D%3D',
            'd-s': '1653456768',
            'lc': '1653456768',
        }

        self.headers = {
            'authority': 'els1489b.enterprise.slack.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryHV5FiRmQTKpLPunm',
            'origin': 'https://app.slack.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
        }

        self.data = '------WebKitFormBoundaryHV5FiRmQTKpLPunm\r\nContent-Disposition: form-data; name="token"\r\n\r\nxoxc-3358908082211-3352251468998-3573777012787-3c41fd3ab75572e637707ebfe0336c8fd739b1b5b62e1c5939fb727f760e3b93\r\n------WebKitFormBoundaryHV5FiRmQTKpLPunm--\r\n'

        self.response = requests.post('https://slack.com/api/enterprise.prefs.get', headers=self.headers, data=self.data, cookies=self.cookies)
        self.enterprise_prefs = json.loads(self.response.text)

    def run_tests(self):
       return self.jailbreak_detection() + \
              self.saml_enabled() + \
              self.create_public_channels() + \
              self.manage_slackbot_responses() + \
              self.sign_into_other_apps() + \
              self.unmanaged_mobile_notification_preview() + \
              self.sso_email_change() + \
              self.workflow_creation_permission()

    def jailbreak_detection(self) -> list:
        test_name = 'Jailbreak detection enabled'
        if self.enterprise_prefs['locked_prefs']['enterprise_mobile_device_check'] is True:
            return [{
                "item": self.enterprise_id,
                "item_type": "enterprise_id",
                "test_name": test_name,
                "test_result": "no_issue_found",
                "timestamp": time.time()
             }]
        else:
            return [{
                "item": self.enterprise_id,
                "item_type": "enterprise_id",
                "test_name": test_name,
                "test_result": "issue_found",
                "timestamp": time.time()
            }]

    def saml_enabled(self) -> list:
        test_name = 'SAML enabled'
        if self.enterprise_prefs['locked_prefs']['saml_enable'] is None or not self.enterprise_prefs['locked_prefs']['saml_enable']:
            return [{
               "item": self.enterprise_id,
               "item_type": "enterprise_id",
               "test_name": test_name,
               "test_result": "issue_found",
               "timestamp": time.time()

            }]
        else:
            return [{
               "item": self.enterprise_id,
               "item_type": "enterprise_id",
               "test_name": test_name,
               "test_result": "no_issue_found",
               "timestamp": time.time()

           }]

    def create_public_channels(self) -> list:  # restricted to org owners and admins
        test_name = 'who can create public channels'
        if self.enterprise_prefs['locked_prefs']['who_can_manage_public_channels']['type'].count("ORG_ADMINS_AND_OWNERS") <= 0:
            return [{
                "item": self.enterprise_id,
                "item_type": "enterprise_id",
                "test_name": test_name,
                "test_result": "issue_found",
                "timestamp": time.time()

            }]
        else:
            return [{
                "item": self.enterprise_id,
                "item_type": "enterprise_id",
                "test_name": test_name,
                "test_result": "no_issue_found",
                "timestamp": time.time()

            }]

    def manage_slackbot_responses(self) -> list:  # restricting to admins
        test_name = 'who can manage slackbot responses'
        if self.enterprise_prefs['locked_prefs']['slackbot_responses_disabled'] is False:
            if self.enterprise_prefs['locked_prefs']['slackbot_responses_only_admins'] is True:
                return [{
                    "item": self.enterprise_id,
                    "item_type": "enterprise_id",
                    "test_name": test_name,
                    "test_result": "no_issue_found",
                    "timestamp": time.time()

               }]
        else:
            return [{
                    "item": self.enterprise_id,
                    "item_type": "enterprise_id",
                    "test_name": test_name,
                    "test_result": "issue_found",
                    "timestamp": time.time()

               }]

    def sign_into_other_apps(self) -> list:
        # checking for this setting to be disabled since user details will be compromised
        test_name = 'user can sign into other apps with slack account'
        if self.enterprise_prefs['unlocked_prefs']['sign_in_with_slack_disabled'] is False:
            return [{
                "item": self.enterprise_id,
                "item_type": "enterprise_id",
                "test_name": test_name,
                "test_result": "no_issue_found",
                "timestamp": time.time()

            }]
        else:
            return [{
                "item": self.enterprise_id,
                "item_type": "enterprise_id",
                "test_name": test_name,
                "test_result": "issue_found",
                "timestamp": time.time()

            }]

    def unmanaged_mobile_notification_preview(self) -> list:
        # redacting to least duration available in options = 5 minutes
        test_name = 'mobile passcode force reset limit'
        if self.enterprise_prefs['locked_prefs']['mobile_passcode_timeout_in_seconds'] == 300:
            return [{
                "item": self.enterprise_id,
                "item_type": "enterprise_id",
                "test_name": test_name,
                "test_result": "no_issue_found",
                "timestamp": time.time()

            }]
        else:
            return [{
                "item": self.enterprise_id,
                "item_type": "enterprise_id",
                "test_name": test_name,
                "test_result": "issue_found",
                "timestamp": time.time()

            }]

    def sso_email_change(self) -> list:  # restricting to email change not allowed
        test_name = 'sso email change allowed'
        if self.enterprise_prefs['locked_prefs']['sso_change_email'] is None or self.enterprise_prefs['locked_prefs']['sso_change_email'] is False:
            return [{
                "item": self.enterprise_id,
                "item_type": "enterprise_id",
                "test_name": test_name,
                "test_result": "no_issue_found",
                "timestamp": time.time()

            }]
        else:
            return [{
                "item": self.enterprise_id,
                "item_type": "enterprise_id",
                "test_name": test_name,
                "test_result": "issue_found",
                "timestamp": time.time()

            }]

    def workflow_creation_permission(self) -> list:  # restricting creation permission to org admin
        test_name = 'permissions to create workflows'
        if self.enterprise_prefs['locked_prefs']['who_can_create_workflows']['type'].count("org_admin") > 0:
            if self.enterprise_prefs['locked_prefs']['who_can_create_workflows']['type'].count("org_owner") > 0:
                return [{
                    "item": self.enterprise_id,
                    "item_type": "enterprise_id",
                    "test_name": test_name,
                    "test_result": "no_issue_found",
                    "timestamp": time.time()

                }]
        else:
            return [{
                "item": self.enterprise_id,
                "item_type": "enterprise_id",
                "test_name": test_name,
                "test_result": "issue_found",
                "timestamp": time.time()

                }]

    def view_member_analytics(self) -> list:
        test_name = 'permission to view member analytics'
        if self.enterprise_prefs['locked_prefs']['member_analytics_disabled'] is False:
            return [{
                "item": self.enterprise_id,
                "item_type": "enterprise_id",
                "test_name": test_name,
                "test_result": "no_issue_found",
                "timestamp": time.time()

            }]
        else:
            return [{
                "item": self.enterprise_id,
                "item_type": "enterprise_id",
                "test_name": test_name,
                "test_result": "issue_found",
                "timestamp": time.time()

            }]


print(Tester().run_tests())


