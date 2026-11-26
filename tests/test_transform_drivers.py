import datetime as dt
from pathlib import Path

import pandas as pd
import pytest

from src.transform_drivers import age_on, build_dim_driver

pytestmark = pytest.mark.skip(reason="Story 1: remova esta linha ao implementar")

DATA = Path(__file__).parent / "data"


def carregar():
    return pd.read_csv(DATA / "drivers_sample.csv", dtype=str, keep_default_na=False)


def test_colunas_e_ordem():
    out = build_dim_driver(carregar())
    assert list(out.columns) == [
        "driver_id", "driver_ref", "code", "full_name", "dob", "nationality", "number",
    ]


def test_uma_linha_por_piloto():
    out = build_dim_driver(carregar())
    assert len(out) == 4
    assert out["driver_id"].is_unique


def test_nome_completo_sem_espacos_sobrando():
    out = build_dim_driver(carregar()).set_index("driver_id")
    assert out.loc[1, "full_name"] == "Lewis Hamilton"
    assert out.loc[3, "full_name"] == "Max Verstappen"


def test_marcador_de_nulo_vira_nulo():
    out = build_dim_driver(carregar()).set_index("driver_id")
    assert pd.isna(out.loc[2, "number"])
    assert pd.isna(out.loc[4, "code"])


def test_tipos():
    out = build_dim_driver(carregar())
    assert str(out["driver_id"].dtype) == "Int64"
    assert str(out["number"].dtype) == "Int64"
    assert pd.api.types.is_datetime64_any_dtype(out["dob"])


def test_idade_completa():
    assert age_on(dt.date(1985, 1, 7), dt.date(2009, 3, 29)) == 24


def test_idade_antes_do_aniversario():
    assert age_on(dt.date(1985, 1, 7), dt.date(2009, 1, 6)) == 23


def test_idade_no_dia_do_aniversario():
    assert age_on(dt.date(1985, 1, 7), dt.date(2009, 1, 7)) == 24
