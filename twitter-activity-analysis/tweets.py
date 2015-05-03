import os
import glob
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

token = requests.post(auth_url, headers=auth_header, data=auth_data)

print token.text
