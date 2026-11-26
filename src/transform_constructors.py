"""Story 4 - Construtores (equipes): dimensão `dim_constructor`.

Entrada: DataFrame `constructors` como chega da bronze (tudo texto, com `\\N` como nulo).
"""

import pandas as pd

from src.common import clean_nulls  # noqa: F401  (use na sua implementação)


def build_dim_constructor(constructors: pd.DataFrame) -> pd.DataFrame:
  #1. Limpar os nulos
  df = clean_nulls(constructors)

  #2. Renomear constructorId e constructorRef
  df = df.rename(columns={"constructorId": "constructor_id", "constructorRef": "constructor_ref"})

  #3. Converter o constructor_id para Int64
  df["constructor_id"] = df["constructor_id"].astype("Int64")

  #3.1. Pôr nationality mais bonita
  df["nationality"] = df["nationality"].str.upper()

  #4. Devolver as colunas constructor_id, constructor_ref, name, nationality
  return df[["constructor_id", "constructor_ref", "name", "nationality"]]
