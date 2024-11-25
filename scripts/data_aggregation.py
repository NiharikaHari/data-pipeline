from utils.file_utils import write_file, load_data
from utils.logger_utils import get_logger, log_error
from utils.dataframe_utils import flatten_data

import config
import os


def aggregate_data(groupby_cols, agg_params, data_type=None):
    """
    Generalized function to aggregate mixed data with optional filtering by Data_Type.

    Parameters
    ----------

    groupby_cols: list
        List of columns to group by.

    agg_params: dict
        Dictionary of column names and aggregation functions.
        e.g., {'Age': 'mean', 'Value_of_Consumption_Last_30_Day': 'sum'}

    data_type: str or None
        Filter data by `Data_Type` column if specified.

    Returns
    -------

    pd.DataFrame
        Aggregated dataframe.
    """

    logger = get_logger(__name__)

    try:

        logger.info("Loading merged tsv data...")
        df = load_data(config.MERGED_TSV_PATH, 'tsv')
        logger.info("Merged tsv data loaded")

        if data_type:
            df = df[df['Data_Type'] == data_type]

        agg_cols = list(agg_params.keys())
        df = df.dropna(subset=agg_cols, how="all")

        aggregated_df = df.groupby(groupby_cols).agg(
            agg_params).round(2).reset_index()
        for key, val in agg_params.items():
            aggregated_df.rename(
                columns={key: key+"_"+str(val)}, inplace=True)

        output_file = os.path.join(config.AGGREGATED_DATA_DIR, ("-".join(
            [str(col) for col in groupby_cols]) + "-" + "-".join([str(col) for col in agg_cols]) + '.tsv'))

        write_file(aggregated_df, output_file, 'tsv')
        logger.info(f"Aggregation completed. Output stored at {
                    config.AGGREGATED_DATA_DIR}")
        return aggregated_df

    except Exception as error:
        log_error(logger, error)
