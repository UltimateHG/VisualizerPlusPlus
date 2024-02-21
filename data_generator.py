import numpy as np

# generate phone numbers 

def generate_phone_numbers(n_samples):
    phone_numbers = []
    for i in range(n_samples):
        phone_number = "0" + str(np.random.randint(100000000, 999999999))
        phone_numbers.append(phone_number)
    return phone_numbers

# generate phone logs for every phone number

def generate_phone_logs(phone_numbers, n_logs):
    phone_logs = []
    # (caller, callee, duration)
    for phone_number in phone_numbers:
        for i in range(n_logs):
            caller = phone_number
            callee = phone_numbers[np.random.randint(0, len(phone_numbers))]
            duration = np.random.randint(0, 3600)
            phone_logs.append((caller, callee, duration))
    return phone_logs

# generate phone logs file for each user

def generate_phone_logs_file(phone_logs, phone_numbers):
    for phone_number in phone_numbers:
        with open(f"dumps/{phone_number}.csv", "w") as f:
            f.write("phone,status,duration\n")
            for phone_log in phone_logs:
                caller, callee, duration = phone_log
                if caller == phone_number:
                    f.write(f"{callee},{'incoming'},{duration}\n")
                if callee == phone_number:
                    f.write(f"{caller},{'outgoing'},{duration}\n")


if __name__ == "__main__":
    n_samples = 10
    n_logs = 70
    phone_numbers = generate_phone_numbers(n_samples)
    phone_logs = generate_phone_logs(phone_numbers, n_logs)
    generate_phone_logs_file(phone_logs, phone_numbers)