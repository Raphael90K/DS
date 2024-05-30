import math

import ntplib
from time import time, sleep, ctime
import pandas as pd
from matplotlib import pyplot as plt


def get_ntp(server='pool.ntp.org'):
    client = ntplib.NTPClient()
    response = client.request(server, version=3)
    return response


def collect_time_data(servers, duration_seconds, interval_seconds):
    data = {server: [] for server in servers}
    start_time = time()

    while time() - start_time < duration_seconds:
        time_passed = int(math.floor(time() - start_time))
        for server in servers:
            try:
                response = get_ntp(server)
                time_difference = response.dest_time - response.tx_time

                data[server].append({
                    'Timestamp': ctime(response.orig_time),
                    'Time Passed': time_passed,
                    'PC Time': response.dest_time,
                    'Server Time': response.tx_time,
                    'Time Difference (s)': time_difference,
                    'Offset': response.offset,
                    'Delay (s)': response.delay
                })

                print(f"Collected data at {ctime(response.dest_time)} - Difference: {time_difference:.2f} seconds")

            except Exception as e:
                print(f"Error: {e}")

        sleep(interval_seconds)

    return data


def save_to_csv(data, base_filename='protocol'):
    for server, server_data in data.items():
        df = pd.DataFrame(server_data)
        filename = f"{base_filename}_{server.replace('.', '_')}.csv"
        df.to_csv(filename, index=False)


def plot_time_data(servers, minutes, base_filename='protocol'):
    plt.figure(figsize=(12, 6))

    for server in servers:
        filename = f"{base_filename}_{server.replace('.', '_')}.csv"
        df = pd.read_csv(filename)

        plt.plot(df['Time Passed'], df['Offset'], marker='o', linestyle='-', label=server)

    plt.xlabel('Time Passed (s)')
    plt.ylabel('Offset (s)')
    plt.title(f'Local time difference compared to NTP Server time over {minutes} minutes')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig('time_difference_plot.png')
    plt.show()


def get_stratum(servers):
    stratum = {}
    for server in servers:
        stratum[server] = get_ntp(server).stratum

    return stratum


def main():
    servers = ['pool.ntp.org', 'ptbtime1.ptb.de', 'time.windows.com', 'time-f-wwv.nist.gov']
    duration = 3600
    interval = 30
    stratum = get_stratum(servers)
    print(stratum)
    data = collect_time_data(servers, duration, interval)
    save_to_csv(data)
    plot_time_data(servers, str(duration / 60))


if __name__ == "__main__":
    main()
