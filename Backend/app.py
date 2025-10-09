from flask import Flask, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)

# Path to your data file
DATA_FILE = os.path.join(os.path.dirname(__file__), "FeeCollectionAPI", "CollectFee", "fees_data.json")


# --- Helper function ---
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# --- API ROUTES ---

@app.route("/")
def home():
    return "Fee Collection API is running 🚀"


# Collect Fee (POST)
@app.route("/CollectFee", methods=["POST"])
def collect_fee():
    try:
        data = request.get_json()
        fees = load_data()

        data["id"] = len(fees) + 1
        data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fees.append(data)

        save_data(fees)
        return jsonify({"message": "Fee collected successfully", "data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# View Fees (GET)
@app.route("/ViewFees", methods=["GET"])
def view_fees():
    try:
        fees = load_data()
        return jsonify(fees), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update Fee (PUT)
@app.route("/UpdateFee/<int:fee_id>", methods=["PUT"])
def update_fee(fee_id):
    try:
        data = request.get_json()
        fees = load_data()

        for fee in fees:
            if fee["id"] == fee_id:
                fee.update(data)
                save_data(fees)
                return jsonify({"message": "Fee updated successfully", "data": fee}), 200

        return jsonify({"message": "Fee not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Delete Fee (DELETE)
@app.route("/DeleteFee/<int:fee_id>", methods=["DELETE"])
def delete_fee(fee_id):
    try:
        fees = load_data()
        updated_fees = [fee for fee in fees if fee["id"] != fee_id]

        if len(fees) == len(updated_fees):
            return jsonify({"message": "Fee not found"}), 404

        save_data(updated_fees)
        return jsonify({"message": "Fee deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
