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

        if not all([student_name, month]):
            return func.HttpResponse("Missing required fields: student_name or month", status_code=400)

        new_data = [record for record in data if not (record.get("student_name") == student_name and record.get("month") == month)]

        if len(new_data) == len(data):
            return func.HttpResponse("Record not found", status_code=404)

        with open(data_file, "w") as f:
            json.dump(new_data, f, indent=4)

        return func.HttpResponse(
            json.dumps({"message": "Fee record deleted successfully!"}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
