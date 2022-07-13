# Airflow-Tutorial

# Task group in Airflow

Before `Task Groups` in `Airflow 2.0`, Subdags were the go-to API to group tasks. With `Airflow 2.0`, `SubDags` **are being relegated** and now replaced with the `Task Group` feature. The `TaskFlow API` is simple and allows for a proper code structure, favoring a clear separation of concerns.

## Create `Task Groups` with `TaskGroup`
Read my example `simple_task_group.py`.

## Create `Task Groups` with `Decorator (@)`
Read my example `decorator_task_group.py`.