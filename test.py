import requests

# URL of the Add Car endpoint
url = 'http://192.168.0.206:8000/api/cars'

# Data to be sent to the endpoint
car_data = {
    "model_name": "RAV4",
    "brand_name": "Toyota",
    "segment_name": "SUV",
    "production_date": "2022-01-01",
    "mileage": 0,
    "license_plate": "ABC1234",
    "vin": "1HGBH41JXMN109186"
}


# Send POST request
response = requests.post(url, json=car_data)

# Print the response from the server
print(f'Status Code: {response.status_code}')
print(f'Response Body: {response.text}')
