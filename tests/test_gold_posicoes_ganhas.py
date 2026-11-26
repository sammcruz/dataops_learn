import pytest

from src.gold_posicoes_ganhas import build_gold_posicoes_ganhas
from tests import gold_data

pytestmark = pytest.mark.skip(reason="Gold 2: remova esta linha ao implementar")


def gerar():
    return build_gold_posicoes_ganhas(gold_data.fact_results(), gold_data.dim_driver())


def test_colunas_e_ordem():
    assert list(gerar().columns) == ["driver_id", "full_name", "corridas", "posicoes_ganhas"]


def test_soma_ignora_nulos():
    out = gerar().set_index("driver_id")
    assert out.loc[1, "posicoes_ganhas"] == 1
    assert out.loc[1, "corridas"] == 2
    assert out.loc[2, "posicoes_ganhas"] == 2
    assert out.loc[2, "corridas"] == 1


def test_maior_saldo_primeiro():
    assert gerar().loc[0, "full_name"] == "Nick Heidfeld"
