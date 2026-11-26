"""Story 1 - Pilotos: dimensão `dim_driver`.

Entrada: DataFrame `drivers` como chega da bronze (tudo texto, com `\\N` como nulo).
Use `src.common.clean_nulls` como primeiro passo.
"""

import pandas as pd

from src.common import clean_nulls  # noqa: F401  (use na sua implementação)


def build_dim_driver(drivers: pd.DataFrame) -> pd.DataFrame:
    """Monta a dimensão de pilotos.

    Colunas de saída, nesta ordem:
      driver_id (Int64), driver_ref, code, full_name, dob (data), nationality, number (Int64)

    Regras:
      - `\\N` e texto vazio viram nulo
      - full_name = nome + " " + sobrenome, sem espaços sobrando
      - dob vira data
      - number vira inteiro (nulo quando não existe)
    """
    raise NotImplementedError("Implemente build_dim_driver")


def age_on(dob, ref_date) -> int:
    """Idade em anos completos de quem nasceu em `dob`, na data `ref_date`.

    Exemplo: nascido em 1985-01-07, em 2009-03-29, tem 24 anos.
    Atenção ao aniversário que ainda não aconteceu no ano.
    """
    raise NotImplementedError("Implemente age_on")
