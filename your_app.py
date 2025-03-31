from kafka import KafkaProducer, KafkaConsumer
import time
import json

# Конфигурация Kafka
KAFKA_BROKER = 'localhost:9092'  # Замените на ваше значение, если необходимо
TOPIC_NAME = 'test_topic'

def create_producer():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    return producer

def create_consumer():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',
        group_id='my-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    return consumer

def produce_messages(producer):
    for i in range(10):
        message = {'number': i}
        producer.send(TOPIC_NAME, value=message)
        print(f'Sent: {message}')
        time.sleep(1)  # Задержка в 1 секунду между сообщениями
    producer.flush()

def consume_messages(consumer):
    print("Waiting for messages...")
    for message in consumer:
        print(f'Received: {message.value}')

if __name__ == '__main__':
    producer = create_producer()
    consumer = create_consumer()

    # Запуск продюсера и консюмера в отдельных потоках
    import threading

    producer_thread = threading.Thread(target=produce_messages, args=(producer,))
    consumer_thread = threading.Thread(target=consume_messages, args=(consumer,))

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()
