from kafka import KafkaConsumer
from redis import StrictRedis
import json

redis_client = StrictRedis(
    host='localhost',
    port=6379,
    db=0
)

def consume_from_kafka():
    consumer = KafkaConsumer(
        'market_data',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    print("Kafka consumer initialized")

    for message in consumer:
        print("Received a message from Kafka")
        data = message.value
        print(f"Received data: {data}")

        if 'key' in data and 'value' in data:
            # Serialize the value to a JSON string
            serialized_value = json.dumps(data['value'])
            # Use HSET to store data in Redis as a hash
            redis_client.hset('my_hash', data['key'], serialized_value)
            print(f"Data saved to Redis as hash: key={data['key']}, value={serialized_value}")
        else:
            print("Received data does not contain 'key' and 'value' fields")

if __name__ == "__main__":
    consume_from_kafka()
