import requests
import base64

# Let's get our bearer token
auth_file = open('auth.txt', 'r')
key = auth_file.readline().strip()
secret = auth_file.readline().strip()

token_creds = key + ':' + secret
base64_token_creds = base64.b64encode(token_creds)

auth_url = 'https://api.twitter.com/oauth2/token'
auth_header = {'Authorization': 'Basic {}'.format(base64_token_creds),
               'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
               'User-Agent': 'Content Analyzer'}
auth_data = {'grant_type': 'client_credentials'}

token_response = requests.post(auth_url, headers=auth_header, data=auth_data)
token_json = token_response.json()

token = token_json["access_token"]

# Cool. We are authenticated. Now let's pull down the timeline.
tweets = list()

timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
query_headers = {'Authorization': 'Bearer {}'.format(token),
                 'User-Agent': 'Content Analyzer'}
query_params = {'screen_name': 'EttusResearch',
                'exclude_replies': 'true',
                'count': '200'}

#print json.dumps(timeline_json, sort_keys=True, indent=4, separators=(',', ': '))

last_id = -1

while True:
    timeline_response = requests.get(timeline_url, headers=query_headers, params=query_params)
    timeline_json = timeline_response.json()

    max_id = timeline_json[len(timeline_json) - 1]["id"]

    if(max_id == last_id):
        break
    else:
        last_id = max_id
        tweets.extend(timeline_json)
        query_params['max_id'] = '{}'.format(max_id)

print "Pulled {} tweets.".format(len(tweets))
