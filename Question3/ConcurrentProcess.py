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

    return end - start, (result_35, result_38, result_40)

def fibonacci_worker(n, timings):
    start = time.perf_counter_ns()
    result = fibonacci(n)
    end = time.perf_counter_ns()

    timings[n] = (start, end, result)

def run_threaded_round():
    timings = {}
    threads = []

    for n in (35, 38, 40):
        thread = threading.Thread(target=fibonacci_worker, args=(n, timings))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    earliest_start = min(start for start, end, result in timings.values())
    latest_end = max(end for start, end, result in timings.values())

    results = []
    for n in (35, 38, 40):
        results.append(timings[n][2])

    return latest_end - earliest_start, results


def show_experiment(label, run_round, rounds):
    print(f"=== Fibonacci Computation ({label}) ===")
    total = 0

    for count in range(1, rounds + 1):
        elapsed, results = run_round()
        result_35, result_38, result_40 = results
        total += elapsed

        print(
            f"Round {count:2}: "
            f"Fib(35)={result_35}, Fib(38)={result_38}, Fib(40)={result_40} "
            f"| T = {elapsed:,} ns"
        )

    average = total / rounds
    print(f"Total T ({label}): {total:,} ns")
    print(f"Average T ({label}): {average:,.1f} ns\n")
    return average


def main():
    rounds = 10
    threaded = show_experiment("With Multithreading", run_threaded_round, rounds)
    sequential = show_experiment("Without Multithreading", run_sequential_round, rounds)

    if threaded == sequential:
        print("Observation: Both methods had the same average completion time.")
    else:
        change = (threaded - sequential) / sequential * 100

        if change > 0:
            direction = "increased"
        else:
            direction = "reduced"

        print(
            f"Observation: Multithreading {direction} the average "
            f"completion time by approximately {abs(change):,.1f}%."
        )

if __name__ == "__main__":
    main()