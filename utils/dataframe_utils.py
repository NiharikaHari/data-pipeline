import pandas as pd


def flatten_data(data, path, meta):
    """
    Flatten JSON data to dataframe at specified data path.
    """
    df = pd.json_normalize(data['data'], record_path=path, meta=meta)
    return df


def drop_unknown(df):
    """
    Drop all rows with 'Unknown' value from dataframe.
    """
    def check_for_unknown(row):
        if 'Unknown' in row.values:
            df.drop(index=row.name, inplace=True)
    df.apply(check_for_unknown, axis=1)
    return df


def drop_indexes(df, indexes):
    """
    Drop specified indexes from dataframe.
    """
    for ind in df.index:
        for str in indexes:
            if str in ind:
                df = df.drop(ind)
    return df


def strip_strings(df):
    """
    Strip all strings in dataframe.
    """
    df = df.replace(' ', None)
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: x.strip() if isinstance(x, str) else x)
    return df


def drop_empty_columns(df):
    """
    Drop columns with no data.
    """
    df.dropna(axis=1, how='all', inplace=True)


def drop_na_from_columns(df, cols, how):
    """
    Drop rows with no data in specified columns
    """
    check = all(e in df.columns for e in cols)
    if check:
        df.dropna(subset=cols, how=how, inplace=True)


def fill_na_with_unknown(df, cols):
    """
    Fill NA with 'Unknown' in dataframe 'df' for columns 'cols'
    """
    for col in cols:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown')


def format_numeric_columns(df, numeric_columns=None, decimal_places=2):
    """
    Format decimal places for all numeric columns.
    """
    if numeric_columns == None:
        numeric_columns = df.select_dtypes('number')
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col], errors='coerce').round(decimal_places)
    return df


def capitalize_strings(df, cols):
    """
    Capitalize values in all specified columns
    """
    for col in cols:
        if col in df.columns:
            df[col].apply(str.capitalize)
    return df


def replace_not_known_with_unknown(df, cols):
    """
    Replace 'Not Known' with 'Unknown' in specified columns
    """
    for col in cols:
        if col in df.columns:
            df[col] = df[col].replace('Not   known', 'Unknown')


def fill_na_with_imputation(df, cols, method):
    """
    Fill NA values with specified imputation method for specified columns
    """
    for col in cols:
        if col in df.columns:
            if method == 'median':
                df[col] = df[col].fillna(df['Age'].median().round(0))


def compute_monthly_yearly_expenditure(df):
    """
    Compute empty monthly and yearly expenditure values from one another
    """
    if 'Value_of_Consumption_Last_30_Day' in df.columns and 'Value_Consumption_Last_365_Days' in df.columns:

        df['Value_Consumption_Last_365_Days'] = df['Value_Consumption_Last_365_Days'].astype(float).fillna(
            df['Value_of_Consumption_Last_30_Day'] * 12)
        df['Value_of_Consumption_Last_30_Day'] = df['Value_of_Consumption_Last_30_Day'].astype(float).fillna(
            (df['Value_Consumption_Last_365_Days'] / 12)).round(0)


def get_common_columns(df1, df2, ignore_columns=None):
    """
    Returns list of common columns between 2 dataframes, while ignoring specified columns.
    """
    common_columns = []
    for col in df1.columns:
        if col not in df2.columns:
            continue
        elif col not in ignore_columns:
            common_columns.append(col)
    return common_columns


def get_grouped_dict(df, groupby, name):
    """
    Converts dataframe records to dictionary, grouped by a field.
    """
    grouped_dict = df.groupby(groupby).apply(
        lambda x: x.to_dict(orient='records'), include_groups=False
    ).reset_index(name=name)
    return grouped_dict


def count_if_adult(series):
    """
    Returns the count of values in the series where value >18
    """
    return series[series >= 18].count()
