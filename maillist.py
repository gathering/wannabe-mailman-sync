import re

from mailmanclient import Client, Settings
from mailmanclient.restobjects.domain import Domain

class maillist(object):
    def __init__(self, **args):
        self.client = Client(
            args['rest_url'], args['rest_username'], args['rest_password'])
        self.domain = self.client.get_domain(args['domain'])

    def get_lists(self):
        mailists = []
        for list in self.domain.lists:
            mailists.append(list.fqdn_listname)
        return mailists

    def create_list(self, **args):
        list = args['list']
        name = list.split('@')[0]
        print(list)
        print(name)
        self.domain.create_list(name)
        self.set_settings(list)

    def set_settings(self, list_fqdn):
        list = self.client.get_list(list_fqdn)
        for key, value in self.default_settings().items():
            #print(key)
            list.settings[key] = value
        list.settings.save()

    def get_list_members(self, list_fqdn):
        members = []
        list = self.client.get_list(list_fqdn)
        for member in list.members:
            members.append(member.address.email.lower())
        return members

    def sync_members(self, list_fqdn, wannabe_members):
        members = self.get_list_members(list_fqdn)
        list = self.client.get_list(list_fqdn)

        todo_add = set(wannabe_members) - set(members)
        if len(todo_add) > 0:
            print('Will add')
            print(todo_add)

        todo_remove = set(members) - set(wannabe_members)
        if len(todo_remove) > 0:
            print('Will remove')
            print(todo_remove)
        for user in todo_remove:
            list.unsubscribe(user)
        for user in todo_add:
            list.subscribe(user, pre_verified=True, pre_confirmed=True, pre_approved=True)
        return True


    def default_settings(self):
        return {
            "acceptable_aliases": [],
            "accept_these_nonmembers": [],
            "admin_immed_notify": True,
            "admin_notify_mchanges": False,
            "administrivia": False,
            "advertised": False,
            "allow_list_posts": True,
            "anonymous_list": False,
            "archive_policy": "private",
            "archive_rendering_mode": "text",
            "autorespond_owner": "none",
            "autorespond_postings": "none",
            "autorespond_requests": "none",
            "autoresponse_grace_period": "90d",
            "autoresponse_owner_text": "",
            "autoresponse_postings_text": "",
            "autoresponse_request_text": "",
            "bounce_info_stale_after": "7d",
            "bounce_notify_owner_on_disable": True,
            "bounce_notify_owner_on_removal": True,
            "bounce_score_threshold": 5,
            "bounce_you_are_disabled_warnings": 3,
            "bounce_you_are_disabled_warnings_interval": "7d",
            "collapse_alternatives": True,
            "convert_html_to_plaintext": False,
            "default_member_action": "defer",
            "default_nonmember_action": "hold",
            "description": "Wannabe list",
            "digest_send_periodic": False,
            "digest_size_threshold": 30.0,
            "digest_volume_frequency": "monthly",
            "digests_enabled": False,
            "discard_these_nonmembers": [],
            "dmarc_mitigate_action": "munge_from",
            "dmarc_mitigate_unconditionally": True,
            "dmarc_moderation_notice": "",
            "dmarc_wrapped_message_text": "",
            "emergency": False,
            "filter_action": "discard",
            "filter_content": False,
            "filter_extensions": [],
            "filter_types": [],
            "first_strip_reply_to": False,
            "forward_unrecognized_bounces_to": "administrators",
            "gateway_to_mail": False,
            "gateway_to_news": False,
            "hold_these_nonmembers": [],
            "include_rfc2369_headers": True,
            "info": "",
            "linked_newsgroup": "",
            "max_message_size": 128,
            "max_num_recipients": 12,
            "max_days_to_hold": 0,
            "member_roster_visibility": "moderators",
            "moderator_password": None,
            "newsgroup_moderation": "none",
            "nntp_prefix_subject_too": True,
            "pass_types": [],
            "pass_extensions": [],
            "personalize": "none",
            "posting_pipeline": "default-posting-pipeline",
            "preferred_language": "no",
            "process_bounces": True,
            "reject_these_nonmembers": [],
            "reply_goes_to_list": "no_munging",
            "reply_to_address": "",
            "require_explicit_destination": False,
            "respond_to_post_requests": True,
            "send_welcome_message": False,
            "subscription_policy": "moderate",
            "unsubscription_policy": "moderate",
            "usenet_watermark": None,
        }
