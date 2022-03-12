import datetime as dt
from pathlib import Path
import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import timedelta

def _calculate_stats(input_path, output_path):
    """Calculates event statistics."""
    events = pd.read_json(input_path)
    stats = events.groupby(["date", "user"]).size().reset_index()
    Path(output_path).parent.mkdir(exist_ok = True)
    stats.to_csv(output_path, index = False)

default_args = {
    'owner': 'Kos Nhan',
    'start_date': dt.datetime(2019, 1, 1),
    'email': ['datacollectoriu@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes = 5),
}

dag = DAG(dag_id = "query_dates", default_args = default_args,
          schedule_interval = "@daily") # Specify that this is an unscheduled DAG.

''' Original way
fetch_events = BashOperator(task_id = "fetch_events",
                            bash_command = ("mkdir -p /data && "
                                            "curl -o /data/events.json "
                                            "https:/ /localhost:5000/events?"
                                            "start_date={{execution_date.strftime('%Y-%m-%d')}}&"
                                            "end_date={{next_execution_date.strftime('%Y-%m-%d')}}"),
                            dag = dag)
'''

fetch_events = BashOperator(task_id = "fetch_events",
                            bash_command = ("mkdir -p /data && "
                                            "curl -o /data/events.json "
                                            "https:/ /localhost:5000/events?"
                                            "start_date={{ds}}&"
                                            "end_date={{next_ds}}"),
                            dag = dag)

calculate_stats = PythonOperator(task_id = "calculate_stats", python_callable = _calculate_stats,
                                 op_kwargs = {"input_path": "/data/events.json", "output_path": "/data/stats.csv"},
                                 dag = dag)

fetch_events >> calculate_stats
