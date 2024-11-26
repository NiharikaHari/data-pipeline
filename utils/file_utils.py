import json
import config
import pandas as pd
import os


def load_merged_data():
    """
    Load merged data.

    Returns
    -------
    file
        Json file of merged data.
    """
    merged_data = json.load(open(config.MERGED_JSON_PATH))
    return merged_data


def load_cleaned_data():
    """
    Load cleaned data.

    Returns
    -------
    dict
        Dictionary of TSV files of cleaned data.
    """
    cleaned_data = {}
    cleaned_data['Cleaned_Demographic_Data'] = pd.read_csv(
        config.CLEANED_DEMOGRAPHICS_PATH, sep="\t").to_dict(orient='records')
    cleaned_data['Cleaned_Expenditure_Data'] = pd.read_csv(
        config.CLEANED_EXPENDITURE_PATH, sep="\t").to_dict(orient='records')
    return cleaned_data


def load_dataframe(filePath):
    """
    Load data file in the specified format.

    Parameters
    ----------
    filePath : str
        The path of the file to be loaded. Currently supported types are ('csv', 'json', 'tsv').

    Returns
    -------
    pandas.DataFrame
        The loaded data as a pandas DataFrame.

    Raises
    ------
    ValueError
        If the `fileType` is not one of the supported types ('csv', 'json', 'tsv').

    """

    fileType = os.path.splitext(filePath)[1]

    valid_filetypes = ('.csv', '.json', '.tsv')

    if fileType == '.csv':
        loaded_data = pd.read_csv(filePath, sep=',')
        return loaded_data
    elif fileType == '.tsv':
        loaded_data = pd.read_csv(filePath, sep='\t')
        return loaded_data
    elif fileType == '.json':
        loaded_data = json.load(open(filePath))
        loaded_data = pd.DataFrame(loaded_data['data'])
        return loaded_data
    else:
        raise ValueError(f'Invalid file type {fileType}. Allowed types are {
                         valid_filetypes}')


def write_file(input_df, output_file, output_type):
    """
    Write a given DataFrame to a file in the specified format.

    Parameters
    ----------
    input_df : pandas.DataFrame
        The DataFrame to be written to the file.
    output_file : str
        The path of the output file where the data will be saved.
    output_type : str
        The type of the output file. Currently supports only 'tsv'.

    Raises
    ------
    ValueError
        If the `output_type` is not a valid file type.

    """
    valid_filetypes = ('tsv')
    if output_type == 'tsv':
        input_df.to_csv(output_file, sep="\t", index=False)
    else:
        raise ValueError(f'Invalid file type {output_type}. Allowed types are{
                         valid_filetypes}')
