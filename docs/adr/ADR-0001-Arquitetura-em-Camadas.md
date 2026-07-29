# ADR-0001 — Arquitetura em Camadas

## Status

Aceito

---

## Contexto

A plataforma será composta por diversos módulos de negócio e deverá evoluir ao longo de várias Sprints, incorporando novas funcionalidades sem comprometer a organização do código.

Era necessário definir uma arquitetura que facilitasse manutenção, testes e evolução.

---

## Problema

Misturar interface, regras de negócio e persistência aumenta o acoplamento, dificulta testes e torna a evolução do sistema mais custosa.

---

## Alternativas Consideradas

* Arquitetura monolítica sem separação de responsabilidades.
* Arquitetura em três camadas.
* Arquitetura em camadas com domínio centralizado.

---

## Decisão

Foi adotada uma arquitetura em camadas composta por:

* Interface;
* Fachada;
* Domínio;
* Infraestrutura;
* Persistência.

Cada camada possui responsabilidades exclusivas e depende apenas da camada imediatamente inferior.

---

## Consequências

### Benefícios

* baixo acoplamento;
* alta coesão;
* facilidade de testes;
* maior legibilidade;
* preparação para APIs e interface web.

### Custos

* maior número de arquivos;
* necessidade de disciplina arquitetural;
* maior planejamento inicial.

---

## Referências

* `docs/02_ARQUITETURA.md`
* `docs/03_PADROES_DE_DESENVOLVIMENTO.md`
