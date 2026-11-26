# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# MAGIC %md
# MAGIC # 03. Camada gold
# MAGIC
# MAGIC Cada seção usa a função gold que uma pessoa implementou em `src/`. Rode antes o `02_transformacoes`
# MAGIC (as silvers precisam existir) e depois rode a sua seção.
# MAGIC
# MAGIC As funções recebem DataFrames pandas (as tabelas de F1 são pequenas). Os testes automáticos
# MAGIC do GitHub usam as mesmas funções com amostras em `tests/data/`.

# COMMAND ----------

import os
import sys

# Torna a raiz do repositório (Git folder) importável: `from src... import ...`
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), "..")))

dbutils.widgets.text("catalogo", "dataops_learn", "Catálogo")
dbutils.widgets.text("schema", "f1", "Schema")
CATALOGO = dbutils.widgets.get("catalogo")
SCHEMA = dbutils.widgets.get("schema")

try:
    spark.sql(f"DESCRIBE SCHEMA {CATALOGO}.{SCHEMA}")
except Exception:
    CATALOGO = "workspace"


def ler(nome):
    return spark.table(f"{CATALOGO}.{SCHEMA}.silver_{nome}").toPandas()


def gravar(pdf, nome):
    # Nulos do pandas (pd.NA, NaN) viram None, que o Spark entende
    limpo = pdf.astype(object).where(pdf.notna(), None)
    destino = f"{CATALOGO}.{SCHEMA}.{nome}"
    spark.createDataFrame(limpo).write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(destino)
    print(f"{nome}: {len(pdf)} linhas")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold 1: vitórias por piloto

# COMMAND ----------

from src.gold_vitorias_piloto import build_gold_vitorias_piloto

gold_vitorias = build_gold_vitorias_piloto(ler("fact_results"), ler("dim_driver"))
display(gold_vitorias.head(10))
gravar(gold_vitorias, "gold_vitorias_piloto")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold 2: posições ganhas por piloto

# COMMAND ----------

from src.gold_posicoes_ganhas import build_gold_posicoes_ganhas

gold_posicoes = build_gold_posicoes_ganhas(ler("fact_results"), ler("dim_driver"))
display(gold_posicoes.head(10))
gravar(gold_posicoes, "gold_posicoes_ganhas")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold 3: pontos por temporada

# COMMAND ----------

from src.gold_pontos_temporada import build_gold_pontos_temporada

gold_pontos = build_gold_pontos_temporada(ler("fact_results"), ler("dim_race"))
display(gold_pontos.head(10))
gravar(gold_pontos, "gold_pontos_temporada")