import requests
from collections import Counter
from itertools import chain

class FlowerDataProcessor:
    def __init__(self, url="http://localhost:5000/get_flower_data"):
        self.url = url
        self.raw_data = None
        self.data_lake = []
        self.data_warehouse = {}

    def fetch_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.raw_data = response.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")

    def create_data_lake(self):
        if not self.raw_data:
            print("No data to process.")
            return

        extractors = {
            "MongoDB": lambda d: d["flowers"],
            "Neo4J": lambda d: d["relationships"],
            "Redis": lambda d: [{"zip_code": v["zip_code"], "source": "Redis", "flower": k} 
                                for k, v in d["inventory"].items()],
            "SQL": lambda d: d["flower_sales"]
        }

        self.data_lake = list(chain.from_iterable(extractors[source](data) 
                                                  for source, data in self.raw_data.items() 
                                                  if source in extractors))

    def transform_to_warehouse(self):
        zip_codes = (item["zip_code"] for item in self.data_lake if item["zip_code"].isdigit())
        self.data_warehouse = dict(Counter(zip_codes))

    def process_data(self):
        self.create_data_lake()
        self.transform_to_warehouse()

    def print_results(self):
        print("Data Lake (first 5 entries):")
        print(self.data_lake[:5])
        print("\nData Warehouse:")
        print(self.data_warehouse)

def main():
    processor = FlowerDataProcessor()
    processor.fetch_data()
    processor.process_data()
    processor.print_results()

if __name__ == "__main__":
    main()