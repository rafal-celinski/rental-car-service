import json
import requests


url = 'https://parseapi.back4app.com/classes/Car_Model_List?limit=100&excludeKeys=Year'
headers = {
    'X-Parse-Application-Id': 'hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z',
    'X-Parse-Master-Key': 'SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW'
}
data = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))

segments = set()
brands = set()
models = []

for car in data['results']:
    segment = car.get('Category')
    brand = car.get('Make')
    model = car.get('Model')

    if segment:
        segments.add(segment.split(',')[0].strip())

    if brand:
        brands.add(brand)
    if brand and model:
        models.append((brand, model, segment.split(',')[0].strip()))

insert_segments = "INSERT INTO segment (name) VALUES "
insert_segments += ", ".join([f"('{segment}')" for segment in segments]) + " ON CONFLICT DO NOTHING;"

insert_brands = "INSERT INTO brand (name) VALUES "
insert_brands += ", ".join([f"('{brand}')" for brand in brands]) + " ON CONFLICT DO NOTHING;"

insert_models = "INSERT INTO model (model_name, brand_name, segment_name) VALUES "
insert_models += ", ".join([f"('{model}', '{brand}', '{segment}')" for brand, model, segment in models]) + " ON CONFLICT DO NOTHING;"


with open('/car_model_inserts.sql', 'w') as file:
    file.write(insert_segments + '\n')
    file.write(insert_brands + '\n')
    file.write(insert_models + '\n')

print("SQL insert statements have been saved to 'car_model_inserts.sql'")