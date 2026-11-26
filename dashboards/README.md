# Dashboards

Cada pessoa guarda aqui o dashboard que criou sobre a sua tabela gold, como arquivo `.lvdash.json`.
Depois os arquivos são reunidos em um dashboard consolidado.

## Como exportar

1. Abra o seu dashboard no Databricks.
2. No menu (⋮) do dashboard, escolha a opção de exportar ou baixar o arquivo `.lvdash.json`.
3. Coloque o arquivo nesta pasta, no seu Pull Request.

## Nome do arquivo

Use o nome do tema da sua story:

- `vitorias_piloto.lvdash.json`
- `posicoes_ganhas.lvdash.json`
- `pontos_temporada.lvdash.json`

## Regras

- As consultas do dashboard devem usar o nome completo da tabela, por exemplo
  `dataops_learn.f1.gold_vitorias_piloto`, para funcionar em qualquer workspace.
- Não apague nem altere o dashboard de outra pessoa. O consolidado é um arquivo novo.
