"""Story 3 - Resultados: fato `fact_results`.

Entrada: DataFrames `results` e `status` como chegam da bronze (tudo texto, `\\N` como nulo).
"""

import pandas as pd
from src.common import clean_nulls

def build_fact_results(results: pd.DataFrame, status: pd.DataFrame) -> pd.DataFrame:
    r = clean_nulls(results).rename(
        columns={
            "resultId": "result_id",
            "raceId": "race_id",
            "driverId": "driver_id",
            "constructorId": "constructor_id",
            "position": "finish_position",
        }
    )
    s = clean_nulls(status)

    for col in ["result_id", "race_id", "driver_id", "constructor_id", "grid", "finish_position"]:
        r[col] = r[col].astype("Int64")
    r["points"] = r["points"].astype(float)

    # grid 0 = largada dos boxes: não conta como posição
    r["positions_gained"] = (r["grid"] - r["finish_position"]).where(r["grid"] > 0)

    df = r.merge(s, on="statusId", how="left")

    return df[
        [
            "result_id", "race_id", "driver_id", "constructor_id", "grid",
            "finish_position", "positions_gained", "points", "status",
        ]
    ]
