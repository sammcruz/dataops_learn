"""Gold 3 - Pontos por temporada: tabela `gold_pontos_temporada`.

Entradas: `fact_results` (silver_fact_results) e `dim_race` (silver_dim_race).
"""

import pandas as pd


def build_gold_pontos_temporada(
    fact_results: pd.DataFrame, dim_race: pd.DataFrame
) -> pd.DataFrame:
    """Conta as corridas e soma os pontos distribuídos em cada temporada.

    Colunas de saída, nesta ordem: season, corridas (Int64), pontos (float)

    Passo a passo:
      1. Traga a temporada de cada resultado:
         fact_results.merge(dim_race[["race_id", "season"]], on="race_id")
      2. Agrupe por temporada:
         .groupby("season").agg(corridas=("race_id", "nunique"), pontos=("points", "sum"))
         e use .reset_index() no final
      3. corridas como Int64 e pontos como float
      4. Ordene por season, da mais antiga para a mais recente
      5. Devolva só as colunas pedidas, na ordem, com reset_index(drop=True)
    """

    #1. Trazer a temporada de cada resultado com um merge (dim_race e race_id)
    df = fact_results.merge(dim_race[["race_id", "season"]], on="race_id")

    #2. Agrupar por temporada (número de corridas e soma dos pontos)
    df = (
        df.groupby("season")
        .agg(corridas=("race_id", "nunique"), pontos=("points", "sum"))
        .reset_index()
    )

    #3. Ordenar da temporada mais antiga à mais recente
    df["corridas"] = df["corridas"].astype("Int64")
    df["pontos"] = df["pontos"].astype(float)
    df = df.sort_values("season")

    return df[["season", "corridas", "pontos"]].reset_index(drop=True)
