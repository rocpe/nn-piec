# Program to create, manage and work with regression neural network. 

## Prerequisitions
Look at requirements.txt


## Usage
In terminal type
"python run.py PATH_TO_DATA_CSV"
there will be 5 options:
1. preprocess_data
2. create_model
3. train_model
4. predict_train
5. all
6. predict_new (not implemented yet)

If you are starting this program for the first time is good to run "all"
option. WARNING! "create_model" and "preprocess_data" tweak some files for
neural network so you shouldn't run them alone ie. run "preprocess_data" and
then "predict". It will work but it won't give any meaningful results (Now I
won't explain why).

## Quick-start
1. python run.py PATH_TO_DATA_CSV
2. choose "all" option and proceed
3. plots are saved in plots folder
4. statistics are saved in data folder
5. if you want to change network go to file src/create_model.py and change
source code of the model (look for ### EDIT HERE:) and run script again with
"all" option.
