### 1. Import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

### 2. Defining DAG arguments

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
'''Explain arguments:
+ owner: the owner name.
+ start_date: When this DAG should run from: days_ago(0) mean today.
+ email: The email address where the alerts are sent to.
+ email_on_failure: If True alert must be sent on failure.
+ email_on_retry: If True alert must be sent on retry.
+ retries: The number of retries in case of failure.
+ retry_delay: The time delay between retries
'''

### 3. Defining the DAG

# define the DAG
dag = DAG(
    'my-first-dag',
    default_args=default_args,
    description='My first DAG',
    schedule_interval=timedelta(days=1),
)
'''Explain arguments:
+ my-first-dag is the ID of the DAG. This is what you see on web console.
+ default_args: passing the dictonary default_args in which all the defaults are defined.
+ description: help us in understanding what this DAG does.
+ schedule_interval: tell us how frequently this DAG runs. timedelta(days=1) mean every day.
'''

### 4. Defining the tasks

# define the first task

extract = BashOperator(
    task_id='extract',
    bash_command = "echo extract",
    dag=dag,
)


# define the second task
transform_and_load = BashOperator(
    task_id='transform',
    bash_command = "echo transform and load",
    dag=dag,
)
''' Explain is defined using: 
+ task_id: is a string and helps in identifying the task.
+ bash_command: What bash command it represents.
+ dag: Which dag this task belongs to.
'''

# task pipeline
extract >> transform_and_load
'''Explain:
Task pipeline helps us to organize the order of tasks.
'''