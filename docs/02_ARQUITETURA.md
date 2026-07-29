# Arquitetura do Sistema

## Objetivo

Este documento descreve a arquitetura de software adotada pelo Sistema de Homologação Solar, definindo as responsabilidades de cada camada, as dependências permitidas entre módulos e os princípios utilizados durante o desenvolvimento.

O objetivo principal é garantir que o crescimento da plataforma ocorra de forma organizada, previsível e sustentável.

---

# Princípios Arquiteturais

A arquitetura foi concebida seguindo os seguintes princípios:

* Separação de responsabilidades.
* Baixo acoplamento entre módulos.
* Alta coesão.
* Centralização das regras de negócio.
* Facilidade de testes automatizados.
* Evolução incremental da plataforma.
* Preparação para múltiplas empresas (SaaS Multiempresa).
* Preparação para futura migração para banco de dados relacional.
* Preparação para APIs e interface web.

Cada decisão arquitetural deve preservar esses princípios.

---

# Arquitetura em Camadas

A aplicação está organizada em cinco camadas principais.

```text
                Interface
                    │
                    ▼
                 Fachada
                    │
                    ▼
                 Domínio
                    │
                    ▼
             Infraestrutura
                    │
                    ▼
              Persistência
```

Cada camada possui responsabilidades exclusivas.

Uma camada nunca deve assumir responsabilidades pertencentes à outra.

---

# Camada de Interface

Localização:

```text
app/interface/
```

Responsabilidades:

* interação com o operador;
* exibição de menus;
* leitura de entradas;
* apresentação de mensagens;
* apresentação de relatórios;
* chamada das funções públicas das fachadas.

A Interface **não pode**:

* validar regras de negócio;
* acessar JSON;
* alterar listas internas;
* implementar lógica do domínio.

Toda regra de negócio deve ser delegada.

---

# Camada de Fachada

Localização:

```text
app/
```

Exemplos:

```text
clientes.py
empresas.py
usuarios.py
projetos.py
orcamentos.py
```

A Fachada representa a API pública de cada módulo.

Responsabilidades:

* coordenar operações;
* integrar módulos;
* validar dependências externas;
* localizar entidades;
* chamar funções do domínio;
* persistir alterações;
* devolver objetos para a interface.

A Fachada não deve conter regras complexas do negócio.

Seu papel é coordenar.

---

# Camada de Domínio

Localização:

```text
app/dominio/
```

Esta é a camada mais importante do sistema.

Todo conhecimento do negócio deve estar concentrado aqui.

Responsabilidades:

* validações;
* regras de negócio;
* estados;
* transições;
* criação de objetos;
* consistência dos dados.

O Domínio nunca:

* grava JSON;
* imprime mensagens;
* solicita dados ao usuário;
* conhece menus.

---

# Camada de Infraestrutura

Localização:

```text
app/infraestrutura/
```

Responsabilidades:

* leitura dos arquivos;
* gravação dos arquivos;
* acesso ao mecanismo de persistência;
* adaptação entre domínio e armazenamento.

Atualmente utiliza JSON.

No futuro poderá utilizar PostgreSQL, MySQL ou outro banco de dados sem alterar as regras do domínio.

---

# Camada de Persistência

Atualmente:

```text
data/
```

Contém arquivos JSON.

Exemplos:

```text
clientes.json
empresas.json
usuarios.json
projetos.json
orcamentos.json
```

Essa camada não possui inteligência de negócio.

Ela apenas armazena dados.

---

# Fluxo Geral de Execução

Uma operação típica segue o fluxo abaixo.

```text
Operador
    │
    ▼
Interface
    │
    ▼
Fachada
    │
    ▼
Domínio
    │
    ▼
Infraestrutura
    │
    ▼
Persistência
```

O retorno percorre exatamente o caminho inverso.

---

# Dependências Permitidas

A arquitetura estabelece uma direção única para as dependências.

```text
Interface
      ↓

Fachada
      ↓

Domínio
      ↓

Infraestrutura
      ↓

Persistência
```

Nunca deve existir uma chamada no sentido contrário.

Exemplos proibidos:

```text
Domínio → Interface

Domínio → JSON

Infraestrutura → Interface

Persistência → Domínio
```

---

# Comunicação entre Módulos

Nenhum módulo deve alterar diretamente os dados internos de outro módulo.

Em vez disso, toda interação deve ocorrer através de funções públicas.

Exemplo correto:

```python
usuarios.obter_usuario(...)
```

Exemplo incorreto:

```python
usuarios.usuarios.append(...)
```

Essa regra reduz acoplamento e facilita futuras alterações internas.

---

# Organização do Projeto

Estrutura principal:

```text
app/
│
├── dominio/
├── infraestrutura/
├── interface/
│
├── clientes.py
├── empresas.py
├── usuarios.py
├── projetos.py
├── orcamentos.py
├── menu.py
```

Cada módulo possui responsabilidades claramente definidas.

---

# Tratamento de Erros

O sistema utiliza exceções para representar falhas de negócio.

Fluxo:

```text
Domínio
      ↓
Fachada
      ↓
Interface
      ↓
Operador
```

A Interface é responsável apenas por apresentar mensagens amigáveis.

As camadas inferiores não exibem mensagens diretamente.

---

# Testabilidade

Toda arquitetura foi planejada para facilitar testes automatizados.

Cada camada pode ser testada isoladamente através do uso de mocks.

A separação das responsabilidades reduz dependências e aumenta a confiabilidade da suíte de testes.

---

# Escalabilidade

Embora a versão atual utilize arquivos JSON, a arquitetura foi preparada para evolução.

As próximas etapas previstas incluem:

* banco de dados relacional;
* autenticação;
* API REST;
* interface web;
* processamento assíncrono;
* integrações externas;
* notificações automáticas;
* múltiplas empresas;
* múltiplos usuários simultâneos.

Essas evoluções poderão ocorrer sem reestruturar o núcleo do domínio.

---

# Visão Arquitetural

A arquitetura adotada prioriza simplicidade, clareza e baixo acoplamento.

Cada camada possui responsabilidades bem definidas e comunica-se apenas com a camada imediatamente inferior.

Essa organização permite que o Sistema de Homologação Solar evolua gradualmente de uma aplicação de terminal para uma plataforma SaaS completa, preservando a estabilidade do código e reduzindo o impacto das futuras expansões.
