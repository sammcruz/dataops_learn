"""Story 2 - Corridas e circuitos: dimensão `dim_race`.

Entrada: DataFrames `races` e `circuits` como chegam da bronze (tudo texto, `\\N` como nulo).
"""

import pandas as pd

from src.common import clean_nulls  # noqa: F401  (use na sua implementação)


def build_dim_race(races: pd.DataFrame, circuits: pd.DataFrame) -> pd.DataFrame:
    """Monta a dimensão de corridas, já com os dados do circuito.

    Colunas de saída, nesta ordem:
      race_id (Int64), season (Int64), round (Int64), race_name, race_date (data),
      circuit_id (Int64), circuit_name, city, country, lat (float), lng (float)
    """
    # 1. limpar nulos
    races = clean_nulls(races)
    circuits = clean_nulls(circuits)

    # 2. renomear antes do join
    races = races.rename(columns={"raceId": "race_id", "year": "season", "name": "race_name",
                                  "date": "race_date", "circuitId": "circuit_id"})
    circuits = circuits.rename(columns={"circuitId": "circuit_id", "name": "circuit_name",
                                        "location": "city"})

    # 3. juntar
    df = races.merge(circuits, on="circuit_id", how="left")

    # 4. tipos
    df = df.astype({"race_id": "Int64", "season": "Int64", "round": "Int64",
                    "circuit_id": "Int64", "lat": float, "lng": float})
    df["race_date"] = pd.to_datetime(df["race_date"])

    # 5. colunas pedidas, na ordem
    return df[["race_id", "season", "round", "race_name", "race_date",
               "circuit_id", "circuit_name", "city", "country", "lat", "lng"]]
