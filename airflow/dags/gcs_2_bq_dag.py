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
BIGQUERY_PROD_DATASET = os.environ.get("BIGQUERY_DATASET", 'bandcamp_sale_prod')

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

DATASET_PATH = "data/preprocessed"
INPUT_PART = "processed"
INPUT_FILETYPE = "parquet"

CREATE_EXTERNAL_TABLE = (
    f"""
    CREATE OR REPLACE EXTERNAL TABLE 
        `{BIGQUERY_DATASET}.external_non_part`
    OPTIONS (
      format = 'PARQUET',
      uris = ['gs://{BUCKET}/{DATASET_PATH}/*.parquet']
    );
    """
    )

CREATE_INTERNAL_TABLE = (
    f"""
    CREATE OR REPLACE TABLE 
        `{BIGQUERY_DATASET}.bandcamp_data`
    AS
        SELECT
            *
        FROM
            `{BIGQUERY_DATASET}.external_non_part`
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


    insert_external_job = BigQueryInsertJobOperator(
    task_id="create_ext_non_part_task",
    configuration={
        "query": {
            "query": CREATE_EXTERNAL_TABLE,
            "useLegacySql": False,
        }
    },
    location="asia-southeast1",
    )

    insert_internal_job = BigQueryInsertJobOperator(
    task_id="create_int_non_part_task",
    configuration={
        "query": {
            "query": CREATE_INTERNAL_TABLE,
            "useLegacySql": False,
        }
    },
    location="asia-southeast1",
    )



    wait_task >>  insert_external_job >> insert_internal_job