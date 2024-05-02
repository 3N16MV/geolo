#
# Alexis '3N1GMV' Lariviere
# CYB333-25957
# 27APR2024
# geojson.py Ch.13 Ex.1
# Written in Python 3.11 using PyCharm
#

#
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
#

# Ask the user to enter a username

import json
import ssl
import urllib.error
import urllib.parse
import urllib.request


def safe_input(prompt):
    """Safely get input from the user"""
    while True:  # Loop until a valid input is given
        try:
            return input(prompt)
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user.")
            return None


# Heavily rate limited proxy of Google api
# Get your own Google Maps API Key from https://developers.google.com/maps/documentation/geocoding/start
api_key = 42
serviceurl = 'http://py4e-data.dr-chuck.net/json?'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    address = input('Enter location: ')
    if not address:
        print("No location provided, exiting.")
        break

    parms = {'address': address, 'key': api_key}
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)

    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')

    try:
        js = json.loads(data)
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON.")
        print("Response data:", data)  # Print raw data for debugging
        continue  # Skip to the next iteration

    except urllib.error.URLError as e:
        print(f"Error: Could not retrieve data. Reason: {e.reason}")
        continue
    except json.JSONDecoderError:
        print("Error: Failed to parse JSON.")
        continue

    # Extract Country Code
    country_code = False
    for component in js['results'][0]['address_components']:
        if 'country' in component['types']:
            country_code = component['short_name']
            break

        if country_code:
            print('Country code:', country_code)
        else:
            print('Country code not found')

        formatted_address = js['results'][0].get('formatted_address', 'No formatted address found')
        print('Formatted address:', formatted_address)

    try:
        location = js['results'][0]['formatted_address']
    except KeyError:
        print("Warning: 'formatted_address' not found.")
        location = "Location data might be incomplete." # Set a fallback message

        print(json.dumps(js, indent=4))

        lat = js['results'][0]['geometry']['location']['lat']
        lng = js['results'][0]['geometry']['location']['lng']
        print('lat', lat, 'lng', lng)
        location = js['results'][0]['formatted_address']
        print(location)