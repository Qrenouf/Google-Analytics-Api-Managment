"""A simple example of how to access the Google Analytics API."""

import argparse, csv, json, io

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pprint
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

# abc.setdefault(key,[])
  
def link_user(service):
	
	try:
	  account_summaries = service.management().accountSummaries().list().execute()
												 
	  

	except TypeError, error:
	  
	  print ('There was an error in constructing your query : %s' % error)

	except urllib2.HttpError, error:
	 
	  print ('There was an API error : %s : %s' %
			 (error.resp.status, error.resp.reason))
	
	with io.open('data.json', 'w', encoding='utf-8') as f:
		f.write(unicode(json.dumps(account_summaries, ensure_ascii=False)))


def transform_csv() :

	sep = ';'



	j = json.load(open('data.json'))



	csvfile = open("account.csv", 'a')



	# print "username{0}kind{0}kind{0}kind{0}name{0}level{0}kind{0}type{0}id{0}name{0}internalWebPropertyId{0}id".format(sep)

	csvfile.write("name{0}type{0}id_view{0}name_view{0}id\n".format(sep))





	for a in j['items'] :

		for b in a['webProperties'] :

			for c in b['profiles'] :

				l = "{1}{0}{2}{0}{3}{0}{4}{0}{5}\n".format(sep,

																								b['name'].encode("utf-8", 'ignore'),

																								c['type'].encode("utf-8", 'ignore'),

																								c['id'].encode("utf-8", 'ignore'),

																								c['name'].encode("utf-8", 'ignore'),

																								b['id'].encode("utf-8", 'ignore'))

				

				csvfile.write(l)		
		
		
		

			
def main():
  
  scope = ['https://www.googleapis.com/auth/analytics.edit']

  # Put you services account here
  service_account_email = '696657385087-lnmooj4dv65es59qoeheo4i5l4prg8ho@developer.gserviceaccount.com'
  
  # Put the path to your key file :
  key_file_location = 'C:/users/trenouf/documents/mystuffpython/gap/client_secrets.p12'

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location,
    service_account_email)
  link_user(service)
  transform_csv()
  


if __name__ == '__main__':
	main()