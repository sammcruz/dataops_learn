"""Gold 2 - Posições ganhas por piloto: tabela `gold_posicoes_ganhas`.

Entradas: `fact_results` (silver_fact_results) e `dim_driver` (silver_dim_driver).
"""

import pandas as pd


def build_gold_posicoes_ganhas(
    fact_results: pd.DataFrame, dim_driver: pd.DataFrame
) -> pd.DataFrame:
    """Soma as posições ganhas na corrida (largada menos chegada) de cada piloto.

    Colunas de saída, nesta ordem: driver_id, full_name, corridas, posicoes_ganhas

    Passo a passo:
      1. Agrupe por piloto, contando e somando a coluna positions_gained:
         fact_results.groupby("driver_id").agg(corridas=("positions_gained", "count"),
                                               posicoes_ganhas=("positions_gained", "sum"))
         (o count e o sum ignoram os nulos sozinhos; use .reset_index() no final)
      2. Fique só com quem tem corridas > 0
      3. Traga o nome com merge: dim_driver[["driver_id", "full_name"]], on="driver_id"
      4. corridas e posicoes_ganhas como Int64
      5. Ordene por posicoes_ganhas (maior primeiro) e depois por full_name
      6. Devolva só as colunas pedidas, na ordem, com reset_index(drop=True)
    """
    df = (
        fact_results.groupby("driver_id")
        .agg(
            corridas=("positions_gained", "count"),
            posicoes_ganhas=("positions_gained", "sum")
        )
        .reset_index()
    )

    df = df[df["corridas"] > 0]

    df = df.merge(
        dim_driver[["driver_id", "full_name"]],
        on="driver_id",
        how="left"
    )

    df["corridas"] = df["corridas"].astype("Int64")
    df["posicoes_ganhas"] = df["posicoes_ganhas"].astype("Int64")

    df = df.sort_values(
        by=["posicoes_ganhas", "full_name"],
        ascending=[False, True]
    )

    return df[
        ["driver_id", "full_name", "corridas", "posicoes_ganhas"]
    ].reset_index(drop=True)

    raise NotImplementedError("Implemente build_gold_posicoes_ganhas")
