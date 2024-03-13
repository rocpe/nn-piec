import sys
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error
from paths import *



## Load apropiate data
# load model
model = tf.keras.models.load_model(nn_path)

# load data
data_path = sys.argv[3]
data = pd.read_csv(data_path, sep=';') # for unnormalization
test_set = pd.read_csv(test_set_path, sep=';')
history = pd.read_csv(train_history_path, sep=';')

# get test input and output
input_labels = sys.argv[1].split(";")
output_labels = sys.argv[2].split(";")
test_input = test_set[input_labels].values
test_output = test_set[output_labels].values


## Predict data
predictions = model.predict(test_input)


## Draw plots
# draw train loss and mse ~ epoch
train_loss = history['loss']
mse = history['mse']
epochs = range(1, len(train_loss) + 1)
plt.figure(1)
plt.plot(epochs, train_loss, label='Training Loss')
plt.plot(epochs, mse, label='MSE')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.grid(True)
plt.legend()
plt.title('Training and MSE ~ Epoch')
plt.savefig('plots/loss_epoch.pdf', bbox_inches='tight')

# draw test output (real values) and predictions ~ number of prediction (rows)
plt.figure(2)
plt.plot(test_output, label=[s + ' real' for s in output_labels])
plt.plot(predictions, label=[s + ' predicted' for s in output_labels])
plt.xlabel('Number of Prediction')
plt.ylabel('Normalized value')
plt.grid(True)
plt.legend()
plt.title('Real and Predicted ~ Prediction')
plt.savefig('plots/re_pred_num.pdf', bbox_inches='tight')

plt.figure(3)

# draw real values against nn output
for col_idx in range(predictions.shape[1]):
    plt.scatter(test_output[:, col_idx], predictions[:, col_idx],\
                label=output_labels[col_idx])

x = np.linspace(min(test_output.min(), predictions.min()),\
                max(test_output.max(), predictions.max()), 100)
plt.plot(x, x, color='black', linestyle='--', label='y=x')

plt.xlabel('Normalized real values')
plt.ylabel('Normalized predicted value')
plt.title('Predicted ~ Real')
plt.grid(True)
plt.legend()
plt.savefig('plots/pred_real.pdf', bbox_inches='tight')

plt.show()


## Calculate R2, R2adj, RMSE
# preprocess data a bit
data[data == 'x'] = np.nan
data.dropna(how='any', inplace=True)
data = data[output_labels]
data = data.astype('float64')

# unnormalize data
test_output = test_output * (data.max() - data.min()).values + data.min().values
predictions = predictions * (data.max() - data.min()).values + data.min().values

#  calculate statistics for each column pair
statistics_data = []
for col_idx in range(predictions.shape[1]):
    actual_values = test_output[:, col_idx]
    predicted_values = predictions[:, col_idx]
    
    r2 = r2_score(actual_values, predicted_values)
    adj_r2 = 1 - (1 - r2) * (len(actual_values) - 1) / (len(actual_values)\
                                                     - predictions.shape[1] - 1)
    rmse = np.sqrt(mean_squared_error(actual_values, predicted_values))
    
    statistics_data.append([r2, adj_r2, rmse])

# create a pandas DataFrame to store the results
statistics_df = pd.DataFrame(statistics_data,\
                             columns=['R-squared', 'Adjusted R-squared',\
                                      'RMSE [units]'], index=output_labels)

# save the DataFrame to a CSV file
statistics_df.to_csv(stats_path, header=True)

# print the statistics 
print(statistics_df)
