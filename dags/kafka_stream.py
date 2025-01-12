from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
from confluent_kafka import Producer
import json

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = 'broker:29092'
KAFKA_TOPIC = 'api_data'

# API configuration
API_URL = 'https://randomuser.me/api/'


# Fetch data from API
def fetch_data_from_api():
    response = requests.get(API_URL)
    if response.status_code == 200:
        response = response.json()
        response = response['results'][0]

        data = {}
        data['first_name'] = response['name']['first']
        data['last_name'] = response['name']['last']
        data['gender'] = response['gender']
        data['username'] = response['login']['username']
        data['timestamp'] = datetime.now().isoformat()

        return data
    else:
        raise ValueError(f"Failed to fetch data from API: {response.status_code}")


# Send data to Kafka
def send_data_to_kafka():
    data = fetch_data_from_api()
    producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

    producer.produce(KAFKA_TOPIC, json.dumps(data).encode('utf-8'))
    producer.flush()


# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'api_to_kafka_to_s3',
    default_args=default_args,
    description='Fetch data from API, send to Kafka, and then to S3',
    schedule_interval=timedelta(minutes=2),
    catchup=False,
)

# Task to fetch data and send to Kafka
fetch_and_send_task = PythonOperator(
    task_id='fetch_and_send_to_kafka',
    python_callable=send_data_to_kafka,
    dag=dag,
)
