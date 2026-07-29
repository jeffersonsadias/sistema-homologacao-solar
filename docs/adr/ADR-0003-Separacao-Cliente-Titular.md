# ADR-0003 — Separação entre Cliente e Titular

## Status

Aceito

---

## Contexto

Durante a modelagem do domínio observou-se que a pessoa que contrata os serviços nem sempre é a titular da Unidade Consumidora.

---

## Problema

Modelar Cliente e Titular como a mesma entidade criaria inconsistências em diversos cenários reais.

---

## Alternativas Consideradas

* Cliente e Titular como uma única entidade.
* Cliente contendo informações do Titular.
* Entidades independentes.

---

## Decisão

Cliente e Titular passam a representar conceitos distintos.

O Cliente mantém o relacionamento comercial.

O Titular representa o responsável legal pela Unidade Consumidora.

---

## Consequências

### Benefícios

* maior aderência ao domínio;
* flexibilidade;
* redução de inconsistências.

### Custos

* necessidade de relacionamentos adicionais entre entidades.

---

## Referências

* `docs/04_MODELO_DE_DOMINIO.md`
