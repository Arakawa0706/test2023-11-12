

from datetime import datetime, timedelta

def read_log(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().split(',') for line in file.readlines()]

def detect_server_failures(log_entries, timeout_threshold, average_threshold, window_size):
    failures = {}
    current_failure = None
    timeout_count = 0
    response_times = []

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

            response_times.append(int(response_time))
            if len(response_times) > window_size:
                response_times.pop(0)

            if len(response_times) == window_size and sum(response_times) / window_size > average_threshold:
                if current_failure is None:
                    current_failure = {'start_time': timestamp, 'server_address': server_address}
            else:
                current_failure = None

    return failures


def main():
    log_entries = read_log('logfile.txt')
    server_failures = detect_server_failures(log_entries, 3, 5, 10)

    for address, failure in server_failures.items():
        print(f"Server {address} is down from {failure['start_time']} to {failure['end_time']}")

if __name__ == "__main__":
    main()
