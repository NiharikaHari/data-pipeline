import pandas as pd
import config

from utils.logger_utils import get_logger, log_error
from utils.file_utils import load_data, load_merged_data, write_file
from utils.dataframe_utils import get_common_columns, get_grouped_dict


def merge_data(expenditure_file, demographic_file):
    """
    Merge expenditure and demographic data

    Parameters
    ----------

    expenditure_file : str
        Path of expenditure data
    demographic_file : str
        Path of demographic data
    output_file : str
        Path of output merged data

    """

    logger = get_logger(__name__)
    logger.info(f'Merging files {expenditure_file} and {demographic_file}')

    try:

        # Load the datasets
        logger.info('Loading cleaned files to be merged')
        expenditure_df = load_data(expenditure_file)
        demographic_df = load_data(demographic_file)
        logger.info('Cleaned files loaded')

        # Get common columns between the datasets
        common_columns = get_common_columns(
            expenditure_df, demographic_df, ['Round_Centre_Code'])
        common_columns_df = expenditure_df[common_columns]
        common_columns_df = common_columns_df.drop_duplicates()

        # Remove common columns from both the datasets
        common_columns.remove('HHID')
        expenditure_df.drop(columns=common_columns, inplace=True)
        demographic_df.drop(columns=common_columns, inplace=True)

        # Group data into dictionary list, grouping by HHID
        expenditure_data = get_grouped_dict(df=expenditure_df, groupby='HHID',
                                            name='Expenditure_Data')
        demographic_data = get_grouped_dict(df=demographic_df, groupby='HHID',
                                            name='Demographic_Data')

        # Merge expenditure data and demographic data into the common dataset based on HHID key
        merged_df = pd.merge(common_columns_df, demographic_data,
                             on="HHID", how="inner")
        merged_df = pd.merge(merged_df, expenditure_data,
                             on="HHID", how="inner")

        # Flattern and export merged data
        merged_df.to_json(config.MERGED_JSON_PATH, orient='table', index=False)
        flat_merged_df = flatten_merged_json(load_merged_data())
        write_file(flat_merged_df, config.MERGED_TSV_PATH, 'tsv')

        # Export to tsv file

        logger.info(
            f'Merging completed. Merged data is stored at: {config.MERGED_DATA_DIR}')

    except Exception as error:
        log_error(logger, error)


def flatten_merged_json(data):
    """
    Flatten merged JSON data

    Parameters
    ----------

    data : json file
        Path of expenditure data
    """

    json_data = data['data']

    flattened_rows = []

    # Iterate through each household
    for household in json_data:
        household_level_data = {k: v for k, v in household.items(
        ) if k not in ["Demographic_Data", "Expenditure_Data"]}

        # Flatten Demographic_Data
        for person in household.get("Demographic_Data", []):
            row = {**household_level_data, **person}
            row['Data_Type'] = 'Demographic'  # Tag for identification
            flattened_rows.append(row)

        # Flatten Expenditure_Data
        for expenditure in household.get("Expenditure_Data", []):
            row = {**household_level_data, **expenditure}
            row['Data_Type'] = 'Expenditure'  # Tag for identification
            flattened_rows.append(row)

    df = pd.DataFrame(flattened_rows)

    return df
