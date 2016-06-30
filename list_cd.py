"""A simple example of how to access the Google Analytics API."""

import argparse, csv

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

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

  credentials = SignedJwtAssertionCredentials(service_account_email, key,
    scope=scope)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service

# Uses the Python client library.

# Note: This code assumes you have an authorized Analytics service object.

# This request lists all custom dimensions for the authorized user.
def link_user(service):
	try:
	  dimensions = service.management().customDimensions().list(
		  accountId='',
		  webPropertyId='',
	  ).execute()

	except TypeError, error:
	  # Handle errors in constructing a query.
	  print 'There was an error in constructing your query : %s' % error

	except HttpError, error:
	  # Handle API errors.
	  print ('There was an API error : %s : %s' %
			 (error.resp.status, error.resp.reason))

	myfile = open('cD.csv', 'wb')
	fieldnames = ['ID','Name','Index','Scope','Statut']
	wr = csv.DictWriter(myfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
	wr.writeheader()

	for dimension in dimensions.get('items', []):
	  ID = dimension.get('id')
	  Name = dimension.get('name')
	  Index = dimension.get('index')
	  Scope = dimension.get('scope')
	  Statut = dimension.get('active')
	  
	  wr.writerow({'ID' : ID, 'Name' : Name, 'Index':Index,'Scope': Scope, 'Statut': Statut})
	  
	  print '%s;%s;%s;%s;%s' % (dimension.get('id'),dimension.get('name'),dimension.get('index'), dimension.get('scope'),dimension.get('active'))
	  
	  
def main():
  # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/analytics.readonly']

  # Use the developer console and replace the values with your
  # service account email and relative location of your key file.
  service_account_email = ''
  key_file_location = ''

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location,
    service_account_email)
  link_user(service)


if __name__ == '__main__':
	main()