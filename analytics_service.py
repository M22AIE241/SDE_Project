from kafka import KafkaConsumer
from collections import defaultdict

consumer = KafkaConsumer('hotel-bookings', bootstrap_servers='your_kafka_bootstrap_servers', group_id='analytics-group')
analytics_data = defaultdict(int)

def update_analytics(data):
    # Implement your analytics logic here
    analytics_data['total_bookings'] += 1
    analytics_data['total_days_booked'] += data.get('days_stay', 0)
    # Add more analytics as needed

if __name__ == '__main__':
    for message in consumer:
        data = eval(message.value)  # Deserialize JSON data from Kafka
        update_analytics(data)
        print("Analytics updated:", analytics_data)
