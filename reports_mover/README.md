# get_reports.py

## Description

A simple command line utility to dump the Name, ID and Last Run Date of Salesforce Reports 
based on a filter. The filter can be one of the following:
* Folder name
* Reports NOT executed in last N days
* Reports executed in last N days

## Dependenices

* requests (http://docs.python-requests.org/en/master/)
* pyyaml (https://pypi.python.org/pypi/PyYAML)
* simple_salesforce (https://pypi.python.org/pypi/simple-salesforce)
* sfdc (https://github.com/ysfdc/salesforce_scripts/blob/master/sfdc.py)

## Usage

* Create sfdc.yaml with your Salesforce org credentials
* Run get_reports.py and follow the on-screen options