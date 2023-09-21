import requests
import json

# Request the password list from NordPass
headers = {
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'Referer': 'https://nordpass.com/most-common-passwords-list/',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get('https://nordpass.com/json-data/top-worst-passwords/findings/all.json', headers=headers)

print(response.text)

# Convert the response to a JSON object
json_object = json.dumps(response.json())

# Write the JSON object to a file
with open("./data/nordpass_wordlist.json", "w") as outfile:
    outfile.write(json_object)