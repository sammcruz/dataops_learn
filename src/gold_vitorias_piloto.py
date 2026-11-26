"""Gold 1 - Vitórias por piloto: tabela `gold_vitorias_piloto`.

Entradas: `fact_results` (silver_fact_results) e `dim_driver` (silver_dim_driver).
Os dados já vêm limpos e com os tipos certos da camada silver.
"""

import pandas as pd


def build_gold_vitorias_piloto(
    fact_results: pd.DataFrame, dim_driver: pd.DataFrame
) -> pd.DataFrame:
    """Conta quantas corridas cada piloto venceu.

    Colunas de saída, nesta ordem: driver_id, full_name, vitorias (Int64)

    Passo a passo:
      1. Fique só com as vitórias: venceu = fact_results[fact_results["finish_position"] == 1]
      2. Conte por piloto: venceu.groupby("driver_id").size().rename("vitorias").reset_index()
      3. Traga o nome com merge: dim_driver[["driver_id", "full_name"]], on="driver_id"
      4. vitorias como Int64
      5. Ordene por vitorias (maior primeiro) e depois por full_name:
         sort_values(["vitorias", "full_name"], ascending=[False, True])
      6. Devolva só as colunas pedidas, na ordem, com reset_index(drop=True)
    Só aparecem pilotos com pelo menos uma vitória.
    """
    raise NotImplementedError("Implemente build_gold_vitorias_piloto")
