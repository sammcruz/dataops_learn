from pathlib import Path

import pandas as pd
import pytest

from src.transform_results import build_fact_results

pytestmark = pytest.mark.skip(reason="Story 3: remova esta linha ao implementar")

DATA = Path(__file__).parent / "data"


def carregar():
    kw = dict(dtype=str, keep_default_na=False)
    return (
        pd.read_csv(DATA / "results_sample.csv", **kw),
        pd.read_csv(DATA / "status_sample.csv", **kw),
    )


def test_colunas_e_ordem():
    out = build_fact_results(*carregar())
    assert list(out.columns) == [
        "result_id", "race_id", "driver_id", "constructor_id", "grid", "finish_position",
        "positions_gained", "points", "status",
    ]


def test_uma_linha_por_resultado():
    out = build_fact_results(*carregar())
    assert len(out) == 5
    assert out["result_id"].is_unique


def test_posicoes_ganhas():
    out = build_fact_results(*carregar()).set_index("result_id")
    assert out.loc[1, "positions_gained"] == 0   # largou em 1o, chegou em 1o
    assert out.loc[4, "positions_gained"] == 1   # largou em 3o, chegou em 2o
    assert out.loc[5, "positions_gained"] == 1   # largou em 10o, chegou em 9o


def test_largada_dos_boxes_nao_tem_posicoes_ganhas():
    out = build_fact_results(*carregar()).set_index("result_id")
    assert pd.isna(out.loc[3, "positions_gained"])   # grid 0


def test_quem_nao_terminou_nao_tem_posicao_final():
    out = build_fact_results(*carregar()).set_index("result_id")
    assert pd.isna(out.loc[2, "finish_position"])
    assert pd.isna(out.loc[2, "positions_gained"])


def test_status_vem_do_join():
    out = build_fact_results(*carregar()).set_index("result_id")
    assert out.loc[1, "status"] == "Finished"
    assert out.loc[2, "status"] == "Engine"
    assert out.loc[5, "status"] == "+1 Lap"


def test_pontos_sao_decimais():
    out = build_fact_results(*carregar())
    assert pd.api.types.is_float_dtype(out["points"])
