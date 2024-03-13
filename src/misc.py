import csv
from src.paths import *

def get_labels_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')  # Use ';' as the delimiter
        labels = next(reader)  # Assuming the labels are in the first row of the CSV
        return labels


def get_user_input_labels(labels):
    print("Available labels:")
    for idx, label in enumerate(labels, start=1):
        print(f"{idx}. {label}")

    user_input = input("Enter the numbers of labels you want (comma-separated)\
                       : ")
    selected_indices = [int(idx.strip()) for idx in user_input.split(",")]
    selected_labels = [labels[idx - 1] for idx in selected_indices]
    return selected_labels


def ask_for_number_of_epochs():
    n_epochs = input("How many epochs for training? ")
    return n_epochs


def get_labels(csv_file_path):
    labels = get_labels_from_csv(csv_file_path)

    print("Select input labels for the model:")
    input_labels = get_user_input_labels(labels)

    print("Select output labels for the model:")
    output_labels = get_user_input_labels(labels)

    return input_labels, output_labels


def get_lables_from_label_file():
    input_labels = get_labels_from_csv(input_labels_path)
    output_labels = get_labels_from_csv(output_labels_path)

    return input_labels, output_labels


def save_labels(input_labels, output_labels):
    with open("data/input_labels.csv", mode="w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(input_labels)

    with open("data/output_labels.csv", mode="w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(output_labels)
