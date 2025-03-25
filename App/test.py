import requests
import json

# Test the /ok endpoint
response = requests.get("http://127.0.0.1:8000/ok")
print(response.json())  # shuld print {"message": "ok"}

# Test /hello with a name
response = requests.get("http://127.0.0.1:8000/hello?name=Harsh")
print(response.json())  # expectng {"message": "Hello, Harsh!"}

# Test /orders with query params
response = requests.post("http://127.0.0.1:8000/orders?product=laptop&units=2")
print(response.json())  # should say order placed for laptop

# Test /orders_pydantic with json body
data = {"product": "phone", "units": 1}
response = requests.post("http://127.0.0.1:8000/orders_pydantic", json=data)
print(response.json())  # expecting order confirmation

# Test /product_description with product details
data = {"name": "Laptop", "notes": "4GB RAM, 256 GB Disk"}
response = requests.post("http://127.0.0.1:8000/product_description", json=data)
if response.status_code == 200:
    print(response.json())  # shuld get a generated description with emojis
else:
    print(f"Error: {response.status_code} - {response.text}")