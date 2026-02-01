# Regras para Criação de Testes (Resumido)

## Regra nº1 — Simular a Realidade (Versão Corrigida)

Todo teste deve executar **exatamente** o que a feature faz em produção: criar dados reais na BD, gerar logs reais, chamar serviços reais, etc.

**Antes de criar qualquer registo na base de dados**, o teste deve:

- Listar exatamente que registos serão criados (estrutura, campos, valores).
- Guardar essa informação no relatório Markdown do teste.

---

## Regra nº2 — Testes de IA: Dinâmicos e Interativos

**Não podem existir perguntas/respostas pré-feitas embutidas no teste.**

O teste deve pedir input via terminal (stdin) durante a execução (modo interativo). O utilizador fornece:

- O prompt/entrada.
- O valor esperado (se aplicável) — também por terminal.

O teste invoca o modelo local (CLI configurável, ex.: `$MODEL_CLI`) com stdin; recebe resposta do modelo e compara com o valor esperado.

O teste **não deve "checar selectivamente"** — ele obtém um output, compara com o esperado, e passa/falha conforme igualdade/critério definido.

Se necessário, adicionar tolerâncias (similaridade, thresholds) mas isso deve estar explícito na documentação do teste.

---

## Regra nº3 — Estrutura e Localização

- Sempre criar os ficheiros de teste na pasta indicada pelo utilizador.
- Nome do ficheiro de teste deve seguir convenção: `<pasta>/<nome_feature>__test_<descrição>.py`
- Na mesma pasta, criar `README.md` ou `<nome_feature>__test_doc.md` com documentação do teste (ver secção "Relatório").

---

## Regra nº4 — Comentarios

- Sem comentarios no codigo

---

## Regra nº5 — Comentarios

- Todos os testes no final tem de correr clean.py, para fazer a limpeza dos pycache desnecessarios

---

## Relatório Pós-Teste (Obrigatório)

Após cada execução salvar/mostrar, **no topo do relatório**:

- Data e hora do teste (ISO 8601).
- Quem executou o teste (ex.: Bruno).
- Resultado do teste (PASS / FAIL) e código de saída.
- Resumo do teste: o que foi testado, inputs usados, o que se esperava e porquê.
- Relatorio sempre em ingles USA

O relatório deve ser gerado em markdown (`.md`) e também guardado em `logs/<test-identifier>.log`.

---

## Logs Reais

O teste deve provocar e gravar **logs reais** (Caso a feature crie logs) nas pastas de logs do sistema (não logs simulados). Verificar que as entradas de log geradas correspondem às ações na BD.

**Comparator de logs**: depois do teste, validar que X logs foram criados e que contêm os campos esperados (timestamps, IDs, actions).

---

## Banco de Dados

Fornecer fixtures para:

- Popular dados reais necessários ao cenário.
- Garantir isolamento (schema temporário, transactions, ou DB de teste dedicada).

**Fazer cleanup sempre** (rollback ou truncation).

---

## Naming, Versionamento e Meta

Cada teste tem um identificador único: `faseID_featureID_YYYYMMDD_HHMMSS`.

Incluir no ficheiro cabeçalho com metadados: autor, fase, subfase, requisitos ligados, tags.

---

## Testes de Fase Completa (ex.: FASE 1: FUNDAÇÃO DO SISTEMA)

Quando pedido "teste completo da fase X", executar todos os sub-testes mapeados àquela fase.

Usar pytest + coverage para correr a suite: fornecer comando exato para execução e geração de relatório:

```bash
pytest tests/<phase_folder> --maxfail=1 -q
coverage run -m pytest tests/<phase_folder> && coverage html -d coverage/<phase_folder>
```

Garantir que cada subfase (ex.: 1.1, 1.2, 1.3) tem testes unitários + integração conforme aplicável.

---

## Boas Práticas Adicionais

- Tests podem ter **modos**: `interactive` (default) e `ci` (não-interactive). No `ci` o input vem de ficheiros `.in` e `.expected` (mas apenas se o utilizador aceitar esse modo).
- Usar **variáveis de ambiente** para configuração (DB_URI, MODEL_CLI, LOG_DIR, INTERACTIVE=1).
- Documentar comandos para reproduzir localmente.

---

## Resumo das Regras

| #   | Regra                    | Descrição                                           |
| --- | ------------------------ | --------------------------------------------------- |
| 1   | Simular a Realidade      | Executar exatamente o que a feature faz em produção |
| 2   | Testes de IA Interativos | Input via terminal, sem respostas pré-feitas        |
| 3   | Estrutura e Localização  | Convenção de nomes e pasta definida pelo utilizador |
| 4   | Relatório Obrigatório    | Documentar data, executor, resultado e resumo       |
| 5   | Logs Reais               | Provocar e validar logs reais do sistema            |
| 6   | Banco de Dados           | Fixtures, isolamento e cleanup obrigatório          |
| 7   | Naming e Meta            | Identificador único e metadados no cabeçalho        |
| 8   | Testes de Fase           | Suite completa com pytest + coverage                |
| 9   | Boas Práticas            | Modos interactive/ci, variáveis de ambiente         |
