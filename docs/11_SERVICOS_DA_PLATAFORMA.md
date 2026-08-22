# 11 — Serviços da Plataforma

## 1. Objetivo

Este documento registra a modelagem, as decisões arquiteturais, as regras de negócio e a evolução da implementação do ecossistema de Serviços da Plataforma.

O objetivo é permitir que Clientes e Empresas interajam para solicitação, negociação, contratação, execução e acompanhamento de serviços relacionados ao sistema fotovoltaico.

A plataforma deve suportar dois grandes grupos iniciais:

- instalação de sistemas fotovoltaicos;
- serviços de pós-venda.

A arquitetura deve permanecer extensível para novos tipos de serviço no futuro.

Este documento é incremental e deve ser atualizado conforme a implementação evoluir.

---

## 2. Visão geral do ecossistema

O fluxo comercial geral é:

```text
TIPO DE SERVIÇO
       ↓
SERVIÇO OFERTADO PELA EMPRESA

CLIENTE
       ↓
SOLICITAÇÃO DE SERVIÇO
       ↓
PROPOSTA / ORÇAMENTO
       ↓
ACEITE
       ↓
CONTRATAÇÃO
       ↓
PROCESSO OPERACIONAL
```

O processo operacional depende do tipo de serviço.

### Instalação fotovoltaica

```text
Solicitação
    ↓
Orçamento Fotovoltaico
    ↓
Aceite
    ↓
Contratação
    ↓
Projeto
    ↓
Homologação
    ↓
Instalação
```

### Pós-venda

```text
Solicitação
    ↓
Proposta de Serviço
    ↓
Aceite
    ↓
Contratação
    ↓
Ordem de Serviço
    ↓
Execução
    ↓
Conclusão
```

---

## 3. Atores

### 3.1 Cliente

O Cliente pode:

- pesquisar Empresas;
- consultar serviços oferecidos;
- solicitar serviço diretamente a uma Empresa;
- publicar uma solicitação aberta no marketplace;
- responder perguntas das Empresas;
- receber propostas;
- comparar propostas;
- aceitar uma proposta;
- acompanhar a contratação;
- acompanhar a execução;
- contestar a conclusão quando necessário;
- avaliar o serviço realizado.

### 3.2 Empresa

A Empresa pode:

- configurar os serviços que oferece;
- ativar ou desativar serviços;
- definir sua forma de precificação;
- configurar área de atendimento;
- aceitar solicitações diretas;
- participar ou não do marketplace;
- visualizar oportunidades elegíveis;
- solicitar informações complementares;
- apresentar propostas;
- revisar propostas;
- retirar propostas;
- formalizar contratações;
- executar serviços;
- registrar diagnósticos, materiais, evidências e retornos.

### 3.3 Plataforma

A Plataforma deve:

- manter o catálogo mestre;
- controlar elegibilidade;
- distribuir oportunidades;
- proteger os dados de contato do Cliente quando aplicável;
- preservar negociações;
- coordenar aceite e contratação;
- preservar histórico;
- registrar auditoria;
- permitir evolução futura de ranking e reputação.

---

## 4. Catálogo de Serviços

A plataforma possuirá um Catálogo Mestre de Tipos de Serviço.

Exemplos:

- Instalação de Sistema Fotovoltaico;
- Manutenção Preventiva;
- Manutenção Corretiva;
- Limpeza de Módulos;
- Diagnóstico de Baixa Geração;
- Termografia;
- Manutenção de Inversor;
- Substituição de Inversor;
- Substituição de Módulo;
- Reparo Elétrico;
- Monitoramento;
- Visita Técnica;
- Laudo Técnico.

A existência de um serviço no catálogo mestre não obriga todas as Empresas a oferecê-lo.

---

## 5. Serviços oferecidos pelas Empresas

Cada Empresa configura individualmente os serviços que presta.

Estrutura implementada nesta fase:

```text
SERVICO_OFERTADO_EMPRESA

codigo
codigo_empresa
codigo_tipo_servico
modelo_precificacao
valor
aceita_solicitacao_direta
participa_marketplace
area_atendimento
ativo
```

A Empresa poderá:

- ativar/desativar serviços;
- definir preço;
- trabalhar sob consulta;
- definir preço por unidade;
- configurar área específica por serviço;
- participar ou não do marketplace.

A área específica do serviço poderá sobrescrever a área padrão da Empresa.

---

## 6. Serviços personalizados

Além dos tipos padrão da plataforma, uma Empresa poderá cadastrar serviços próprios.

Um Tipo de Serviço poderá ter origem:

```text
PADRAO_PLATAFORMA
PERSONALIZADO_EMPRESA
```

Um serviço personalizado pertence à Empresa que o criou e não deve automaticamente integrar o catálogo das demais Empresas.

---

## 7. Formas de precificação

O domínio deve admitir diferentes formas de precificação.

Modelos implementados nesta fase:

```text
ORCAMENTO
PRECO_FIXO
A_PARTIR_DE
SOB_CONSULTA
```

O preço configurado no catálogo da Empresa não substitui o valor definitivo apresentado em uma proposta quando houver negociação.

---

## 8. Solicitação de Serviço

A Solicitação representa uma necessidade apresentada por um Cliente.

Modalidades:

```text
DIRETA
ABERTA
```

### 8.1 Solicitação direta

O Cliente escolhe uma Empresa específica.

Apenas essa Empresa recebe a solicitação.

### 8.2 Solicitação aberta

O Cliente publica sua necessidade no marketplace.

A plataforma determina quais Empresas são elegíveis para visualizar e responder.

---

## 9. Origem da Solicitação

A origem deve ser separada da modalidade.

Exemplos:

```text
CLIENTE_PLATAFORMA
EMPRESA
```

Isso permite que uma Empresa registre no sistema um atendimento originado fora da plataforma sem alterar o significado de solicitação direta ou aberta.

---

## 10. Dados técnicos da Solicitação

Cada tipo de serviço pode exigir informações diferentes.

Por isso, a Solicitação não deve possuir dezenas de campos técnicos universais.

Ela deve admitir uma estrutura específica de dados técnicos conforme o serviço.

Exemplo — Instalação Fotovoltaica:

```text
consumo_medio_kwh
valor_medio_conta
tipo_imovel
tipo_ligacao
tipo_cobertura
```

Exemplo — Limpeza:

```text
quantidade_modulos
potencia_sistema_kwp
tipo_cobertura
altura_aproximada
ultima_limpeza
```

---

## 11. Privacidade comercial

A privacidade comercial dos Serviços da Plataforma é uma regra
explícita de domínio.

A simples existência dos dados de contato do Cliente não
significa que uma Empresa possua autorização para acessá-los.

A política implementada separa:

dados do Cliente
≠
permissão de acesso aos dados

### 11.1 Nome do Cliente

O nome do Cliente é visível tanto em solicitações diretas quanto abertas.

### 11.2 Solicitação direta

Quando o Cliente envia uma solicitação diretamente para uma Empresa específica:

Nome       → visível
Telefone   → visível para a Empresa destinatária
E-mail     → visível para a Empresa destinatária

### 11.3 Solicitação aberta

Quando o Cliente publica uma solicitação no marketplace:

Nome       → visível
Telefone   → oculto
E-mail     → oculto
WhatsApp   → oculto

A negociação deverá ocorrer dentro da plataforma.

### 11.4 Liberação após aceite

Quando uma proposta de uma solicitação aberta for aceita:

Empresa vencedora
→ recebe autorização para acessar o contato

Demais Empresas
→ continuam sem acesso

A autorização deve ser específica para Cliente + Empresa + Solicitação/Contratação.

---

## 12. Localização e privacidade

Para solicitações abertas, a Empresa poderá receber:

- município;
- UF;
- bairro/região, quando necessário;
- distância aproximada;
- informações técnicas relevantes.

Não é necessário revelar inicialmente:

- número do imóvel;
- coordenada exata;
- informação que permita contato direto indevido.

A plataforma poderá manter localização mais precisa internamente para cálculo de elegibilidade.

---

## 13. Comunicação interna

Solicitações abertas devem permitir comunicação interna entre Cliente e cada Empresa participante.

Cada Empresa possui uma conversa independente.

Solicitação
├── Conversa Empresa A
├── Conversa Empresa B
└── Conversa Empresa C

Uma Empresa não pode acessar a conversa de outra.

O sistema deverá permanecer preparado para moderação de compartilhamento de contatos externos antes do aceite.

---

## 14. Elegibilidade das Empresas

Uma Empresa é elegível para uma Solicitação aberta quando, no mínimo:

empresa_ativa
AND servico_ativo
AND participa_marketplace
AND area_atendimento_compativel
AND cadastro_habilitado

Elegibilidade, ranking, visibilidade e notificação são conceitos distintos.

### Solicitação direta

Para solicitação direta:

empresa_ativa
AND servico_ativo
AND aceita_solicitacao_direta

A área de atendimento não precisa necessariamente bloquear uma solicitação direta.

---

## 15. Área de atendimento

A Área de Atendimento representa a cobertura geográfica associada a uma oferta de serviço da Empresa.

Foi implementada como entidade própria:

AREA_ATENDIMENTO

modalidade
municipio_base
uf_base
raio_km
municipios

---

## 16. Proposta de Serviço

A Proposta representa a resposta comercial de uma Empresa
a uma Solicitação de Serviço.

O núcleo comercial implementado é dividido em:

PROPOSTA_SERVICO

codigo
codigo_solicitacao
codigo_empresa
codigo_servico_ofertado_empresa
status
historico_de_versoes

VERSAO_PROPOSTA_SERVICO

numero
valor
prazo_execucao_dias
validade
descricao_tecnica
itens_incluidos
itens_nao_incluidos
garantias
condicoes_comerciais
observacoes

## 17. Versionamento das Propostas

Uma Proposta já enviada não deve ser sobrescrita silenciosamente.

Exemplo:

V1 — R$ 20.000
V2 — R$ 19.500
V3 — R$ 19.000

---

## 18. Máquina de Estados — Solicitação

Estado inicial:

EM_ELABORACAO

Estados:

EM_ELABORACAO
PUBLICADA
RECEBENDO_PROPOSTAS
EM_ANALISE_PELO_CLIENTE
ENCERRADA_COM_CONTRATACAO
ENCERRADA_SEM_CONTRATACAO
CANCELADA
EXPIRADA

Estados terminais:

ENCERRADA_COM_CONTRATACAO
ENCERRADA_SEM_CONTRATACAO
CANCELADA
EXPIRADA

Solicitações terminais não devem ser reabertas. Uma nova necessidade gera uma nova Solicitação.

---

## 19. Máquina de Estados — Proposta

Estado inicial:

EM_ELABORACAO

Estados:

EM_ELABORACAO
ENVIADA
EM_REVISAO
REVISADA
ACEITA
RECUSADA
NAO_SELECIONADA
RETIRADA
EXPIRADA

Estados terminais:

ACEITA
RECUSADA
NAO_SELECIONADA
RETIRADA
EXPIRADA

`RECUSADA` representa rejeição explícita do Cliente.

`NAO_SELECIONADA` representa proposta concorrente que perdeu porque outra proposta foi escolhida.

### Regras implementadas da máquina

A máquina de estados pertence a:

app/dominio/status_proposta_servico.py

---

## 20. Aceite da Proposta

O aceite é uma operação coordenada.

Em uma Solicitação aberta:

Proposta vencedora → ACEITA
Demais propostas → NAO_SELECIONADA
Solicitação → ENCERRADA_COM_CONTRATACAO
Contratação → criada
Contato → liberado somente para a vencedora
Histórico → registrado

O aceite deve:

- validar a Solicitação;
- validar a Proposta;
- validar a versão;
- validar a Empresa;
- impedir múltiplas vencedoras;
- ser idempotente;
- impedir estados parcialmente alterados em caso de falha.

---

## 21. Contratação de Serviço

A Contratação representa a formalização comercial originada
de uma versão aceita de uma Proposta de Serviço.

O agregado implementado é composto por:


CONTRATACAO_SERVICO

codigo
codigo_solicitacao
codigo_cliente
codigo_tipo_servico
codigo_empresa
codigo_servico_ofertado_empresa
codigo_proposta
snapshot
data_limite_formalizacao
processo_operacional
status

---

## 22. Instalação Fotovoltaica

Instalação Fotovoltaica é um serviço padrão central da plataforma.

A Empresa poderá ativá-lo ou desativá-lo.

Para instalação fotovoltaica, o Orçamento Fotovoltaico existente deve ser integrado ao conceito de proposta comercial, evitando duplicar a mesma negociação em `PropostaServico` e `Orcamento`.

Fluxo conceitual:

Solicitação
    ↓
Orçamento Fotovoltaico
    ↓
Aceite
    ↓
Contratação
    ↓
Projeto
    ↓
Homologação
    ↓
Instalação

A integração exata com o domínio atual de Orçamentos será definida durante a implementação.

---

## 23. Ordem de Serviço Pós-venda

A Ordem de Serviço Pós-venda representa o agregado operacional
responsável pela execução de um serviço de pós-venda originado
de uma Contratação de Serviço.

Módulo implementado:

app/dominio/ordens_servico_pos_venda.py

---

## 24. Execuções e visitas

Uma Ordem de Serviço poderá possuir múltiplas execuções ou
visitas técnicas.

Cada execução é representada por um registro imutável associado
ao histórico da Ordem.

Estrutura implementada:

EXECUCAO_ORDEM_SERVICO

numero
data
responsavel
tecnicos
hora_inicio
hora_fim
descricao_executada
diagnostico_encontrado
solucao_aplicada
materiais_utilizados
observacoes
resultado

---

## 25. Evidências técnicas

O domínio deve permitir evidências como:

FOTO_ANTES
FOTO_DEPOIS
VIDEO
LAUDO
MEDICAO
RELATORIO
COMPROVANTE
OUTRO

Tipos específicos de serviço poderão exigir determinadas evidências.

---

## 26. Cobertura financeira

A execução de um serviço poderá ocorrer como:

GARANTIA
COBRADO
CORTESIA
CONTRATO


O status financeiro deve permanecer separado do status operacional.

Exemplo de estados financeiros:

NAO_APLICAVEL
PENDENTE
PARCIAL
PAGO
ATRASADO
CANCELADO

---

## 27. Garantias

Devem ser diferenciadas:


GARANTIA_ORIGINAL
GARANTIA_GERADA_PELO_SERVICO

Também deve ser identificado o responsável:

EMPRESA
FABRICANTE
TERCEIRO

Uma nova garantia gerada por uma manutenção não altera retroativamente a garantia original da instalação.

---

## 28. Alteração de escopo

Quando surgir trabalho adicional durante a execução, o valor contratado original não deve ser sobrescrito.

Deve ser utilizado futuramente um mecanismo como:

ADITIVO_SERVICO

ou:

ORCAMENTO_COMPLEMENTAR

O Cliente deve aprovar o novo escopo antes da execução adicional quando houver cobrança.

---

## 29. Encerramento da Ordem de Serviço

O encerramento operacional da Ordem de Serviço depende do
resultado técnico e da manifestação do Cliente.

Quando uma execução é registrada como:

RESOLVIDO

---

## 30. Avaliação

Após a conclusão, o Cliente poderá avaliar a Empresa.

A avaliação poderá considerar:

- nota geral;
- qualidade;
- prazo;
- atendimento;
- comentário.

A avaliação deve estar vinculada a uma Ordem de Serviço ou processo efetivamente concluído.

---

## 31. Histórico e Auditoria

Mudanças relevantes não devem existir apenas como estado atual.

Devem ser preservados eventos de:

- Solicitação;
- Proposta;
- Contratação;
- Ordem de Serviço;
- Garantia;
- autorização de contato;
- execução;
- cancelamento;
- alterações automáticas do sistema.

Movimentações devem registrar, quando aplicável:

tipo_evento
data_hora
ator_tipo
ator_codigo
status_anterior
status_novo
descricao
dados_anteriores
dados_novos

Tipos de ator:

CLIENTE
EMPRESA
PLATAFORMA
SISTEMA

---

## 32. Autorização de contato

A liberação de dados de contato possui entidade própria de
domínio e rastreabilidade independente.

Módulo implementado:

app/dominio/privacidade_servicos.py

---

## 33. Exclusão lógica

Entidades que participaram de operações reais não devem ser fisicamente excluídas.

Exemplos:

- Solicitação;
- Proposta;
- Contratação;
- Ordem de Serviço;
- Garantia;
- Avaliação.

Devem ser encerradas, canceladas ou inativadas conforme as regras do domínio.

---

## 34. Histórico x Notificação

Histórico de domínio e notificação são responsabilidades distintas.

MOVIMENTACAO
→ fato permanente

NOTIFICACAO
→ comunicação ao usuário

Uma falha de notificação não pode apagar ou invalidar o acontecimento de domínio.

---

## 35. Módulos previstos

Ordem inicial prevista para implementação:

app/dominio/tipos_servico.py
app/dominio/areas_atendimento.py
app/dominio/servicos_empresa.py

app/dominio/status_solicitacao_servico.py
app/dominio/status_proposta_servico.py
app/dominio/status_contratacao_servico.py
app/dominio/status_ordem_servico.py

app/dominio/solicitacoes_servico.py
app/dominio/propostas_servico.py
app/dominio/contratacoes_servico.py
app/dominio/ordens_servico_pos_venda.py

app/dominio/privacidade_servicos.py
app/dominio/movimentacoes_servicos.py

A coordenação entre agregados será definida após a implementação das responsabilidades locais.

---

## 36. Princípios arquiteturais

1. Cada módulo manipula seus próprios dados e regras.
2. Um módulo não deve modificar diretamente a estrutura interna de outro módulo.
3. Operações que atravessam agregados devem ser coordenadas por camada apropriada.
4. Estado atual e histórico são responsabilidades distintas.
5. Regras devem ser implementáveis e testáveis.
6. Dados comerciais aceitos devem ser preservados por snapshot/versionamento.
7. Fluxos não devem depender de comparação textual com nomes de serviços.
8. O domínio deve permanecer extensível para novos tipos de serviço.
9. Privacidade deve ser regra de domínio, não apenas ocultação visual.
10. Falhas parciais não podem deixar agregados em estados contraditórios.

---

## 37. Decisões consolidadas

Estão aprovadas nesta fase:

- existência de catálogo mestre;
- ativação individual de serviços pelas Empresas;
- serviços personalizados;
- solicitação direta;
- solicitação aberta;
- nome do Cliente sempre visível;
- contato visível em solicitação direta para a Empresa destinatária;
- contato oculto em solicitação aberta;
- liberação do contato após aceite somente para a Empresa vencedora;
- comunicação interna no marketplace;
- elegibilidade por serviço e área;
- área específica por serviço;
- modalidades de Área de Atendimento `RAIO`, `MUNICIPIOS` e `NACIONAL`;
- participação no marketplace separada da elegibilidade operacional;
- oferta sem Área de Atendimento não é elegível operacionalmente para o marketplace;
- Área de Atendimento não realiza cálculo geográfico;
- compatibilidade geográfica com uma Solicitação será tratada separadamente;
- propostas versionadas;
- apenas uma proposta vencedora por Solicitação;
- propostas concorrentes classificadas como `NAO_SELECIONADA`;
- criação de Contratação após aceite;
- snapshot das condições contratadas;
- Ordem de Serviço para pós-venda;
- múltiplas execuções/visitas;
- evidências técnicas;
- garantia original separada de garantia de serviço;
- garantia de fabricante separada da garantia da Empresa;
- confirmação/contestação da conclusão pelo Cliente;
- status financeiro separado do operacional;
- avaliação após conclusão;
- histórico e auditoria permanentes;
- exclusão lógica das entidades comerciais relevantes.

---

## 38. Decisões ainda abertas

Os seguintes pontos permanecem para refinamento durante implementação ou fases futuras:

- limite de Empresas que recebem cada oportunidade;
- limite de propostas por Solicitação;
- algoritmo de ranking;
- prazo de confirmação da conclusão pelo Cliente;
- estratégia inicial de cálculo de distância;
- múltiplas bases operacionais;
- regras detalhadas de moderação do chat;
- auditoria de visualização de dados sensíveis;
- assinatura eletrônica/contratual;
- regras de pagamento;
- mecanismo definitivo de aditivo/orçamento complementar;
- integração técnica exata entre `PropostaServico` e o `Orcamento` fotovoltaico existente;
- modelagem definitiva de anexos/documentos vinculados à Proposta e às suas versões comerciais.

---

## 39. Roadmap de implementação

### 39.1 — Domínio

- [x] Tipos de Serviço / Catálogo Mestre
- [x] Serviços oferecidos pelas Empresas
- [x] Status das entidades
- [x] Solicitação de Serviço
- [x] Proposta de Serviço
- [x] Contratação de Serviço
- [x] Ordem de Serviço Pós-venda
- [x] Privacidade e autorização de contato
- [ ] Movimentações e auditoria
- [ ] Coordenação entre agregados

### 39.2 — Persistência

- [ ] Repositórios
- [ ] Serialização
- [ ] Integridade dos relacionamentos

### 39.3 — Fachadas

- [ ] Operações de aplicação
- [ ] Coordenação dos fluxos

### 39.4 — Interfaces

- [ ] Ambiente Empresa
- [ ] Ambiente Cliente

### 39.5 — Marketplace e indicadores

- [ ] Oportunidades
- [ ] Propostas
- [ ] Ranking futuro
- [ ] Indicadores

### 39.6 — Fechamento

- [ ] Regressão completa
- [ ] Documentação final
- [ ] Atualização do índice
- [ ] Changelog
- [ ] Commit de fechamento

---

## 40. Registro de evolução

### Fase 40.1 — Modelagem

Status: CONCLUÍDA.

Foram modelados:

- catálogo;
- marketplace;
- privacidade;
- Solicitações;
- Propostas;
- Contratações;
- Ordens de Serviço;
- elegibilidade;
- execução;
- garantias;
- encerramento;
- histórico e auditoria.

### Fase 40.2 — Implementação do domínio

Status: EM ANDAMENTO.

#### 40.2.2 — Tipos / Catálogo Mestre de Serviços

Status: CONCLUÍDA.

Módulo implementado:

app/dominio/tipos_servico.py

#### 40.2.3 — Serviços oferecidos pelas Empresas

Status: CONCLUÍDA.

Módulos concluídos nesta etapa:

app/dominio/areas_atendimento.py
app/dominio/servicos_empresa.py

##### Fechamento da 40.2.3

A etapa de Serviços oferecidos pelas Empresas foi concluída após auditoria estrutural, revisão das regras de negócio e regressão completa do sistema.

A entidade `ServicoOfertadoEmpresa` representa o vínculo único entre:

Empresa
+
Tipo de Serviço

#### 40.2.4 — Status das entidades

Status: CONCLUÍDA.

Módulos implementados:

app/dominio/status_solicitacao_servico.py
app/dominio/status_proposta_servico.py
app/dominio/status_contratacao_servico.py
app/dominio/status_ordem_servico.py

#### 40.2.5 — Solicitação de Serviço

Status: CONCLUÍDA.

Módulo implementado:

app/dominio/solicitacoes_servico.py

#### 40.2.6 — Proposta de Serviço

Status: CONCLUÍDA.

Módulos consolidados nesta etapa:

app/dominio/propostas_servico.py
app/dominio/status_proposta_servico.py

#### 40.2.7 — Contratação de Serviço

Status: CONCLUÍDA.

Módulos consolidados nesta etapa:

app/dominio/contratacoes_servico.py
app/dominio/status_contratacao_servico.py


#### 40.2.8 — Ordem de Serviço Pós-venda

Status: CONCLUÍDA.

Módulos consolidados nesta etapa:

app/dominio/ordens_servico_pos_venda.py
app/dominio/status_ordem_servico.py

#### 40.2.9 — Privacidade e autorização de contato

Status: CONCLUÍDA.

Módulo consolidado nesta etapa:

app/dominio/privacidade_servicos.py





