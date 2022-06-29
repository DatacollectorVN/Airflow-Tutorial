# import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Kos Nhan',
    'start_date': days_ago(0),
    'email': ['datacollectoriu@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG

# define the DAG
dag = DAG(
    'my-second-dag',
    default_args=default_args,
    description='My second DAG',
    schedule_interval=timedelta(days=1),
)

# define the tasks

# define the first task

extract = BashOperator(
    task_id='extract',
    bash_command='cut -d":" -f1,3,6 /etc/passwd > ~/extracted-data.txt',
    dag=dag,
)


# define the second task
transform_and_load = BashOperator(
    task_id='transform',
    bash_command='tr ":" "," < ~/extracted-data.txt > ~/transformed-data.csv',
    dag=dag,
)


# task pipeline
extract >> transform_and_load