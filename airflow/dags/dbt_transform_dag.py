from datetime import datetime
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner' : 'airflow'
}

with DAG(
    dag_id="dbt_transform_dag_dev",
    schedule_interval="@once",
    default_args=default_args,
    start_date=datetime(2020, 9, 1),
    end_date=datetime(2020, 10, 10),
    catchup=False,
    max_active_runs=1,
    tags=['bandcamp','test'],
) as dag:

    dbt_setup_prod = BashOperator(
        task_id = 'dbt_setup_prod',
        bash_command= 'cd /dbt && dbt deps && dbt seed --profiles-dir . --target prod'
    )

    dbt_run_prod = BashOperator(
        task_id = 'dbt_run_prod',
        bash_command= 'cd /dbt && dbt run --profiles-dir . --target prod'
    )

    dbt_setup_prod >> dbt_run_prod