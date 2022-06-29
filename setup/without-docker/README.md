# Airflow-Tutorial

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