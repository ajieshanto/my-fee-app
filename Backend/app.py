from flask import Flask, request, jsonify

app = Flask(__name__)

fees_data = []

@app.route("/api/CollectFee", methods=["POST"])
def collect_fee():
    data = request.get_json()
    fees_data.append(data)
    return jsonify({"status": "success", "data": data})

@app.route("/api/ViewFees", methods=["GET"])
def view_fees():
    student = request.args.get("student_name")
    month = request.args.get("month")
    results = fees_data
    if student:
        results = [f for f in results if f["student_name"] == student]
    if month:
        results = [f for f in results if f["month"] == month]
    return jsonify({"fees_records": results})

@app.route("/api/UpdateFee", methods=["POST"])
def update_fee():
    data = request.get_json()
    for f in fees_data:
        if f["student_name"] == data["student_name"] and f["month"] == data["month"]:
            f.update(data)
            return jsonify({"status": "updated", "data": f})
    return jsonify({"status": "error", "message": "Record not found"}), 404

@app.route("/api/DeleteFee", methods=["POST"])
def delete_fee():
    global fees_data
    data = request.get_json()
    fees_data = [f for f in fees_data if not (f["student_name"] == data["student_name"] and f["month"] == data["month"])]
    return jsonify({"status": "deleted"})
