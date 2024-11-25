import requests
import matplotlib.pyplot as plt
from collections import Counter

# URL of the data lake
data_lake_url = "http://127.0.0.1:5500/data_lake"

try:
    response = requests.get(data_lake_url)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from the data lake: {e}")
    data = []

zip_codes = list(map(lambda entry: entry['zip_code'], data))

warehouse = dict(Counter(zip_codes))

zip_codes_list = list(warehouse.keys())
counts_list = list(warehouse.values())

plt.figure(figsize=(10, 6))
plt.bar(zip_codes_list, counts_list, color='skyblue')
plt.xlabel('Zip Code')
plt.ylabel('Count of Entries')
plt.title('Entries per Zip Code')
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('zip_code_distribution.png')

print("Warehouse data (zip code counts):")
print(warehouse)

plt.show()
