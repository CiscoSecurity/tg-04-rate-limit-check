import os
import sys
import requests

# Validate a command-line argument was provided
if len(sys.argv) < 2:
    sys.exit('No API Key provided!\n\n'
             'Usage:\n {0} <API_KEY>\n\n'
             'Example:\n {0} 139ec4f94a8c908e20e7c2dce5092af4'
             .format(os.path.basename(__file__)))

api_key = sys.argv[1]

host_name = 'panacea.threatgrid.com'

def get(query):
    """ Get the URL and return decoded JSON"""
    try:
        response = requests.get(query)
        if response.status_code // 100 != 2:
            return "Error: {}".format(response)
        return response.json()
    except requests.exceptions.RequestException as error_message:
        return 'Error: {}'.format(error_message)

def whoami(_host_name=host_name, _api_key=api_key):
    """ Build the WHOAMI URL """
    whoami_url = 'https://{}/api/v3/session/whoami?api_key={}'.format(_host_name, _api_key)
    return whoami_url

def limit(_login, _host_name=host_name, _api_key=api_key):
    """ Build the rate limit URL """
    rate_limit_url = ('https://{}/api/v3/users/{}/rate-limit?api_key={}'
                      .format(_host_name, _login, _api_key))
    return rate_limit_url

# Get login
login = get(whoami())['data']['login']

# Use login to get rate-limit information
limit = get(limit(login))

# Parse user limits from rate-limit information
user_available = limit['data']['user']['submissions-available']
user_wait = limit['data']['user']['submission-wait-seconds']

# Parse org limits from rate-limit inoformation
org_available = limit['data']['organization']['submissions-available']
org_wait = limit['data']['organization']['submission-wait-seconds']

# Print output
print('Your login is: {}\n'.format(login))

print('You have {} samples available '
      '(if \'None\' there are no user specific limits)'.format(user_available))
print('You must wait {} seconds before submitting another sample\n'.format(user_wait))

print('Your org has {} samples available'.format(org_available))
print('Your org must wait {} seconds before submitting another sample'.format(org_wait))
