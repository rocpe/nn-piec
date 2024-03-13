import sys
import os
from tensorflow import keras



# set labels
input_labels = sys.argv[1].split(";")
output_labels = sys.argv[2].split(";")
train_history_path = sys.argv[3]
nn_path = sys.argv[4]

# NORMALIZATION IS DONE EARILER IN PREPROCESS_DATA.PY
# create layer for noramlization ((x-mean)/std normalization). Range: [-1, 1]
#normalize = keras.layers.Normalization()
#train_set = pd.read_csv('data/train_set.csv', sep=';')
#train_input = train_set[input_labels].values
#normalize.adapt(train_input)

# create model 
n_input = len(input_labels)
n_output = len(output_labels)
# somehow it doesn't work with input_shape=(n_input,) when n_input = 1 that why
# this if statment here. Keep that in mind!
if n_input == 1:
    model = keras.Sequential([
        ### EDIT HERE: layers
        #normalize,
        keras.layers.Dense(n_input, input_shape=(1,), activation = 'relu'),
        keras.layers.Dense(10, activation = 'relu'),
        keras.layers.Dense(256, activation = 'relu'),
        keras.layers.Dense(10, activation = 'relu'),
        keras.layers.Dense(128),
        keras.layers.Dense(n_output)
        ])
else:
    model = keras.Sequential([
        ### EDIT HERE: layers
        #normalize,
        keras.layers.Dense(n_input, input_shape=(n_input,), activation = 'relu'),
        keras.layers.Dense(10, activation = 'relu'),
        keras.layers.Dense(256, activation = 'relu'),
        keras.layers.Dense(10, activation = 'relu'),
        keras.layers.Dense(128),
        keras.layers.Dense(n_output)
        ])

# set up model parameters
### EDIT HERE: optimizer, loss, metrics
model.compile(optimizer = 'adam', loss = 'mse', metrics = ['mse'])

# remove previous model history
if os.path.exists(train_history_path):
    os.remove(train_history_path)

# save model
model.save(nn_path)
#model.save(network/nn)
