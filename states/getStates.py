from dotenv import load_dotenv
load_dotenv()
import requests
import json
import csv
import sys
import os

def main(state_code):
    """
    Fetches city data for a given state and saves it to a CSV file in the 'csv' folder.

    Args:
        state_code (str): The state code to fetch cities for (e.g., 'NY').
    """
    url = f"https://api.countrystatecity.in/v1/countries/US/states/{state_code}/cities"
    API_KEY = os.environ["CSC_API_KEY"]

    headers = {
        'X-CSCAPI-KEY': API_KEY
    }

    response = requests.request("GET", url, headers=headers)

    # Parse the JSON response
    data = json.loads(response.text)

    # Construct the output filename
    output_filename = f"{state_code}_city_names.csv"

    # Extract names and write to CSV in the 'csv' folder
    with open(os.path.join("csv", output_filename), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name'])  # Write header
        for city in data:
            writer.writerow([city['name']])

    # Print count in terminal
    print(f"Total number of cities in {state_code}: {len(data)}")
    print(f"CSV file saved as: csv/{output_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 getStates.py <state_code>")
        sys.exit(1)

    state_code = sys.argv[1]
    main(state_code)
