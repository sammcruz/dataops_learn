# Como contribuir

Siga este roteiro do começo ao fim. Se algo falhar, avise a professora.

## 0. Antes de começar (uma vez)

- Aceite o convite de colaborador no seu e-mail (GitHub).
- No Databricks: **Settings > Linked accounts** e vincule a sua conta do GitHub.
- Tenha uma conta gratuita no Kaggle e a sua credencial (Settings > API).

## 1. Clonar o repositório no Databricks

1. **Workspace > Create > Git folder**.
2. URL: `https://github.com/sammcruz/dataops_learn`, provedor GitHub.
3. Abra `notebooks/01_ingestao_f1.py` e rode tudo. Ele cria as tabelas bronze na sua workspace.

## 2. Pegar a sua story

Abra a aba **Issues** no GitHub e leia a story atribuída a você. Anote o número (por exemplo, `#7`).

## 3. Criar a sua branch

No Git folder, clique no nome da branch (`main`) > **Create branch**.
Nome: `feature/<seu-nome>-<tema>`, por exemplo `feature/ana-pilotos`.

## 4. Implementar e testar

1. Abra o arquivo da sua story em `src/` e implemente a função.
2. Abra o teste correspondente em `tests/` e **remova a linha** `pytestmark = pytest.mark.skip(...)`.
3. Rode os testes (no seu computador: `pytest -v`) ou use o notebook `02_transformacoes` para ver o
   resultado sobre os dados reais.

## 5. Commit e push

No Git folder do Databricks, abra a janela de Git, escreva uma mensagem curta e clique em
**Commit & Push**. Na mensagem, cite a story com `#número`:

```
Implementa dim_driver com nome completo e idade (#7)
```

## 6. Abrir o Pull Request

No GitHub aparece o aviso "Compare & pull request". Clique, preencha o modelo e escreva
`Closes #número` em "Story relacionada". Assim a story fecha sozinha quando o PR for aprovado.

## 7. CI e revisão

- O CI roda `ruff` e `pytest` sozinho. Precisa ficar verde.
- A professora revisa, pode pedir mudanças (comentários no PR) e aprova.
- Para ajustar, faça novos commits na **mesma branch**. O PR atualiza sozinho.

## Convenções

- Uma story, uma branch, um Pull Request.
- Mensagens de commit em português, no presente, citando `#número`.
- Funções puras em `src/`: recebem DataFrame e devolvem DataFrame, sem ler nem gravar tabelas.
