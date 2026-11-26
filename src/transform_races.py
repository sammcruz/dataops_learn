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

    Passo a passo:
      1. races = clean_nulls(races) e circuits = clean_nulls(circuits)
      2. Renomeie as colunas ANTES do join, para os dois `name` não se misturarem:
         races.rename(columns={"raceId": "race_id", "year": "season", "name": "race_name",
                               "date": "race_date", "circuitId": "circuit_id"})
         circuits.rename(columns={"circuitId": "circuit_id", "name": "circuit_name",
                                  "location": "city"})
      3. df = races.merge(circuits, on="circuit_id", how="left")   # how="left" mantém tudo
      4. Converta os tipos: ids, season e round com astype("Int64"),
         race_date com pd.to_datetime, lat e lng com astype(float)
      5. Devolva só as colunas pedidas, na ordem
    """
    raise NotImplementedError("Implemente build_dim_race")
