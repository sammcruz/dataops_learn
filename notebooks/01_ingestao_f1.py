# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# MAGIC %md
# MAGIC # 01. Ingestão do dataset de Fórmula 1 (igual para todos)
# MAGIC
# MAGIC Cada pessoa roda este notebook na **própria** workspace. O resultado é o mesmo para todo mundo:
# MAGIC
# MAGIC 1. Cria catálogo, schema e volume
# MAGIC 2. Baixa o dataset do Kaggle para o volume (ou usa os arquivos que você já enviou por upload)
# MAGIC 3. Cria uma tabela `bronze_<arquivo>` para cada CSV, **tudo como texto e sem limpeza**
# MAGIC
# MAGIC A limpeza e a tipagem são o trabalho das stories (arquivos em `src/`).
# MAGIC
# MAGIC Se o download falhar (sem internet, sem credencial), baixe os CSVs no seu computador e faça upload
# MAGIC na pasta do volume (Catalog > volume > Upload). O notebook detecta que os arquivos já estão lá.

# COMMAND ----------

dbutils.widgets.text("catalogo", "dataops_learn", "Catálogo")
dbutils.widgets.text("schema", "f1", "Schema")
dbutils.widgets.text("volume", "raw", "Volume")
dbutils.widgets.text("dataset", "rohanrao/formula-1-world-championship-1950-2020", "Dataset Kaggle")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Catálogo, schema e volume

# COMMAND ----------

CATALOGO = dbutils.widgets.get("catalogo")
SCHEMA = dbutils.widgets.get("schema")
VOLUME = dbutils.widgets.get("volume")
DATASET = dbutils.widgets.get("dataset")

try:
    spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOGO}")
except Exception as e:
    print(f"Não foi possível criar o catálogo '{CATALOGO}': {str(e)[:150]}")
    print("Usando o catálogo 'workspace'.")
    CATALOGO = "workspace"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOGO}.{SCHEMA}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOGO}.{SCHEMA}.{VOLUME}")

DESTINO = f"/Volumes/{CATALOGO}/{SCHEMA}/{VOLUME}/{DATASET.split('/')[-1]}"
print("Catálogo.schema:", f"{CATALOGO}.{SCHEMA}")
print("Pasta dos CSVs :", DESTINO)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Download do Kaggle (pulado se os CSVs já existem)

# COMMAND ----------

# MAGIC %pip install -q kaggle

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

import getpass
import os

CATALOGO = dbutils.widgets.get("catalogo")
SCHEMA = dbutils.widgets.get("schema")
VOLUME = dbutils.widgets.get("volume")
DATASET = dbutils.widgets.get("dataset")

try:
    spark.sql(f"DESCRIBE VOLUME {CATALOGO}.{SCHEMA}.{VOLUME}")
except Exception:
    CATALOGO = "workspace"

DESTINO = f"/Volumes/{CATALOGO}/{SCHEMA}/{VOLUME}/{DATASET.split('/')[-1]}"
os.makedirs(DESTINO, exist_ok=True)

ja_tem = [f for f in os.listdir(DESTINO) if f.endswith(".csv")]
if ja_tem:
    print(f"{len(ja_tem)} CSVs já estão em {DESTINO}. Download pulado.")
else:
    # Nunca grave a credencial em notebook, commit ou widget. Ela fica só nesta sessão.
    if not (os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY")):
        os.environ["KAGGLE_USERNAME"] = getpass.getpass("Kaggle username: ")
        os.environ["KAGGLE_KEY"] = getpass.getpass("Kaggle API key: ")

    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(DATASET, path=DESTINO, unzip=True, quiet=False)

for f in sorted(os.listdir(DESTINO)):
    print(f"  {f:30s} {os.path.getsize(os.path.join(DESTINO, f)) / 1024:10.1f} KB")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Tabelas bronze (tudo texto, sem limpeza)
# MAGIC O dataset usa o texto `\N` para nulo. A bronze mantém isso como veio.

# COMMAND ----------

resumo = []
for arquivo in sorted(f for f in os.listdir(DESTINO) if f.endswith(".csv")):
    nome = arquivo.removesuffix(".csv")
    df = spark.read.option("header", "true").csv(f"{DESTINO}/{arquivo}")  # sem inferSchema: tudo texto
    df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(
        f"{CATALOGO}.{SCHEMA}.bronze_{nome}"
    )
    resumo.append((f"bronze_{nome}", spark.table(f"{CATALOGO}.{SCHEMA}.bronze_{nome}").count()))

display(spark.createDataFrame(resumo, "tabela string, linhas long"))

# COMMAND ----------

# MAGIC %md
# MAGIC Pronto. Próximo passo: leia a sua story no GitHub, crie a sua branch e implemente a função em `src/`.
# MAGIC Depois use o notebook `02_transformacoes` para rodar o seu código sobre os dados reais.

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from dataops_learn.f1.bronze_constructors

# COMMAND ----------

