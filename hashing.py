class Medicine:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return (
            f"ID: {self.product_id} | "
            f"Name: {self.name} | "
            f"Price: RM{self.price:.2f} | "
            f"Quantity: {self.quantity}"
        )

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash_numeric(self, product_id):
        return product_id % self.size

    def insert(self, product):
        start = self.hash_numeric(product.product_id)

        for i in range(self.size):
            index = (start + i) % self.size
            existing_product = self.table[index]

            if existing_product is None:
                self.table[index] = product
                return True

            if existing_product.product_id == product.product_id:
                return False

        return False

    def search(self, product_id):
        start = self.hash_numeric(product_id)

        for i in range(self.size):
            index = (start + i) % self.size
            product = self.table[index]

            if product is None:
                return False

            if product.product_id == product_id:
                return product

        return False

    def edit(self, product_id, name, price, quantity):
        start = self.hash_numeric(product_id)

        for i in range(self.size):
            index = (start + i) % self.size
            product = self.table[index]

            if product is None:
                return False

            if product.product_id == product_id:
                product.name = name
                product.price = price
                product.quantity = quantity
                return True

        return False

    def delete(self, product_id):
        start = self.hash_numeric(product_id)

        for i in range(self.size):
            index = (start + i) % self.size
            product = self.table[index]

            if product is None:
                return False

            if product.product_id == product_id:
                self.table[index] = None

                next_index = (index + 1) % self.size

                while self.table[next_index] is not None:
                    product_reinsert = self.table[next_index]
                    self.table[next_index] = None
                    self.insert(product_reinsert)

                    next_index = (next_index + 1) % self.size

                return True

        return False

def menu():
    print("==== Pharmacy Inventory System ===")
    print("1. Insert Product")
    print("2. Search Product")
    print("3. Edit Product")
    print("4. Delete Product")

def main():
    table_size = 5
    ht = HashTable(table_size)

    medicines = [
        Medicine(1001, "Paracetamol", 5.50, 50),
        Medicine(1002, "Cough Syrup", 12.00, 20),
        Medicine(1006,"Antihistamine", 9.00, 30)
    ]

    for medicine in medicines:
        if ht.insert(medicine):
            print(f"{medicine.name} is added")
        else:
            print(f"Could not add product {medicine.product_id}")

    search_result = ht.search(1006)

    if search_result is not False:
        print(f"\nMedicine found:")
        print(search_result)
    else:
        print("\nMedicine not found.")

if __name__ == "__main__":
    main()