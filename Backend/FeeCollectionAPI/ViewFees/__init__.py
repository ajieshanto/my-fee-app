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

        # Get query parameters
        student_name = req.params.get("student_name")
        month = req.params.get("month")

        # Filter if parameters provided
        if student_name:
            data = [record for record in data if record.get("student_name") == student_name]
        if month:
            data = [record for record in data if record.get("month") == month]

        return func.HttpResponse(
            json.dumps({"fees_records": data}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
