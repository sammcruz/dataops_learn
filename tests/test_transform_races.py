from pathlib import Path

import pandas as pd
import pytest

from src.transform_races import build_dim_race



DATA = Path(__file__).parent / "data"


def carregar():
    kw = dict(dtype=str, keep_default_na=False)
    return (
        pd.read_csv(DATA / "races_sample.csv", **kw),
        pd.read_csv(DATA / "circuits_sample.csv", **kw),
    )


def test_colunas_e_ordem():
    out = build_dim_race(*carregar())
    assert list(out.columns) == [
        "race_id", "season", "round", "race_name", "race_date",
        "circuit_id", "circuit_name", "city", "country", "lat", "lng",
    ]


def test_mantem_todas_as_corridas():
    out = build_dim_race(*carregar())
    assert len(out) == 3


def test_traz_dados_do_circuito():
    out = build_dim_race(*carregar()).set_index("race_id")
    assert out.loc[1, "circuit_name"] == "Albert Park Grand Prix Circuit"
    assert out.loc[2, "city"] == "Kuala Lumpur"
    assert out.loc[2, "country"] == "Malaysia"


def test_corrida_sem_circuito_fica_com_nulos():
    out = build_dim_race(*carregar()).set_index("race_id")
    assert pd.isna(out.loc[3, "circuit_name"])
    assert pd.isna(out.loc[3, "lat"])


def test_tipos():
    out = build_dim_race(*carregar())
    assert str(out["race_id"].dtype) == "Int64"
    assert str(out["season"].dtype) == "Int64"
    assert pd.api.types.is_datetime64_any_dtype(out["race_date"])
    assert pd.api.types.is_float_dtype(out["lat"])


def test_temporada_vem_do_ano():
    out = build_dim_race(*carregar()).set_index("race_id")
    assert out.loc[1, "season"] == 2009
    assert out.loc[3, "season"] == 2010
