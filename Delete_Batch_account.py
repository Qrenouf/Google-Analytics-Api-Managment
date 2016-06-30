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

  if exception is not None:
    if isinstance(exception, HttpError):
      message = json.loads(exception.content)['error']['message']
      print ('Request %s returned API error : %s : %s ' %
             (request_id, exception.resp.status, message))
	  
  else:
    print response


def del_users(service, service2, delete):
  
	
	account_summaries = service.management().accountSummaries().list().execute()
	
	for account in account_summaries.get('items', []):
		account_id = account.get('id')
		account_links = service2.management().accountUserLinks().list(accountId=account_id).execute()
		batch = BatchHttpRequest(callback=call_back)
		
		for user in account_links.get('items', []) :
			users_ref = user.get('userRef')
			user_mail = users_ref.get('email')
			users_id = user.get('id')
			
			for x in delete : 
				if x == user_mail :
					print x
					print account_id
					
					delete_account = service2.management().accountUserLinks().delete(accountId=account_id,linkId=users_id)
					batch.add(delete_account)
		batch.execute()
		time.sleep(1)
     

  
def main():
  	
  scope = ['https://www.googleapis.com/auth/analytics.edit']
  scope2 = ['https://www.googleapis.com/auth/analytics.manage.users']
   
  service_account_email = '696657385087-lnmooj4dv65es59qoeheo4i5l4prg8ho@developer.gserviceaccount.com'
  key_file_location = 'C:/users/trenouf/documents/mystuffpython/gap/client_secrets.p12'
  
  # Put the user you want to delete
  delete = ['','']
  
  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location,
    service_account_email)
  service2 = get_service('analytics', 'v3', scope2, key_file_location,
    service_account_email)
 
  del_users(service, service2, delete)


if __name__ == '__main__':

  main()