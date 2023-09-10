import requests
from bs4 import BeautifulSoup
import json
import datetime
import re
import os
import time,pytz,schedule



def job():
    with open("coin-list-small.json", 'r') as json_file:
        data = json.load(json_file)
    for url in data:
        # Define the URL to crawl
        # url = "https://coinmarketcap.com/currencies/ethereum/"

        # Extract the currency name from the URL
        currency_name = re.search(r'/currencies/([^/]+)/', url).group(1)

        # Send an HTTP GET request to the URL
        try:
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content of the page
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract the price
                price_element = soup.find("span", class_="sc-16891c57-0 dxubiK base-text")
                price = price_element.text.strip()
            error= None
        except Exception as e:
            price = None
            error=str(e)
        # Create a timestamp
        timestamp = str(datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata')))

        # Create a dictionary with the extracted information
        data = {
            "currency": currency_name,
            "price": price,
            "timestamp": timestamp,
            "source": "coinmarketcap",
        }
        if error != None:
            data.update({"error":error})

        filename = f"{currency_name}-price.json"

        if os.path.exists(filename):
            # If the file exists, load existing data
            with open(filename, 'r') as json_file:
                existing_data = json.load(json_file)

            # Append the new data to the existing data
            existing_data.append(data)

            # Save the updated data back to the file
            with open(filename, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)

            print(f"Data appended to {filename}")
        else:
            # If the file doesn't exist, create a new file with the initial data
            with open(filename, 'w') as json_file:
                json.dump([data], json_file, indent=4)

            print(f"Data saved to {filename}")



schedule.every(1).minutes.do(job)

# Run the loop indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)