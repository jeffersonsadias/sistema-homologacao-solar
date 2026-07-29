"""
Fachada pública dos status de Projeto.

Preserva compatibilidade com módulos que utilizam:

- STATUS_PROJETO;
- STATUS_INICIAL;
- TRANSICOES_PERMITIDAS;
- obter_status();
- status_valido();
- transicao_permitida();
- exibir_status().
"""

from app.dominio.status import (
    STATUS_PROJETO,
    STATUS_INICIAL,
    TRANSICOES_PERMITIDAS,
    obter_status,
    status_valido,
    transicao_permitida,
)

from app.interface.status_interface import (
    exibir_status,
)