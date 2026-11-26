"""Story 3 - Resultados: fato `fact_results`.

Entrada: DataFrames `results` e `status` como chegam da bronze (tudo texto, `\\N` como nulo).
"""

import pandas as pd

from src.common import clean_nulls  # noqa: F401  (use na sua implementação)


def build_fact_results(results: pd.DataFrame, status: pd.DataFrame) -> pd.DataFrame:
    """Monta a tabela de fatos de resultados.

    Colunas de saída, nesta ordem:
      result_id, race_id, driver_id, constructor_id, grid, finish_position,
      positions_gained (todas Int64), points (float), status (texto)

    Passo a passo:
      1. results = clean_nulls(results) e status = clean_nulls(status)
      2. Renomeie: resultId -> result_id, raceId -> race_id, driverId -> driver_id,
         constructorId -> constructor_id, position -> finish_position
      3. Converta result_id, race_id, driver_id, constructor_id, grid e finish_position
         com astype("Int64") e points com astype(float)
      4. positions_gained = grid - finish_position
         MAS grid 0 significa largada dos boxes: nesse caso deixe nulo.
         Dica: df["positions_gained"] = df["positions_gained"].where(df["grid"] > 0)
         (quem não terminou já fica nulo sozinho, porque finish_position é nulo)
      5. Junte com `status` pelo statusId (how="left") para trazer o texto da coluna `status`
      6. Devolva só as colunas pedidas, na ordem
    """
    raise NotImplementedError("Implemente build_fact_results")
