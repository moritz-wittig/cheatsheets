import pandas as pd
import numpy as np

def drop_all_nan_rows(df):
    """ drops all rows with nan values """
    df_copy =  df.dropna()

    return df_copy

def drop_specific_nan_rows(df, column):
    """ drops all row with Nan Values in a specified column"""
    df_copy =  df.dropna(subset=[column])

    return df_copy

def extract_float_from_str(df, column):
    """ Extract only float values from str column """
    df_copy = df.copy()
    df_copy[column] = df_copy[column].str.extract('(\d+\.\d+)', expand=False)
    df_copy = df_copy.dropna(subset=[column])
    df_copy[column] = df_copy[column].astype(float)

    return df_copy[column]

def extract_int_from_str(df, column):
    """ Extract only int values from str column """
    df_copy = df.copy()
    df_copy[column] = df_copy[column].str.extract('(\d+)', expand=False)
    df_copy = df_copy.dropna(subset=[column])
    df_copy[column] = df_copy[column].astype(int)
    
    return df_copy[column]

def change_single_column_name(df, origin_column_name, new_column_name):
    """ Change single column name """
    df.rename(columns={origin_column_name: new_column_name}, inplace=True)

    return df

def random_dates(start, end, n=10):
    """ 
    create df with random datetimes for testing purposes
    exemples for input variables:
        start = pd.to_datetime('2015-01-01')
        end = pd.to_datetime('2018-01-01')
    """
    start_u = start.value//10**9
    end_u = end.value//10**9

    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s').to_frame(index=False, name='random_dates')

def floor_timestamp(df, column, freq="T"):
    """ 
    Round to closest Timestamp 
    package: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.floor.html
    examples for freq:
        - freq="T": Flooring to min (12:58:34 --> 12:58:00)
        - freq="15T": Flooring to min (12:58:34 --> 12:45:00)
        - freq="H": Rounding to hour (12:58:34 --> 12:00:00)
    """
    df[column+"_floored"] = df[column].dt.floor(freq=freq)

    return df

def get_index_of_max(df, column):
    """ get index of max value """
    
    return df[column].idxmax()

def filter_with_multiple_conditions(df, cond1, cond2):
    """ 
    Filter with multiple conditions 
    example for cond: df[‘Salary']>=100000
    """
    return df[(cond1) & (cond2)]

def select_rows_based_on_list(df, column, list):
    """ Select/Filter Dataframe Rows based on List of Values """

    filtered_df = df[df[column].isin(list)]
    # Inverse:
    # filtered_df = df[~df[column].isin(list)]

    return filtered_df

def update_row_values_based_on_condition(df, cond, connecting_column, desired_value):
    """ 
    Update row values where certain condition (might be another df) is met. Connecting_column must be shared by both dfs.
    example for cond: df1['stream'] == 2
    example for connecting_column: 'feat'
    """
    df_copy = df.loc[cond, connecting_column] = desired_value

    return df_copy

