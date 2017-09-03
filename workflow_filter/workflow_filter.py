import json
import yaml
import sys
import codecs
import sfdc

# Valid values for trigger_type in config file:
#
# onCreateOrTriggeringUpdate:
#	Evaluate the rule when a record is created and anytime is
#	edited to meet criteria
#
# onCreateOnly:
#	Evaluate the rule when created
#
# onAllChanges:
#	Evaluate then rule when created and everytime it's edited
#
# Valid values for action_type in config file:
#	Alert, FieldUpdate, OutboundMessage, Task

# path to SFDC account information
SFDC_CONFIG_FILE='./sfdc.yaml'
# path to workflow filter configuration
FILTER_CONFIG_FILE='./workflow_filter.yaml'
# output file
RESULT_FILE='./workflows.txt'

sf = sfdc.SFDC(SFDC_CONFIG_FILE)
if not sf.connected:
	print "[ERROR]: Couldn't connect to salesforce"
	sys.exit(1)

with open(FILTER_CONFIG_FILE) as filter_config:
	filter_settings = yaml.load(filter_config) or {}

trigger_type = None
action_type = None

if 'trigger_type' in filter_settings:
	trigger_type = filter_settings['trigger_type']

if 'action_type' in filter_settings:
	action_type = filter_settings['action_type']

# Get workflow rules
query = "SELECT Id FROM WorkflowRule"
if 'object_name' in filter_settings:
	query = query + " WHERE TableEnumOrId='%s'" % filter_settings['object_name']

results = sf.query_tooling_api(query)
if not results:
	print "[INFO]: No workflow rules found"
	sys.exit(0)

print "[INFO]: Sifting through %d workflow rules" % len(results['records'])

matched_rules_count = 0
out_file = codecs.open(RESULT_FILE, 'wb', 'utf-16')
for record in results['records']:
	workflow_id = record['Id']
	# Get workflow rule information
	query = "SELECT Name, Metadata FROM WorkflowRule WHERE Id='%s'" % workflow_id
	resp = sf.query_tooling_api(query)
	if not resp:
		continue

	workflow_metadata = resp['records'][0]['Metadata']
	# Ignore inactive workflow rules
	if workflow_metadata['active'] == False:
		continue

	# Filter out by workflow trigger type if specified
	if trigger_type and workflow_metadata['triggerType'] != trigger_type:
		continue

	# Filter out by workflow action type when specified
	if action_type:
		actions = workflow_metadata['actions']
		match = any(action['type'] == action_type for action in actions)
		if not match:
			continue

	workflow_name = resp['records'][0]['Name']
	out_file.write("'%s',%s\r\n" % (workflow_name, workflow_id))
	matched_rules_count += 1

print "[INFO]: Found %d rules matching filter criteria" % matched_rules_count

out_file.close()