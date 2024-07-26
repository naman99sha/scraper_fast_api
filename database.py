import json
from pathlib import Path
from cache import Cache

class DatabaseHandler:
    def __init__(self) -> None:
        self.file_path = Path("database.json")
        self.cache = Cache()

    def load_data(self):
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return[]
    
    def save_data(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def update_database(self, products):
        current_data = self.load_data()
        updated_count = 0

        for product in products:
            cached_product = self.cache.get(product["product_title"])
            if cached_product and cached_product['product_price'] == product['product_price']:
                continue
            else:
                current_data.append(product)
                self.cache.set(product['product_title'], product)
                updated_count += 1

        self.save_data(current_data)
        return updated_count