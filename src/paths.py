import os
#Not needed since it is invoked by sript which already imports it
#from src.exit_codes import Err_kind 

## Paths to the important files
train_set_path = "data/train_set.csv"
test_set_path = "data/test_set.csv"
input_labels_path = "data/input_labels.csv"
output_labels_path = "data/output_labels.csv"
train_history_path = "data/train_history.csv"

#nn_path = "network/nn"
nn_path = "network/nn.keras"

preprocess_data_script = "src/preprocess_data.py"
create_model_script = "src/create_model.py"
train_model_script = "src/train_model.py"
predict_train_script = "src/predict_train.py"
predict_new_script = "src/predict_new.py"

stats_path = "data/stats.csv"

def check_dirs():
    if not os.path.exists('data/'):
        print("Directory 'data' doesn't exist. Create it. Aborting!")
        exit(Err_kind.NO_DATA_DIR)

    if not os.path.exists('network/'):
        print("Directory 'network' doesn't exist. Create it. Aborting!")
        exit(Err_kind.NO_NETWORK_DIR)

    if not os.path.exists('src/'):
        print("Directory 'src' doesn't exist. This directory has all the code\
        for runnung the program. Without it nothing will work :(. Aborting!")
        exit(Err_kind.NO_SRC_DIR)
