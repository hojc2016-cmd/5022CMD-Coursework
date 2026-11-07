"""Compare the search methods from hashing.py using separate test inventories."""
import time
import hashing

ROUNDS = 6
REPETITIONS = 1000


def measure_hash_search(inventory, product_id):
    start = time.perf_counter_ns()
    for repeat in range(REPETITIONS):
        inventory.search(product_id)
    return time.perf_counter_ns() - start


def measure_array_search(medicines, product_id):
    start = time.perf_counter_ns()
    for repeat in range(REPETITIONS):
        hashing.array_search(medicines, product_id)
    return time.perf_counter_ns() - start


def compare_search(inventory, medicines, product_id, description):
    for repeat in range(100):
        hash_result = inventory.search(product_id)
        array_result = hashing.array_search(medicines, product_id)
        if hash_result is not array_result:
            raise ValueError('The searches returned different results.')

    hash_total = 0
    array_total = 0

    for round_number in range(ROUNDS):
        if round_number % 2 == 0:
            hash_total += measure_hash_search(inventory, product_id)
            array_total += measure_array_search(medicines, product_id)
        else:
            array_total += measure_array_search(medicines, product_id)
            hash_total += measure_hash_search(inventory, product_id)

    total_searches = ROUNDS * REPETITIONS
    hash_average = hash_total / total_searches
    array_average = array_total / total_searches

    print(f'{description:<18} {hash_average:>18,.1f} {array_average:>18,.1f}')


def run_simulation(number_of_products, create_collisions=False):
    table_size = number_of_products * 2 + 1
    inventory = hashing.HashTable(table_size)
    medicines = []

    for number in range(1, number_of_products + 1):
        if create_collisions:
            product_id = number * table_size
        else:
            product_id = number

        name = f'Test Medicine {number}'
        product = hashing.Medicine(product_id, name, 5.50, 10)
        medicines.append(product)
        if not inventory.insert(product):
            raise ValueError('A test medicine could not be inserted.')

    print('\nProducts:', number_of_products)
    print('Table size:', table_size)
    print(f'Occupied: {number_of_products / table_size * 100:.1f}%')
    if create_collisions:
        print('Case: all IDs start at index 0 (deliberate collision stress test).')
        missing_id = (number_of_products + 1) * table_size
    else:
        print('Case: every ID has a different starting index (favourable case).')
        missing_id = table_size

    print(f'{"Search target":<18} {"Hash ns/search":>18} {"Array ns/search":>18}')
    print('-' * 56)

    first_id = medicines[0].product_id
    middle_id = medicines[number_of_products // 2].product_id
    last_id = medicines[-1].product_id

    compare_search(inventory, medicines, first_id, 'First in array')
    compare_search(inventory, medicines, middle_id, 'Middle in array')
    compare_search(inventory, medicines, last_id, 'Last in array')
    compare_search(inventory, medicines, missing_id, 'Missing ID')


def main():
    print('MEDICINE SEARCH SIMULATION')
    print(f'Each target: {ROUNDS} rounds of {REPETITIONS} searches per method.')
    print('Results show arithmetic average nanoseconds per search; lower is faster.')
    print('Array order is insertion order. Both structures contain the same records.')
    print('Only searches and loop/call overhead are timed, not setup or printing.')
    print('Times vary between runs. Repeated targets do not model every workload.')

    for number_of_products in [10, 100, 1000, 5000]:
        run_simulation(number_of_products)

    run_simulation(1000, create_collisions=True)


if __name__ == '__main__':
    main()
