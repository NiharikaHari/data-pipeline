# Data Pipeline Service API

This Flask-based API service allows users to:

- Run a data pipeline to process demographic and expenditure data.
- Retrieve cleaned, merged, and aggregated data.
- Fetch or list visualizations (charts) generated from the data.

## Project Structure

Here’s a brief overview of the key files and directories:

```
.
├── app.py                      # Main Flask application
├── config.py                   # Configuration variables
├── pipeline.py                 # Script to trigger the pipeline
├── requirements.txt            # Dependencies for the project
├── utils/
│   ├── dataframe_utils.py      # Utilities for dataframe processing
│   ├── file_utils.py           # Utilities for file handling
│   ├── logger_utils.py         # Utilities for logging
│   ├── plot_utils.py           # Utilities for plotting
├── data/
│   ├── raw/                    # Folder for raw input data
│   ├── cleaned/                # Folder for cleaned data
│   ├── merged/                 # Folder for merged data
│   ├── aggregated/             # Folder for aggregated results
│   └── charts/                 # Folder for generated visualizations
├── scripts/
│   ├── data_aggregration.py    # Script for data aggregation
│   ├── data_cleaning.py        # Script for data cleaning
│   ├── data_merging.py         # Script for data merging
│   ├── data_visualization.py   # Script for data visualization
├── logs/                       # Folder for log files
├── requests/                   # Folder for example API requests to test the service
└── README.md                   # This file (instructions for setup)

```

## Getting Started

### Prerequisites

Before running this service, ensure the following are installed on your system:

1. Python (version 3.8 or higher)
2. pip (Python package manager)
3. A suitable code editor (e.g., VS Code) for managing and testing the application.

### Setup Instructions

**1. Clone the repository**

```bash
git clone <repository-url>
cd <repository-name>
```

**2. Set Up a Virtual Environment (Optional but Recommended)**

Create and activate a virtual environment to isolate project dependencies:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

**3. Install Dependencies**
Install all required packages from requirements.txt:

```bash
pip install -r requirements.txt
```

**4. Run the Application**
Start the flask server:

```bash
flask run
```

<br>

## Using the API Service

### Base URL

By default the API runs on

```
http://127.0.0.1:5000
```

This can be modified by updating the below fields in config.py:

```python
# API settings
FLASK_RUN_HOST = "127.0.0.1"
FLASK_RUN_PORT = 5000
FLASK_DEBUG = True
```

> [!NOTE]
> Flask server will need to be restarted with `flask run` command to reflect the change in these settings.

### Configure File Names

1. Place your expenditure and demographic raw data files in the folder `/data/raw`.
2. You may update `config.py` file with the appropriate filenames in the fields below:

```python
# File names
RAW_DEMOGRAPHICS_FILE = "Block_4_Demographic particulars of household members_sample.tsv"
RAW_EXPENDITURE_FILE = "Block_8_Household consumer expenditure_sample.tsv"
CLEANED_DEMOGRAPHICS_FILE = "demographic_cleaned.tsv"
CLEANED_EXPENDITURE_FILE = "expenditure_cleaned.tsv"
MERGED_JSON_FILE = "merged_data.json"
MERGED_TSV_FILE = "merged_data.tsv"
```

3. Alternatively you can specify the raw demographic and expenditure file names while running the pipeline.

<br>

---

Once the flask app is running, you can use the API with tools like **Postman**, **cURL**, or Python scripts. Below are examples for each endpoint:

### **1. Run Pipeline**

**POST** `/run-pipeline`
Trigger the data processing pipeline.

> [!IMPORTANT]
> Ensure that the raw data files (demographic and expenditure) are placed in folder `/data/raw`.

#### Request Parameters

| Field                    | Type     | Required | Description                                                                           | Default Value                     |
| ------------------------ | -------- | -------- | ------------------------------------------------------------------------------------- | --------------------------------- |
| `demographic_file`       | `string` | Optional | Name of the demographic data file.                                                    | `config.RAW_DEMOGRAPHICS_FILE`    |
| `expenditure_file`       | `string` | Optional | Name of the expenditure data file.                                                    | `config.RAW_EXPENDITURE_FILE`     |
| `action`                 | `string` | Optional | Action to perform. Options are: `all`, `clean`, `merge`, `aggregate`, `visualize`<br> | `all`                             |
| `aggregation_parameters` | `list`   | Optional | List of aggregation instructions.<br>                                                 | A default list of 5 aggregations. |

> [!NOTE]
>
> 1. If action is set to `all`, all stages of the pipeline will be executed sequentially.
> 2. You can also mention the filenames of raw data in config.py file in the variables `RAW_DEMOGRAPHICS_FILE` and `RAW_EXPENDITURE_FILE`

<h4 id="aggregation-parameters">Aggregation Parameters</h4>

The field `aggregation_parameters` is expected to be a _list of dictionaries_, where each dictionary has the below key-value pairs:

| Key          | Type   | Required | Description                                                                                                                          |
| ------------ | ------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `groupby`    | `list` | Required | List of columns names along which the data will be grouped.<br>e.g. - `'groupby': ['State', 'MGNREG_jobcard']`                       |
| `agg_params` | `dict` | Required | Dictionary with key-value pairs as: "column_name":"aggregation_function"<br>e.g. - `'agg_params': {"Person_Serial_No": "count"}`<br> |

> [!NOTE]
> The aggregation function can also be a lambda function such as -
> `'agg_params': {"Age": lambda x: x[x >= 18].count()}`

**The default value of `aggregation_parameters` is below:**

```python
[
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
```

#### Examples

**Using Postman or VSCode REST Client Extension**

```html
# POST method to trigger pipeline POST http://127.0.0.1:5000/run-pipeline
Content-Type: application/json { "demographic_file": "Block_4_Demographic.tsv",
"expenditure_file": "Block_8_Expenditure.tsv" }
```

**Using curl**

```bash
curl -X POST http://127.0.0.1:5000/run-pipeline \
-H "Content-Type: application/json" \
-d '{
  "demographic_file": "demographics.tsv",
  "expenditure_file": "expenditure.tsv",
  "action": "aggregate",
  "aggregation_parameters": [
    {"groupby": ["State", "Sector"], "aggregation": {"Age": "mean", "Value_of_Consumption_Last_30_Day": "sum"}}
  ]
}'
```

#### Output

Once the pipeline is executed, the results can be found at below locations:

1. Cleaned data - `/data/cleaned`
2. Merged data - `/data/merged`
3. Aggregated data - `/data/aggregated`
4. Visualizations - `/data/charts`

These results can also be obtained via GET requests as explained below.

<br>

### **2. Fetch Cleaned Data**

**GET** `/data/cleaned`
Retrieve cleaned demographic and expenditure data.

> [!Note]
> The cleaned data is also available at the project folder location `<root>/data/cleaned`

```bash
curl -X GET http://127.0.0.1:5000/data/cleaned
```

<br>

### **3. Fetch Merged Data**

**GET** `/data/merged
Retrieve the merged data.

> [!NOTE]
> The merged data is also available at the project folder location `<root>/data/merged`

```bash
curl -X GET http://127.0.0.1:5000/data/merged
```

<br>

### **4. Fetch Aggregated Data List**

**GET** `/data/aggregated
Retrieve the list of aggregated data files

> [!NOTE]
> The aggregated data is also available at the project folder location `<root>/data/aggregated`

```bash
curl -X GET http://127.0.0.1:5000/data/aggregated
```

<br>

### **5. Fetch Aggregated Data by Filename or Index**

**GET** `/data/aggregated/<filename-or-index>
Retrieve the aggregated data by filename of index

> [!NOTE]
> The aggregated data is also available at the project folder location `<root>/data/aggregated`

**By index**

```bash
curl -X GET http://127.0.0.1:5000/data/aggregated/0
```

**By filename**

```bash
curl -X GET http://127.0.0.1:5000/data/aggregated/HHID-State-Age-Value_of_Consumption_Last_30_Day.tsv
```

<br>

### **6. Fetch List of Visualization Charts**

**GET** `/data/charts
Retrieve the list of charts.

> [!NOTE]
> The charts are also available at the project folder location `<root>/data/charts`

```bash
curl -X GET http://127.0.0.1:5000/data/charts
```

<br>

### **7. Fetch Visualization Charts by Filename or Index**

**GET** `/data/merged/<filename_or_index>
Retrieve the specified chart by filename or index.

> [!NOTE]
> The charts are also available at the project folder location `<root>/data/charts`

```bash
curl -X GET http://127.0.0.1:5000/data/charts/1
```

```bash
curl -X GET http://127.0.0.1:5000/data/charts/grouped.png
```

<br>

## Running the Pipeline via Command Line

In addition to using the API, you can directly run the pipeline script (`pipeline.py`) from the command line. This method allows you to trigger the data processing pipeline without needing to interact with the Flask service.

The result will be the same as calling the `/run-pipeline` API endpoint.

### Available Command-Line Arguments

The `pipeline.py` script accepts the following command-line arguments:

- `--demographic_file`: Name of the cleaned demographic data file (TSV).
- `--expenditure_file`: Name of the cleaned expenditure data file (TSV).
- `--action`: Action to be performed by the pipeline. (e.g., `all`, `aggregate`).
- `--aggregation_parameters`: JSON string specifying the aggregation parameters.

Here is an overview of the arguments you can pass

| Field                    | Required | Description                                                                                                                                                                         | Default Value                     |
| ------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| `demographic_file`       | Optional | Name of the demographic data file.                                                                                                                                                  | `config.RAW_DEMOGRAPHICS_FILE`    |
| `expenditure_file`       | Optional | Name of the expenditure data file.                                                                                                                                                  | `config.RAW_EXPENDITURE_FILE`     |
| `action`                 | Optional | Action to perform. Options are: `all`, `clean`, `merge`, `aggregate`, `visualize`<br>**Note**: If action is set to `all`, all stages of the pipeline will be executed sequentially. | `all`                             |
| `aggregation_parameters` | Optional | List of aggregation instructions.<br>                                                                                                                                               | A default list of 5 aggregations. |

> [!NOTE]
> Aggregation parameters must be in the same format as mentioned under [Aggregation Parameters](#aggregation-parameters)

### Example Commands

```bash
python pipeline.py \
    --demographic-file "Block_4_Demographic.tsv" \
    --expenditure-file "Block_8_Expenditure.tsv" \
    --action "all" \
    --aggregation-parameters '[{"groupby": ["State", "Sector"], "agg_params": {"Age": "mean", "Value_of_Consumption_Last_30_Day": "sum"}}]'
```

```pwsh
python pipeline.py `
    --demographic-file "Block_4_Demographic.tsv" `
    --expenditure-file "Block_8_Expenditure.tsv"
```

```bash
python pipeline.py \
    --action "clean"
```

```bash
python pipeline.py
```

## Built With

- [Flask](https://flask.palletsprojects.com/en/stable/)- Backend framework
- [pandas](https://pandas.pydata.org) - Data manipulation and aggregation
- [matplotlib](https://matplotlib.org) - Plotting and data visualization
- [seaborn](https://seaborn.pydata.org) - Data visualization
