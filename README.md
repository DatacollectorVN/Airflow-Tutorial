# Airflow-Tutorial
## My own Document
+ [Install-and-setup-Airflow-with-virtual-environment](https://docs.google.com/document/d/15jaVu-0WGV-VRKGMFu3ynQDul2-DSVIWFdMfmbtMdLM/edit?usp=sharing)
+ [Introduction-to-Airflow](https://docs.google.com/document/d/1o4sT-T08AQyA9g4klrGZBCyLhWhzeEum5wI9M7nOk0s/edit?usp=sharing)
+ [Anatomy-of-Airflow-and-Airflow-DAG](https://docs.google.com/document/d/1w0edJQPTaYawiXAIdd7Lxk7L7aJU0nTfU9Ae2_jcBco/edit?usp=sharing)
+ [Scheduling-Airflow](https://docs.google.com/document/d/1dlC_nRAxzbK0kILkG0VtXwWxIMEHNwRdX7m9MsKTtOI/edit?usp=sharing)

## Setting up

### Create virtual environment
```bash 
conda create -n airflow-tutorial python=3.8 -y 
conda activate airflow-tutorial
```

### Install airflow with specific version and its constraints
```bash
pip install apache-airflow==2.2.3 --constraint constraints-no-providers.txt
```

### Setup Airflow

**Create Airflow databases**
```bash
airflow db init
```
*Expected output:* ~/airflow/ folder

**Set Airflow home**: Airflow need a home with ~/airflow is default.
```bash
export AIRFLOW_HOME=~/airflow
```

**Create user**
```bash 
airflow users create --username admin --password admin --firstname Kos --lastname Nhan --role Admin --email datacollectoriu@gmail.com
```

**Start Airflow**
```bash
airflow webserver -p 8080
airflow scheduler
```

