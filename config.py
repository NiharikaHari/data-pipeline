import os


# File names
RAW_DEMOGRAPHICS_FILE = "Block_4_Demographic particulars of household members_sample.tsv"
RAW_EXPENDITURE_FILE = "Block_8_Household consumer expenditure_sample.tsv"
CLEANED_DEMOGRAPHICS_FILE = "demographic_cleaned.tsv"
CLEANED_EXPENDITURE_FILE = "expenditure_cleaned.tsv"
MERGED_JSON_FILE = "merged_data.json"
MERGED_TSV_FILE = "merged_data.tsv"


# Define base project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data directories
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
CLEANED_DATA_DIR = os.path.join(DATA_DIR, "cleaned")
MERGED_DATA_DIR = os.path.join(DATA_DIR, "merged")
AGGREGATED_DATA_DIR = os.path.join(DATA_DIR, "aggregated")


# File paths
RAW_DEMOGRAPHICS_PATH = os.path.join(
    RAW_DATA_DIR, RAW_DEMOGRAPHICS_FILE)
RAW_EXPENDITURE_PATH = os.path.join(
    RAW_DATA_DIR, RAW_EXPENDITURE_FILE)
CLEANED_DEMOGRAPHICS_PATH = os.path.join(
    CLEANED_DATA_DIR, CLEANED_DEMOGRAPHICS_FILE)
CLEANED_EXPENDITURE_PATH = os.path.join(
    CLEANED_DATA_DIR, CLEANED_EXPENDITURE_FILE)
MERGED_JSON_PATH = os.path.join(MERGED_DATA_DIR, MERGED_JSON_FILE)
MERGED_TSV_PATH = os.path.join(MERGED_DATA_DIR, MERGED_TSV_FILE)


# Report directories
CHARTS_DIR = os.path.join(DATA_DIR, "charts")

# Logs directory
LOGS_DIR = os.path.join(BASE_DIR, "logs")
PIPELINE_LOG_PATH = os.path.join(LOGS_DIR, "pipeline.log")

# API settings
API_HOST = "127.0.0.1"
API_PORT = 5000
DEBUG = True
