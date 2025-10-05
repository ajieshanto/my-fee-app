import azure.functions as func
import json
import os
from datetime import datetime

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        student_name = req_body.get("student_name")
        month = req_body.get("month")
        amount = req_body.get("amount")
        payment_mode = req_body.get("payment_mode", "Cash")

        if not all([student_name, month, amount]):
            return func.HttpResponse(
                "Missing required fields: student_name, month, amount",
                status_code=400
            )

        fee_record = {
            "student_name": student_name,
            "month": month,
            "amount": amount,
            "payment_mode": payment_mode,
            "date_collected": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        data_file = os.path.join(os.path.dirname(__file__), "fees_data.json")

        if os.path.exists(data_file):
            with open(data_file, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(fee_record)

        with open(data_file, "w") as f:
            json.dump(data, f, indent=4)

        return func.HttpResponse(
            json.dumps({"message": "Fee recorded successfully!", "record": fee_record}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
 