from pathlib import Path

import pandas as pd
import pytest

from src.transform_constructors import build_dim_constructor

DATA = Path(__file__).parent / "data"


def carregar():
    return pd.read_csv(DATA / "constructors_sample.csv", dtype=str, keep_default_na=False)


def test_colunas_e_ordem():
    out = build_dim_constructor(carregar())
    assert list(out.columns) == ["constructor_id", "constructor_ref", "name", "nationality"]


def test_uma_linha_por_construtor():
    out = build_dim_constructor(carregar())
    assert len(out) == 4
    assert out["constructor_id"].is_unique


def test_espacos_sobrando_sao_removidos():
    out = build_dim_constructor(carregar()).set_index("constructor_id")
    assert out.loc[3, "name"] == "Ferrari"


def test_marcador_de_nulo_vira_nulo():
    out = build_dim_constructor(carregar()).set_index("constructor_id")
    assert pd.isna(out.loc[4, "nationality"])


def test_id_e_inteiro():
    out = build_dim_constructor(carregar())
    assert str(out["constructor_id"].dtype) == "Int64"
