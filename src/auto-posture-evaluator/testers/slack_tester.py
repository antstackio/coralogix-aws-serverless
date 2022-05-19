import os
import time
import interfaces
from datetime import datetime
from datetime import timedelta
from slack_sdk import WebClient
import requests
import json
import gzip
import re


class Tester:
    def __init__(self):
        self.slack_client = WebClient(token=os.environ.get("SLACK_USER_TOKEN"))
        self.team_info = self.slack_client.team_info()  # returns enterprise info rather than team
        self.enterprise_id = self.team_info["team"]["id"]

    def declare_tested_service(self) -> str:
        return 'slack'

    def declare_tested_provider(self) -> str:
        return 'slack'

    def run_tests(self) -> list:
        return self.get_public_file_sharing_enabled() + \
               self.get_apps_with_no_privacy_policy() + \
               self.get_apps_with_no_description() + \
               self.get_number_of_workspace_admins_more_than_conf() + \
               self.get_number_of_workspace_owners_more_than_conf() + \
               self.get_list_userids() + \
               self.get_all_session_details() + \
               self.list_all_guest_users() + \
               self.two_factor_auth_enforce() + \
               self.require_app_approval() + \
               self.get_all_admin_users() + \
               self.get_archive_channel_by_admin() + \
               self.msg_edit_window() + \
               self.check_if_file_upload_disabled() + \
               self.restrict_post_at_general_to_admins() + \
               self.check_default_channel() + \
               self.email_display_policy_for_all_users() + \
               self.get_admin_analytics() + \
               self.get_inactive_channels() + \
               self.public_file_sharing() + \
               self.user_groups_permission() + \
               self.single_workspace_owner(self)

    def get_public_file_sharing_enabled(self):
        test_name = "public_file_sharing_enabled"
        response = self.slack_client.files_list(team_id=os.environ.get("TEAM_ID"))
        print(response)
        result = []
        for file in response["files"]:
            if file["public_url_shared"]:
                result.append({
                    "timestamp": time.time(),
                    "account": self.enterprise_id,
                    "item": file["id"],
                    "item_type": "file",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
            else:
                result.append({
                    "timestamp": time.time(),
                    "account": self.enterprise_id,
                    "item": file["id"],
                    "item_type": "file",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
        return result

    def get_apps_with_no_privacy_policy(self):
        test_name = "apps_with_no_privacy_policy"
        response = self.slack_client.admin_apps_approved_list(team_id=os.environ.get("TEAM_ID"))
        result = []
        for app in response['approved_apps']:
            if not app['app']['privacy_policy_url']:
                result.append({
                    "timestamp": time.time(),
                    "account": self.enterprise_id,
                    "item": app["app"]["id"],
                    "item_type": "app",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
            else:
                result.append({
                    "timestamp": time.time(),
                    "account": self.enterprise_id,
                    "item": app["app"]["id"],
                    "item_type": "app",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })
        return result

    def get_apps_with_no_description(self):
        test_name = "apps_with_no_description"
        response = self.slack_client.admin_apps_approved_list(team_id=os.environ.get("TEAM_ID"))
        apps = response["approved_apps"]
        for i in range(len(apps)):
            print(apps[i]["app"]["name"])
            # if apps[i]["app"]["description"] == " " or apps[i]["app"]["description"] is None:
            #     print(apps[i]["app"]["name"])

        result = []
        for app in response['approved_apps']:  # standard format
            if not app['app']['description']:
                result.append({
                    "timestamp": time.time(),
                    "account": self.enterprise_id,
                    "item": app["app"]["id"],
                    "item_type": "app",
                    "test_name": test_name,
                    "test_result": "issue_found"
                })
            else:
                result.append({
                    "timestamp": time.time(),
                    "account": self.enterprise_id,
                    "item": app["app"]["id"],
                    "item_type": "app",
                    "test_name": test_name,
                    "test_result": "no_issue_found"
                })
        return result

    def get_number_of_workspace_admins_more_than_conf(self):
        test_name = "number_of_workspace_admins_more_than_conf"
        response = self.slack_client.admin_users_list(team_id=os.environ.get("TEAM_ID"))
        admin_count = 0
        for user in response['users']:
            if user['is_admin']:
                admin_count += 1
                if admin_count > 2:
                    return [{
                        "timestamp": time.time(),
                        "account": self.enterprise_id,
                        "item": os.environ.get("TEAM_ID"),  # team id same as workspace id
                        "item_type": "workspace",
                        "test_name": test_name,
                        "test_result": "issue_found"
                    }]
        return [{
            "timestamp": time.time(),
            "account": self.enterprise_id,
            "item": os.environ.get("TEAM_ID"),
            "item_type": "workspace",
            "test_name": test_name,
            "test_result": "no_issue_found"
        }]

    def get_number_of_workspace_owners_more_than_conf(self):
        test_name = "number_of_workspace_owners_more_than_conf"
        response = self.slack_client.admin_teams_owners_list(team_id=os.environ.get("TEAM_ID"))
        owner_count = len(response.get('owner_ids', 0))
        if owner_count > 2:
            return [{
                "timestamp": time.time(),
                "account": self.enterprise_id,
                "item": os.environ.get("TEAM_ID"),
                "item_type": "workspace",
                "test_name": test_name,
                "test_result": "issue_found"
            }]
        else:
            return [{
                "timestamp": time.time(),
                "account": self.enterprise_id,
                "item": os.environ.get("TEAM_ID"),
                "item_type": "workspace",
                "test_name": test_name,
                "test_result": "no_issue_found"
            }]

    def get_list_userids(self) -> list:
        users = []
        result = self.slack_client.users_list(team_id=os.environ.get("TEAM_ID"))
        for i in range(len(result["members"])):
            if result["members"][i]["is_bot"] is not True:  # excludes bots and installed apps from list of all users
                if result["members"][i]["is_email_confirmed"] is True:  # verify if email_confirmed for valid users
                    users.append(result["members"][i]["id"])

        return users  # returns list of users in the organization including guest users and admins

    def get_all_session_details(self) -> list:
        result = []
        users = self.get_list_userids()
        test_name = "users_with_session_timeout"
        response = self.slack_client.admin_users_session_getSettings(user_ids=os.environ.get("USER_ID"))
        if response.get("no_settings_applied") is not None:  # store variable
            for i in range(len(response.get('no_settings_applied'))):  # use enumerate instead
                result.append({
                    "item": response.get('no_settings_applied')[i],
                    "item_type": "user_id",
                    "test_name": test_name,
                    "test_result": "issue_found",
                    "timestamp": time.time()
                })
        elif response.get("session_settings"):
            for i in range(len(response.get('session_settings'))):
                result.append({
                    "item": response.get('session_settings')[i]['user_id'],
                    "item_type": "user_id",
                    "test_name": test_name,
                    "test_result": "no_issue_found",
                    "timestamp": time.time()
                })

        return result

    def list_all_guest_users(self) -> list:
        guest_users = []
        result = self.slack_client.users_list(team_id="T03AVMVR6MA")
        for i in range(len(result["members"])):
            if result["members"][i]["is_restricted"]:  # check if is_restricted flag is true which indicates guest_user
                guest_users.append(result["members"][i]["id"])

        return guest_users

    def two_factor_auth_enforce(self) -> list:
        users = self.get_list_userids()
        result = []
        test_name = 'users without two factor auth'
        response = self.slack_client.users_list(team_id=os.environ.get("TEAM_ID"))
        for i in users:
            for j in range(len(response["members"])):
                if response["members"][j]["id"] == i:
                    if response["members"][j]["has_2fa"] is False:
                        result.append({
                            "item": response["members"][j]["id"],
                            "item_type": "user_id",
                            "test_name": test_name,
                            "test_result": "issue_found",
                            "timestamp": time.time()

                        })
                    else:
                        result.append({
                            "item": response["members"][j]["id"],
                            "item_type": "user_id",
                            "test_name": test_name,
                            "test_result": "no_issue_found",
                            "timestamp": time.time()

                        })

        return result

    def require_app_approval(self) -> list:
        result = []
        test_name = 'list apps which have admin approval'
        response = self.slack_client.admin_apps_approved_list(team_id=os.environ.get("TEAM_ID"))
        apps = response["approved_apps"]
        for i in range(len(apps)):
            if apps[i]["app"]["is_app_directory_approved"] is not True:
                result.append({
                    "item": apps[i]["app"]["name"],
                    "item_type": "app_name",
                    "test_name": test_name,
                    "test_result": "issue_found",
                    "timestamp": time.time()
                })
            else:
                result.append({
                    "item": apps[i]["app"]["name"],
                    "item_type": "app_name",
                    "test_name": test_name,
                    "test_result": "no_issue_found",
                    "timestamp": time.time()
                })

        return result

    def get_all_admin_users(self) -> list:
        admin_list = []
        response = self.slack_client.admin_users_list(team_id=os.environ.get("TEAM_ID"))
        for i in range(len(response['users'])):
            if response['users'][i]['is_admin'] is True:
                admin_list.append(response['users'][i]['id'])  # excludes bots and apps

        return admin_list

    def get_archive_channel_by_admin(self) -> list:
        result = []
        test_name = 'check whether channel archived by admin'
        response = self.slack_client.conversations_list(team_id=os.environ.get("TEAM_ID"))
        admin_list = self.get_all_admin_users()
        for i in range(len(response["channels"])):
            if response["channels"][i]["is_archived"] is True:
                if response["channels"][i]["creator"] not in admin_list:
                    result.append({
                        "item": response["channels"][i]["id"],
                        "item_type": "channel_id",
                        "test_name": test_name,
                        "test_result": "issue_found",
                        "timestamp": time.time()

                    })
                else:
                    result.append({
                        "item": response["channels"][i]["id"],
                        "item_type": "channel_id",
                        "test_name": test_name,
                        "test_result": "no issue_found",
                        "timestamp": time.time()
                    })

        return result

    def msg_edit_window(self) -> list:
        # returns issue found if editing is disabled , no issue found if time window for editing is allowed
        test_name = 'reasonable time window for message editing/deletion'
        response = self.slack_client.team_preferences_list()
        if response.get('msg_edit_window_mins') == 0:
            return [{
                "item": self.slack_client.team_info().get("team")["name"],
                "item_type": "organization_name",
                "test_name": test_name,
                "test_result": "issue_found",
                "timestamp": time.time()
            }]
        else:
            return [{
                "item": self.slack_client.team_info().get("team")["name"],
                "item_type": "organization_name",
                "test_name": test_name,
                "test_result": "no issue_found",
                "timestamp": time.time()
            }]

    def check_if_file_upload_disabled(self) -> list:
        test_name = 'check if file upload is disabled'
        response = self.slack_client.team_preferences_list()
        if response.get('disable_file_uploads') == "allow_all":
            return [{
                "item": self.slack_client.team_info().get("team")["name"],
                "item_type": "organization_name",
                "test_name": test_name,
                "test_result": "issue_found",
                "timestamp": time.time()
            }]
        elif response.get('disable_file_uploads') == "disallow_all":
            return [{
                "item": self.slack_client.team_info().get("team")["name"],
                "item_type": "organization_name",
                "test_name": test_name,
                "test_result": "no issue_found",
                "timestamp": time.time()
            }]

    def check_default_channel(self) -> list:
        test_name = 'check_default_channel_is_#general'
        response = self.slack_client.admin_teams_settings_info(team_id=os.environ.get("TEAM_ID"))
        is_def = response.get('team')['default_channels'][0]  # only one channel can be default channel
        res = self.slack_client.conversations_list(team_id=os.environ.get("TEAM_ID")).get("channels")
        for i in range(len(res)):
            if res[i]["id"] == is_def:
                if res[i]["is_general"] is False:
                    return [{

                        "item": response.get('team')['id'],
                        "item_type": "teamID",
                        "test_name": test_name,
                        "test_result": "issue_found",
                        "timestamp": time.time()

                    }]
                elif res[i]["is_general"] is True:
                    return [{

                        "item": response.get('team')['id'],
                        "item_type": "teamID",
                        "test_name": test_name,
                        "test_result": "no_issue_found",
                        "timestamp": time.time()
                    }]

    def restrict_post_at_general_to_admins(self) -> list:
        # only admins can post, users can reply, nobody else can use @everyone, @channel and @here except admins
        test_name = 'restricting admins to post in general'
        gen_channel_id = self.slack_client.conversations_list(team_id=os.environ.get("TEAM_ID"))
        channel_id = gen_channel_id.get("channels")[0]["id"]
        response = self.slack_client.admin_conversations_getConversationPrefs(channel_id=channel_id)
        if response.get('prefs')['who_can_post']['type'][0] == "admin":  # only admins can post
            if response.get('prefs')['can_thread']['type'][0] == "ra":  # any member of channel can reply
                if response.get('prefs')['enable_at_channel']['enabled']:  # @channel is enabled only for admins
                    if response.get('prefs')['enable_at_here']['enabled']:  # @here is enabled only for admins
                        return [{
                            "item": channel_id,
                            "item_type": "channel_id",
                            "test_name": test_name,
                            "test_result": "no_issue_found",
                            "timestamp": time.time()
                        }]
        else:
            return [{
                "item": channel_id,
                "item_type": "channel_id",
                "test_name": test_name,
                "test_result": "issue_found",
                "timestamp": time.time()

            }]

    def email_display_policy_for_all_users(self) -> list:
        # if email being displayed , shows just one username (error case)
        # not to be presumed that email is not being shown for others, email is displayed for every other user
        test_name = 'email being displayed in members slack profiles'
        response = self.slack_client.users_profile_get()
        try:
            if response.get('profile')["email"]:
                return [{

                    "item": response.get("profile")["first_name"],
                    "item_type": "profile_name",
                    "test_name": test_name,
                    "test_result": "issue_found",
                    "timestamp": time.time()

                }]
        except KeyError:
            return [{

                "item": response.get("profile")["first_name"],
                "item_type": "profile_name",
                "test_name": test_name,
                "test_result": "no_issue_found",
                "timestamp": time.time()

            }]

    def get_admin_analytics(self) -> list:  # retrieves admin analytics (only for primary owners)
        auth_token = os.environ.get("SLACK_USER_TOKEN")
        hed = {'Authorization': 'Bearer ' + auth_token, 'Content-Type': 'text/html', 'encoding': 'ISO-8859-1'}
        prev_date = str(datetime.now().date() - timedelta(days=2))
        r = requests.get(
            'https://slack.com/api/admin.analytics.getFile?type=public_channel&metadata_only=false&date={0}'.format(
                prev_date),
            headers=hed)  # note: the date parameter only accepts date two days earlier than today's date
        # admin analytics logs are not generated two days later. Always search for two days earlier logs
        with open('myfile.txt.gz', 'wb') as fd:  # downloads analytics file as txt.gz format , downloaded to local drive
            fd.write(r.content)

        a = gzip.open('myfile.txt.gz', 'rb')  # reading downloaded analytics file
        channel_data = []
        my_json = a.read().decode('utf-8')  # decoding into readable format
        my_json = my_json.split("\n")  # list cleaning
        my_json.remove('')  # split causes one extra '' in list
        for i in range(len(my_json)):
            channel_data.append(json.loads(my_json[i]))

        return channel_data  # contains JSON data of admin analytics

    def get_inactive_channels(self) -> list:
        # method looks into admin analytics file and obtains inactive channels under the particular enterprise
        test_name = 'list inactive channel IDs'
        result = []
        channel_data = self.get_admin_analytics()
        for i in range(len(channel_data)):
            last_active_date = channel_data[i]["date_last_active"]
            d1 = datetime.fromtimestamp(last_active_date)
            d2 = datetime.now()
            time_window = d2 - d1
            if time_window.days > 30:  # assuming a channel is considered inactive if time window is more than 30 days
                result.append({

                    "item": channel_data[i]['channel_id'],
                    "item_type": "channel_id",
                    "test_name": test_name,
                    "test_result": "issue_found",
                    "timestamp": time.time()

                })
            else:
                result.append({

                    "item": channel_data[i]['channel_id'],
                    "item_type": "channel_id",
                    "test_name": test_name,
                    "test_result": "no_issue_found",
                    "timestamp": time.time()

                })

        return result

    def public_file_sharing(self) -> list:
        # if public file URL creation is turned on , then permalink_public in files.list API appears , else disappears
        test_name = 'public file sharing URL creation enabled or not'
        result = []
        response = self.slack_client.files_list(team_id=os.environ.get("TEAM_ID"))
        file = response.get('files')
        for i in range(len(file)):
            try:
                if file[i]['permalink_public']:  # if flag exists then public file URL creation is enabled
                    result.append({
                        "item": file[i]["id"],
                        "item_type": "file_id",
                        "test_name": test_name,
                        "test_result": "issue_found",
                        "timestamp": time.time()

                    })
            except KeyError:
                result.append({
                    "item": file[i]["id"],
                    "item_type": "file_id",
                    "test_name": test_name,
                    "test_result": "no_issue_found",
                    "timestamp": time.time()

                })
        return result

    def user_groups_permission(self) -> list:
        result = []
        guest_users = self.list_all_guest_users()
        test_name = 'check whether user group created by guest'
        response = self.slack_client.usergroups_list(team_id=os.environ.get("TEAM_ID"))
        # response = self.slack_client.usergroups_list(team_id=os.environ.get("TEAM_ID"))
        for i in range(len(response.get('usergroups'))):
            if response['usergroups'][i]["created_by"] in guest_users:
                result.append({
                    "item": response['usergroup'][i]['id'],
                    "item_type": "usergroup_id",
                    "test_name": test_name,
                    "test_result": "no_issue_found",
                    "timestamp": time.time()
                })
            else:
                result.append({
                    "item": response['usergroup'][i]['id'],
                    "item_type": "usergroup_id",
                    "test_name": test_name,
                    "test_result": "issue_found",
                    "timestamp": time.time()
                })

        return result

    def single_workspace_owner(self) -> list:
        test_name = 'check whether single workspace owner or multiple'
        response = self.slack_client.admin_teams_owners_list(team_id=os.environ.get('TEAM_ID'))
        if len(response.get('owner_ids') ) == 1:
            return [{

                "item": response.get('owner_ids')[0],
                "item_type": "workspace_owner_id",
                "test_name": test_name,
                "test_result": "issue_found",
                "timestamp": time.time()

            }]
        elif len(response.get('owner_ids')) > 1:
            return [{

                "item": response.get('owner_ids')[0],
                "item_type": "one_of_the_workspace_owners_id_since_multiple",
                "test_name": test_name,
                "test_result": "issue_found",
                "timestamp": time.time()

            }]

    


