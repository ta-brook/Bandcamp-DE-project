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
    end_date=datetime(2020, 10, 10),
    catchup=False,
    max_active_runs=1,
    tags=['bandcamp','test'],
) as dag:

    dbt_debug_task = BashOperator(
        task_id = 'dbt_debug',
        bash_command= 'cd /dbt && dbt debug'
    )

    dbt_deps_task = BashOperator(
        task_id = 'dbt_deps',
        bash_command= 'cd /dbt && dbt deps'
    )

    dbt_run_test_task = BashOperator(
        task_id = 'dbt_run_test',
        bash_command= 'cd /dbt && dbt run'
    )
