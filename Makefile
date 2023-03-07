env_up:
	docker compose up -d

env_down:
	docker compose down

env_clean:
	docker rmi spark-master-img spark-worker-img airflow-img

run:
	docker exec -it spark_worker /bin/bash spark-submit /opt/airflow/src/tdk_usecase.py