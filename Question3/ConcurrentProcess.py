import threading
import time

def fibonacci(n):
    current = 0
    next = 1

    for _ in range(n):
        current, next = next, current + next

    return current

def run_sequential_round():
    start = time.perf_counter_ns()

    result_35 = fibonacci(35)
    result_38 = fibonacci(38)
    result_40 = fibonacci(40)

    end = time.perf_counter_ns()

    print(f"F(35) = {result_35}")
    print(f"F(38) = {result_38}")
    print(f"F(40) = {result_40}")
    return end - start


if __name__ == "__main__":
    rounds = 10
    total_time = 0

    for count in range(1, rounds + 1):
        elapsed = run_sequential_round()
        total_time += elapsed
        print(f"Round {count}: {elapsed:,} ns\n")

    average_time = total_time / rounds
    print(f"Total for {rounds} rounds: {total_time:,} ns")
    print(f"Average per round: {average_time:,.1f} ns")