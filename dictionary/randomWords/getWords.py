import requests

url = "https://free-random-word-generator-api.p.rapidapi.com/random-word"

headers = {
	"x-rapidapi-key": "ac047a5ee6msh6a36c242bd7baa1p17b71fjsnfbb66fea3fa7",
	"x-rapidapi-host": "free-random-word-generator-api.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response)

