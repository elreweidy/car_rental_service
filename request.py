import requests
import json

# Replace the URL with the endpoint URL of your Flask app
url = "http://localhost:5000/bookings"

# Replace the data with the booking information you want to add
data = {
    "customer_id": 2,
    "vehicle_id": 2,
    "hire_date": "2023-03-15",
    "return_date": "2023-03-20",
}

# Set the content type to JSON
headers = {"Content-type": "application/json"}

# Make a POST request to the endpoint with the data
response = requests.post(url, data=json.dumps(data), headers=headers)

# Print the response status code and message
print(f"Status code: {response.status_code}")
print(f'Response message: {response.json()["message"]}')
