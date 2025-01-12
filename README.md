## Smart City Project ##
This is an end-to-end data processing pipeline designed for smart city applications. The data is processed using a combination of open-source tools and AWS services, including Apache Kafka for streaming, Apache Airflow for workflow orchestration, and AWS services like Amazon S3, AWS Glue and Amazon Athena for interactive querying. The project is containerized using Docker.

## System Architecture ##
![smart-city-airflow-](https://github.com/user-attachments/assets/1d6e6812-ce1a-4f41-b026-e9a641564993)


## Usefull Commands ##
docker exec -it broker /bin/bash <br>
kafka-topics --list --bootstrap-server broker:29092 <br>
kafka-topics --delete --topic <topic_name>  --bootstrap-server broker:29092 <br>

docker exec -it smart_city_kafka-spark-master-1 spark-submit \--master spark://spark-master:7077 \--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk:1.11.468 jobs/spark-city.py
