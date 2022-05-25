# found another API which is nowhere mentioned in official documentation of Slack
# found out that in order to access this API , cookie information is required and since cookies cannot be hardcoded
# we need to obtain cookies everytime we want to perform a query since they have an expiration date / time
# used selenium for this purpose and now this API is accessible giving access to many setting flags.


# for non-approachable slack tickets in monday

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import *
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import json

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")


driver = webdriver.Chrome(options=chrome_options)
driver.get('https://els1489b.enterprise.slack.com/?no_sso=1&redir=%2F%3F')  # make sure to disable sso and 2FA
driver.find_element(by=By.NAME, value="email").send_keys("admin@cparanoid.com")  # email ID compromised
driver.find_element(by=By.NAME, value="password").send_keys("CparaniodTest")  # password compromised
driver.find_element(by=By.ID, value="signin_btn").click()
sleep(5)
driver.find_element(by=By.XPATH, value="//button[@data-workspace-id='T03AVMVR6MA']").click()
driver.switch_to.window(driver.window_handles[1])
sleep(2)  # incorporate explicit waits here
driver.get('https://app.slack.com/manage/E03AJSQ2E67/security/security')
sleep(5)
cookies = driver.get_cookies()
cookies_dict = {}
for cookie in cookies:
    cookies_dict[cookie['name']] = cookie['value']
print(cookies_dict)



# cookies = {
#     '_gcl_au': '1.1.1542836719.1650613053',
#     '_rdt_uuid': '1650613053787.81cb135e-b2c1-4cbe-8cc1-026801ba561a',
#     '_cs_c': '1',
#     '__qca': 'P0-709187251-1651150244744',
#     '_lc2_fpi': 'e00b11ac9c9b--01g1sx7y9tb76150z67nzzr14m',
#     '__adroll_fpc': '9bba03567c37846d30288e10dc4bb945-1651210713991',
#     '_fbp': 'fb.1.1651210714318.719127099',
#     'shown_ssb_redirect_page': '1',
#     'shown_download_ssb_modal': '1',
#     'show_download_ssb_banner': '1',
#     'no_download_ssb_banner': '1',
#     'documentation_banner_cookie': '1',
#     'optimizelyEndUserId': 'oeu1651478650447r0.1835736783103279',
#     '__pdst': 'c95fa726ea3048d8b748b4391965c23d',
#     '_ga': 'GA1.4.1410203528.1650613054',
#     'utm': '%7B%22utm_source%22%3A%22in-prod%22%2C%22utm_medium%22%3A%22inprod-btn_app_install-index-c%22%7D',
#     'b': '.9f2cc801d2e6c2f3c68fdb0d48a535db',
#     '__zlcmid': '19wkv2zTr9VfL7Z',
#     '_gid': 'GA1.2.609856375.1653277312',
#     'ec': 'enQtMzU1NDk0NzQ4MTYzOS01NTZjNGQ1N2M4NTc3OTY5YjU1NGI0ZmUzYmNkMmNmYzdhYjZhNTRjNDQwYjNiZTdjNjIzMDlhOWZlZDBjNDYx',
#     'DriftPlaybook': 'B',
#     'PageCount': '2',
#     'OptanonConsent': 'isGpcEnabled=0&datestamp=Wed+May+25+2022+10%3A33%3A12+GMT%2B0530+(India+Standard+Time)&version=6.22.0&isIABGlobal=false&hosts=&consentId=ee5603e9-4cd8-4b2e-8d21-ec2631fdb661&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0002%3A1%2CC0003%3A1%2CC0001%3A1&AwaitingReconsent=false',
#     '_ga': 'GA1.1.1410203528.1650613054',
#     '_cs_id': '958a8adc-e2c9-a66d-dbfc-293b893ec0aa.1651150244.115.1653454992.1653454992.1.1685314244623',
#     '__ar_v4': 'KDMBLDIYHFHI5NUNKGJ4LV%3A20220501%3A7%7C4UHU5P4P3FESHLUMNBLWAU%3A20220429%3A58%7CQCM34G7NBZEHHATIFDIUBJ%3A20220429%3A58%7CK2HN2U4VSJGOVKC2WJLQNH%3A20220429%3A50%7CAQ63PRL2SFHGJD4OJ7DH42%3A20220501%3A1',
#     '_li_dcdm_c': '.slack.com',
#     '_ga_QTJQME5M5D': 'GS1.1.1653454985.80.1.1653454996.49',
#     'x': '9f2cc801d2e6c2f3c68fdb0d48a535db.1653456759',
#     'd': 'xoxd-rBL2RqsGXeXZlkxniNuypM8VN0UV1FeKVWW12wIzfXUOU0bLMurHWS0zbC%2FPugAcdoD3E5r6piNwBpI8FULqOGLciB5WKlp4mYdmH1LA714jaAAHeGnzSN%2BnEp5A0zSdbL2qUnaQnKjoJD6C5l%2Fa882a4%2BLwLu8upVvmLqaWZkZwNPAPBfuwbCrpMA%3D%3D',
#     'd-s': '1653456768',
#     'lc': '1653456768',
# }

headers = {
    'authority': 'els1489b.enterprise.slack.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryHV5FiRmQTKpLPunm',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_gcl_au=1.1.1542836719.1650613053; _rdt_uuid=1650613053787.81cb135e-b2c1-4cbe-8cc1-026801ba561a; _cs_c=1; __qca=P0-709187251-1651150244744; _lc2_fpi=e00b11ac9c9b--01g1sx7y9tb76150z67nzzr14m; __adroll_fpc=9bba03567c37846d30288e10dc4bb945-1651210713991; _fbp=fb.1.1651210714318.719127099; shown_ssb_redirect_page=1; shown_download_ssb_modal=1; show_download_ssb_banner=1; no_download_ssb_banner=1; documentation_banner_cookie=1; optimizelyEndUserId=oeu1651478650447r0.1835736783103279; __pdst=c95fa726ea3048d8b748b4391965c23d; _ga=GA1.4.1410203528.1650613054; utm=%7B%22utm_source%22%3A%22in-prod%22%2C%22utm_medium%22%3A%22inprod-btn_app_install-index-c%22%7D; b=.9f2cc801d2e6c2f3c68fdb0d48a535db; __zlcmid=19wkv2zTr9VfL7Z; _gid=GA1.2.609856375.1653277312; ec=enQtMzU1NDk0NzQ4MTYzOS01NTZjNGQ1N2M4NTc3OTY5YjU1NGI0ZmUzYmNkMmNmYzdhYjZhNTRjNDQwYjNiZTdjNjIzMDlhOWZlZDBjNDYx; DriftPlaybook=B; PageCount=2; OptanonConsent=isGpcEnabled=0&datestamp=Wed+May+25+2022+10%3A33%3A12+GMT%2B0530+(India+Standard+Time)&version=6.22.0&isIABGlobal=false&hosts=&consentId=ee5603e9-4cd8-4b2e-8d21-ec2631fdb661&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0002%3A1%2CC0003%3A1%2CC0001%3A1&AwaitingReconsent=false; _ga=GA1.1.1410203528.1650613054; _cs_id=958a8adc-e2c9-a66d-dbfc-293b893ec0aa.1651150244.115.1653454992.1653454992.1.1685314244623; __ar_v4=KDMBLDIYHFHI5NUNKGJ4LV%3A20220501%3A7%7C4UHU5P4P3FESHLUMNBLWAU%3A20220429%3A58%7CQCM34G7NBZEHHATIFDIUBJ%3A20220429%3A58%7CK2HN2U4VSJGOVKC2WJLQNH%3A20220429%3A50%7CAQ63PRL2SFHGJD4OJ7DH42%3A20220501%3A1; _li_dcdm_c=.slack.com; _ga_QTJQME5M5D=GS1.1.1653454985.80.1.1653454996.49; x=9f2cc801d2e6c2f3c68fdb0d48a535db.1653456759; d=xoxd-rBL2RqsGXeXZlkxniNuypM8VN0UV1FeKVWW12wIzfXUOU0bLMurHWS0zbC%2FPugAcdoD3E5r6piNwBpI8FULqOGLciB5WKlp4mYdmH1LA714jaAAHeGnzSN%2BnEp5A0zSdbL2qUnaQnKjoJD6C5l%2Fa882a4%2BLwLu8upVvmLqaWZkZwNPAPBfuwbCrpMA%3D%3D; d-s=1653456768; lc=1653456768',
    'origin': 'https://app.slack.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
}

params = {
    '_x_id': 'noversion-1653456962.779',
    '_x_version_ts': 'noversion',
    '_x_gantry': 'true',
    'fp': 'b5',
}

data = '------WebKitFormBoundaryHV5FiRmQTKpLPunm\r\nContent-Disposition: form-data; name="token"\r\n\r\nxoxc-3358908082211-3352251468998-3573777012787-3c41fd3ab75572e637707ebfe0336c8fd739b1b5b62e1c5939fb727f760e3b93\r\n------WebKitFormBoundaryHV5FiRmQTKpLPunm--\r\n'

response = requests.post('https://slack.com/api/enterprise.prefs.get', headers=headers, data=data, cookies=cookies_dict)
enterprise_prefs = json.loads(response.text)

# below are just examples 

# attempting un-approachable tickets from monday because of unavailability of APIs
jailbreak_detection = enterprise_prefs['locked_prefs']['enterprise_mobile_device_check']
if jailbreak_detection is True:  # jailbreak detection enabled in security tab
    print("OK")
else:
    print("NOT OK!!")

if enterprise_prefs['locked_prefs']['google_sso_enable'] is None:  # SSO disabled
    print("Not OK")
else:
    print("SSO Enabled")

pub_channels = enterprise_prefs['locked_prefs']['who_can_manage_public_channels']
# who can create / manage public channels restrict to org owners
if pub_channels['type'].index == 0:
    print("OK")  # org primary owner means NULL list
else:
    print("Not ok")

if enterprise_prefs['locked_prefs']['slackbot_responses_disabled'] is False:
    if enterprise_prefs['locked_prefs']['slackbot_responses_only_admins'] is True:
        print("OK")
    else:
        print("NOT OK")




