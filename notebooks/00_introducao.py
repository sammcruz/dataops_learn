# Databricks notebook source
# MAGIC %md
# MAGIC # Projeto F1: introdução
# MAGIC
# MAGIC Neste projeto a turma constrói, em equipe, uma pequena plataforma de dados de **Fórmula 1** no
# MAGIC Databricks e pratica o fluxo de **CI/CD**: cada pessoa implementa uma transformação em uma
# MAGIC *feature branch*, abre um *Pull Request*, o GitHub roda os testes automáticos e a professora revisa.
# MAGIC
# MAGIC ## O que vamos fazer
# MAGIC
# MAGIC 1. **Bronze (igual para todos):** o notebook `01_ingestao_f1` baixa o dataset do Kaggle e cria uma tabela
# MAGIC    por arquivo CSV, com tudo em texto.
# MAGIC 2. **Silver (uma story por pessoa):** cada pessoa escreve uma função em `src/` que limpa e organiza uma tabela.
# MAGIC 3. **Testes:** cada função tem um teste pronto em `tests/`. Você remove a linha `skip`, e o teste precisa passar.
# MAGIC 4. **Pull Request:** CI verde (`ruff` + `pytest`) e aprovação da professora para entrar na `main`.
# MAGIC
# MAGIC | Story | Função | Entrada (bronze) | Saída (silver) |
# MAGIC |---|---|---|---|
# MAGIC | 1. Pilotos | `build_dim_driver` | `drivers` | `silver_dim_driver` |
# MAGIC | 2. Corridas | `build_dim_race` | `races` + `circuits` | `silver_dim_race` |
# MAGIC | 3. Resultados | `build_fact_results` | `results` + `status` | `silver_fact_results` |
# MAGIC | 4. Equipes | `build_dim_constructor` | `constructors` | `silver_dim_constructor` |
# MAGIC
# MAGIC As quatro stories são **independentes**: ninguém espera o trabalho de outra pessoa.

# COMMAND ----------

# MAGIC %md
# MAGIC ## O dataset: 14 tabelas ligadas por chaves
# MAGIC
# MAGIC O dataset vem do banco Ergast, que guarda o histórico da Fórmula 1 desde 1950. Cada tabela é um
# MAGIC arquivo CSV, e elas se ligam por colunas de id (`raceId`, `driverId`, `constructorId`, `circuitId`,
# MAGIC `statusId`).
# MAGIC
# MAGIC O diagrama abaixo mostra as tabelas e como elas se relacionam. Cada linha entre duas tabelas é um
# MAGIC relacionamento: `||--o{` lê-se "um para muitos" (por exemplo, **uma** corrida tem **muitos** resultados).
# MAGIC
# MAGIC Se o diagrama aparecer como texto no seu workspace, veja a tabela de relações logo depois dele.
# MAGIC
# MAGIC ```mermaid
# MAGIC erDiagram
# MAGIC     SEASONS ||--o{ RACES : "year"
# MAGIC     CIRCUITS ||--o{ RACES : "circuitId"
# MAGIC     RACES ||--o{ RESULTS : "raceId"
# MAGIC     RACES ||--o{ SPRINT_RESULTS : "raceId"
# MAGIC     RACES ||--o{ QUALIFYING : "raceId"
# MAGIC     RACES ||--o{ LAP_TIMES : "raceId"
# MAGIC     RACES ||--o{ PIT_STOPS : "raceId"
# MAGIC     RACES ||--o{ DRIVER_STANDINGS : "raceId"
# MAGIC     RACES ||--o{ CONSTRUCTOR_STANDINGS : "raceId"
# MAGIC     RACES ||--o{ CONSTRUCTOR_RESULTS : "raceId"
# MAGIC     DRIVERS ||--o{ RESULTS : "driverId"
# MAGIC     DRIVERS ||--o{ SPRINT_RESULTS : "driverId"
# MAGIC     DRIVERS ||--o{ QUALIFYING : "driverId"
# MAGIC     DRIVERS ||--o{ LAP_TIMES : "driverId"
# MAGIC     DRIVERS ||--o{ PIT_STOPS : "driverId"
# MAGIC     DRIVERS ||--o{ DRIVER_STANDINGS : "driverId"
# MAGIC     CONSTRUCTORS ||--o{ RESULTS : "constructorId"
# MAGIC     CONSTRUCTORS ||--o{ SPRINT_RESULTS : "constructorId"
# MAGIC     CONSTRUCTORS ||--o{ QUALIFYING : "constructorId"
# MAGIC     CONSTRUCTORS ||--o{ CONSTRUCTOR_STANDINGS : "constructorId"
# MAGIC     CONSTRUCTORS ||--o{ CONSTRUCTOR_RESULTS : "constructorId"
# MAGIC     STATUS ||--o{ RESULTS : "statusId"
# MAGIC     STATUS ||--o{ SPRINT_RESULTS : "statusId"
# MAGIC
# MAGIC     DRIVERS {
# MAGIC         int driverId PK
# MAGIC         string driverRef
# MAGIC         string number
# MAGIC         string code
# MAGIC         string forename
# MAGIC         string surname
# MAGIC         date dob
# MAGIC         string nationality
# MAGIC     }
# MAGIC     CONSTRUCTORS {
# MAGIC         int constructorId PK
# MAGIC         string constructorRef
# MAGIC         string name
# MAGIC         string nationality
# MAGIC     }
# MAGIC     CIRCUITS {
# MAGIC         int circuitId PK
# MAGIC         string circuitRef
# MAGIC         string name
# MAGIC         string location
# MAGIC         string country
# MAGIC         float lat
# MAGIC         float lng
# MAGIC         int alt
# MAGIC     }
# MAGIC     SEASONS {
# MAGIC         int year PK
# MAGIC     }
# MAGIC     RACES {
# MAGIC         int raceId PK
# MAGIC         int year FK
# MAGIC         int round
# MAGIC         int circuitId FK
# MAGIC         string name
# MAGIC         date date
# MAGIC         string time
# MAGIC     }
# MAGIC     RESULTS {
# MAGIC         int resultId PK
# MAGIC         int raceId FK
# MAGIC         int driverId FK
# MAGIC         int constructorId FK
# MAGIC         int grid
# MAGIC         int position
# MAGIC         int positionOrder
# MAGIC         float points
# MAGIC         int laps
# MAGIC         string milliseconds
# MAGIC         string fastestLapTime
# MAGIC         int statusId FK
# MAGIC     }
# MAGIC     QUALIFYING {
# MAGIC         int qualifyId PK
# MAGIC         int raceId FK
# MAGIC         int driverId FK
# MAGIC         int constructorId FK
# MAGIC         int position
# MAGIC         string q1
# MAGIC         string q2
# MAGIC         string q3
# MAGIC     }
# MAGIC     LAP_TIMES {
# MAGIC         int raceId FK
# MAGIC         int driverId FK
# MAGIC         int lap
# MAGIC         int position
# MAGIC         string time
# MAGIC         int milliseconds
# MAGIC     }
# MAGIC     PIT_STOPS {
# MAGIC         int raceId FK
# MAGIC         int driverId FK
# MAGIC         int stop
# MAGIC         int lap
# MAGIC         string duration
# MAGIC         int milliseconds
# MAGIC     }
# MAGIC     DRIVER_STANDINGS {
# MAGIC         int driverStandingsId PK
# MAGIC         int raceId FK
# MAGIC         int driverId FK
# MAGIC         float points
# MAGIC         int position
# MAGIC         int wins
# MAGIC     }
# MAGIC     CONSTRUCTOR_STANDINGS {
# MAGIC         int constructorStandingsId PK
# MAGIC         int raceId FK
# MAGIC         int constructorId FK
# MAGIC         float points
# MAGIC         int position
# MAGIC         int wins
# MAGIC     }
# MAGIC     CONSTRUCTOR_RESULTS {
# MAGIC         int constructorResultsId PK
# MAGIC         int raceId FK
# MAGIC         int constructorId FK
# MAGIC         float points
# MAGIC     }
# MAGIC     SPRINT_RESULTS {
# MAGIC         int resultId PK
# MAGIC         int raceId FK
# MAGIC         int driverId FK
# MAGIC         int constructorId FK
# MAGIC         int grid
# MAGIC         int position
# MAGIC         float points
# MAGIC         int statusId FK
# MAGIC     }
# MAGIC     STATUS {
# MAGIC         int statusId PK
# MAGIC         string status
# MAGIC     }
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### As relações em texto
# MAGIC
# MAGIC | Tabela "um" | Tabela "muitos" | Chave de ligação |
# MAGIC |---|---|---|
# MAGIC | `circuits` | `races` | `circuitId` |
# MAGIC | `races` | `results`, `qualifying`, `lap_times`, `pit_stops`, `driver_standings`, `constructor_standings` | `raceId` |
# MAGIC | `drivers` | `results`, `qualifying`, `lap_times`, `pit_stops`, `driver_standings` | `driverId` |
# MAGIC | `constructors` | `results`, `qualifying`, `constructor_standings` | `constructorId` |
# MAGIC | `status` | `results` | `statusId` |
# MAGIC
# MAGIC ## Como ler o modelo
# MAGIC
# MAGIC - **Dimensões** (quem, onde, quando): `drivers`, `constructors`, `circuits`, `races`, `status`.
# MAGIC - **Fatos** (o que aconteceu): `results`, `qualifying`, `lap_times`, `pit_stops`.
# MAGIC - A corrida (`races`) é o centro: quase todo fato aponta para ela por `raceId`.
# MAGIC - `results` tem uma linha por piloto em cada corrida. É a tabela mais usada.
# MAGIC
# MAGIC ## Pegadinhas dos dados
# MAGIC
# MAGIC - O nulo vem como o texto `\N`, e não como vazio. A função `clean_nulls` (em `src/common.py`) já resolve isso.
# MAGIC - `grid = 0` significa largada dos boxes. Não existe posição 0.
# MAGIC - `position` fica nulo quando o piloto não terminou a corrida.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Espie os dados
# MAGIC
# MAGIC Rode as células abaixo depois de executar o notebook `01_ingestao_f1`. Elas mostram as tabelas bronze
# MAGIC que você vai transformar.

# COMMAND ----------

dbutils.widgets.text("catalogo", "dataops_learn", "Catálogo")
dbutils.widgets.text("schema", "f1", "Schema")
CATALOGO = dbutils.widgets.get("catalogo")
SCHEMA = dbutils.widgets.get("schema")

try:
    spark.sql(f"DESCRIBE SCHEMA {CATALOGO}.{SCHEMA}")
except Exception:
    CATALOGO = "workspace"

display(spark.sql(f"SHOW TABLES IN {CATALOGO}.{SCHEMA}"))

# COMMAND ----------

# Troque o nome da tabela para explorar: drivers, races, circuits, results, status, constructors...
display(spark.table(f"{CATALOGO}.{SCHEMA}.bronze_drivers").limit(10))

# COMMAND ----------

# Exemplo de relacionamento: resultados com o nome do piloto (join por driverId)
display(spark.sql(f"""
    SELECT r.raceId, d.forename, d.surname, r.grid, r.position, r.points
    FROM {CATALOGO}.{SCHEMA}.bronze_results r
    JOIN {CATALOGO}.{SCHEMA}.bronze_drivers d ON d.driverId = r.driverId
    LIMIT 10
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Próximos passos
# MAGIC
# MAGIC 1. Leia o `CONTRIBUTING.md` e a sua issue no GitHub (ela tem um passo a passo).
# MAGIC 2. Crie a sua branch no Git folder: `feature/<seu-nome>-<tema>`.
# MAGIC 3. Implemente a função em `src/`, remova a linha `skip` do seu teste e rode `pytest`.
# MAGIC 4. Abra o Pull Request com `Closes #<número da issue>`.
