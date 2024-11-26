from flask import Flask, request, jsonify, send_file
import os
import config
import traceback

from pipeline import run_pipeline
from utils.file_utils import load_cleaned_data, load_merged_data, load_dataframe

app = Flask(__name__)

# Set environment variables from config.py
os.environ["FLASK_RUN_HOST"] = config.FLASK_RUN_HOST
os.environ["FLASK_RUN_PORT"] = str(config.FLASK_RUN_PORT)
os.environ["FLASK_DEBUG"] = str(config.FLASK_DEBUG)

# Endpoint to trigger the pipeline


@app.route('/run-pipeline', methods=['POST'])
def run_pipeline_api():
    """
    Runs the data pipeline based on provided input parameters.

    Request Body (JSON):
    - demographic_file (str): File name of the demographic data file.
    - expenditure_file (str): File name of the expenditure data file.
    - action (str): Action to perform (e.g., all, clean, aggregate).
    - aggregation_parameters (list[dict]): Parameters for data aggregation (if applicable).

    Response:
    - 200: Successful execution of the pipeline.
    - 500: Internal server error with the error message.
    """
    try:
        request_data = {}
        if request.content_type == 'application/json':
            request_data = request.get_json() or {}

        demographic_file = request_data.get('demographic_file')
        expenditure_file = request_data.get('expenditure_file')
        action = request_data.get('action')
        aggregation_parameters = request_data.get('aggregation_parameters')

        run_pipeline(demographic_file, expenditure_file,
                     action, aggregation_parameters)

        return jsonify({"message": "Pipeline executed successfully!"}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# Endpoint to fetch cleaned data
@app.route('/data/cleaned', methods=['GET'])
def get_cleaned_data():
    """
    Fetches cleaned demographic and expenditure data from pre-defined paths.

    Response:
    - 200: Returns the cleaned data as a JSON object.
    - 500: Internal server error with the error message.
    """
    try:
        data = load_cleaned_data()
        return jsonify(data), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# Endpoint to fetch merged data
@app.route('/data/merged', methods=['GET'])
def get_merged_data():
    """
    Fetches merged data combining demographic and expenditure data.

    Response:
    - 200: Returns the merged data as a JSON object.
    - 500: Internal server error with the error message.
    """
    try:
        data = load_merged_data()
        return jsonify(data), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# Endpoint to list available aggregated data
@app.route('/data/aggregated', methods=['GET'])
def list_aggregations():
    """
    Lists all available aggregated data files in the aggregation directory.

    Response:
    - 200: Returns a list of filenames as JSON.
    - 500: Internal server error with the error message.
    """
    try:
        aggregations = os.listdir(config.AGGREGATED_DATA_DIR)
        return jsonify({"aggregated-data-links": aggregations}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# Endpoint to fetch a specific aggregation by name or index
@app.route('/data/aggregated/<name>', methods=['GET'])
def get_aggregation_by_name(name):
    """
    Fetches a specific aggregated data file by name or index.

    Path Parameter:
    - name (str): Name of the aggregated data file.

    Response:
    - 200: Returns the aggregated data as a JSON object.
    - 404: Aggregation file not found.
    - 500: Internal server error with the error message.
    """
    try:
        if name.isnumeric():
            files = os.listdir(config.AGGREGATED_DATA_DIR)
            if int(name) >= len(files):
                return jsonify({"error": f"Aggregation not found: {name}"}), 404
            else:
                name = files[int(name)]

        filepath = os.path.join(config.AGGREGATED_DATA_DIR, name)

        if os.path.exists(filepath):
            data = load_dataframe(filepath).to_dict(orient='records')
            return jsonify(data), 200
        else:
            return jsonify({"error": f"Aggregation not found: {name}"}), 404
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# Endpoint to list available visualizations
@app.route('/data/charts', methods=['GET'])
def list_charts():
    """
    Lists all available visualization files in the charts directory.

    Response:
    - 200: Returns a list of visualization filenames as JSON.
    - 500: Internal server error with the error message.
    """
    try:
        charts = os.listdir(config.CHARTS_DIR)
        return jsonify({"chart-image-links": charts}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# Endpoint to fetch a specific visualization by name or index
@app.route('/data/charts/<name>', methods=['GET'])
def get_chart_by_name(name):
    """
    Fetches a specific visualization file by name or index.

    Path Parameter:
    - name (str): Name or index of the visualization file.

    Response:
    - 200: Returns the visualization file (image).
    - 404: Visualization file not found.
    - 500: Internal server error with the error message.
    """
    try:
        if name.isnumeric():
            files = os.listdir(config.CHARTS_DIR)
            if int(name) >= len(files):
                return jsonify({"error": f"Chart not found: {name}"}), 404
            else:
                name = files[int(name)]
        filepath = os.path.join(config.CHARTS_DIR, name)
        if os.path.exists(filepath):
            return send_file(filepath, mimetype='image/png')
        else:
            return jsonify({"error": f"Chart not found: {name}"}), 404
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host=config.API_HOST, port=config.API_PORT, debug=config.DEBUG)
