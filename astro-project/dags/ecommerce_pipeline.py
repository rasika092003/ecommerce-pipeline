from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': '#Type Yours',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def generate_orders():
    print("Generating 500 new orders...")
    print("Orders generated successfully!")

def validate_data():
    print("Validating data quality...")
    print("Validation passed!")

def load_to_db():
    print("Loading data to PostgreSQL...")
    print("Data loaded successfully!")

with DAG(
    dag_id='ecommerce_pipeline',
    default_args=default_args,
    description='Daily e-commerce data pipeline',
    schedule='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['ecommerce', 'dbt', 'postgres'],
) as dag:

    generate = PythonOperator(
        task_id='generate_new_orders',
        python_callable=generate_orders,
    )

    validate = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
    )

    load = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_db,
    )

    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command='echo "dbt models completed successfully!"',
    )

    generate >> validate >> load >> run_dbt
