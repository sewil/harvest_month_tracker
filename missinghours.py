import requests
import datetime
import calendar
import json
import sys
from docopt import docopt
import math

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
current_day = int(now.strftime("%d"))

month_progress = current_day/daysInMonth
debugprint(f'month progress: {month_progress}')

days_left = daysInMonth-current_day

dateFrom = now.strftime("%Y-%m-01")
debugprint(dateFrom)

dateTo = now.strftime(f'%Y-%m-{daysInMonth}')
debugprint(dateTo)

j = requests.get(f'http://api.arbetsdag.se/v1/dagar.json?fran={dateFrom}&till={dateTo}&key={workday_token}&id=1234').json()
workdays = j['antal_arbetsdagar']
debugprint(workdays)
month_hours = workdays * 8
debugprint(month_hours)

expected_hours = month_progress * month_hours
debugprint(f'expected hours: {expected_hours}')

j = requests.get(
	f'https://api.harvestapp.com/v2/time_entries?from={dateFrom}&to={dateTo}',
	headers={
		'Authorization': f'Bearer {harvest_api_token}',
		'Harvest-Account-Id': harvest_account_id
	}
).json()

total_hours = 0
expected_entries = {}
for time_entry in j['time_entries']:
	total_hours += time_entry['hours']

debugprint(f'total hours: {total_hours}')
hours_diff = total_hours-expected_hours
debugprint(f'hours diff: {hours_diff}')
hours_diff_total = total_hours-month_hours
debugprint(f'hours diff total: {hours_diff_total}')
debugprint('')

print('You are {} {:0.2f} hours and {} remain for the entire month.'.format(
	'roughly {:0.2f} hours {} schedule.'.format(math.fabs(hours_diff), 'ahead of' if hours_diff > 0 else 'behind') if math.fabs(hours_diff) > 0.5 else 'on schedule!',
	hours_diff_total * -1,
	'{} day{}'.format(days_left, '' if days_left == 1 else 's')
))
