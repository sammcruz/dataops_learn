import pandas as pd

from src.common import clean_nulls


def test_clean_nulls_troca_marcador_e_vazio_por_nulo():
    df = pd.DataFrame({"a": ["\\N", "", "x"]})
    out = clean_nulls(df)
    assert out["a"].isna().tolist() == [True, True, False]


def test_clean_nulls_remove_espacos_das_pontas():
    df = pd.DataFrame({"a": ["  ola ", "tchau"]})
    assert clean_nulls(df)["a"].tolist() == ["ola", "tchau"]


def test_clean_nulls_nao_altera_o_original():
    df = pd.DataFrame({"a": [" x "]})
    clean_nulls(df)
    assert df["a"].iloc[0] == " x "
