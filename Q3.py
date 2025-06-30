import threading
import time
import random

def generate_random_numbers():
    numbers = []
    for _ in range(100):
        num = random.randint(0, 10000)
        for _ in range(1000):  # heavier workload
            temp = random.random() * num
            num = (num + int(temp)) % 10000
        numbers.append(num)
    return numbers

def multithreaded_run():
    results = [None] * 3
    threads = []

    start_time = time.time_ns()
    for i in range(3):
        def task(idx=i):
            results[idx] = generate_random_numbers()
        t = threading.Thread(target=task)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    end_time = time.time_ns()
    return end_time - start_time

def non_multithreaded_run():
    start_time = time.time_ns()
    results = []
    for _ in range(3):
        results.append(generate_random_numbers())
    end_time = time.time_ns()
    return end_time - start_time

def main():
    rounds = 10
    mt_times = []
    nm_times = []

    print("Round-by-Round Performance Comparison:\n")
    print("+--------+----------------------------+------------------------------+---------------------------+")
    print("| Round  | Multithreading Time (ns)  | Non-Multithreading Time (ns) | Difference (ns)           |")
    print("+--------+----------------------------+------------------------------+---------------------------+")

    for i in range(1, rounds + 1):
        mt = multithreaded_run()
        nm = non_multithreaded_run()
        diff = mt - nm

        mt_times.append(mt)
        nm_times.append(nm)

        print(f"| {i:<6} | {mt:<26} | {nm:<28} | {diff:<25} |")

    print("+--------+----------------------------+------------------------------+---------------------------+\n")

    total_mt = sum(mt_times)
    total_nm = sum(nm_times)
    total_diff = total_mt - total_nm
    avg_mt = total_mt / rounds
    avg_nm = total_nm / rounds
    avg_diff = avg_mt - avg_nm

    print("Summary of Results:\n")
    print("+----------------+----------------------------+------------------------------+---------------------------+")
    print("| Metric         | Multithreading (ns)        | Non-Multithreading (ns)      | Difference (ns)           |")
    print("+----------------+----------------------------+------------------------------+---------------------------+")
    print(f"| Total Time     | {total_mt:<26} | {total_nm:<28} | {total_diff:<25} |")
    print(f"| Average Time   | {avg_mt:<26.1f} | {avg_nm:<28.1f} | {avg_diff:<25.1f} |")
    print("+----------------+----------------------------+------------------------------+---------------------------+\n")

    print("Analysis:")
    if avg_diff > 0:
        print(f"Multithreading is SLOWER on average by {avg_diff:.1f} ns")
    else:
        print(f"Multithreading is FASTER on average by {-avg_diff:.1f} ns")

if __name__ == "__main__":
    main()
