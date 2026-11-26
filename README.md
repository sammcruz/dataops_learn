# dataops_learn

Projeto colaborativo de **DataOps e CI/CD** com Databricks (Free Edition), usando o dataset de
Fórmula 1 do Kaggle. Cada pessoa trabalha em uma branch, abre um Pull Request, o CI roda os testes
automáticos e a professora revisa e aprova.

## O fluxo

```
issue (story) -> branch -> código + testes -> Pull Request -> CI verde + revisão -> merge
```

Passo a passo para contribuir: [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `notebooks/01_ingestao_f1.py` | Baixa o dataset do Kaggle e cria as tabelas bronze (igual para todos) |
| `notebooks/02_transformacoes.py` | Roda as funções de `src/` sobre os dados reais e grava as tabelas silver |
| `src/` | Funções de transformação, uma por story. **É aqui que você trabalha** |
| `tests/` | Testes automáticos, com amostras pequenas em `tests/data/` |
| `docs/modelo-semantico.md` | Como as tabelas de F1 se relacionam |
| `.github/workflows/ci.yml` | Lint (`ruff`) e testes (`pytest`) a cada Pull Request |
| `notebooks/00_teste_kaggle.py` | Teste isolado de conexão com o Kaggle |

## Rodar os testes na sua máquina

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
ruff check .
pytest -v
```

Os testes das stories começam **pulados** (`skipped`). Quando você implementar a sua função, remova a
linha `pytestmark = pytest.mark.skip(...)` do seu arquivo de teste e veja os testes passarem.

## Regras

- Nunca faça push direto na `main`: sempre por Pull Request.
- Nunca grave credenciais (Kaggle, tokens) em arquivo, notebook ou commit.
- Não envie os CSVs do Kaggle para o repositório. Os testes usam só as amostras de `tests/data/`.
