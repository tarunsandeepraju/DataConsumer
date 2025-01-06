from flask import Flask, request, jsonify
from redis import StrictRedis

app = Flask(__name__)

# Connect to Redis
redis_client = StrictRedis(
    host='redis.finvedic.in',
    port=6379,
    db=0
)

@app.route('/save', methods=['POST'])
def save_data():
    data = request.get_json()
    print(f"Received data: {data}")  # Debug: Print received data
    key = data.get('key')
    value = data.get('value')
    redis_client.set(key, value)
    return jsonify({"message": "Data saved to Redis!"}), 200

if __name__ == "__main__":
    app.run(port=5001, debug=True)