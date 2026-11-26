from pathlib import Path

import pandas as pd
import pytest

from src.transform_results import build_fact_results, lap_time_to_ms

pytestmark = pytest.mark.skip(reason="Story 3: remova esta linha ao implementar")

DATA = Path(__file__).parent / "data"


def carregar():
    kw = dict(dtype=str, keep_default_na=False)
    return (
        pd.read_csv(DATA / "results_sample.csv", **kw),
        pd.read_csv(DATA / "status_sample.csv", **kw),
    )


def test_tempo_de_volta_com_minutos():
    assert lap_time_to_ms("1:27.452") == 87452


def test_tempo_de_volta_so_segundos():
    assert lap_time_to_ms("59.900") == 59900


@pytest.mark.parametrize("valor", ["\\N", "", None])
def test_tempo_de_volta_ausente(valor):
    assert lap_time_to_ms(valor) is None


def test_colunas_e_ordem():
    out = build_fact_results(*carregar())
    assert list(out.columns) == [
        "result_id", "race_id", "driver_id", "constructor_id", "grid", "finish_position",
        "positions_gained", "points", "laps", "status", "is_finished", "fastest_lap_ms",
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


def test_status_e_flag_de_terminou():
    out = build_fact_results(*carregar()).set_index("result_id")
    assert out.loc[1, "status"] == "Finished" and bool(out.loc[1, "is_finished"])
    assert out.loc[2, "status"] == "Engine" and not bool(out.loc[2, "is_finished"])
    assert out.loc[5, "status"] == "+1 Lap" and bool(out.loc[5, "is_finished"])


def test_melhor_volta_em_milissegundos():
    out = build_fact_results(*carregar()).set_index("result_id")
    assert out.loc[1, "fastest_lap_ms"] == 87452
    assert out.loc[4, "fastest_lap_ms"] == 59900
    assert pd.isna(out.loc[2, "fastest_lap_ms"])


def test_pontos_sao_decimais():
    out = build_fact_results(*carregar())
    assert pd.api.types.is_float_dtype(out["points"])
