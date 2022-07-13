from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.models.baseoperator import chain
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup

DEFAULT_ARGS = {
    'owner': 'Nathan Ngo',
    'start_date': days_ago(0),
    'email': ['datacollectoriu@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes = 5),
}
with DAG(
    dag_id = 'simple-task-group',
    default_args = DEFAULT_ARGS,
    dagrun_timeout = timedelta(minutes=7),
    schedule_interval='*/5 * * * *',
) as dag:
    begin = DummyOperator(task_id = "begin")

    with TaskGroup(group_id = 'group1') as tg1:
        t1 = DummyOperator(task_id = 'task1')
        t2 = DummyOperator(task_id = 'task2')

        t1 >> t2

    with TaskGroup(group_id='group2') as tg2:
        t3 = DummyOperator(task_id='task3')
        t4 = DummyOperator(task_id='task4')

        [t3, t3]
    
    end = DummyOperator(task_id="end")
    
        
chain(
    begin, 
    tg1,
    tg2,
    end
)