"""Story 4 - Construtores (equipes): dimensão `dim_constructor`.

Entrada: DataFrame `constructors` como chega da bronze (tudo texto, com `\\N` como nulo).
"""

import pandas as pd

from src.common import clean_nulls  # noqa: F401  (use na sua implementação)


def build_dim_constructor(constructors: pd.DataFrame) -> pd.DataFrame:
    """Monta a dimensão de construtores.

    Colunas de saída, nesta ordem:
      constructor_id (Int64), constructor_ref, name, nationality

    Passo a passo:
      1. df = clean_nulls(constructors)
      2. Renomeie constructorId -> constructor_id e constructorRef -> constructor_ref
      3. df["constructor_id"] = df["constructor_id"].astype("Int64")
      4. Devolva só as colunas pedidas, na ordem
    """
    raise NotImplementedError("Implemente build_dim_constructor")
