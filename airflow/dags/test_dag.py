import os
import logging

from datetime import datetime
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateClusterOperator,
    DataprocDeleteClusterOperator,
    DataprocSubmitJobOperator,
)

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
CLUSTER_NAME = os.environ.get("CLUSTER_NAME")
REGION = os.environ.get("REGION")
AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/opt/airflow/')

DATA_SOURCE = 'data'
DATA_RAW = f'{DATA_SOURCE}/raw'
DATA_PREPROCESSED = f'{DATA_SOURCE}/preprocessed'
ZONE = f"{REGION}-b"
PYSPARK_FILE = 'script/spark.py'
CLUSTER_CONFIG = {
    "master_config": {
        "num_instances": 1,
        "machine_type_uri": "n1-standard-2",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 10},
    },
    "worker_config": {
        "num_instances": 2,
        "machine_type_uri": "n1-standard-2",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 5},

    },
}
TIMEOUT = {"seconds": 1 * 24 * 60 * 60}


PYSPARK_JOB = {
    "reference": {"project_id": PROJECT_ID},
    "placement": {"cluster_name": CLUSTER_NAME},
    "pyspark_job": {
            "main_python_file_uri": f"gs://{BUCKET}/{PYSPARK_FILE}",
            "args": [
                "--input_path=gs://{BUCKET}/{DATA_RAW}/bandcamp_data.csv", 
                "--output_path=gs://{BUCKET}/{DATA_PREPROCESSED}/"
                ]
    }

}


default_args = {
    "owner": "airflow",
}

bandcamp_sale_data = DAG(
    dag_id="test_dag_dev",
    schedule_interval="@once",
    default_args=default_args,
    start_date=datetime(2020, 9, 1),
    catchup=True,
    max_active_runs=1,
    tags=['bandcamp', 'test'],
) 

with bandcamp_sale_data:

    wait_task = ExternalTaskSensor(
        task_id='dag_sensor', 
        external_dag_id = 'test_download_dag_dev', 
        external_task_id = None, 
        mode = 'reschedule'
    )

    create_cluster = DataprocCreateClusterOperator(
        task_id="create_cluster",
        project_id=PROJECT_ID,
        cluster_config=CLUSTER_CONFIG,
        region=REGION,
        cluster_name=CLUSTER_NAME,
    )

    pyspark_task = DataprocSubmitJobOperator(
        task_id="pyspark_task", job=PYSPARK_JOB, region=REGION, project_id=PROJECT_ID
    )

    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_cluster",
        project_id=PROJECT_ID,
        cluster_name=CLUSTER_NAME,
        region=REGION,
        trigger_rule=TriggerRule.ALL_DONE,
    )

    test_task = BashOperator(
        task_id='bash_test_task',
        bash_command=f'echo "Bash connected"'
    )

    # wait_task >> test_task >> create_cluster >> pyspark_task >> delete_cluster
    wait_task >> test_task  >> pyspark_task 


