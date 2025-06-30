import random
import datetime

# Generate valid Malaysian IC number
def generate_realistic_ic():
    start_date = datetime.date(1950, 1, 1)
    end_date = datetime.date(2020, 12, 31)
    delta_days = random.randint(0, (end_date - start_date).days)
    dob = start_date + datetime.timedelta(days=delta_days)
    dob_str = dob.strftime("%y%m%d")
    state_code = f"{random.randint(1, 99):02d}"
    sequential = f"{random.randint(0, 999):03d}"
    gender = random.randint(0, 9)
    return dob_str + state_code + sequential + str(gender)

# Folding hash function
def folding_hash(ic_number, table_size):
    if len(ic_number) != 12 or not ic_number.isdigit():
        raise ValueError("IC number must be 12 digits.")
    parts = [int(ic_number[i:i + 3]) for i in range(0, 12, 3)]
    return sum(parts) % table_size

# Insert ICs and return table, collisions, and collision rate
def insert_to_hash_table(ic_list, table_size):
    table = [[] for _ in range(table_size)]
    collisions = 0
    for ic in ic_list:
        idx = folding_hash(ic, table_size)
        if table[idx]:
            collisions += 1
        table[idx].append(ic)
    rate = collisions / len(ic_list)
    return table, collisions, rate

# Display table like image
def display_table(table, max_lines=20):
    print(f"Hash Table with size {len(table)}:")
    for i in range(min(len(table), max_lines)):
        if table[i]:
            chain = " --> ".join(table[i])
            print(f"table[{i}] --> {chain}")
        else:
            print(f"table[{i}] --> [empty]")

# Run 10 rounds and compute averages
def run_multiple_rounds():
    rounds = 10
    sizes = [1009, 2003]
    all_results = {size: {'collisions': [], 'rates': []} for size in sizes}

    for round_num in range(1, rounds + 1):
        print(f"\n========== ROUND {round_num} ==========")
        ic_numbers = [generate_realistic_ic() for _ in range(1000)]

        for size in sizes:
            table, collisions, rate = insert_to_hash_table(ic_numbers, size)
            all_results[size]['collisions'].append(collisions)
            all_results[size]['rates'].append(rate)

            print(f"\nHash Table Size {size}:")
            print(f"Total Collisions: {collisions}")
            print(f"Collision Rate: {rate:.4f}")
            print(f"Load Factor: {len(ic_numbers) / size:.4f}")

            if round_num == 1:
                display_table(table)

    # Display average results
    print("\n========== AVERAGE SUMMARY (after 10 rounds) ==========")
    for size in sizes:
        avg_collisions = sum(all_results[size]['collisions']) / rounds
        avg_rate = sum(all_results[size]['rates']) / rounds
        print(f"\nHash Table Size {size}:")
        print(f"Average Collisions: {avg_collisions:.2f}")
        print(f"Average Collision Rate: {avg_rate:.4f}")

# Entry point
if __name__ == "__main__":
    run_multiple_rounds()
