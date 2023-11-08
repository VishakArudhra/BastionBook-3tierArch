import requests
import json

url='http://localhost:5001/'
get_all_data = {
    'operation': 'getall'
}
response = requests.post(
    url,
    json=get_all_data,
    headers={'Accept': 'application/json'}
)


#test using the following unix/linux command: 
# curl -X POST -H "Content-Type: application/json" \
# localhost:5001/print_payload -d '{"payload":"hello world!"}'

print(response.json())