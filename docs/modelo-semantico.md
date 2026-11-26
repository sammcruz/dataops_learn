# Modelo semântico do dataset de Fórmula 1

O dataset do Kaggle é uma cópia do banco Ergast: 14 tabelas ligadas por chaves numéricas
(`raceId`, `driverId`, `constructorId`, `circuitId`, `statusId`). Os nomes das colunas abaixo são
os dos arquivos CSV. **Confirme na sua workspace** com `DESCRIBE bronze_<tabela>`, porque o autor
do dataset pode ter mudado algo.

```mermaid
erDiagram
    SEASONS ||--o{ RACES : "year"
    CIRCUITS ||--o{ RACES : "circuitId"
    RACES ||--o{ RESULTS : "raceId"
    RACES ||--o{ SPRINT_RESULTS : "raceId"
    RACES ||--o{ QUALIFYING : "raceId"
    RACES ||--o{ LAP_TIMES : "raceId"
    RACES ||--o{ PIT_STOPS : "raceId"
    RACES ||--o{ DRIVER_STANDINGS : "raceId"
    RACES ||--o{ CONSTRUCTOR_STANDINGS : "raceId"
    RACES ||--o{ CONSTRUCTOR_RESULTS : "raceId"
    DRIVERS ||--o{ RESULTS : "driverId"
    DRIVERS ||--o{ SPRINT_RESULTS : "driverId"
    DRIVERS ||--o{ QUALIFYING : "driverId"
    DRIVERS ||--o{ LAP_TIMES : "driverId"
    DRIVERS ||--o{ PIT_STOPS : "driverId"
    DRIVERS ||--o{ DRIVER_STANDINGS : "driverId"
    CONSTRUCTORS ||--o{ RESULTS : "constructorId"
    CONSTRUCTORS ||--o{ SPRINT_RESULTS : "constructorId"
    CONSTRUCTORS ||--o{ QUALIFYING : "constructorId"
    CONSTRUCTORS ||--o{ CONSTRUCTOR_STANDINGS : "constructorId"
    CONSTRUCTORS ||--o{ CONSTRUCTOR_RESULTS : "constructorId"
    STATUS ||--o{ RESULTS : "statusId"
    STATUS ||--o{ SPRINT_RESULTS : "statusId"

    DRIVERS {
        int driverId PK
        string driverRef
        string number
        string code
        string forename
        string surname
        date dob
        string nationality
    }
    CONSTRUCTORS {
        int constructorId PK
        string constructorRef
        string name
        string nationality
    }
    CIRCUITS {
        int circuitId PK
        string circuitRef
        string name
        string location
        string country
        float lat
        float lng
        int alt
    }
    SEASONS {
        int year PK
    }
    RACES {
        int raceId PK
        int year FK
        int round
        int circuitId FK
        string name
        date date
        string time
    }
    RESULTS {
        int resultId PK
        int raceId FK
        int driverId FK
        int constructorId FK
        int grid
        int position
        int positionOrder
        float points
        int laps
        string milliseconds
        string fastestLapTime
        int statusId FK
    }
    QUALIFYING {
        int qualifyId PK
        int raceId FK
        int driverId FK
        int constructorId FK
        int position
        string q1
        string q2
        string q3
    }
    LAP_TIMES {
        int raceId FK
        int driverId FK
        int lap
        int position
        string time
        int milliseconds
    }
    PIT_STOPS {
        int raceId FK
        int driverId FK
        int stop
        int lap
        string duration
        int milliseconds
    }
    DRIVER_STANDINGS {
        int driverStandingsId PK
        int raceId FK
        int driverId FK
        float points
        int position
        int wins
    }
    CONSTRUCTOR_STANDINGS {
        int constructorStandingsId PK
        int raceId FK
        int constructorId FK
        float points
        int position
        int wins
    }
    CONSTRUCTOR_RESULTS {
        int constructorResultsId PK
        int raceId FK
        int constructorId FK
        float points
    }
    SPRINT_RESULTS {
        int resultId PK
        int raceId FK
        int driverId FK
        int constructorId FK
        int grid
        int position
        float points
        int statusId FK
    }
    STATUS {
        int statusId PK
        string status
    }
```

## Como ler

- **Dimensões** (quem, onde, quando): `drivers`, `constructors`, `circuits`, `races`, `seasons`, `status`.
- **Fatos** (o que aconteceu): `results`, `qualifying`, `lap_times`, `pit_stops`, `sprint_results`,
  além das classificações do campeonato (`driver_standings`, `constructor_standings`,
  `constructor_results`).
- A corrida (`races`) é o centro: quase todo fato aponta para ela por `raceId`.
- `results` é a tabela mais usada nas perguntas do dia: uma linha por piloto em cada corrida.

## Onde cada story entra

| Story | Entrada | Saída (silver) |
|---|---|---|
| 1. Pilotos | `drivers` | `silver_dim_driver` |
| 2. Corridas e circuitos | `races` + `circuits` | `silver_dim_race` |
| 3. Resultados | `results` + `status` | `silver_fact_results` |
| Professora (gold) | as três silvers | KPIs e painel |

Na gold, `silver_fact_results` liga a `silver_dim_driver` por `driver_id` e a `silver_dim_race` por
`race_id`: é a estrela do projeto.

## Pegadinhas conhecidas

- O nulo vem como o texto `\N`, não como vazio.
- `grid = 0` significa largada dos boxes (não existe posição 0).
- `position` fica nulo quando o piloto não terminou (veja `positionText`, que traz `R`, `D`, `W`...).
- Tempos vêm como texto (`1:27.452`), e `milliseconds` só existe para quem completou a corrida inteira.
