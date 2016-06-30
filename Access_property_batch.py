"""A simple example of how to access the Google Analytics API."""
import json
import oauth2client
from apiclient.errors import HttpError
from apiclient.http import BatchHttpRequest
import random
import time

import argparse

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

import urllib2


def get_service(api_name, api_version, scope, key_file_location,
                service_account_email):
  """Get a service that communicates to a Google API.

  Args:
    api_name: The name of the api to connect to.
    api_version: The api version to connect to.
    scope: A list auth scopes to authorize for the application.
    key_file_location: The path to a valid service account p12 key file.
    service_account_email: The service account email address.

  Returns:
    A service that is connected to the specified API.
  """

  f = open(key_file_location, 'rb')
  key = f.read()
  f.close()

  credentials = ServiceAccountCredentials.from_p12_keyfile(service_account_email,key_file_location, scopes=scope)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service


"""A simple example of Google Analytics batched user permissions."""


def call_back(request_id, response, exception):
  """Handle batched request responses."""
  print request_id
  if exception is not None:
    if isinstance(exception, HttpError):
      message = json.loads(exception.content)['error']['message']
      print ('Request %s returned API error : %s : %s ' %
             (request_id, exception.resp.status, message))
	  
  else:
    print response


def add_users(users, permissions, service, accounts):
  for i in accounts :
	property = 'UA-%s-1' % i
	account_id = i
	batch = BatchHttpRequest(callback=call_back)
	for user in users :
		  
		  
		  link = service.management().webpropertyUserLinks().insert(
					accountId=account_id,
					webPropertyId=property,
							body={
							'permissions': {
								'local': permissions},
							'userRef': {
								'email': user }
						})
		  batch.add(link)
	batch.execute()
	time.sleep(1)
      

  
def main():
  # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/analytics.manage.users']

  # Use the developer console and replace the values with your
  # service account email and relative location of your key file.
  service_account_email = ''
  key_file_location = ''

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location,
    service_account_email)
	
  users = ['hedi.benjaafar@ext.mpsa.com']

  # call the add_users function with the list of desired permissions.
  permissions = ['COLLABORATE','_READ_AND_ANALYZE']
  accounts = ['','']
  add_users(users, permissions, service, accounts)


if __name__ == '__main__':
# Construct a list of users.
  
  main()