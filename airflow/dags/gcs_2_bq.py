import os
import logging
from datetime import datetime
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator, BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCheckOperator,
    BigQueryCreateEmptyDatasetOperator,
    BigQueryCreateEmptyTableOperator,
    BigQueryDeleteDatasetOperator,
    BigQueryGetDataOperator,
    BigQueryInsertJobOperator,
    BigQueryIntervalCheckOperator,
    BigQueryValueCheckOperator,
)

AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/opt/airflow/')
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'bandcamp_sale_all_data')

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

DATASET_PATH = "data/preprocessed"
NEW_DATASET = 'bandcamp_sale'
INPUT_PART = "processed"
INPUT_FILETYPE = "parquet"

CREATE_EXTERNAL_TABLE = (
    f"""
    CREATE OR REPLACE EXTERNAL TABLE `{BIGQUERY_DATASET}.external_test_airflow`
    OPTIONS (
      format = 'PARQUET',
      uris = ['gs://{BUCKET}/{DATASET_PATH}/*.parquet']
    );
    """
    )

default_args = {
    "owner": "airflow"
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="gcs_2_bq_dev",
    schedule_interval="@once",
    default_args=default_args,
    start_date=datetime(2020, 9, 1),
    catchup=False,
    max_active_runs=1,
    tags=['bandcamp','test'],
) as dag:

    wait_task = ExternalTaskSensor(
        task_id='dag_sensor', 
        external_dag_id = 'transform_dag_dev', 
        external_task_id = None, 
        mode = 'reschedule'
    )


    insert_query_job = BigQueryInsertJobOperator(
    task_id="create_external_job",
    configuration={
        "query": {
            "query": CREATE_EXTERNAL_TABLE,
            "useLegacySql": False,
        }
    },
    location="asia-southeast1",
)

    # gcs_2_bq_ext = BigQueryCreateExternalTableOperator(
    # task_id="bigquery_external_table_task",
    #     table_resource={
    #         "tableReference": {
    #             "projectId": PROJECT_ID,
    #             "datasetId": BIGQUERY_DATASET,
    #             "tableId": f"external_bandcamp_sale",
    #         },
    #         "externalDataConfiguration": {
    #             'autodetect':True,
    #             "sourceFormat": f"{INPUT_FILETYPE.upper()}",
    #             "sourceUris": [f"gs://{DATASET}/{PROCESSED}/*.{INPUT_FILETYPE}"],
    #         },
    #     }
    # )

    wait_task >>  insert_query_job