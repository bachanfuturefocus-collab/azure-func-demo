# HttpTrigger/__init__.py
import logging
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger processed a request.")

    try:
        data = req.get_json()
    except ValueError:
        data = None

    name = data.get("name") if data else req.params.get("name")
    if not name:
        return func.HttpResponse(
            json.dumps({"error": "Please pass a name in JSON body or ?name="}),
            status_code=400,
            mimetype="application/json"
        )

    resp = {"message": f"Hello, {name}!"}
    return func.HttpResponse(
        json.dumps(resp),
        status_code=200,
        mimetype="application/json"
    )
