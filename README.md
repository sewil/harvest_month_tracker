# Missing Hours
This script checks your worked time in harvest and compares it to the full-time hours of the current month, and tells your how much you're behind or ahead of the expected worked time up until this point of the month.

# Requirements
- Python 3
- Harvest account

# Dependencies
- [Requests](http://docs.python-requests.org/en/master/)
- [Docopt](http://docopt.org/)

You can install the above dependencies with this command:
```
pip install requests docopt
```

# Usage
```
missinghours.py <harvest-api-token> <harvest-account-id> [--debug]
```

## Harvest Token and Account ID
Go to the [Harvest Developer Tools](https://id.getharvest.com/developers) and create a personal access token to retrieve the Account ID and Token.
