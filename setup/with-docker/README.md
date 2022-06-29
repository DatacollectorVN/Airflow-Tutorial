# Airflow-Tutorial
To installing Airflow with Docker, you can follow the tutorial from author ([here](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)). But this tutorial, clone the `docker-compose.yaml` with bunch of packages that you do not really need. Therefore, we prepair the `docker-compose.yaml` and `.env` configuration for building Airflow with Docker.

## 1. Prerequirement
Your local machine must setuo `Docker` and `Docker-compose` before following our instructions.

## 2. Installing Airflow with Docker
- Clone this repository
```bash
git clone https://github.com/DatacollectorVN/Airflow-Tutorial
cd Airflow-Tutorial
```

- Explore `docker-compose.yaml` an `.env`. You can configure your Airflow webserver and database in `.env`. 

- Build Airflow by Docker compose
```bash
docker-compose up -d
```

- Check the status of Docker container, make sure all of it have `healthy` status.
```
docker ps -a
```
*Note:* This command help us get the `CONTAINER ID` of each Docker container.

- Go to `Airflow UI` via website with port `8080` in localhost. URL: `localhost:8080`. The `user name` and `password` are corresponding to your configuration in `.env` file.

## 3. Interation with Airflow inside Docker container
Because, we're running Airflow by Docker container, so to working with it is more difficult.

After you run `docker-compose up -d`. This will create for you 3 files `dags`, `logs` and `plugins`. That means if you change the content each of it and rebuild Docker compose, that can change Airflow inside container.

## 3.1. Update or add DAGs file in Airflow.
- You can add or update the DAG file in `dags` folder and rebuild Docker compose:
```bash
docker-compose up -d --build
```

## 3.2. DAGs file read or write files during running data pipeline.
When you check containers status by `docker ps -a`, you will see just 3 container are running `airflow-webserve`, `airflow-scheduler` and `airflow-database` (by default is `postgres`).

- All of files that are writed or read by Airflow is included in `airflow-scheduler`, you can go inside this container by 
```bash
docker exec -it <airflow-scheduler-id> bash
```

- If your DAGs file must running outside file to running such as configuration file. You must to copy this file to `airflow-scheduler` container.
```bash
docker cp <path_file_outside> <airflow-scheduler-id>:<path_file_inside>
```

*Note:* we usually `path_file_inside` in `/tmp/` folder.
