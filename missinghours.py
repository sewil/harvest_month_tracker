import requests
import datetime
import calendar
import json
import sys
from docopt import docopt

arguments = docopt("""Missing Hours.

Usage:
  missinghours.py <harvest-api-token> <harvest-account-id> [--debug]

Options:
  -h, --help        Show this screen.
  -v, --version     Show version.
  -d, --debug       Display debug output.
""", argv=None, help=True, version='Missing Hours 0.1.0', options_first=False)


def debugprint(message):
	if arguments['--debug']:
		print(message)

harvest_api_token = arguments['<harvest-api-token>']
harvest_account_id = arguments['<harvest-account-id>']
workday_token = '6beda5db0166cdf21a74ad4a85b6772c241e1e26'
debugprint(arguments)
debugprint(harvest_api_token)
debugprint(harvest_account_id)
debugprint(workday_token)

def isWorkday(date):
	j = requests.get(f'http://api.arbetsdag.se/v1/dagar.json?fran={date}&till={date}&key={workday_token}&id=1234').json()
	isWorkday = j['antal_helgdagar'] == 0
	debugprint('{} {}'.format(date, 'is a workday' if isWorkday else 'is not a workday'))
	return isWorkday

now = datetime.datetime.now()
daysInMonth = calendar.monthrange(now.year, now.month)[1]
debugprint(daysInMonth)
dateFrom = now.strftime("%Y-%m-01")
debugprint(dateFrom)

dateTo = now.strftime(f'%Y-%m-{daysInMonth}')
debugprint(dateTo)

j = requests.get(f'http://api.arbetsdag.se/v1/dagar.json?fran={dateFrom}&till={dateTo}&key={workday_token}&id=1234').json()
debugprint(j)
workdays = j['antal_arbetsdagar']
debugprint(workdays)
month_hours = workdays * 8
debugprint(month_hours)

j = requests.get(
	f'https://api.harvestapp.com/v2/time_entries?from={dateFrom}&to={dateTo}',
	headers={
		'Authorization': f'Bearer {harvest_api_token}',
		'Harvest-Account-Id': harvest_account_id
	}
).json()

debugprint(j['time_entries'])
total_hours = 0
expected_entries = {}
for time_entry in j['time_entries']:
	total_hours += time_entry['hours']
	spent_date = time_entry['spent_date']
	if spent_date not in expected_entries and isWorkday(spent_date):
		expected_entries[spent_date] = time_entry

debugprint(total_hours)
expected_hours = min(month_hours, len(expected_entries) * 8)
debugprint(expected_hours)
hours_diff = total_hours-expected_hours
debugprint(hours_diff)
hours_diff_total = total_hours-month_hours
debugprint(hours_diff_total)
debugprint('')

if hours_diff != 0 or hours_diff_total != 0:
	print('You are {:0.2f} hours {} schedule. {:0.2f} hours {} for the entire month.'.format(
		hours_diff,
		'ahead of' if hours_diff > 0 else 'behind',
		hours_diff_total,
		'ahead' if hours_diff_total > 0 else 'remaining'
	))
else:
	print('You are on schedule!')
