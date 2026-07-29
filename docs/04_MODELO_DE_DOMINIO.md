# Modelo de Domínio

## Objetivo

Este documento descreve o modelo conceitual da SolarCore Platform.

Seu propósito é representar as entidades do negócio, seus relacionamentos, responsabilidades e regras fundamentais, servindo como referência para toda a evolução da plataforma.

Toda nova funcionalidade deverá respeitar o modelo descrito neste documento.

---

# Linguagem Ubíqua (Ubiquitous Language)

A plataforma adota uma linguagem única para evitar ambiguidades entre desenvolvedores, analistas e usuários.

Os principais termos utilizados são:

| Termo                | Significado                                                       |
| -------------------- | ----------------------------------------------------------------- |
| Empresa              | Organização que utiliza a plataforma para gerenciar sua operação. |
| Usuário              | Pessoa autorizada a acessar a plataforma em nome de uma Empresa.  |
| Cliente              | Pessoa que contrata serviços da Empresa.                          |
| Projeto              | Processo técnico relacionado a uma instalação fotovoltaica.       |
| Orçamento            | Proposta comercial que pode originar um Projeto.                  |
| Unidade Consumidora  | Conta de energia vinculada ao Projeto.                            |
| Unidade Geradora     | Unidade onde o sistema fotovoltaico será instalado.               |
| Unidade Beneficiária | Unidade que receberá compensação de energia.                      |
| Titular              | Responsável legal pela Unidade Consumidora.                       |
| Concessionária       | Distribuidora de energia responsável pela homologação.            |
| Homologação          | Processo de aprovação do Projeto perante a concessionária.        |

---

# Visão Geral do Domínio

A SolarCore Platform foi concebida como uma plataforma SaaS multiempresa.

Cada Empresa administra seus próprios Clientes, Projetos e Usuários, sem compartilhar informações com outras Empresas.

```text
Empresa
│
├── Usuários
│
├── Clientes
│
│   └── Projetos
│       │
│       ├── Orçamento
│       ├── Unidade Geradora
│       ├── Unidades Beneficiárias
│       ├── Titular
│       └── Homologação
│
└── Configurações
```

---

# Entidades

## Empresa

Representa a organização que utiliza a plataforma.

É a entidade raiz da operação.

### Responsabilidades

* administrar Usuários;
* administrar Clientes;
* administrar Projetos;
* controlar permissões;
* isolar seus próprios dados.

### Relacionamentos

```text
Empresa

1 → N Usuários

1 → N Clientes

1 → N Projetos
```

---

## Usuário

Representa uma pessoa autorizada a operar a plataforma.

Todo Usuário pertence obrigatoriamente a uma única Empresa.

### Responsabilidades

* acessar a plataforma;
* executar operações conforme seu perfil;
* registrar ações no sistema.

### Estados

```text
ATIVO

INATIVO

BLOQUEADO

CANCELADO
```

---

## Cliente

Representa a pessoa que contrata os serviços da Empresa.

Inicialmente será sempre Pessoa Física.

O Cliente não representa necessariamente o titular da conta de energia.

Essa separação é intencional.

Um Cliente pode possuir diversos Projetos.

---

## Projeto

Representa todo o processo técnico relacionado à implantação de um sistema fotovoltaico.

É a principal entidade operacional da plataforma.

Todo Projeto pertence a:

* uma Empresa;
* um Cliente.

Cada Projeto possui exatamente:

* um status;
* uma Unidade Geradora.

E pode possuir:

* nenhuma ou várias Unidades Beneficiárias.

---

## Orçamento

Representa a proposta comercial apresentada ao Cliente.

Pode existir sem originar um Projeto.

Quando aprovado, transforma-se em Projeto.

---

## Unidade Consumidora

Representa uma conta de energia elétrica.

Dependendo do contexto do Projeto, pode assumir papéis diferentes.

### Papéis possíveis

```text
Unidade Geradora

Unidade Beneficiária
```

Essa distinção é contextual.

Fisicamente trata-se do mesmo conceito.

---

## Unidade Geradora

Representa a Unidade Consumidora onde será instalado o sistema fotovoltaico.

Cada Projeto possui exatamente uma.

---

## Unidade Beneficiária

Representa uma Unidade Consumidora participante da compensação de créditos de energia.

Um Projeto pode possuir nenhuma, uma ou diversas.

---

## Titular

Representa o responsável legal pela Unidade Consumidora.

Pode ser:

* Pessoa Física;
* Pessoa Jurídica.

O Titular não é necessariamente o Cliente da plataforma.

---

## Concessionária

Representa a distribuidora responsável pela análise e homologação do Projeto.

Cada Projeto está vinculado a apenas uma Concessionária.

---

# Agregados (Aggregates)

Para preservar a consistência do domínio, algumas entidades formam agregados.

## Agregado Empresa

Raiz:

```text
Empresa
```

Contém:

* Usuários;
* Clientes;
* Configurações.

---

## Agregado Projeto

Raiz:

```text
Projeto
```

Contém:

* Orçamento associado;
* Unidade Geradora;
* Unidades Beneficiárias;
* Titular;
* Histórico;
* Processo de Homologação.

Toda alteração nesses elementos deve ocorrer através do Projeto.

---

# Objetos de Valor (Value Objects)

Embora inicialmente sejam armazenados como estruturas simples, estes conceitos representam Objetos de Valor e poderão evoluir para classes próprias.

Exemplos:

* endereço;
* telefone;
* e-mail;
* potência instalada;
* consumo médio;
* tensão elétrica;
* coordenadas geográficas;
* datas de protocolo;
* número do protocolo.

---

# Serviços de Domínio

Algumas operações não pertencem exclusivamente a uma entidade.

Exemplos futuros:

* geração automática de protocolos;
* validação documental;
* cálculo de dimensionamento;
* distribuição de créditos;
* análise de elegibilidade.

Essas operações deverão ser implementadas como Serviços de Domínio.

---

# Limites de Contexto (Bounded Contexts)

A plataforma poderá evoluir para múltiplos contextos independentes.

Inicialmente são previstos:

```text
Gestão Corporativa

Homologação

CRM

Financeiro

Instalações

Pós-venda

Business Intelligence
```

Cada contexto possuirá seu próprio modelo interno, comunicando-se por interfaces bem definidas.

---

# Princípios do Modelo

Durante toda a evolução da plataforma deverão ser preservados os seguintes princípios:

* baixo acoplamento;
* alta coesão;
* isolamento entre Empresas;
* separação entre Cliente e Titular;
* centralização das regras de negócio;
* consistência transacional dos agregados;
* evolução incremental do domínio;
* documentação sincronizada com a implementação.

---

# Evolução do Modelo

Este documento representa o modelo oficial da SolarCore Platform.

Novas entidades poderão ser incorporadas conforme a evolução da plataforma, desde que mantenham compatibilidade com os princípios arquiteturais e com a linguagem ubíqua aqui estabelecida.

O objetivo é permitir que a plataforma cresça continuamente sem perda de consistência, tornando o domínio cada vez mais completo e expressivo.
