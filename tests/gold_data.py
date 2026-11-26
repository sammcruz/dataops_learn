"""Amostras pequenas no formato da silver, usadas pelos testes da gold."""

import pandas as pd


def fact_results():
    df = pd.DataFrame(
        {
            "result_id": [1, 2, 3, 4, 5],
            "race_id": [1, 1, 2, 2, 3],
            "driver_id": [1, 2, 2, 1, 1],
            "constructor_id": [1, 2, 2, 1, 1],
            "grid": [1, 5, 3, 0, 2],
            "finish_position": [1, pd.NA, 1, 3, 1],
            "positions_gained": [0, pd.NA, 2, pd.NA, 1],
            "points": [10.0, 0.0, 10.0, 4.0, 10.0],
            "status": ["Finished", "Engine", "Finished", "Finished", "Finished"],
        }
    )
    for col in ["result_id", "race_id", "driver_id", "constructor_id", "grid",
                "finish_position", "positions_gained"]:
        df[col] = df[col].astype("Int64")
    return df


def dim_driver():
    return pd.DataFrame(
        {
            "driver_id": pd.array([1, 2, 3], dtype="Int64"),
            "full_name": ["Lewis Hamilton", "Nick Heidfeld", "Max Verstappen"],
        }
    )


def dim_race():
    return pd.DataFrame(
        {
            "race_id": pd.array([1, 2, 3], dtype="Int64"),
            "season": pd.array([2009, 2009, 2010], dtype="Int64"),
        }
    )
