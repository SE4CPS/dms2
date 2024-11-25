import requests
import matplotlib.pyplot as plt
from collections import Counter
from itertools import chain

class FlowerDataProcessor:
    def __init__(self, url="http://localhost:5000/get_flower_data"):
        self.url = url
        self.raw_data = None
        self.data_lake = []
        self.data_warehouse = Counter()

    def fetch_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.raw_data = response.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")

    def process_data(self):
        if not self.raw_data:
            print("No data to process.")
            return

        self._create_data_lake()
        self._transform_to_warehouse()

    def _create_data_lake(self):
        extractors = {
            "MongoDB": lambda d: d["flowers"],
            "Neo4J": lambda d: d["relationships"],
            "Redis": lambda d: [{"zip_code": v["zip_code"], "source": "Redis", "flower": k} 
                                for k, v in d["inventory"].items()],
            "SQL": lambda d: d["flower_sales"]
        }

        for source, data in self.raw_data.items():
            if source in extractors:
                self.data_lake.extend(extractors[source](data))

    def _transform_to_warehouse(self):
        valid_zip_codes = (item["zip_code"] for item in self.data_lake if item["zip_code"].isdigit())
        self.data_warehouse = Counter(valid_zip_codes)

    def visualize_data(self):
        if not self.data_warehouse:
            print("No data to visualize.")
            return

        zip_codes, counts = zip(*self.data_warehouse.items())

        plt.figure(figsize=(10, 6))
        plt.bar(zip_codes, counts, color='lightgreen')
        plt.xlabel("Zip Code")
        plt.ylabel("Entry Count")
        plt.title("Data Warehouse: Entries per Zip Code")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def print_results(self):
        print("Data Lake Sample (first 5 entries):")
        print(self.data_lake[:5])
        print("\nData Warehouse:")
        print(dict(self.data_warehouse))

def main():
    processor = FlowerDataProcessor()
    processor.fetch_data()
    processor.process_data()
    processor.print_results()
    processor.visualize_data()

if __name__ == "__main__":
    main()