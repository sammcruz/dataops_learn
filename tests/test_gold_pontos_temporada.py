import pandas as pd

from src.gold_pontos_temporada import build_gold_pontos_temporada
from tests import gold_data


def gerar():
    return build_gold_pontos_temporada(gold_data.fact_results(), gold_data.dim_race())


def test_colunas_e_ordem():
    assert list(gerar().columns) == ["season", "corridas", "pontos"]


def test_uma_linha_por_temporada():
    assert list(gerar()["season"]) == [2009, 2010]


def test_corridas_e_pontos():
    out = gerar().set_index("season")
    assert out.loc[2009, "corridas"] == 2
    assert out.loc[2009, "pontos"] == 24.0
    assert out.loc[2010, "corridas"] == 1
    assert out.loc[2010, "pontos"] == 10.0


def test_pontos_sao_decimais():
    assert pd.api.types.is_float_dtype(gerar()["pontos"])
