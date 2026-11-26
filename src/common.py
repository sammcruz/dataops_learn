"""Funções de apoio compartilhadas (já prontas e testadas).

A bronze guarda tudo como texto, e o dataset de F1 usa o texto `\\N` para representar nulo.
Estas funções são o ponto de partida das transformações da silver.
"""

import pandas as pd

NULL_MARKER = "\\N"


def clean_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Remove espaços nas pontas dos textos e troca `\\N` e texto vazio por nulo.

    Não altera o DataFrame recebido: devolve uma cópia.
    """
    out = df.copy()
    for col in out.columns:
        out[col] = out[col].map(_clean_value)
    return out


def _clean_value(value):
    if not isinstance(value, str):
        return value
    stripped = value.strip()
    if stripped == "" or stripped == NULL_MARKER:
        return pd.NA
    return stripped
