import json
import os
import matplotlib.pyplot as plt


def process_json_file(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    rounds = data['rounds']

    round_numbers = [round_data['round'] for round_data in rounds]
    connected_counts = [len(round_data['connected']) for round_data in rounds]
    participants_counts = [len(round_data['participants']) for round_data in rounds]
    late_throws_counts = [len(round_data['late_throws']) for round_data in rounds]

    file_name = os.path.splitext(os.path.basename(json_file_path))[0]

    plt.figure(figsize=(10, 6))

    x = round_numbers

    plt.plot(x, connected_counts, label='Verbundene Clients', marker='o')
    plt.plot(x, participants_counts, label='Mitspieler', marker='o')
    plt.plot(x, late_throws_counts, label='Verspätete Würfe', marker='o')

    plt.title(file_name)
    plt.xlabel('Runde')
    plt.ylabel('Anzahl')
    plt.legend(loc='center right')

    output_file_path = f'{file_name}.png'
    plt.savefig(output_file_path)
    plt.close()


def process_all_json_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            json_file_path = os.path.join(directory, filename)
            process_json_file(json_file_path)


json_directory = 'C:\\Users\\rapha\\PycharmProjects\\DS\\A1\\E2a\\logs'

process_all_json_files(json_directory)
