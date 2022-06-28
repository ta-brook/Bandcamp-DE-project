from datetime import datetime
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner' : 'airflow'
}

with DAG(
    dag_id="dbt_test_dag_dev",
    schedule_interval="@once",
    default_args=default_args,
    start_date=datetime(2020, 9, 1),
    catchup=False,
    max_active_runs=1,
    tags=['bandcamp','test'],
) as dag:

    test_dbt_task = BashOperator(
        task_id = 'dbt_test',
        bash_command= 'cd /dbt && dbt debug'
    )

    test_dbt_2_task = BashOperator(
        task_id = 'dbt_2_test',
        bash_command= 'cd /dbt && dbt deps'
    )