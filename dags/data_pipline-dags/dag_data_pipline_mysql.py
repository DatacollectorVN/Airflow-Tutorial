from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from pandas import json_normalize
from airflow.models.baseoperator import chain
from airflow.operators.dummy import DummyOperator
from datetime import datetime
from datetime import timedelta
import json

DEFAULT_ARGS = {
    'owner': 'Nathan Ngo',
    'start_date': datetime(2019, 1, 1),
    'email': ['datacollectoriu@gmail.com']
}
def _processing_user(ti):
    # https://airflow.apache.org/docs/apache-airflow/stable/concepts/xcoms.html
    users = ti.xcom_pull(task_ids = ['extracting_user'])
    if not len(users) or 'results' not in users[0]:
        raise ValueError('User is empty')
    user = users[0]['results'][0]
    processed_user = json_normalize({
        'firstname': user['name']['first'],
        'lastname': user['name']['last'],
        'country': user['location']['country'],
        'username': user['login']['username'],
        'password': user['login']['password'],
        'email': user['email']
    })
    processed_user.to_csv('/tmp/processed_user.csv', index = None, header = None)

def _store_user(mysql_conn_id_name, custom_sql, file_name):
    hook = MySqlHook(mysql_conn_id_name)
    hook.bulk_load_custom(
        table= 'users',
        tmp_file= file_name,
        extra_options= custom_sql
    )
with DAG(
    dag_id='data_pipeline_MySQL',
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(minutes=7),
    schedule_interval='*/5 * * * *'
) as dag:
    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")

    create_table = MySqlOperator(
        task_id='creating_table',
        mysql_conn_id='db_mysql_local_store',
        sql='''
                CREATE TABLE IF NOT EXISTS users (
                    firstname VARCHAR(100) NOT NULL,
                    lastname VARCHAR(100) NOT NULL,
                    country VARCHAR(100) NOT NULL,
                    username VARCHAR(100) NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL
                )
            '''
    )

    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='api/' # the base will verify     
    )

    extracting_user = SimpleHttpOperator(
        task_id = 'extracting_user',
        http_conn_id='user_api',
        endpoint='api/',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    processing_user = PythonOperator(
        task_id = 'processing_user',
        python_callable=_processing_user
    )

    storing_user = PythonOperator(
        task_id = 'storing_user',
        python_callable=_store_user,
        op_kwargs={
            'mysql_conn_id_name': 'db_mysql_local_store',
            'custom_sql': "FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n'",
            'file_name': '/tmp/processed_user.csv' 
        }
    )
    
chain(
    begin, 
    create_table,
    is_api_available,
    extracting_user,
    processing_user,
    storing_user,
    end
)