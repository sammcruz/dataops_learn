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

    Regras:
      - `\\N` e texto vazio viram nulo
      - season vem de `year`, race_name vem de `name` da corrida, city vem de `location`
      - circuit_name vem de `name` do circuito
      - mantenha todas as corridas, mesmo as sem circuito correspondente (left join)
    """
    raise NotImplementedError("Implemente build_dim_race")
