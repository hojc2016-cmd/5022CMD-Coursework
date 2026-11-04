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

def get_integer(prompt):
    value = None

    while value is None:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")

    return value


def get_float(prompt):
    value = None

    while value is None:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

    return value


def get_text(prompt):
    value = input(prompt).strip()

    while not value:
        print("This field cannot be empty.")
        value = input(prompt).strip()

    return value

def print_menu():
    print("==== Pharmacy Inventory System ===")
    print("1. Insert Product")
    print("2. Search Product")
    print("3. Edit Product")
    print("4. Delete Product")
    print("5. Exit")

def main():
    table_size = 5
    inventory = HashTable(table_size)

    choice = 0

    while choice != 5:
        print_menu()
        choice = get_integer("Enter choice(1-5): ")

        if choice == 1:
            product_id = get_integer("Enter Product ID: ")
            name = get_text("Enter Product Name: ")
            price = get_float("Enter Product Price: ")
            quantity = get_integer("Enter Stock Quantity: ")
            medicine = Medicine(product_id, name, price, quantity)

            if inventory.insert(medicine):
                print(f"Medicine is added")
            else:
                print(f"Could not add product {medicine.product_id}")
        elif choice == 2:
            product_id = get_integer("Enter Product ID: ")
            search_result = inventory.search(product_id)

            if search_result is not False:
                print(search_result)
            else:
                print("Medicine not found")

        elif choice == 3:
            product_id = get_integer("Enter Product ID: ")
            name = get_text("Enter Product Name: ")
            price = get_float("Enter Product Price: ")
            quantity = get_integer("Enter Stock Quantity: ")

            if inventory.edit(product_id, name, price, quantity):
                print(f"Medicine is edited.")
            else:
                print("Medicine not found.")
        elif choice == 4:
            product_id = get_integer("Enter Product ID: ")

            if inventory.delete(product_id):
                print("Medicine deleted successfully.")
            else:
                print("Medicine not found.")
        elif choice == 5:
            print("Exiting Inventory System. Goodbye!")

if __name__ == "__main__":
    main()