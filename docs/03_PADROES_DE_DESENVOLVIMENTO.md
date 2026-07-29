# Padrões de Desenvolvimento

## Objetivo

Este documento estabelece os padrões oficiais de desenvolvimento da SolarCore Platform.

Seu propósito é garantir que todo código produzido siga uma mesma filosofia arquitetural, mantendo consistência, legibilidade, facilidade de manutenção e evolução contínua.

Todos os módulos atuais e futuros deverão respeitar estes padrões.

---

# Filosofia de Desenvolvimento

A SolarCore Platform é desenvolvida priorizando:

* clareza antes de complexidade;
* simplicidade antes de otimização prematura;
* evolução incremental;
* documentação contínua;
* testes automatizados;
* separação de responsabilidades.

Cada alteração deve tornar o sistema mais organizado do que antes.

---

# Estrutura do Projeto

A estrutura principal da aplicação é:

```text
app/
docs/
data/
tests/
```

### Responsabilidades

| Diretório | Responsabilidade          |
| --------- | ------------------------- |
| app       | Código-fonte da aplicação |
| docs      | Documentação técnica      |
| data      | Persistência dos dados    |
| tests     | Testes automatizados      |

---

# Organização dos Módulos

Cada módulo deverá possuir uma responsabilidade claramente definida.

Exemplo:

```text
clientes.py
usuarios.py
empresas.py
projetos.py
orcamentos.py
```

Cada módulo atua como a fachada pública de seu domínio.

---

# Organização Interna

Sempre que possível, os módulos seguirão esta ordem:

1. Imports
2. Constantes
3. Variáveis globais controladas
4. Funções privadas
5. Funções públicas
6. Menus

Essa organização facilita leitura e manutenção.

---

# Convenção de Nomes

## Arquivos

Utilizar:

```text
snake_case.py
```

Exemplo:

```text
historico.py
repositorio_clientes_json.py
```

---

## Funções

Utilizar verbos.

Exemplos:

```python
cadastrar_cliente()
buscar_cliente()
listar_clientes()
salvar_projetos()
```

Evitar nomes genéricos como:

```python
processar()
executar()
teste()
```

---

## Variáveis

Utilizar nomes descritivos.

Bom exemplo:

```python
codigo_cliente
potencia_instalada
unidade_geradora
```

Evitar:

```python
x
a
temp
lista2
```

---

# Encapsulamento

Funções auxiliares devem ser privadas.

Exemplo:

```python
def _validar_cpf():
```

A Interface deve utilizar apenas funções públicas.

---

# Comunicação entre Módulos

É proibido acessar diretamente estruturas internas de outro módulo.

Exemplo incorreto:

```python
usuarios.append(...)
```

Exemplo correto:

```python
usuarios.cadastrar_usuario(...)
```

Essa regra reduz acoplamento e protege a evolução interna dos módulos.

---

# Responsabilidade das Camadas

## Interface

Responsável apenas por:

* interação com o usuário;
* menus;
* entrada de dados;
* apresentação de informações.

Nunca deve conter regras de negócio.

---

## Fachada

Responsável por coordenar operações entre módulos.

Nunca deve armazenar conhecimento do negócio.

---

## Domínio

Toda regra de negócio pertence ao domínio.

O domínio:

* valida;
* cria objetos;
* controla estados;
* aplica regras.

Nunca:

* imprime mensagens;
* lê teclado;
* grava arquivos.

---

## Infraestrutura

Responsável apenas pela persistência.

Pode ser substituída sem alterar o domínio.

---

# Tratamento de Erros

Erros de negócio devem utilizar exceções específicas.

Exemplo:

```python
ClienteNaoEncontradoError
ProjetoInvalidoError
```

A Interface é responsável por transformar essas exceções em mensagens compreensíveis para o usuário.

---

# Persistência

Atualmente utiliza arquivos JSON.

Nenhum módulo deve acessar arquivos diretamente.

Todo acesso deverá ocorrer através dos repositórios da camada de infraestrutura.

---

# Testes Automatizados

Toda funcionalidade nova deverá possuir testes correspondentes.

Os testes devem validar:

* comportamento esperado;
* cenários alternativos;
* tratamento de erros;
* casos de borda.

Sempre que um defeito for corrigido, um teste deve ser criado para evitar regressões.

---

# Documentação

Toda mudança significativa deve atualizar, quando aplicável:

* Visão Geral;
* Arquitetura;
* Modelo de Domínio;
* Regras de Negócio;
* Sprint correspondente;
* Changelog.

Código e documentação devem evoluir juntos.

---

# Git

Cada commit deve representar uma alteração lógica e coerente.

Mensagens de commit devem ser claras.

Exemplos:

```text
feat: adiciona gerenciamento de usuários

fix: corrige validação de CPF

refactor: simplifica fachada de projetos

test: adiciona testes de estados dos usuários

docs: atualiza modelo de domínio
```

---

# Princípios de Projeto

A SolarCore Platform adota gradualmente princípios inspirados em boas práticas de engenharia de software.

Entre eles:

* responsabilidade única (Single Responsibility);
* baixo acoplamento;
* alta coesão;
* encapsulamento;
* composição antes de duplicação;
* orientação ao domínio;
* separação entre infraestrutura e regras de negócio.

Esses princípios orientam toda decisão técnica da plataforma.

---

# Evolução Contínua

Este documento deverá ser revisado periodicamente.

Novos padrões poderão ser incorporados conforme a plataforma evoluir, desde que mantenham compatibilidade com a arquitetura existente e contribuam para a qualidade do software.
