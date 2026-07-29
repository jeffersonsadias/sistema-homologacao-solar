"""
Fachada pública dos status de Orçamento.

Preserva a compatibilidade com os módulos que utilizam:

- STATUS_ORCAMENTO;
- STATUS_INICIAL;
- TRANSICOES_PERMITIDAS;
- obter_status();
- status_valido();
- transicao_permitida();
- exibir_status().
"""

from app.dominio.status_orcamento import (
    STATUS_ORCAMENTO,
    STATUS_INICIAL,
    TRANSICOES_PERMITIDAS,
    obter_status,
    status_valido,
    transicao_permitida,
)

from app.interface.status_orcamento_interface import (
    exibir_status,
)