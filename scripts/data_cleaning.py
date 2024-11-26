import pandas as pd
from utils.logger_utils import get_logger, log_error
from utils.file_utils import load_dataframe, write_file
from utils.dataframe_utils import *


def clean_data(input_file, output_file, critical_columns=None, category_columns=None, numeric_columns=None):
    """
    Cleans data file and exports it.

    Parameters
    ----------
    input_file : string
        The path of the file to be cleaned.
    output_file : string
        The path to store the cleaned data file.
    critical_columns : list (default=None)
        List of columns whose values called be null.
    category_columns : list (default=None)
        List of columns that have categorical values.
    numeric_columns : list (default=None)
        List of columns that have numerical values.

    """

    logger = get_logger(__name__)
    logger.info(f'Cleaning file {input_file}')

    # Set default values of parameters
    critical_columns = critical_columns or ['HHID']
    category_columns = category_columns or ['Status_of_Current_Attendance', 'Type_of_Educationa_Institution',
                                            'Registered_with_Emp_Exchange', 'Vocational_Training', 'Field_of_Training',
                                            'MGNREG_jobcard', 'MGNREG_work', 'General_Education']
    numeric_columns = numeric_columns or ['Age', 'Value_of_Consumption_Last_30_Day',
                                          'Value_of_Consumption_Last_30_Day']

    try:
        # load data
        logger.info(f'Loading input file: {input_file}')
        input_df = load_dataframe(input_file)
        logger.info(f'File loading completed: {input_file}')

        # Methods for general cleaning
        input_df = strip_strings(input_df)
        drop_empty_columns(input_df)
        drop_na_from_columns(input_df, critical_columns, how='any')
        fill_na_with_unknown(input_df, category_columns)
        input_df.drop_duplicates(inplace=True)
        format_numeric_columns(input_df)
        input_df = capitalize_strings(input_df, category_columns)

        # Methods specific to demographic and expenditure datasets
        format_numeric_columns(
            input_df, numeric_columns=numeric_columns, decimal_places=0)

        replace_not_known_with_unknown(
            input_df, ['Type_of_Educationa_Institution'])
        fill_na_with_imputation(input_df, ['Age'], 'median')
        drop_na_from_columns(input_df, [
                             'Value_of_Consumption_Last_30_Day', 'Value_of_Consumption_Last_30_Day'], how='all')
        compute_monthly_yearly_expenditure(input_df)

        # export data
        write_file(input_df, output_file, 'tsv')
        logger.info(
            f'File cleaned and output stored in {output_file}')

    except Exception as error:
        log_error(logger, error)
