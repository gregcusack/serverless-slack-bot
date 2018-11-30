import requests
import sys
import os
import json
from slackclient import SlackClient
from urllib.parse import urlparse, parse_qs

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


def handle(req):
    parse_dict = parse_qs(req)#.query)
    #need a check here maybe?
    # this gets called when outgoing webhook is sent
    # check that incoming webhook is from our webhook!
    slack_token = os.getenv("auth_token_write")#"plVnQdHqD6q5kXaj28hgQ3FF"
    slack_client = SlackClient(slack_token)
    print("slack_client: {}".format(slack_client))
    print("SLACK_TOKEN: {}".format(slack_token)) 
    channels = list_channels(slack_client)
    print("req: {}".format(req))
    if channels:
        #print("Channels: ")
        for c in channels:
            #print(c['name'] + " (" + c["id"] + ")")
            detailed_info = channel_info(c['id'], slack_client)
            if detailed_info and c['name'] == 'general':
              send_message(c['id'], req, slack_client)
                send_message(c['id'], parse_dict, slack_client)
                user = parse_dict['user_name'][0] #technically a list, so take first one
                userID = parse_dict["user_id"][0]
                message = parse_dict['text'][0]
                send_message_and_tag(c['id'], userID, " says " + message, slack_client)
            print("-----")
    else:
        print("Unable to authenticate.")

    #res = requests.post('http://192.168.99.100:31112    
    #return req








