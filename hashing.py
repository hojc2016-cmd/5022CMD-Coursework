from time import perf_counter_ns

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
        self.deleted = [False] * size

    def hash_numeric(self, product_id):
        return product_id % self.size

    def insert(self, product):
        start = self.hash_numeric(product.product_id)
        first_deleted = None

        for i in range(self.size):
            index = (start + i) % self.size
            existing_product = self.table[index]

            if self.deleted[index]:
                if first_deleted is None:
                    first_deleted = index
                continue

            if existing_product is None:
                if first_deleted is not None:
                    index = first_deleted

                self.table[index] = product
                self.deleted[index] = False
                return True

            if existing_product.product_id == product.product_id:
                return False

        if first_deleted is not None:
            self.table[first_deleted] = product
            self.deleted[first_deleted] = False
            return True

        return False

    def search(self, product_id):
        start = self.hash_numeric(product_id)

        for i in range(self.size):
            index = (start + i) % self.size
            product = self.table[index]

            if self.deleted[index]:
                continue

            if product is None:
                return False

            if product.product_id == product_id:
                return product

        return False

    def edit(self, product_id, name, price, quantity):
        product = self.search(product_id)

        if product is False:
            return False

        product.name = name
        product.price = price
        product.quantity = quantity
        return True

    def delete(self, product_id):
        start = self.hash_numeric(product_id)

        for i in range(self.size):
            index = (start + i) % self.size
            product = self.table[index]

            if self.deleted[index]:
                continue

            if product is None:
                return False

            if product.product_id == product_id:
                self.table[index] = None
                self.deleted[index] = True
                return True

        return False

    def display(self):
        total_products = sum(1 for product in self.table if product is not None)

        occupied_percentage = (total_products / self.size) * 100

        print("\n==== Current Inventory ====")
        print(f"Total products / Table size: {total_products}/{self.size}")
        print(f"Occupied: {occupied_percentage:.1f}%")

        border = (
            "+-------+------------+--------------------------+"
            "------------+----------+"
        )

        print(border)
        print(
            f"| {'Index':<5} | {'Product ID':<10} | {'Name':<24} | "
            f"{'Price (RM)':>10} | {'Quantity':>8} |"
        )
        print(border)

        for index, product in enumerate(self.table):
            if product is None:
                if self.deleted[index]:
                    status = "(deleted)"
                else:
                    status = "(empty)"

                print(
                    f"| {index:<5} | {'-':<10} | {status:<24} | "
                    f"{'-':>10} | {'-':>8} |"
                )
            else:
                print(
                    f"| {index:<5} | {product.product_id:<10} | {product.name:<24} | "
                    f"{product.price:>10.2f} | {product.quantity:>8} |"
                )

        print(border)

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

def get_product_id(prompt):
    product_id = get_integer(prompt)

    while product_id <= 0:
        print("Product ID must be greater than 0.")
        product_id = get_integer(prompt)

    return product_id

def get_quantity(prompt):
    quantity = get_integer(prompt)

    while quantity < 0:
        print("Stock quantity cannot be negative.")
        quantity = get_integer(prompt)

    return quantity

def get_price(prompt):
    price = get_float(prompt)

    while price <= 0:
        print("Product price must be greater than zero.")
        price = get_float(prompt)

    return price

def print_menu():
    print("\n==== Pharmacy Inventory System ===")
    print("1. Insert Product")
    print("2. Search Product")
    print("3. Edit Product")
    print("4. Delete Product")
    print("5. Show Inventory")
    print("6. Exit")

def insert_product(inventory):
    product_id = get_product_id("Enter New Product ID: ")

    if inventory.search(product_id) is not False:
        print(f"Product ID {product_id} already exists.")
        return

    name = get_text("Enter Product Name: ")
    price = get_price("Enter Product Price: ")
    quantity = get_quantity("Enter Stock Quantity: ")
    medicine = Medicine(product_id, name, price, quantity)

    if inventory.insert(medicine):
        print("Medicine is added")
    else:
        print("Could not add product, the hash table is full.")

def search_product(inventory):
    product_id = get_product_id("Enter Product ID to Search: ")
    product = inventory.search(product_id)

    if product is not False:
        print("Product Found!")
        print(product)
    else:
        print("Medicine not found.")

    medicines = [
        product
        for product in inventory.table
        if product is not None
    ]

    compare_search(inventory, medicines, product_id)


def edit_product(inventory):
    product_id = get_product_id("Enter Product ID to Edit: ")
    product = inventory.search(product_id)

    if product is False:
        print("Medicine not found.")
        return

    print("Current medicine details:")
    print(product)

    name = get_text("Enter New Product Name: ")
    price = get_price("Enter New Product Price: ")
    quantity = get_quantity("Enter New Stock Quantity: ")

    if inventory.edit(product_id, name, price, quantity):
        print("Medicine is edited.")
    else:
        print("Medicine not found.")


def delete_product(inventory):
    product_id = get_product_id("Enter Product ID to Delete: ")

    if inventory.delete(product_id):
        print("Medicine deleted successfully.")
    else:
        print("Medicine not found.")

def array_search(medicines, product_id):
    for medicine in medicines:
        if medicine.product_id == product_id:
            return medicine

    return False

def compare_search(inventory, medicines, product_id):
    repetitions = 1000

    start = perf_counter_ns()

    for _ in range(repetitions):
        inventory.search(product_id)

    hash_time = perf_counter_ns() - start

    start = perf_counter_ns()

    for _ in range(repetitions):
        array_search(medicines, product_id)

    array_time = perf_counter_ns() - start

    print(f"\nSearching for product ID: {product_id}")
    print(f"Number of searches: {repetitions}")

    print(f"Hash table total: {hash_time:,} ns")
    print(f"Array total:      {array_time:,} ns")

    print(f"Hash table average: {hash_time / repetitions:.2f} ns/search")
    print(f"Array average:      {array_time / repetitions:.2f} ns/search")

def main():
    table_size = 11
    inventory = HashTable(table_size)

    medicines = [
        Medicine(101, "Paracetamol", 5.50, 50),
        Medicine(123, "Cough Syrup", 12.00, 20),
        Medicine(111, "Antibiotics", 9.00, 30),
        Medicine(150, "Vitamin A", 10.00, 45),
        Medicine(151, "Vitamin B", 9.50, 40)
    ]

    for medicine in medicines:
        inventory.insert(medicine)

    choice = 0

    while choice != 6:
        print_menu()
        choice = get_integer("Enter choice(1-6): ")

        while choice < 1 or choice > 6:
            print("Please choose a number from 1 to 6.")
            choice = get_integer("Enter choice (1-6): ")

        if choice == 1:
            insert_product(inventory)
        elif choice == 2:
            search_product(inventory)
        elif choice == 3:
            edit_product(inventory)
        elif choice == 4:
            delete_product(inventory)
        elif choice == 5:
            inventory.display()
        elif choice == 6:
            print("Exiting Inventory System. Goodbye!")

if __name__ == "__main__":
    main()