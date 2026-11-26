# Databricks notebook source
# MAGIC %md
# MAGIC # 02. Transformações (silver)
# MAGIC
# MAGIC Cada seção usa a função que uma pessoa implementou em `src/`. Rode só a sua seção enquanto
# MAGIC desenvolve, e a turma inteira roda tudo no final.
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
    return spark.table(f"{CATALOGO}.{SCHEMA}.bronze_{nome}").toPandas()


def gravar(pdf, nome):
    # Nulos do pandas (pd.NA, NaN) viram None, que o Spark entende
    limpo = pdf.astype(object).where(pdf.notna(), None)
    destino = f"{CATALOGO}.{SCHEMA}.{nome}"
    spark.createDataFrame(limpo).write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(destino)
    print(f"{nome}: {len(pdf)} linhas")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Story 1: pilotos (`dim_driver`)

# COMMAND ----------

from src.transform_drivers import build_dim_driver

dim_driver = build_dim_driver(ler("drivers"))
display(dim_driver.head(10))
gravar(dim_driver, "silver_dim_driver")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Story 2: corridas e circuitos (`dim_race`)

# COMMAND ----------

from src.transform_races import build_dim_race

dim_race = build_dim_race(ler("races"), ler("circuits"))
display(dim_race.head(10))
gravar(dim_race, "silver_dim_race")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Story 3: resultados (`fact_results`)

# COMMAND ----------

from src.transform_results import build_fact_results

fact_results = build_fact_results(ler("results"), ler("status"))
display(fact_results.head(10))
gravar(fact_results, "silver_fact_results")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold (professora): integração e painel
# MAGIC Depois que os três PRs forem aprovados, as tabelas `silver_*` se juntam por `race_id` e `driver_id`.
# MAGIC Exemplos de perguntas: quem mais venceu, circuitos com as voltas mais rápidas, quem mais ganha
# MAGIC posições na largada.

# COMMAND ----------

# Exemplo para a professora (rode depois dos três PRs):
# vitorias = spark.sql(f"""
#   SELECT d.full_name, COUNT(*) AS vitorias
#   FROM {CATALOGO}.{SCHEMA}.silver_fact_results f
#   JOIN {CATALOGO}.{SCHEMA}.silver_dim_driver d ON d.driver_id = f.driver_id
#   WHERE f.finish_position = 1
#   GROUP BY d.full_name ORDER BY vitorias DESC LIMIT 10
# """)
# display(vitorias)
