import os
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from dotenv import load_dotenv
from services.data_collector import CityDataCollector

# Load environment variables
load_dotenv()

GOOGLE_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
AQI_KEY = os.getenv("OPENWEATHER_API_KEY")

# Initialize Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "smart_city_secret"

# Enable CORS for React
CORS(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# Initialize data collector
collector = CityDataCollector(GOOGLE_KEY, AQI_KEY)


# ---------------------------------------------------
# Home Route
# ---------------------------------------------------
@app.route("/")
def home():
    return jsonify({
        "project": "Smart City Predictive Traffic System",
        "status": "online",
        "modules": [
            "Traffic Prediction",
            "Emergency Corridor Optimizer",
            "Pollution Aware Routing"
        ]
    })


# ---------------------------------------------------
# City Status API
# ---------------------------------------------------
@app.route("/api/status", methods=["GET"])
def get_city_status():
    try:
        df = collector.collect_snapshot()

        if df is None or df.empty:
            return jsonify({
                "message": "No data available"
            }), 200

        return jsonify(df.to_dict(orient="records"))

    except Exception as e:
        print("STATUS API ERROR:", e)

        return jsonify({
            "error": str(e),
            "message": "Failed to fetch real-time data"
        }), 500


# ---------------------------------------------------
# Traffic Prediction Broadcast
# ---------------------------------------------------
@app.route("/api/predict", methods=["POST"])
def receive_prediction():

    try:
        prediction_data = request.json

        socketio.emit("traffic_forecast", prediction_data)

        return jsonify({
            "status": "broadcast_complete",
            "data": prediction_data
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e),
            "message": "Prediction broadcast failed"
        }), 500


# ---------------------------------------------------
# Emergency Corridor System
# ---------------------------------------------------
@socketio.on("emergency_trigger")
def handle_emergency(data):

    ambulance = data.get("ambulance_id", "Unknown")

    print(f"🚑 EMERGENCY CORRIDOR ACTIVATED for {ambulance}")

    emit(
        "emergency_alert",
        {
            "msg": "Clear Lane 1 - Ambulance approaching",
            "ambulance": ambulance
        },
        broadcast=True
    )


# ---------------------------------------------------
# Backend Runner
# ---------------------------------------------------
if __name__ == "__main__":

    print("🚦 Smart City Backend Running...")
    print("📡 API running at: http://localhost:5000")
    print("🌍 Status API: http://localhost:5000/api/status")

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True
    )