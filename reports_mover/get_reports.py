import sys
import sfdc

MAIN_MENU_TEXT="""
Dump the Name, ID and Last Run Date of Salesforce Reports based on 
one of the following search options.
Please select one of the following options:
 1. Folder name
 2. Reports NOT executed in last N days
 3. Reports executed in last N days

Enter the search criterion [1-3]: """
SEARCH_BY_FOLDER = 1
SEARCH_BY_NOT_RUN = 2
SEARCH_BY_RUN = 3
RESULTS_OUTPUT_FILE = 'reports.txt'
REPORT_IDS_OUTPUT_FILE = 'report_ids.txt'

def dump_reports(soql):
	""" Dumps Salesforce report details given a SOQL """
	sf = sfdc.SFDC('sfdc.yaml')
	if not sf.connected:
		print "[ERROR]: No connection to Salesforce"
		return False

	results = sf.run_soql(soql)
	if not results or not results.get('totalSize', 0):
		print "[INFO]: No reports matching search criterion"
		return False

	print "[INFO]: %d reports matched" % results.get('totalSize')
	report_ids = []
	lines = []
	for record in results.get('records'):
		line = "%s,%s,%s" % (record.get('Id'), 
							 record.get('Name'), 
							 record.get('LastRunDate'))
		lines.append(line)
		report_ids.append(record.get('Id'))

	with open(RESULTS_OUTPUT_FILE, 'wb') as full_results_file:
		full_results_file.write('\r\n'.join(lines))
	with open(REPORT_IDS_OUTPUT_FILE, 'wb') as report_ids_file:
		report_ids_file.write('\r\n'.join(report_ids))
	print ("[INFO]: Full results: %s, Report IDs: %s"
		   % (RESULTS_OUTPUT_FILE, REPORT_IDS_OUTPUT_FILE))
	return True

def main():
	criteria = int(raw_input(MAIN_MENU_TEXT))
	if criteria == SEARCH_BY_FOLDER:
		folder_name = raw_input("Enter folder name: ")
		print "[INFO]: Searching for reports in folder %s" % folder_name
		soql = ("SELECT Id, Name, LastRunDate FROM Report "
				"WHERE IsDeleted = FALSE AND "
				"FolderName = '%s'" % folder_name)
	elif criteria == SEARCH_BY_NOT_RUN:
		ndays = int(raw_input("Enter number of days: "))
		print ("[INFO]: Searching for reports that were NOT "
			   "executed in the last %d days" % ndays)
		# if report was never executed, the LastRunDate will be null
		soql = ("SELECT Id, Name, LastRunDate FROM Report "
				"WHERE IsDeleted = FALSE AND "
				"((LastRunDate = null) OR "
				"(LastRunDate < LAST_N_DAYS:%d))" % ndays)
	elif criteria == SEARCH_BY_RUN:
		ndays = int(raw_input("Enter number of days: "))
		print ("[INFO]: Searching for reports that were "
			   "executed in the last %d days" % ndays)
		soql = ("SELECT Id, Name, LastRunDate FROM Report "
				"WHERE IsDeleted = FALSE AND "
				"LastRunDate >= LAST_N_DAYS:%d" % ndays)
	else:
		print "Invalid search option."
		return

	dump_reports(soql)

if __name__ == "__main__":
	main()