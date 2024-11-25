import requests
import matplotlib.pyplot as plt
from collections import Counter


def fetch_data(data_lake_url):
    try:
        response = requests.get(data_lake_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the data lake: {e}")
        return []


def process_data(data):
    zip_codes = list(map(lambda entry: entry.get('zip_code', 'Unknown'), data))
    return dict(Counter(zip_codes))


def plot_data(warehouse):
    zip_codes_list = list(warehouse.keys())
    counts_list = list(warehouse.values())

    plt.figure(figsize=(12, 8))
    plt.bar(zip_codes_list, counts_list, color='lightgreen')
    plt.xlabel('Zip Code', fontsize=14)
    plt.ylabel('Count of Entries', fontsize=14)
    plt.title('Entries per Zip Code', fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.savefig('zip_code_distribution_updated.png', dpi=300)
    plt.show()


def print_warehouse_data(warehouse):
    print("Warehouse data (zip code counts):")
    for zip_code, count in warehouse.items():
        print(f"{zip_code}: {count}")


def main():
    data_lake_url = "http://127.0.0.1:5500/data_lake"
    data = fetch_data(data_lake_url)
    warehouse = process_data(data)
    print_warehouse_data(warehouse)
    plot_data(warehouse)


if __name__ == "__main__":
    main()
