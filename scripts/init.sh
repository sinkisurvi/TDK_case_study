#!/usr/bin/env bash
airflow db init

airflow users create --role Admin --username airflow --password airflow --email airflow@example.com --firstname foo --lastname bar

parallel ::: "airflow webserver" "airflow scheduler"
