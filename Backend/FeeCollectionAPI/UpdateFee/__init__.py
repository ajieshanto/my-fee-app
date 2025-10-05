import azure.functions as func
import json
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Path to fees_data.json
        data_file = os.path.join(os.path.dirname(__file__), "../CollectFee/fees_data.json")

        if os.path.exists(data_file):
            with open(data_file, "r") as f:
                data = json.load(f)
        else:
            data = []

        req_body = req.get_json()
        student_name = req_body.get("student_name")
        month = req_body.get("month")
        new_amount = req_body.get("amount")
        new_payment_mode = req_body.get("payment_mode")

        if not all([student_name, month]):
            return func.HttpResponse("Missing required fields: student_name or month", status_code=400)

        updated = False
        for record in data:
            if record.get("student_name") == student_name and record.get("month") == month:
                if new_amount:
                    record["amount"] = new_amount
                if new_payment_mode:
                    record["payment_mode"] = new_payment_mode
                updated = True
                break

        if not updated:
            return func.HttpResponse("Record not found", status_code=404)

        with open(data_file, "w") as f:
            json.dump(data, f, indent=4)

        return func.HttpResponse(
            json.dumps({"message": "Fee record updated successfully!", "record": record}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
