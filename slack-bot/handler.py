import requests
import sys
import os
import json
from slackclient import SlackClient
from urllib.parse import urlparse, parse_qs

"""
def list_channels(slack_client):
    channels_call = slack_client.api_call("channels.list")
    if channels_call['ok']:
        return channels_call['channels']
    return None

def channel_info(channel_id, slack_client):
    channel_info = slack_client.api_call("channels.info", channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None

def send_message(channel_id, message, slack_client):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='Welcome Bot',
        icon_emoji=':robot_face:'
    )

def send_message_and_tag(channel_id, userID, message, slack_client):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        #link_names=1,
        text='<@' + userID + '>' + message, #need to use userID for new slack API update
        username='Welcome Bot',
        icon_emoji=':robot_face:'
    )

def welcome_to_channel(channel_id, userID, slack_client):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text="Let's welcome <@" + userID + "> to the channel!" + " :aceventura_dance: :donut_parrot: :aww_yeah: :avocato2:",
        username='Welcome Bot',
        icon_emoji=':finger_guns:'
    )
"""

def welcome_to_channel_v2(channel_id, userID, slack_client):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text="Let's welcome <@" + userID + "> to the <#" + channel_id + "> channel!" + " :aceventura_dance: :donut_parrot: :aww_yeah: :avocato2:",
        username='Welcome Bot',
        icon_emoji=':finger_guns:'
    )

def handle(req):
    parsed_json = json.loads(req)
    secret = os.getenv("slack_auth_token")
    if parsed_json["token"] != secret:
        print("Invalid token.  Request possibly not sent from Slack.  Exiting...")
        return

    # Avoid duplicate event triggers when scaling from 0
    try:
        retry_header = os.getenv("Http_X_Slack_Retry_Num")
        if retry_header:
            return
    except:
        pass

    slack_token = os.getenv("auth_token_write")#"plVnQdHqD6q5kXaj28hgQ3FF"
    slack_client = SlackClient(slack_token)
    try:
        joined_channel = parsed_json["event"]["channel"] #same as c['id']
        userID = parsed_json["event"]["user"]
        welcome_to_channel_v2(joined_channel, userID, slack_client)
    except:
        print("Error!  Bad request.  Can't parse JSON")






