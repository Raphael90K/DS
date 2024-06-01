import json
import os
import matplotlib.pyplot as plt

def process_json_file(json_file_path):
    # JSON-Datei einlesen
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Daten aus JSON extrahieren
    rounds = data['rounds']

    # Daten vorbereiten
    round_numbers = [round_data['round'] for round_data in rounds]
    connected_counts = [len(round_data['connected']) for round_data in rounds]
    participants_counts = [len(round_data['participants']) for round_data in rounds]
    late_throws_counts = [len(round_data['late_throws']) for round_data in rounds]

    # Dateiname ohne Erweiterung
    file_name = os.path.splitext(os.path.basename(json_file_path))[0]

    # Grafik erstellen
    plt.figure(figsize=(10, 6))

    # Runden als x-Achse
    x = round_numbers

    # Anzahl der 'connected', 'participants' und 'late_throws' als y-Achsen
    plt.plot(x, connected_counts, label='Connected', marker='o')
    plt.plot(x, participants_counts, label='Participants', marker='o')
    plt.plot(x, late_throws_counts, label='Late Throws', marker='o')

    # Titel und Labels hinzufügen
    plt.title(file_name)
    plt.xlabel('Round')
    plt.ylabel('Count')
    plt.legend()

    # Grafik speichern
    output_file_path = f'{file_name}.png'
    plt.savefig(output_file_path)
    plt.close()

def process_all_json_files(directory):
    # Alle Dateien im Verzeichnis durchgehen
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            json_file_path = os.path.join(directory, filename)
            process_json_file(json_file_path)

# Verzeichnis mit den JSON-Dateien
json_directory = 'C:\\Users\\rapha\\PycharmProjects\\DS\\A1\\E2a\\logs'

# Alle JSON-Dateien im Verzeichnis verarbeiten
process_all_json_files(json_directory)
