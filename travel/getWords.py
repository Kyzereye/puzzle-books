import requests
import json

# API endpoint URL
url = "https://api.datamuse.com/words?rel_trg=travel"

try:
    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Print the categories (or process as needed)
        if 'categories' in data:
            categories = data['categories']
            for category in categories:
                print(f"Category ID: {category['id']}")
                print(f"Category Title: {category['title']}")
                print(f"Category Description: {category['description']}")
                print("-" * 20)  # Separator for readability
        else:
            print("No 'categories' found in the response.")

    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)  # Print the response content for debugging

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except json.JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}")
    print(response.text)  # Print the raw response content for debugging
