"""A simple example of how to access the Google Analytics API."""

import argparse
import oauth2client
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

  # Insert user email here
users = {'',''}

  # Insert list of GA account 
account = {'',''}


def link_user(service):
	for u in users :
		for x in account : 
			
			try:
			   service.management().accountUserLinks().insert(
				accountId='%s' % x,
						body={
						'permissions': {
							'local': [
								'MANAGE_USERS',
								'EDIT',
								'READ',
								'COLLABORATE',
								'ANALYZE'
								]},
						'userRef': {
							'email': '%s'% u }
					}
			   ).execute()

			   print "%s::%s::added" % (u, x)
			except TypeError, error:
			  # Handle errors in constructing a query.
			  print 'There was an error in constructing your query : %s' % error

			except urllib2.HTTPError, error:
			  # Handle API errors.
			  print ('There was an API error : %s : %s' %
					 (error.resp.status, error.resp.reason))
		# print "%s::added::user::%s" % (account[0], u)
			
						 
def main():
  scope = ['https://www.googleapis.com/auth/analytics.manage.users']
  
  # service account email and relative location of your key file.
  service_account_email = ''
  key_file_location = 'C:/users/trenouf/documents/mystuffpython/gap/client_secrets.p12'

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location,
    service_account_email)
  link_user(service)


if __name__ == '__main__':
	main()