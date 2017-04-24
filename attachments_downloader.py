from simple_salesforce import Salesforce
import requests
import logging
import argparse
import os

def download_attachments(args):
	session = requests.Session()
	try:
		sf = Salesforce(username=args.get('user'), 
						password=args.get('passwd'), 
						security_token=args.get('token'), 
						session=session)
	except Exception, e:
		logging.error("Failed to connect SFDC: %s", str(e))
		return

	auth_id = 'Bearer ' + sf.session_id
	req_headers = {'Authorization': auth_id}

	query = "SELECT Id, Name, Body FROM Attachment"
	result = sf.query_all(query)

	total_records = result.get('totalSize', 0)
	if not total_records:
		logging.info("No attachments found")
		return

	logging.debug("Starting to download %d attachments", total_records)
	
	storage_dir = args.get('storage')
	sf_pod = sf.base_url.replace("https://", "").split('.salesforce.com')[0]
	records = result.get('records', {})
	for record in records:
		body_uri = record.get('Body')
		if not body_uri:
			logging.warning("No body URI for file id %s", record.get('Id', ''))
			continue

		remote_file = "https://{0}.salesforce.com{1}".format(sf_pod, body_uri)
		local_file = os.path.join(storage_dir, record.get('Name'))
		if os.path.exists(local_file):
			alt_local_filename = "%s_%s" % (record.get('Id'), 
											record.get('Name'))
			local_file = os.path.join(storage_dir, alt_local_filename)
			logging.warning("Local file %s exists; Storing as %s",
							record.get('Name'),
							alt_local_filename)

		logging.info("Downloading %s to %s", record.get('Name'), local_file)
		logging.debug("Remote URL: %s", remote_file)

		resp = session.get(remote_file, headers=req_headers)
		if resp.status_code != 200:
			logging.error("Download failed [%d]", resp.status_code)
			continue

		with open(local_file, 'wb') as out_file:
			out_file.write(resp.content)

if __name__ == "__main__":
	cli_parser = argparse.ArgumentParser(description='SFDC Attachments Downloader')
	cli_parser.add_argument('-u', '--user',  help='SFDC username')
	cli_parser.add_argument('-p', '--passwd', help='SFDC password')
	cli_parser.add_argument('-t', '--token', help='SFDC security token')
	cli_parser.add_argument('-s', '--storage', help='Path to store attachments')
	
	args = cli_parser.parse_args()
	if any(v is None for v in vars(args).values()):
		print "All arguments are required!"
		sys.exit(1)

	print "Starting downloader..."

	logging.basicConfig(level=logging.DEBUG, 
						format='%(asctime)s - %(levelname)s - %(message)s',
						filename='attachments_downloader.log',
						filemode='w')

	download_attachments(vars(args))

	print "Done."