Overview and business case: https://sf9to5.com/2017/10/11/salesforce-mass-report-mover/

# get_reports.py

A simple command line utility to dump the Name, ID, Folder Name and Last Run Date of Salesforce Reports 
based on a filter. The filter can be one of the following:
* Folder name
* Reports NOT executed in last N days
* Reports executed in last N days

## Usage

* Create sfdc.yaml with your Salesforce org credentials
* Run get_reports.py and follow the on-screen options

# mass_reports_mover.py

A command line utility to mass move Salesforce reports into a folder. 
The script takes a file with report IDs and a folder name and moves all the reports to the folder.
To get the report IDs, you can use the get_reports.py script.

## Usage

* Create sfdc.yaml with your Salesforce org credentials
* Create a text file with report IDs (each report ID on its own line)
* Run mass_reports_mover.py -i PATH_TO_FILE -f FOLDER_NAME
 

# Dependenices

* requests (http://docs.python-requests.org/en/master/)
* pyyaml (https://pypi.python.org/pypi/PyYAML)
* simple_salesforce (https://pypi.python.org/pypi/simple-salesforce)
* sfdc (https://github.com/ysfdc/salesforce_scripts/blob/master/sfdc.py)