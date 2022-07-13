# Airflow-Tutorial

# TXComs
`XComs` (short for “cross-communications”) are a mechanism that let `Tasks` talk to each other, as by default Tasks are entirely isolated and may be running on entirely different machines.
Almost cases in Airflow, `XComs` is used with `PythonOperator`.

Source [here](https://betterdatascience.com/apache-airflow-xcoms/)

## How to Push a Value to Airflow XComs
Let's start with pushing a value to `Airflow XComs`. This can be done in multiple ways, but by far the most explicit one is by specifying the `do_xcom_push=True` as a task parameter.

```bash
task_get_date = PythonOperator(
        task_id='get_date',
        python_callable=get_date,
        do_xcom_push=True
    )
```

Test the `get_date` task.
```bash
airflow tasks test xcom_dag get_date 2022-7-1
```

*Expected output:* Check the output log: `INFO - Done. Returned value was: 2022-07-13 20:43:38.363660`

## How to Get the XCom Value through Airflow
We'll now write yet another task - `task_save_date `- which calls the `save_date()` Python function.

Python function to get the value from Airflow task:
```bash
def save_date(ti) -> None:
    dt = ti.xcom_pull(task_ids=['get_date'])
    if not dt:
        raise ValueError('No value currently stored in XComs.')

    with open('/tmp/date.txt', 'w') as f:
        f.write(dt[0])
```

Airflow task:
```bash
task_save_date = PythonOperator(
        task_id='save_date',
        python_callable=save_date
    )
```
Test the `save_date` task.

```bash
airflow tasks test xcom_dag save_date 2022-7-1
cat /tmp/date.txt
```
*Expected output:* 
```bash
2022-07-13 20:43:38.363660
<class 'list'>
```