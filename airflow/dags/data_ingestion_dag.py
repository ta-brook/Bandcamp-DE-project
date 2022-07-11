import csv
import os
import logging

from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator

AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/opt/airflow')

LOCAL_DATA_PATH = AIRFLOW_HOME + '/data'
LOCAL_SCRIPT_PATH = AIRFLOW_HOME + '/dags/script'

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


default_args = {
    "owner": "airflow",
}

bandcamp_sale_data = DAG(
    dag_id="Ingestion_dag_dev",
    schedule_interval="@once",
    default_args=default_args,
    start_date=datetime(2020, 9, 1),
    catchup=True,
    max_active_runs=1,
    tags=['bandcamp', 'test'],
) 

with bandcamp_sale_data:

    pwd_task = BashOperator(
        task_id='pwd_task',
        bash_command=f'pwd'
    )

    ls_task = BashOperator(
        task_id='ls_task',
        bash_command=f'ls {AIRFLOW_HOME}'
    )

    download_task = BashOperator(
        task_id='download_unzip_data_task',
        bash_command=f'bash $AIRFLOW_HOME/dags/sh/download_n_unzip.sh bandcamp_data {AIRFLOW_HOME}'
    )

    ls_data_task = BashOperator(
        task_id='ls_data_task',
        bash_command=f'ls {LOCAL_DATA_PATH}'
    )

    upload_data_lake = PythonOperator(
            task_id='ingest_data_lake_task',
            python_callable=upload_to_gcs,
            op_kwargs={
                "bucket": BUCKET,
                "object_name": 'data/raw/bandcamp_data.csv',
                "local_file": f"{LOCAL_DATA_PATH}/bandcamp_data.csv",
            },
        )
    
    # rm_task = BashOperator(
    #     task_id='rm_data_task',
    #     bash_command=f'rm {LOCAL_DATA_PATH}/bandcamp_data.csv'
    # )

    upload_script_task = PythonOperator(
            task_id='upload_script_task',
            python_callable=upload_to_gcs,
            op_kwargs={
                "bucket": BUCKET,
                "object_name": 'script/spark.py',
                "local_file": f"{LOCAL_SCRIPT_PATH}/spark.py",
            },
        )


# $ docker exec -it docker_spark_1 spark-submit --master spark://spark:7077 /usr/local/spark/app/hello-world.py /usr/local/spark/resources/data/airflow.cfg

    # spark_job = SparkSubmitOperator(
    # task_id="spark_job",
    # application=f"{AIRFLOW_HOME}/dags/spark.py", # Spark application path created in airflow and spark cluster
    # name="hello-world-module",
    # conn_id="spark_default",
    # verbose=1,
    # conf={"spark.master":"spark://spark:7077"},
    # application_args=["--input_path={AIRFLOW_HOME}/data/*.csv", "--output_path={AIRFLOW_HOME}/data/raw/"],
    # )

    pwd_task >> ls_task >> download_task >> ls_data_task >> upload_data_lake >> upload_script_task
