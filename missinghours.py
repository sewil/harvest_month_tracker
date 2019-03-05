import requests
import datetime
import calendar
import json
import sys
from docopt import docopt

arguments = docopt("""Missing Hours.

Usage:
  missinghours.py <harvest-api-token> <harvest-account-id> <workday-token>

Options:
  -h, --help        Show this screen.
  -v, --version     Show version.
""", argv=None, help=True, version='Missing Hours 0.1.0', options_first=False)

print(arguments)
harvest_api_token = arguments['<harvest-api-token>']
harvest_account_id = arguments['<harvest-account-id>']
workday_token = arguments['<workday-token>']
print(harvest_api_token)
print(harvest_account_id)
print(workday_token)

now = datetime.datetime.now()
daysInMonth = calendar.monthrange(now.year, now.month)[1]
print(daysInMonth)
dateFrom = now.strftime("%Y-%m-01")
print(dateFrom)

dateTo = now.strftime(f'%Y-%m-{daysInMonth}')
print(dateTo)

j = requests.get(f'http://api.arbetsdag.se/v1/dagar.json?fran={dateFrom}&till={dateTo}&key={workday_token}&id=1234').json()
print(j)
print(month_hours)
workdays = j['antal_arbetsdagar']
print(workdays)
month_hours = workdays * 8

j = requests.get(
    f'https://api.harvestapp.com/v2/time_entries?from={dateFrom}&to={dateTo}',
    headers={
        'Authorization': f'Bearer {harvest_api_token}',
        'Harvest-Account-Id': harvest_account_id
    }
).json()

print(j['time_entries'])
total_hours = 0
for time_entry in j['time_entries']:
	total_hours += time_entry['hours']
print(total_hours)
expected_hours = min(month_hours, len(j['time_entries']) * 8)
print(expected_hours)
hours_diff = total_hours-expected_hours
print(hours_diff)
hours_diff_total = total_hours-month_hours
print(hours_diff_total)
print()

if hours_diff < 0:
    print('You are {:0.2f} hours behind. {:0.2f} hours for the entire month.'.format(hours_diff, hours_diff_total))
else:
    print('You are {:0.2f} hours ahead. {:0.2f} hours for the entire month.'.format(hours_diff, hours_diff_total))
