import requests


response = requests.get('http://localhost:80/recommendations?user_id=18')
print(response.json())

response = requests.get('http://localhost:80/recommendations?user_id=18&returnMetadata=true')
print(response.json())

response = requests.get('http://localhost:80/features?user_id=18')
print(response.json())
