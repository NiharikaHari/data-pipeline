# Define base project directory
import matplotlib
import config

from utils.file_utils import load_merged_data
from utils.dataframe_utils import flatten_data
from utils.plot_utils import plot_stacked_bar_chart, plot_grouped_bar_chart, plot_pie_charts, plot_stacked_histogram, plot_heatmap
from utils.logger_utils import get_logger, log_error


def visualize_data():
    """
    Draws charts from merged data
    """

    matplotlib.use('Agg')

    logger = get_logger(__name__)
    logger.info("Starting data visualization")

    try:
        logger.info("Loading merged data...")
        merged_data = load_merged_data()
        logger.info("Merged data loaded")

        # Preparing dataframes from JSON merged data
        meta = ['HHID', 'Multiplier_comb', 'Sector', 'State', 'District_Code']
        demographic_df = flatten_data(merged_data, 'Demographic_Data', meta)
        expenditure_df = flatten_data(merged_data, 'Expenditure_Data', meta)

        # Plotting charts
        plot_stacked_bar_chart(expenditure_df)
        plot_grouped_bar_chart(demographic_df)
        plot_pie_charts(demographic_df)
        plot_stacked_histogram(demographic_df)
        plot_heatmap(expenditure_df)

        logger.info(f'Visualization completed. Charts stored at: {
                    config.CHARTS_DIR}')

    except Exception as error:
        log_error(logger, error)
