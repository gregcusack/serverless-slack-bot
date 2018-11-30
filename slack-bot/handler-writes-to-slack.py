import requests
import sys
import os
import json
from slackclient import SlackClient

#SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)
#SLACK_TOKEN = os.getenv("auth_token") #should get from env.yml
#SLACK_TOKEN = "plVnQdHqD6q5kXaj28hgQ3FF"
#slack_client = SlackClient(SLACK_TOKEN)
#print("SLACK_TOKsEN: ".format(SLACK_TOKEN)) 


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


def handle(req):
    #need a check here maybe?
    # this gets called when outgoing webhook is sent
    slack_token = os.getenv("auth_token_write")#"plVnQdHqD6q5kXaj28hgQ3FF"
    slack_client = SlackClient(slack_token)
    print("slack_client: {}".format(slack_client))
    print("SLACK_TOKEN: {}".format(slack_token)) 
    channels = list_channels(slack_client)
    if channels:
        print("Channels: ")
        for c in channels:
            print(c['name'] + " (" + c["id"] + ")")
            detailed_info = channel_info(c['id'], slack_client)
            if detailed_info:
                print('Latest text from ' + c['name'] + ':')
                print(detailed_info['latest']['text'], slack_client)
            if c['name'] == 'general':
                send_message(c['id'], "Hello " +
                             c['name'] + "! Here is the msg: " + req, slack_client)
        print("-----")
    else:
        print("Unable to authenticate.")

    #res = requests.post('http://192.168.99.100:31112    
    return req








