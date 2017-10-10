import json
import argparse
import sfdc

def move_reports(input_file, folder_name):
	""" Moves Salesforce Reports to a folder """
	sf = sfdc.SFDC('sfdc.yaml')
	if not sf.connected:
		print "[ERROR]: No connection to Salesforce"
		return False

	soql = "SELECT Id FROM Folder WHERE Name='%s'" % folder_name
	results = sf.run_soql(soql)
	# We only expect one result as folder name is unique
	if not results or results.get('totalSize', -1) != 1:
		print "[ERROR]: Cannot folder %s" % folder_name
		return False

	record = results.get('records')[0]
	folder_id = record.get('Id')
	print "[INFO]: Folder %s, ID: %s" % (folder_name, folder_id)

	with open(input_file, 'r') as input_file:
		report_ids = filter(None, input_file.read().splitlines())

	print "[INFO]: Moving %d reports" % (len(report_ids))
	params = json.dumps({
		"reportMetadata": {
			"folderId": folder_id
		}})
	for report_id in report_ids:
		sf.update_analytics_api(report_id, params)

if __name__ == "__main__":
	cli_parser = argparse.ArgumentParser(description="Mass Reports Mover")
	cli_parser.add_argument('-f',
							'--folder',
							help='Folder name',
							required=True)
	cli_parser.add_argument('-i',
							'--input_file',
							help='File containing Reports ID',
							required=True)
	args = cli_parser.parse_args()
	# All options are required
	if any(v is None for v in vars(args).values()):
		cli_parser.print_help()
		sys.exit(1)
		
	move_reports(args.input_file, args.folder)