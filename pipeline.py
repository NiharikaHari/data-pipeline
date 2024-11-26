from scripts.data_cleaning import clean_data
from scripts.data_merging import merge_data
from scripts.data_visualization import visualize_data
from scripts.data_aggregation import aggregate_data

import config
import os
import argparse

from utils.logger_utils import configure_logger, get_logger, log_error


def run_pipeline(demographic_file=None, expenditure_file=None, action=None, aggregation_parameters=None):
    """
    Orchestrates the pipeline: cleaning, merging, aggregation and visualization.

    Parameters
    ----------

    demographic_file : string (default=None)
        File name of demographic data.
    expenditure_file : string (default=None)
        File name of expenditure data.
    action : string (default=None)
        Stage of pipeline to run. Options > 'clean', 'merge', 'aggregate', 'visualize', 'all'
    aggregation_parameters : list (default=None)
        List of dictionaries with aggregation parameters

    """

    if demographic_file:
        RAW_DEMOGRAPHICS_PATH = os.path.join(
            config.RAW_DATA_DIR, demographic_file)
    else:
        RAW_DEMOGRAPHICS_PATH = config.RAW_DEMOGRAPHICS_PATH

    if expenditure_file:
        RAW_EXPENDITURE_PATH = os.path.join(
            config.RAW_DATA_DIR, expenditure_file)

    else:
        RAW_EXPENDITURE_PATH = config.RAW_EXPENDITURE_PATH

    action = action or 'all'

    aggregation_parameters = aggregation_parameters or [
        {
            # Average age and number of individuals grouped by state
            'groupby': ['State'],
            'agg_params': {"Age": "mean", "Person_Serial_No": "count"}
        },
        {
            # Average age and number of individuals grouped by Sex, Education Level, and Status of Current Attendance
            'groupby': ['Sex', 'General_Education', 'Status_of_Current_Attendance'],
            'agg_params': {"Age": "mean", "Person_Serial_No": "count"}
        },
        {
            # Average expenditure in last 30 days grouped by state and District
            'groupby': ['State', 'District_Code'],
            'agg_params': {"Value_of_Consumption_Last_30_Day": "mean"}
        },
        {
            # Count of people registered in MGNREG grouped by State
            'groupby': ['State', 'MGNREG_jobcard'],
            'agg_params': {"Person_Serial_No": "count"}
        },
        {
            # Count of unmarried people who are adults grouped by State, Distric, HHID
            'groupby': ['State', 'District_Code', 'HHID', 'Marital_Status'],
            'agg_params': {"Age": lambda x: x[x >= 18].count()}
        }
    ]

    configure_logger()
    logger = get_logger(__name__)

    try:

        logger.info("Running pipeline...")
        print("Running pipeline...")

        if action in ['clean', 'all']:

            # Step 1: Clean data
            logger.info("Stage: Cleaning data...")
            print("Stage: Cleaning data...")

            clean_data(RAW_DEMOGRAPHICS_PATH,
                       config.CLEANED_DEMOGRAPHICS_PATH)
            clean_data(RAW_EXPENDITURE_PATH,
                       config.CLEANED_EXPENDITURE_PATH)

            logger.info("Stage: Cleaning data completed")

        if action in ['merge', 'all']:

            # Step 2: Merge data
            logger.info("Stage: Merging data...")
            print("Stage: Merging data...")

            merge_data(config.CLEANED_EXPENDITURE_PATH,
                       config.CLEANED_DEMOGRAPHICS_PATH)

            logger.info("Stage: Merging data completed")

        if action in ['aggregate', 'all']:
            # Step 3: Generate aggregations
            logger.info("Stage: Generating aggregations...")
            print("Stage: Generating aggregations....")

            for param in aggregation_parameters:
                aggregate_data(param['groupby'],
                               param['agg_params'])

            logger.info("Stage: Generating aggregations completed")

        if action in ['visualize', 'all']:

            # Step 4: Generate visualizations
            logger.info("Stage: Generate visualizations...")
            print("Stage: Generate visualizations...")

            visualize_data()

            logger.info("Stage:  Generate visualizations completed")

        logger.info("Pipeline completed.")
        print("Pipeline completed!")

    except Exception as error:
        log_error(logger, error)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the data pipeline.")
    parser.add_argument("--demographic_file", type=str,
                        default=None, help="Path to the demographic data file.")
    parser.add_argument("--expenditure_file", type=str,
                        default=None, help="Path to the expenditure data file.")
    parser.add_argument("--action", type=str, choices=["clean", "merge", "aggregate", "visualize", "all"],
                        default="all", help="List of action to perform.")
    parser.add_argument("--aggregation_parameters", type=str,
                        default=None, help="List of dictonaries containing aggregation parameters.")
    args = parser.parse_args()

    demographic_file = args.demographic_file
    expenditure_file = args.expenditure_file
    action = args.action
    if args.aggregation_parameters:
        aggregation_parameters = eval(args.aggregation_parameters)
    else:
        aggregation_parameters = None

    run_pipeline(
        demographic_file=demographic_file,
        expenditure_file=expenditure_file,
        action=action,
        aggregation_parameters=aggregation_parameters
    )
