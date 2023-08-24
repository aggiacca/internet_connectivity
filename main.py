import csv
import socket
import time
from datetime import datetime, date


def check_internet_connection():
    try:
        # Try to connect to a well-known website using a socket
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False


def log_message(message, filename):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{current_time}] {message}\n"
    print(log_entry)
    with open(filename, "a") as f:
        f.write(log_entry)


def write_stats_to_file(stats_file, start_time, outage_count, avg_outage_duration, max_outage_duration, last_updated):
    with open(stats_file, "w") as f:
        f.write(f"Program start time: {start_time}\n")
        f.write(f"Total outages: {outage_count}\n")
        f.write(f"Average outage: {avg_outage_duration:.2f} seconds\n")
        f.write(f"Highest outage: {max_outage_duration:.2f} seconds\n")
        f.write(f"Last updated: {last_updated}\n")


def write_to_csv(incidents_only_csv, outage_duration):
    with open(incidents_only_csv, "a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"{outage_duration:.2f}"])


def main():
    program_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_date = date.today()

    # Incident Variables
    outage_start_time = None
    raw_log_file = f"raw_log_{current_date.strftime('%Y-%m-%d')}.txt"
    incidents_only_csv = f"incidents_log_{current_date.strftime('%Y-%m-%d')}.csv"

    # Stat Variables
    outage_count = 0
    total_outage_duration = 0
    max_outage_duration = 0


    while True:
        if check_internet_connection():
            if outage_start_time is not None:
                # Incident Work
                outage_duration = time.time() - outage_start_time
                log_message(
                    f"Internet connection is back. Outage duration: {outage_duration:.2f} seconds",
                    filename=raw_log_file
                )
                outage_start_time = None
                outage_count += 1  # Increment the outage counter
                # Write incident to CSV for easier graphing
                write_to_csv(incidents_only_csv, outage_duration)

                # Stat Info Work
                total_outage_duration += outage_duration
                max_outage_duration = max(max_outage_duration, outage_duration)
                avg_outage_duration = total_outage_duration / outage_count if outage_count > 0 else 0

                stats_log_file = f"outage_statistics_{current_date.strftime('%Y-%m-%d')}.txt"
                write_stats_to_file(stats_log_file, program_start_time, outage_count, avg_outage_duration,
                                    max_outage_duration, last_updated=datetime.now())


                # Reset outage stats as it's a new day
                if current_date != date.today():
                    outage_count = 0
                    total_outage_duration = 0
                    max_outage_duration = 0
                    current_date = date.today()
            else:
                log_message("Internet connection is available.", filename=raw_log_file)
        else:
            if outage_start_time is None:
                outage_start_time = time.time()
                log_message("No internet connection.", filename=raw_log_file)

        time.sleep(10)  # Wait for 10 seconds before checking again


if __name__ == "__main__":
    main()
