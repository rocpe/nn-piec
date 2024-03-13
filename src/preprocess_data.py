import sys
import pandas as pd
import numpy as np
from scipy.stats import median_abs_deviation
from exit_codes import Err_kind
from paths import train_set_path, test_set_path



# first argument is data file
data_file = sys.argv[1]



# useful functions defs
def is_float(a):
    try:
        float(a)
        return True
    except ValueError:
        return False


def read_file(file_path):
    try:
        # Try reading as CSV with comma as decimal separator
        df = pd.read_csv(file_path, sep=';', decimal=',')
        return df, 'csv'
    except Exception:
        try:
            # Try reading as CSV with period as decimal separator
            df = pd.read_csv(file_path, sep=',', decimal='.')
            return df, 'csv'
        except Exception:
            try:
                # Try reading as Excel
                df = pd.read_excel(file_path)
                return df, 'xlsx'
            except Exception as e:
                # Unable to read as either CSV or Excel
                print(e)
                return None, 'unknown'


def norm(data):
    # normalization (range [0,1])
    data = (data - data.min()) / (data.max() - data.min())
    return data


def unnorm(norm_data, real_data):
    # from [0,1] to real values
    return real_data * (norm_data.max() - norm_data.min()).values +\
norm_data.min().values


# removing outliers based of mean and std
def remove_outlier_rows_mstd(df, threshold):
    # Calculate the mean and std for each column
    column_means = df.mean()
    column_stds = df.std
    
    # Calculate the lower and upper bounds for each column
    lower_bounds = column_means - threshold * column_stds
    upper_bounds = column_means + threshold * column_stds
    
    # Identify outlier rows for each column
    outlier_rows = ((df < lower_bounds) | (df > upper_bounds)).any(axis=1)
    
    # Remove rows containing at least one outlier
    filtered_df = df[~outlier_rows]
    
    return filtered_df


# removing outliers based of median and mad
def remove_outlier_rows_mmad(df, threshold):
    # Calculate the median and quartile deviation for each column
    column_medians = df.median()
    column_qd = df.apply(median_abs_deviation)
    
    # Calculate the lower and upper bounds for each column
    lower_bounds = column_medians - threshold * column_qd
    upper_bounds = column_medians + threshold * column_qd
    
    # Identify outlier rows for each column
    outlier_rows = ((df < lower_bounds) | (df > upper_bounds)).any(axis=1)
    
    # Remove rows containing at least one outlier
    filtered_df = df[~outlier_rows]
    
    return filtered_df


# removing outliers  but cutting prec% from the smallest values and from the larges
#TODO: implementation
def remove_outlier_rows_prec(df, prec):
    return filtered_df


# load data
data, file_type = read_file(data_file)
if data is not None:
    print(f"The file '{data}' is successfully read as {file_type}.")
else:
    print(f"Error: Unable to read the file '{data}' as either CSV or Excel.")
    exit(Err_kind.READ_DATA_FAILED)

# remove NaN and x values
data[data == 'x'] = np.nan
data.dropna(how='any', inplace=True)

# make sure that type of each column is float64
data = data.astype('float64')

# remove outliers
user_input = input("How do you want to delete outliers? (choose number)\n\
1. mean-threshold*std method\n\
2. median-threshold*mad method\n\
3. There is no outliers. Just continue.\n")

options = ["1", "2", "3"]  

if user_input not in options:
    print("Unknown option!\nAborting!")
    exit(Err_kind.UNKNOWN_OPTION)
elif user_input == options[0]:
    th = input("Enter threshold: ")
    if is_float(th):
        data = remove_outlier_rows_mstd(data, float(th))
    else:
        print("Threshold is not a number!\nAborting!")
        exit(Err_kind.TH_IS_NOT_NUMBER)
elif user_input == options[1]:
    th = input("Enter threshold: ")
    if is_float(th):
        data = remove_outlier_rows_mmad(data, float(th))
    else:
        print("Threshold is not a number!\nAborting!")
        exit(Err_kind.TH_IS_NOT_NUMBER)

# norm data
data = norm(data)

# devide data into training set and test set and save them
train_set = data.sample(frac=0.8, random_state=0)
test_set = data.drop(train_set.index)

train_set.to_csv(train_set_path, sep=';', index=False, header=True)
test_set.to_csv(test_set_path, sep=';', index=False, header=True)

print("Preprocessing done!")
