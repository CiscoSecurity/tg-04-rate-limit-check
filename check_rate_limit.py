import os
import sys
import requests


def get(url):
    """ GET the URL and return decoded JSON"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error_message:
        sys.exit(error_message)


def whoami(_host_name, _api_key):
    """
    Build and query whoami URL
    Return login for API key
    """
    whoami_url = f'https://{_host_name}/api/v3/session/whoami?api_key={_api_key}'
    return get(whoami_url)['data']['login']


def limits(_login, _host_name, _api_key):
    """
    Build and query rate limit URL
    Return dictionary with elements we care about
    """
    rate_limit_url = (f'https://{_host_name}/api/v3/users/{_login}/rate-limit?api_key={_api_key}')
    response = get(rate_limit_url)

    user_available = response['data']['user']['submissions-available']
    user_wait = response['data']['user']['submission-wait-seconds']
    org_available = response['data']['organization']['submissions-available']
    org_wait = response['data']['organization']['submission-wait-seconds']

    return {'user_available':user_available,
            'user_wait':user_wait,
            'org_available':org_available,
            'org_wait':org_wait}


try:
    api_key = sys.argv[1]
except IndexError as error_message:
    sys.exit('No API Key provided!\n\n'
             'Usage:\n {0} <API_KEY>\n\n'
             'Example:\n {0} 139ec4f94a8c908e20e7c2dce5092af4'
             .format(os.path.basename(__file__)))

host_name = 'panacea.threatgrid.com'

# Get login
login = whoami(host_name, api_key)

# Use login to get rate-limit information
limits = limits(login, host_name, api_key)

# Print output
print(f'Your login is: {login}\n')

if limits["user_available"]:
    print(f'You have {limits["user_available"]} samples available ')
else:
    print('You have no user specific limits')
print(f'You must wait {limits["user_wait"]} seconds before submitting another sample\n')

print(f'Your org has {limits["org_available"]} samples available')
print(f'Your org must wait {limits["org_wait"]} seconds before submitting another sample')
