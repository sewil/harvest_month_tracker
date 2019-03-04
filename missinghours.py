import configparser
import requests
import datetime
import calendar
import json
import functools
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
week_days = j['antal_vardagar']
print(week_days)
month_hours = week_days * 8
print(month_hours)

j = requests.get(
    f'https://api.harvestapp.com/v2/time_entries?from={dateFrom}&to={dateTo}',
    headers={
        'Authorization': f'Bearer {harvest_api_token}',
        'Harvest-Account-Id': harvest_account_id
    }
).json()

print(j['time_entries'])
total_hours = functools.reduce(lambda a, b: a['hours']+b['hours'], j['time_entries'])
print(total_hours)
expected_hours = min(month_hours, len(j['time_entries']) * 8)
print(expected_hours)
hours_diff = total_hours-expected_hours
print(hours_diff)
hours_diff_total = total_hours-month_hours
print(hours_diff_total)
print()

if hours_diff < 0:
    print(f'You are {hours_diff} hours behind. {hours_diff_total} hours for the entire month.')
else:
    print(f'You are {hours_diff} hours ahead. {hours_diff_total} hours for the entire month.')
