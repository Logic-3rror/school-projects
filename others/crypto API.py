import requests # used to send HTTP requests
import time # use for sleep
# URL for CoinDesk Bitcoin Price Index
# The coindesk API is accessed through URL calls
url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
# Send a GET request to the URL
response = requests.get(url)
#
# Parse the JSON response
data = response.json()
# Extract the current price of Bitcoin in USD
# You can look at the JSON result to see how this can be done.
price_usd = data['bpi']['USD']['rate']
print(price_usd)

# How might this be looped?

while True:
    time.sleep(60)
    response = requests.get(url)
    data = response.json()
    price_usd = data['bpi']['USD']['rate']
    print(price_usd)

# Create a simple game that lets you guess if the price
# of bitcoin will go up or down in the next minuite.
# ideas
# - Could you pick between a set of cyrpto currencies?
# - Have a count down (maybe in 5 second increments)
# - Keep a score
# - link to TK inter / GUI
# - any other ideas!
