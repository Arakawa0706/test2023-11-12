
from datetime import datetime, timedelta

def read_log(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().split(',') for line in file.readlines()]

def detect_server_failures(log_entries, timeout_threshold):
    failures = {}
    current_failure = None
    timeout_count = 0

    for timestamp_str, server_address, response_time in log_entries:
        timestamp = datetime.strptime(timestamp_str, '%Y%m%d%H%M%S')

        if response_time == '-':
            if current_failure is None:
                current_failure = {'start_time': timestamp, 'server_address': server_address}
            timeout_count += 1
        else:
            if current_failure is not None:
                current_failure['end_time'] = timestamp
                if timeout_count >= timeout_threshold:
                    failures[current_failure['server_address']] = current_failure
                current_failure = None
                timeout_count = 0

    return failures


def main():
    log_entries = read_log('logfile.txt')
    server_failures = detect_server_failures(log_entries,3)

    for address, failure in server_failures.items():
        print(f"Server {address} is down from {failure['start_time']} to {failure['end_time']}")

if __name__ == "__main__":
    main()
