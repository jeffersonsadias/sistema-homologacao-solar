# Sprint 2

## Objetivo

Consolidar o domínio do Sistema de Homologação Solar,
estabelecendo a arquitetura definitiva da plataforma,
a modelagem do processo de homologação e a base para a
evolução do sistema até um ambiente SaaS.

---

## Principais Entregas

### Arquitetura

- consolidação da arquitetura em camadas;
- separação entre Interface, Fachada, Domínio,
  Infraestrutura e Persistência;
- padronização dos módulos da aplicação.

### Modelagem do Domínio

Implementação e refinamento das entidades:

- Empresa;
- Usuário;
- Cliente;
- Projeto;
- Orçamento;
- Unidade Consumidora;
- Titular;
- Concessionária;
- Homologação.

### Processo de Homologação

Implementação completa do Aggregate Root Homologação,
incluindo:

- documentos;
- versionamento documental;
- submissões;
- respostas da concessionária;
- exigências;
- histórico;
- movimentações;
- eventos de negócio;
- máquina de estados.

### Qualidade

- ampliação significativa da suíte de testes;
- consolidação das validações do domínio;
- garantia de atomicidade das operações críticas;
- padronização dos helpers internos.

### Documentação

- criação da documentação oficial;
- definição dos ADRs;
- atualização do modelo de domínio;
- registro das decisões arquitetônicas.

---

## Resultado

Ao término da Sprint 2 o sistema passou a possuir:

- domínio consolidado;
- arquitetura multicamadas estável;
- processo completo de homologação modelado;
- documentação sincronizada;
- base preparada para integração entre módulos.

A partir desse ponto o foco do projeto passa a ser a
integração do domínio ao fluxo operacional da aplicação,
marcando o início da Sprint 3.