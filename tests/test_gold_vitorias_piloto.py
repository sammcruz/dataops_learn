
from src.gold_vitorias_piloto import build_gold_vitorias_piloto
from tests import gold_data


def gerar():
    return build_gold_vitorias_piloto(gold_data.fact_results(), gold_data.dim_driver())


def test_colunas_e_ordem():
    assert list(gerar().columns) == ["driver_id", "full_name", "vitorias"]


def test_so_pilotos_com_vitoria():
    assert len(gerar()) == 2


def test_contagem_e_ordem():
    out = gerar()
    assert out.loc[0, "full_name"] == "Lewis Hamilton"
    assert out.loc[0, "vitorias"] == 2
    assert out.loc[1, "full_name"] == "Nick Heidfeld"
    assert out.loc[1, "vitorias"] == 1
