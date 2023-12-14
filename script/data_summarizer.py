import utils.util as util
import pandas as pd

def summarize_data(df):
    
    if not util.is_dataframe(df):
        print("Input is not a DataFrame.")
        return None
    numeric_stats = df.describe().transpose()
    missing_values = df.isnull().sum()
    summary_df = pd.DataFrame(index=df.columns)
    summary_df['Shape'] = df.shape
    summary_df['Data Type'] = df.dtypes
    summary_df['Missing Values'] = missing_values
    summary_df['Unique Values'] = df.nunique()
    summary_df = summary_df.join(numeric_stats[['mean', 'std', 'min', '25%', '50%', '75%', 'max']])
    return summary_df


def categorical_summary(df,dtype='object'):
    if not isinstance(df, pd.DataFrame):
        print("Input is not a DataFrame.")
        return None

    categorical_columns = df.select_dtypes(include=[dtype]).columns 

    if len(categorical_columns) == 0:
        print("No categorical columns found in the DataFrame.")
        return None


    summary_df = summarize_data(df)


    categorical_summary_df = pd.DataFrame(index=categorical_columns, columns=['Unique Values', 'Value Counts'])

    for column in categorical_columns:
        value_counts = df[column].value_counts()
        categorical_summary_df.at[column, 'Unique Values'] = len(value_counts)
        categorical_summary_df.at[column, 'Value Counts'] = value_counts

    return categorical_summary_df


def group_and_aggregate(df, group_column, agg_columns):
    #(df, GroupColumn', {'Column': 'mean', 'AnotherColumn': 'sum'})
    if not isinstance(df, pd.DataFrame):
        print("Input is not a DataFrame.")
        return None
    grouped_df = df.groupby(group_column).agg(agg_columns)
    return grouped_df

def value_counts_summary(df, column_name):
    if not isinstance(df, pd.DataFrame):
        print("Input is not a DataFrame.")
        return None
    value_counts = df[column_name].value_counts()
    return value_counts


def calculate_correlation(df):
    if not isinstance(df, pd.DataFrame):
        print("Input is not a DataFrame.")
        return None
    correlation_matrix = df.corr()
    return correlation_matrix

def create_crosstab(df, column1, column2):
    if not isinstance(df, pd.DataFrame):
        print("Input is not a DataFrame.")
        return None
    crosstab_table = pd.crosstab(df[column1], df[column2])
    return crosstab_table

def create_pivot_table(df, numeric_column, index_column, columns_column, aggfunc='mean'):
    if not isinstance(df, pd.DataFrame):
        print("Input is not a DataFrame.")
        return None
        
    pivot_table = pd.pivot_table(df, values=numeric_column,
                                 index=index_column, columns=columns_column,
                                 aggfunc=aggfunc)
    return pivot_table

def find_min_max_in(df, col):
    if not isinstance(df, pd.DataFrame):
        print("Input is not a DataFrame.")
        return None
    top = df[col].idxmax()
    top_df = pd.DataFrame(df.loc[top])
    bottom = df[col].idxmin()
    bottom_df = pd.DataFrame(df.loc[bottom])
    info_df = pd.concat([top_df, bottom_df], axis=1)
    return info_df
find_min_max_in(movies_df, 'budget')