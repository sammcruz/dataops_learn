# Databricks notebook source
# MAGIC %md
# MAGIC # Teste: Kaggle API dentro do Databricks
# MAGIC
# MAGIC Objetivo: descobrir se o Databricks (Free Edition) consegue baixar um dataset do Kaggle
# MAGIC e gravar os CSVs em um volume do Unity Catalog.
# MAGIC
# MAGIC Etapas:
# MAGIC 1. Criar catálogo, schema e volume
# MAGIC 2. Testar se existe acesso à internet até o Kaggle
# MAGIC 3. Baixar e descompactar o dataset no volume
# MAGIC 4. Ler um CSV com Spark para confirmar
# MAGIC
# MAGIC Se a etapa 2 falhar, o caminho alternativo é baixar o dataset no seu computador e fazer upload no volume (Catalog > volume > Upload).

# COMMAND ----------

dbutils.widgets.text("catalogo", "dataops_learn", "Catálogo")
dbutils.widgets.text("schema", "f1", "Schema")
dbutils.widgets.text("volume", "raw", "Volume")
dbutils.widgets.text("dataset", "rohanrao/formula-1-world-championship-1950-2020", "Dataset Kaggle (dono/nome)")

CATALOGO = dbutils.widgets.get("catalogo")
SCHEMA = dbutils.widgets.get("schema")
VOLUME = dbutils.widgets.get("volume")
DATASET = dbutils.widgets.get("dataset")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Catálogo, schema e volume
# MAGIC Se não for possível criar o catálogo (permissão ou limite do workspace), o notebook usa o catálogo `workspace`.

# COMMAND ----------

try:
    spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOGO}")
except Exception as e:
    print(f"Não foi possível criar o catálogo '{CATALOGO}': {str(e)[:200]}")
    print("Usando o catálogo 'workspace'.")
    CATALOGO = "workspace"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOGO}.{SCHEMA}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOGO}.{SCHEMA}.{VOLUME}")

RAIZ = f"/Volumes/{CATALOGO}/{SCHEMA}/{VOLUME}"
print("Volume pronto em:", RAIZ)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Existe acesso à internet até o Kaggle?
# MAGIC Esta é a pergunta principal do teste. Na Free Edition o acesso de saída pode ser restrito a alguns domínios.

# COMMAND ----------

import urllib.request, urllib.error

def testar(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return f"OK ({r.status})"
    except urllib.error.HTTPError as e:
        return f"alcançou o servidor (HTTP {e.code})"   # 401/403/404 também provam que há conexão
    except Exception as e:
        return f"FALHOU: {type(e).__name__}: {str(e)[:120]}"

for url in ["https://pypi.org", "https://www.kaggle.com", "https://www.kaggle.com/api/v1/datasets/list"]:
    print(f"{url:55s} {testar(url)}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Baixar o dataset
# MAGIC Você precisa de uma credencial do Kaggle (Kaggle > Settings > API). **Nunca grave a credencial em notebook, commit ou widget.**
# MAGIC A célula abaixo pede o valor na hora e o guarda só na variável de ambiente da sessão.

# COMMAND ----------

# MAGIC %pip install -q kaggle

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

import os, getpass

# Reexecute esta célula depois do restart para recarregar as variáveis
CATALOGO = dbutils.widgets.get("catalogo")
SCHEMA = dbutils.widgets.get("schema")
VOLUME = dbutils.widgets.get("volume")
DATASET = dbutils.widgets.get("dataset")
try:
    spark.sql(f"DESCRIBE VOLUME {CATALOGO}.{SCHEMA}.{VOLUME}")
except Exception:
    CATALOGO = "workspace"
RAIZ = f"/Volumes/{CATALOGO}/{SCHEMA}/{VOLUME}"

if not (os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY")):
    os.environ["KAGGLE_USERNAME"] = getpass.getpass("Kaggle username: ")
    os.environ["KAGGLE_KEY"] = getpass.getpass("Kaggle API key: ")

# COMMAND ----------

from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

DESTINO = f"{RAIZ}/{DATASET.split('/')[-1]}"
os.makedirs(DESTINO, exist_ok=True)
api.dataset_download_files(DATASET, path=DESTINO, unzip=True, quiet=False)

print("Arquivos baixados:")
for f in sorted(os.listdir(DESTINO)):
    print(f"  {f:35s} {os.path.getsize(os.path.join(DESTINO, f)) / 1024:10.1f} KB")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Confirmar a leitura com Spark

# COMMAND ----------

csvs = [f for f in os.listdir(DESTINO) if f.endswith(".csv")]
primeiro = csvs[0]
df = spark.read.option("header", "true").option("nullValue", "\\N").csv(f"{DESTINO}/{primeiro}")
print(primeiro, "->", df.count(), "linhas")
display(df.limit(10))
