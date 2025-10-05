import logging
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing a fee collection request.')

    try:
        # Parse JSON from request
        req_body = req.get_json()
        student_name = req_body.get("student_name")
        amount = req_body.get("amount")

        if not student_name or not amount:
            return func.HttpResponse(
                json.dumps({"error": "Missing student_name or amount"}),
                status_code=400,
                mimetype="application/json"
            )

        # Here you could save the data locally or to a database
        response = {
            "message": f"Fee collected successfully for {student_name}",
            "amount": amount
        }

        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
            mimetype="application/json"
        )

    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON"}),
            status_code=400,
            mimetype="application/json"
        )
