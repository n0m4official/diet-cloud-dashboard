import json
import time

import azure.functions as func

from lambda_function import build_response_payload, clean_and_aggregate, load_dataset_from_blob

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="analyze", methods=["GET"])
def analyze(req: func.HttpRequest) -> func.HttpResponse:
    started_at = time.perf_counter()

    try:
        diet_filter = req.params.get("diet", "all")
        df, blob_name = load_dataset_from_blob()
        filtered_df, records = clean_and_aggregate(df, diet_filter=diet_filter)
        payload = build_response_payload(
            filtered_df,
            records,
            source_blob=blob_name,
            started_at=started_at,
        )
        return func.HttpResponse(
            json.dumps(payload),
            status_code=200,
            mimetype="application/json",
        )
    except Exception as exc:
        error_payload = {"error": str(exc)}
        return func.HttpResponse(
            json.dumps(error_payload),
            status_code=500,
            mimetype="application/json",
        )
