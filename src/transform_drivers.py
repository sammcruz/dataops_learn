"""Story 1 - Pilotos: dimensão `dim_driver`.

Entrada: DataFrame `drivers` como chega da bronze (tudo texto, com `\\N` como nulo).
"""

import pandas as pd

from src.common import clean_nulls  # noqa: F401  (use na sua implementação)


def build_dim_driver(drivers: pd.DataFrame) -> pd.DataFrame:
    """Monta a dimensão de pilotos.

    Colunas de saída, nesta ordem:
      driver_id (Int64), driver_ref, code, full_name, dob (data), nationality, number (Int64)

    Passo a passo:
      1. df = clean_nulls(drivers)            # `\\N` e vazio viram nulo
      2. df["full_name"] = df["forename"] + " " + df["surname"]
      3. df["driver_id"] = df["driverId"].astype("Int64")      # idem para number
      4. df["dob"] = pd.to_datetime(df["dob"])
      5. renomeie driverRef para driver_ref e devolva só as colunas pedidas, na ordem
    """
    raise NotImplementedError("Implemente build_dim_driver")
