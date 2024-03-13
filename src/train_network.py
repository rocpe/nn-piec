import sys
import tensorflow as tf
import pandas as pd
from paths import *



# load model
#model = tf.keras.models.load_model('network/nn')
model = tf.keras.models.load_model(nn_path)

# load data
#train_set = pd.read_csv('data/train_set.csv', sep=';')
train_set = pd.read_csv(train_set_path, sep=';')

# get columns you want
input_labels = sys.argv[2].split(";")
output_labels = sys.argv[3].split(";")
train_input = train_set[input_labels].values
train_output = train_set[output_labels].values
 
# train model and save history
n_epochs = int(sys.argv[1])
#csv_logger = tf.keras.callbacks.CSVLogger('data/train_history.csv',
                                          #separator=";", append=True)
csv_logger = tf.keras.callbacks.CSVLogger(train_history_path,\
                                          separator=";", append=True)
model.fit(train_input, train_output, epochs = n_epochs, callbacks=[csv_logger])

# save model
#model.save('network/nn')
model.save(nn_path)
