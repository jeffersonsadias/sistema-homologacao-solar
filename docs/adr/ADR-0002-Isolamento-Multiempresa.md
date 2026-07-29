# ADR-0002 — Isolamento Multiempresa

## Status

Aceito

---

## Contexto

Desde as primeiras modelagens identificou-se que a plataforma deveria atender diferentes empresas utilizando a mesma base de software.

---

## Problema

Sem isolamento entre empresas, haveria risco de exposição de dados e dificuldade para evoluir a plataforma como um produto SaaS.

---

## Alternativas Consideradas

* Uma instância separada para cada empresa.
* Compartilhamento de todos os dados.
* Isolamento lógico por Empresa.

---

## Decisão

Foi adotado o isolamento lógico.

Toda entidade operacional pertence obrigatoriamente a uma Empresa.

Nenhuma operação pode acessar registros pertencentes a outra organização.

---

## Consequências

### Benefícios

* arquitetura SaaS;
* segurança lógica;
* escalabilidade;
* facilidade de expansão.

### Custos

* necessidade de validar Empresa em todas as operações.

---

## Referências

* `docs/04_MODELO_DE_DOMINIO.md`
* `docs/05_REGRAS_DE_NEGOCIO.md`
