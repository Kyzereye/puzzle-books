from dotenv import load_dotenv
load_dotenv()
import requests
import json
import csv
import os

us_state_abbreviations = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

def get_cities(state_code):
    url = f"https://api.countrystatecity.in/v1/countries/US/states/{state_code}/cities"
    API_KEY = os.environ["CSC_API_KEY"]

    headers = {
        'X-CSCAPI-KEY': API_KEY
    }

    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)

    output_filename = f"{state_code}_city_names.csv"

    with open(os.path.join("csv", output_filename), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name'])
        for city in data:
            writer.writerow([city['name']])

    return len(data)

def main():
    state_city_counts = {}
    for state_code in us_state_abbreviations:
        city_count = get_cities(state_code)
        state_city_counts[state_code] = city_count
        print(f"Processed {state_code}: {city_count} cities")

    with open('state_city_counts.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['State', 'Number of Cities'])
        for state, count in state_city_counts.items():
            writer.writerow([state, count])

    print("State city counts saved to state_city_counts.csv")

if __name__ == "__main__":
    main()

