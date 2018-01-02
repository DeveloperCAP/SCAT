import requests
import json


def fetch_team(domain):
    """
    This function uses the SlackArchive API endpoint to fetch the metadata of the team that belongs to a domain.
    :param domain: The domain of the Slack team. Eg. 'kubernetes' in 'https://kubernetes.slackarchive.io/'
    :return: A dict containing the metadata of the team that belongs to the domain passed as the parameter.
    """
    url = 'https://api.slackarchive.io/v1/team?domain=%s' % domain
    origin_header = {"referer": "https://%s.slackarchive.io/" % domain}
    s = requests.Session()
    teams = s.get(url, headers=origin_header)
    return json.loads(teams.content.decode('utf-8'))['team'][0]


def fetch_channels(domain, team_id):
    """
    This function uses the SlackArchive API endpoint to fetch all the channels that are in a team along
    with the relevant channel metadata.
    :param domain: The domain of the Slack team. Eg. 'kubernetes' in 'https://kubernetes.slackarchive.io/'
    :param team_id: The unique team identifier as returned by the fetch_team function.
    :return: A dict containing all the channels that are in the team identified by team_id, along with
    relevant channel metadata.
    """
    url = 'https://api.slackarchive.io/v1/channels?team_id=%s' % team_id
    origin_header = {"referer": "https://%s.slackarchive.io/" % domain}
    s = requests.Session()
    channels = s.get(url, headers=origin_header)
    return json.loads(channels.content.decode('utf-8'))['channels']


def fetch_messages(domain, team_id, channel_id, size, offset):
    """
    This function returns a list of messages from a channel according to the range specified by the size
    and offset parameters.
    :param domain: The domain of the Slack team. Eg. 'kubernetes' in 'https://kubernetes.slackarchive.io/'
    :param team_id: The unique team identifier as returned by the fetch_team function.
    :param channel_id: The unique channel identifier as returned by the fetch_channel function.
    :param size: The number of messages to fetch, in a reverse-chronological order.
    :param offset: The number of messages to skip while fetching, in a reverse-chronological order. An
    offset of 5 with a size of 100 will fetch the 100 messages after the 5 latest messages in a channel.
    :return: A dict containing a list of messages from the specified channel, in a reverse-chronological
    order, according to the range specified by the size and offset parameters.
    """
    url = "https://api.slackarchive.io/v1/messages?size=%d&team=%s&channel=%s&offset=%d" % (size, team_id, channel_id, offset)
    origin_header = {"referer": "https://%s.slackarchive.io/" % domain}
    s = requests.Session()
    messages = s.get(url, headers=origin_header)
    return json.loads(messages.content.decode('utf-8'))

def initialize():
    team_name = input('Enter team name : ')
    team_data = fetch_team(team_name)
    channels = fetch_channels(team_name, team_data['team_id'])
    team_to_json(team_data)
    channel_to_json(channels)
    messages_to_json(team_name, team_data, channels)
    users_to_json(team_name, team_data, channels)


def messages_to_json(team_name, team_data, channels):
    list_messages = []
    for channel in channels:
        if channel['name'] != '':
            for i in range(0, 1000, 100):
                messages = fetch_messages(team_name, team_data['team_id'], channel['channel_id'], 100, i)
                list_messages = list_messages + messages['messages']
            
            print('Completing ' + channel['name'])

            parsed_messages = json.dumps(list_messages, indent=4, sort_keys=True)

            message_file = open('messages/' + channel['name'] + '.json', 'w')
            message_file.write(parsed_messages)
            message_file.close()

def users_to_json(team_name, team_data, channels):
    list_users = []
    for channel in channels:
        if channel['name'] != '':
            for i in range(0, 1000, 100):
                users = fetch_messages(team_name, team_data['team_id'], channel['channel_id'], 100, 0)
                
            print('Completing ' + channel['name'])

            user_related = users['related']
            parsed_users = json.dumps(user_related['users'], indent=4, sort_keys=True)

            user_file = open('users/' + channel['name'] + '.json')
            user_file.write(parsed_users)
            user_file.close()

def team_to_json(team_data):
    parsed_team_data = json.dumps(team_data, indent=4, sort_keys=True)
    team_file = open('team.json', 'w')
    team_file.write(parsed_team_data)
    team_file.close()

def channel_to_json(channels):
    parsed_channels = json.dump(channels, indent=4, sort_keys=True)
    channel_file = open('channel.json', 'w')
    channel_file.write(parsed_channels)
    channel_file.close() 


if __name__ == "__main__":
    # Frame the test cases along these lines. These are to provide you an example for usage of this module.
    team_data = fetch_team('kubernetes')
    channels = fetch_channels('kubernetes', team_data['team_id'])
    list_messages = []
    for channel in channels:
        if channel['name'] != '':
            for i in range(0, 10, 100):
                messages = fetch_messages('kubernetes', team_data['team_id'], channel['channel_id'], 100, i)
                list_messages = list_messages + messages["messages"]
            print('Completing ' + channel['name'])

            parsed_data_messages = json.dumps(list_messages, indent=4, sort_keys=True)

            kub_data = open('messages/' + channel['name'] + '_messages.json', 'w')
            kub_data.write(parsed_data_messages)
            kub_data.close()

    
    parsed_data_channels = json.dumps(channels, indent=4, sort_keys=True)
    parsed_data_team = json.dumps(team_data, indent=4, sort_keys=True)


    kub_data = open('channels.json', 'w')
    kub_data.write(parsed_data_channels)
    kub_data.close()

    kub_data = open('team.json', 'w')
    kub_data.write(parsed_data_team)
    kub_data.close()