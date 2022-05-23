import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import *
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")


class SlackTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(
            'https://els1489b.enterprise.slack.com/?no_sso=1&redir=%2F%3F')  # make sure to disable sso and 2FA
        self.driver.find_element(by=By.NAME, value="email").send_keys("admin@cparanoid.com")  # email ID compromised
        self.driver.find_element(by=By.NAME, value="password").send_keys("CparaniodTest")  # password compromised

        self.driver.find_element(by=By.ID, value="signin_btn").click()
        sleep(2)  # incorporate explicit waits here , would be feasible
        self.driver.find_element(by=By.XPATH, value="//button[@data-workspace-id='T03AVMVR6MA']").click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(2)  # incorporate explicit waits here
        self.driver.get('https://app.slack.com/manage/E03AJSQ2E67/security/security')
        sleep(5)

    def test_selenium_settings_org(self):
        # test case for checking block file downloads
        self.block_file_downloads = self.driver.find_element(by=By.XPATH,
                                                             value="//div[@data-qa='enterprise-security-settings-block-file-downloads']")
        sleep(5)
        if self.block_file_downloads.find_element(by=By.CLASS_NAME, value="bold").text == "Enabled":
            print([{
                "item": self.driver.find_element(by=By.XPATH, value="//div[@data-qa='ent-nav-header-name']").text,
                "item_type": "enterprise-name",
                "test_name": self.block_file_downloads.find_element(by=By.CLASS_NAME,
                                                                    value="p-settings_item___header").text,
                "test_result": "no_issue_found",
                "timestamp": time()

            }])
        else:
            print([{

                "item": self.driver.find_element(by=By.XPATH, value="//div[@data-qa='ent-nav-header-name']").text,
                "item_type": "enterprise-name",
                "test_name": self.block_file_downloads.find_element(by=By.CLASS_NAME,
                                                                    value="p-settings_item__label").text,
                "test_result": "issue_found",
                "timestamp": time()

            }])

        # test case for checking Jailbreak or root detection enabled/disabled
        self.jailbreak = self.driver.find_element(by=By.XPATH,
                                                  value="//div[@data-qa='enterprise-security-settings-mobile_device_check']")
        sleep(5)
        if self.jailbreak.find_element(by=By.CLASS_NAME, value="bold").text == "Enabled":
            print([{
                "item": self.driver.find_element(by=By.XPATH, value="//div[@data-qa='ent-nav-header-name']").text,
                "item_type": "enterprise-name",
                "test_name": self.jailbreak.find_element(by=By.CLASS_NAME, value="p-settings_item___header").text,
                "test_result": "no_issue_found",
                "timestamp": time()

            }])
        else:
            print([{

                "item": self.driver.find_element(by=By.XPATH, value="//div[@data-qa='ent-nav-header-name']").text,
                "item_type": "enterprise-name",
                "test_name": self.jailbreak.find_element(by=By.CLASS_NAME, value="p-settings_item__label").text,
                "test_result": "issue_found",
                "timestamp": time()

            }])

        # messaging policies
        try:
            self.driver.get('https://app.slack.com/manage/E03AJSQ2E67/settings/org-policies/permissions')
            sleep(10)
            at_everyone = self.driver.find_element(By.XPATH, value="//div[@data-qa-pref='who_can_at_everyone']").text
            if at_everyone.find("Workspace Owners and Admins only"):
                print([{
                    "item": self.driver.find_element(by=By.XPATH, value="//div[@data-qa='ent-nav-header-name']").text,
                    "item_type": "enterprise-name",
                    "test_name": self.driver.find_element(By.XPATH,
                                                          value="//div[@data-qa-pref='who_can_at_everyone']").text[
                                 :self.driver.find_element(By.XPATH,
                                                           value="//div[@data-qa-pref='who_can_at_everyone']").text.index(
                                     '\n')].strip(":"),
                    "test_result": "no_issue_found",
                    "timestamp": time()

                }])
            else:
                print([{

                    "item": self.driver.find_element(by=By.XPATH, value="//div[@data-qa='ent-nav-header-name']").text,
                    "item_type": "enterprise-name",
                    "test_name": self.driver.find_element(By.XPATH,
                                                          value="//div[@data-qa-pref='who_can_at_everyone']").text[
                                 :self.driver.find_element(By.XPATH,
                                                           value="//div[@data-qa-pref='who_can_at_everyone']").text.index(
                                     '\n')].strip(":"),
                    "test_result": "issue_found",
                    "timestamp": time()

                }])

        except NoSuchElementException:
            print('No Policy Created for Messaging Organization Policies')

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
