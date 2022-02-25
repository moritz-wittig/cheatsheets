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

def count_nan_values_in_series(df, column):
    """ counts all the nan values within a pandas series """
    
    return len(df[np.isnan(df[column].values.tolist())])
    

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

def extract_numerical_values_from_pd_timedelta(df, column):
    """Pandas Timedelta extract numerical hour values"""
    
    return df[column].dt.total_seconds()/60/60

def get_index_of_max(df, column):
    """ get index of max value """
    
    return df[column].idxmax()

def count_freq_of_value_occurence(df, column):
    """ Count the Frequency a Value Occurs in Pandas Dataframe """
    
    return df[column].value_counts() 

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

def create_new_id_column_with_range(df, to_id_column):
    """ 
    Create ID with range 
    Background: For plotting ids on the axis 
    """ 
    df[to_id_column+"_id"] = pd.Series("#" + str(i) for i in range(len(df)))
    # In case this returns nan values:
    # df[to_id_column] = pd.Series("#" + str(i) for i in range(len(df))).values

    return df


def convert_string_series_to_unique_int_ids(df, column):
    """Convert pandas series from string to unique int ids"""
    df[column] = df[column].astype('category').cat.codes
    return df

def assign_value_depending_on_other_df(df, df1, condition, value):
    """ 
    Assign value depending on another dataframe.
    condition must be a "shared" column between these two dfs
    """

    df[value] = df[condition].map(df1.set_index(condition)[value])
    # Series
    # df[value] = df[condition].map(df1)

    return df


def set_value_of_one_column_based_on_value_in_other_column(df, cond, origin_column, target_column):
    """ 
    Set value of one column based on value in another column 
    example:
        - cond: df_copy['bat_cap'] < df_copy['energy']
        - origin_column: "energy"
        - target column: "bat_cap"
    """
    df_copy = df.copy()
    df_copy.loc[cond, target_column] = df_copy[origin_column]

    return df_copy

def set_new_values_in_column_based_on_multiple_condition(df):
    """
    Set new values in a column, based on multiple conditions/columns.
    JUST EXEMPLARY HERE TO GET THE IDEA!
    """
    def func(x):
        if pd.isna(x["outside_quartile_max"]):
            bat_cap = x["upper_quartile"] * 1.3
            
        if not pd.isna(x["outside_quartile_max"]):
            bat_cap = x["outside_quartile_max"] * 1.2
            
        if not pd.isna(x["upper_outlier"]):
            bat_cap = x["upper_outlier"] * 1.1

        return bat_cap

    df['battery_capacity'] = df.apply(func, axis = 1)
    
    return df

def timezone_localize(df, column):
    """ Localize tz-naive index of a Series or DataFrame to target time zone """
    
    df_copy = df.copy()
    # Transform series to datetime type
    # Needs to be specified according to the input str
    
    df_copy[column] = pd.to_datetime(df_copy[column], format='%a, %d %b %Y %H:%M:%S GMT')

    # In case there is e.g. a NonExistentTimeError, which is most likely to be due to DST switch (Daylight Saving Time/Sommerzeit), one
    # option is to exclude these values

    mask_1 =  ((df_copy[column]>datetime.strptime("2019-03-31 02:00:00","%Y-%m-%d %H:%S:%M")) & (df_copy[column]<datetime.strptime("2019-03-31 03:00:00","%Y-%m-%d %H:%S:%M")))

    print(str(len(df_copy.loc[mask_1])) + " rows of the "  + column + " column is being deleted from the dataset, due to errors with DST")
    df_copy = df_copy.loc[~mask_1]

    # ambiguous="NaT" argument will return NaT where there are ambiguous times
    df_copy[column] = df_copy[column].dt.tz_localize(tz = tz, ambiguous="NaT")

    return df_copy
    
