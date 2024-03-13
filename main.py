import subprocess
import sys
from src.exit_codes import Err_kind
#from src.paths import check_dirs, preprocess_data_script
from src.paths import *
from src.misc import *



## First argument is a data file
if not len(sys.argv) > 1:
    print("No data file passed to the script.\n\
Usage: python main.py PATH_TO_DATA\n\
Aborting!")
    exit(Err_kind.NO_DATA_FILE_PASSED)
else:
    data_file = sys.argv[1]



## Check if needed direcotries exist
check_dirs()



## Functions which start other scripts
def preprocess_data():
    print("Preprocessing data")
    subprocess.run(['python', preprocess_data_script, data_file])


def create_model(input_labels, output_labels):
    print("Creating model with input labels:", ", ".join(input_labels))
    print("Output labels for the model:", ", ".join(output_labels))

    input_labels = ";".join(input_labels)
    output_labels = ";".join(output_labels)


    subprocess.run(['python', create_model_script, input_labels,\
                    output_labels, train_history_path, nn_path])


def train_model(input_labels, output_labels):
    print("Training model")
    n_epochs = ask_for_number_of_epochs()

    input_labels = ";".join(input_labels)
    output_labels = ";".join(output_labels)

    subprocess.run(['python', 'src/train_network.py', n_epochs, input_labels,\
                    output_labels])


def predict_train(input_labels, output_labels, data_file):
    print("Making predictions")

    input_labels = ";".join(input_labels)
    output_labels = ";".join(output_labels)

    subprocess.run(['python', predict_train_script, input_labels, output_labels,
                    data_file])



## Running main
if __name__ == "__main__":
    actions = ["preprocess_data", "create_model", "train_model",
               "predict_train", "all", "predict_new"]
    user_action = input(f"Choose an action from {', '.join(actions)}: ")

    input_labels = []
    output_labels = []

    if user_action not in actions:
        print("Invalid action. Please choose from the given options.")
        exit()

    if user_action == "create_model" or user_action == "all":
        input_labels, output_labels = get_labels(data_file)
        #input_labels, output_labels = get_labels(train_set_path)

    if input_labels or output_labels:
        save_labels(input_labels, output_labels)

    if user_action == "preprocess_data" or user_action == "all":
        preprocess_data()

    if user_action == "create_model" or user_action == "all":
        create_model(input_labels, output_labels)

    if user_action == "train_model" or user_action == "all":
        if user_action == "train_model":
            input_labels, output_labels = get_lables_from_label_file()

        train_model(input_labels, output_labels)

    if user_action == "predict_train" or user_action == "all":
        if user_action == "predict_train":
            input_labels, output_labels = get_lables_from_label_file()

        predict_train(input_labels, output_labels, data_file)
