import io
import json
import os
import time

import pandas as pd
from azure.storage.blob import BlobServiceClient

NUMERIC_COLS = ["Protein(g)", "Carbs(g)", "Fat(g)"]


def load_dataset_from_blob() -> tuple[pd.DataFrame, str]:
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("DATASET_CONTAINER")
    blob_name = os.getenv("DATASET_BLOB_NAME", "All_Diets.csv")

    if not connection_string or not container_name:
        raise ValueError(
            "Missing required environment settings: "
            "AZURE_STORAGE_CONNECTION_STRING and DATASET_CONTAINER."
        )

    blob_client = BlobServiceClient.from_connection_string(connection_string).get_blob_client(
        container=container_name,
        blob=blob_name,
    )
    csv_bytes = blob_client.download_blob().readall()
    return pd.read_csv(io.BytesIO(csv_bytes)), blob_name


def clean_and_aggregate(df: pd.DataFrame, diet_filter: str = "all") -> tuple[pd.DataFrame, list[dict]]:
    if "Diet_type" not in df.columns:
        raise ValueError("Dataset missing required column: Diet_type")

    df[NUMERIC_COLS] = df[NUMERIC_COLS].apply(pd.to_numeric, errors="coerce")
    df[NUMERIC_COLS] = df[NUMERIC_COLS].fillna(df[NUMERIC_COLS].mean())

    if diet_filter.lower() != "all":
        df = df[df["Diet_type"].astype(str).str.lower() == diet_filter.lower()]

    grouped = df.groupby("Diet_type")[NUMERIC_COLS].mean().reset_index().round(2)
    return df, grouped.to_dict(orient="records")


def build_response_payload(
    filtered_df: pd.DataFrame,
    records: list[dict],
    source_blob: str,
    started_at: float,
) -> dict:
    execution_time_ms = round((time.perf_counter() - started_at) * 1000, 2)
    return {
        "metadata": {
            "execution_time_ms": execution_time_ms,
            "record_count": int(len(filtered_df)),
            "diet_count": int(filtered_df["Diet_type"].nunique()),
            "dataset_blob": source_blob,
        },
        "data": records,
    }


def run_task_3_simulation() -> None:
    """Local/CI simulation so this script still runs outside Azure."""
    started_at = time.perf_counter()
    print("--- Task 3: Nutritional Analysis Simulation ---")

    input_file = "data/All_Diets.csv"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found in current directory.")
        return

    df = pd.read_csv(input_file)
    filtered_df, records = clean_and_aggregate(df, diet_filter="all")
    payload = build_response_payload(
        filtered_df,
        records,
        source_blob=input_file,
        started_at=started_at,
    )

    print("Success: Local simulation completed.")
    print(json.dumps(payload, indent=2)[:1500])


if __name__ == "__main__":
    run_task_3_simulation()