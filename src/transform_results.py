"""Story 3 - Resultados: fato `fact_results`.

Entrada: DataFrames `results` e `status` como chegam da bronze (tudo texto, `\\N` como nulo).
"""

import pandas as pd

from src.common import clean_nulls  # noqa: F401  (use na sua implementação)


def lap_time_to_ms(value) -> "int | None":
    """Converte o tempo de volta em milissegundos.

    Exemplos: "1:27.452" -> 87452 ; "59.900" -> 59900 ; "\\N", "" ou nulo -> None
    """
    raise NotImplementedError("Implemente lap_time_to_ms")


def build_fact_results(results: pd.DataFrame, status: pd.DataFrame) -> pd.DataFrame:
    """Monta a tabela de fatos de resultados.

    Colunas de saída, nesta ordem:
      result_id, race_id, driver_id, constructor_id, grid, finish_position, positions_gained,
      points (float), laps, status, is_finished (bool), fastest_lap_ms
      (as colunas de identificação, grid, finish_position, positions_gained, laps e
       fastest_lap_ms são Int64, com nulo quando não houver valor)

    Regras:
      - finish_position vem de `position` (nulo quando o piloto não terminou)
      - positions_gained = grid - finish_position, só quando grid > 0 e há finish_position
        (grid 0 significa largada dos boxes: nulo)
      - status vem do join com a tabela `status` pelo statusId
      - is_finished é verdadeiro quando status é "Finished" ou começa com "+" (voltas atrás)
      - fastest_lap_ms usa lap_time_to_ms sobre `fastestLapTime`
    """
    raise NotImplementedError("Implemente build_fact_results")
