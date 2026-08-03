# Regras de Negócio

## Objetivo

Este documento reúne as regras funcionais da SolarCore Platform.

Seu propósito é definir, de forma independente da implementação, o comportamento esperado do sistema. As regras aqui descritas representam o contrato funcional da plataforma e devem orientar tanto o desenvolvimento quanto os testes.

---

# Princípios Gerais

Todas as operações da plataforma devem observar os seguintes princípios:

* isolamento completo entre Empresas;
* rastreabilidade das operações;
* preservação da integridade dos dados;
* histórico de alterações sempre que aplicável;
* consistência das transições de estado;
* validação das regras de negócio antes da persistência.

---

# Empresas

## Cadastro

Uma Empresa representa uma organização que utiliza a plataforma.

### Regras

* cada Empresa possui um identificador único;
* Empresas são independentes entre si;
* dados de uma Empresa nunca podem ser acessados por outra;
* todos os registros operacionais pertencem a uma Empresa.

---

# Usuários

Todo Usuário pertence exatamente a uma Empresa.

## Estados permitidos

* Ativo
* Inativo
* Bloqueado
* Cancelado

## Regras

* apenas usuários ativos podem operar normalmente;
* usuários bloqueados não podem autenticar-se;
* usuários cancelados permanecem apenas para fins históricos;
* alterações de estado devem respeitar a máquina de estados definida.

---

# Clientes

Cliente representa quem contrata os serviços da Empresa.

## Regras

* inicialmente somente Pessoa Física;
* um Cliente pode possuir diversos Projetos;
* Cliente não representa necessariamente o Titular da Unidade Consumidora;
* exclusão física de Clientes deve ser evitada quando houver Projetos vinculados.

---

# Projetos

Projeto representa o processo completo de implantação e homologação de um sistema fotovoltaico.

## Regras

Todo Projeto deve possuir:

* uma Empresa;
* um Cliente;
* um status válido;
* exatamente uma Unidade Geradora.

Pode possuir:

* nenhuma;
* uma;
* várias Unidades Beneficiárias.

---

# Orçamentos

Orçamento representa uma proposta comercial.

## Regras

* pode existir sem Projeto;
* pode ser aprovado ou rejeitado;
* apenas um orçamento aprovado pode originar um Projeto;
* após convertido em Projeto, deve permanecer disponível para consulta histórica.

---

# Unidade Consumidora

Uma Unidade Consumidora assume papéis diferentes conforme o contexto do Projeto.

## Unidade Geradora

Regras:

* exatamente uma por Projeto;
* representa o local de instalação do sistema;
* caracteriza tecnicamente o Projeto.

## Unidade Beneficiária

Regras:

* quantidade variável;
* recebe compensação de créditos de energia;
* pode coexistir com a Unidade Geradora.

---

# Titular

Representa o responsável legal pela Unidade Consumidora.

## Regras

* pode ser Pessoa Física ou Jurídica;
* não precisa ser o Cliente da plataforma;
* alterações de titularidade devem ser registradas no histórico.

---

# Homologação

A Homologação representa todo o processo de aprovação do
Projeto perante a concessionária.

Ela coordena:

- documentos técnicos;
- submissões;
- respostas da concessionária;
- exigências;
- histórico de movimentações.

## Regras

- toda Homologação pertence a um único Projeto;
- documentos podem possuir múltiplas versões;
- toda Submissão deve respeitar sua sequência cronológica;
- respostas são vinculadas à Submissão correspondente;
- exigências pertencem a uma única Resposta;
- exigências somente podem ser atendidas por Submissões
  compatíveis;
- toda alteração relevante gera uma Movimentação;
- mudanças de estado devem respeitar a máquina de estados
  oficial da Homologação;
- o sistema deve preservar a consistência de todo o
  agregado antes da persistência.

## Estados

1. Aguardando documentação
2. Documentação recebida
3. Em análise pela distribuidora
4. Correção solicitada
5. Aprovado
6. Instalação concluída
7. Vistoria solicitada
8. Vistoria aprovada
9. Homologado
10. Cancelado

Cada transição deve obedecer à máquina de estados oficial da plataforma.

---

# Histórico

Sempre que ocorrer alteração relevante, o sistema deverá preservar evidências da mudança.

Exemplos:

* alteração de titular;
* alteração de carga instalada;
* alteração de Unidade Consumidora;
* mudança de status;
* atualização de documentação.

O histórico deve permitir auditoria completa.

---

# Concessionárias

Cada Projeto está vinculado a uma única concessionária.

## Regras

* a concessionária deve ser compatível com a Unidade Geradora;
* regras específicas poderão ser parametrizadas futuramente.

---

# Consistência dos Dados

A plataforma deve impedir:

* referências inválidas;
* duplicidades indevidas;
* estados inconsistentes;
* vínculos entre Empresas diferentes;
* perda de rastreabilidade.

---

# Auditoria

Toda alteração crítica poderá gerar um registro de auditoria contendo:

* data e hora;
* usuário responsável;
* operação realizada;
* entidade afetada;
* valores anteriores;
* novos valores.

Essa funcionalidade será expandida nas próximas versões.

---

# Evolução das Regras

Este documento é incremental.

Novas regras serão adicionadas à medida que novos módulos forem incorporados à SolarCore Platform.

As regras aqui definidas têm prioridade sobre detalhes de implementação. Sempre que houver divergência, o código deverá ser ajustado para refletir este documento.
