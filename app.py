from flask import Flask, render_template, request, jsonify
import uuid
from time import sleep
from json import dumps
from kafka import KafkaProducer

app = Flask(__name__)

# Temporary data store for bookings (replace with a database in a real application)
bookings = {}
def generate_booking_id():
    return str(uuid.uuid4())

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book_hotel():
    data = {
        'user_id': request.form['user_id'],
        'user_name': request.form['user_name'],
        'hotel_name': request.form['hotel_name'],
        'days_stay': int(request.form['days_stay'])
    }

    # Generate a unique booking ID (replace with a more robust solution in production)
    topic_name="topic1"
    producer=KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda a:dumps(a).encode('utf-8'))
    booking_id = generate_booking_id()
    bookings[booking_id] = data
    print(bookings)
    producer.send(topic_name,value=bookings)
    sleep(2)

    return render_template('booking_success.html', booking_id=booking_id, data=data)



@app.route('/update/<booking_id>', methods=['GET'])
def update_form(booking_id):
    if booking_id in bookings.keys():
        print(booking_id, bookings)
        return render_template('update.html', booking_id=booking_id, data=len(bookings))
    else:
        return render_template('booking_not_found.html', booking_id=booking_id)

@app.route('/update/<booking_id>', methods=['POST'])
def update_booking(booking_id):
    if booking_id in bookings.keys():
        data = {
            'user_id': request.form['user_id'],
            'user_name': request.form['user_name'],
            'hotel_name': request.form['hotel_name'],
            'days_stay': int(request.form['days_stay'])
        }
        # write code to make data stream to apache kafka. From Kafka we can have connector triggers which
        # push data to snowflake tables.
        bookings[booking_id] = data
        return render_template('update_success.html', booking_id=booking_id, data=data)
    else:
        return render_template('booking_not_found.html', booking_id=booking_id)


if __name__ == '__main__':
    app.run(debug=True)
