from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Adapter l'URL si nécessaire
client = MongoClient("mongodb://localhost:27017")
db = client["open5gs"]

@app.route('/imeisv', methods=['GET'])
def get_imeisv():
    subscriber = db.subscribers.find_one(
        {"imsi": "001012345678901"},
        {"_id": 0, "imeisv": 1}
    )

    if not subscriber:
        return jsonify({"error": "subscriber not found"}), 404

    return jsonify({"imeisv": subscriber.get("imeisv")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)


