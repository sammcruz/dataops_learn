"""Gold 1 - Vitórias por piloto: tabela `gold_vitorias_piloto`.

Entradas: `fact_results` (silver_fact_results) e `dim_driver` (silver_dim_driver).
Os dados já vêm limpos e com os tipos certos da camada silver.
"""

import pandas as pd


def build_gold_vitorias_piloto(
    fact_results: pd.DataFrame, dim_driver: pd.DataFrame
) -> pd.DataFrame:

    # 1. só as vitórias
    venceu = fact_results[fact_results["finish_position"] == 1]

    # 2. contar por piloto
    vitorias = venceu.groupby("driver_id").size().rename("vitorias").reset_index()

    # 3. trazer o nome
    df = vitorias.merge(dim_driver[["driver_id", "full_name"]], on="driver_id")

    # 4. tipo
    df["vitorias"] = df["vitorias"].astype("Int64")

    # 5. ordenar: mais vitórias primeiro, desempate por nome
    df = df.sort_values(["vitorias", "full_name"], ascending=[False, True])

    # 6. colunas pedidas, na ordem
    return df[["driver_id", "full_name", "vitorias"]].reset_index(drop=True)