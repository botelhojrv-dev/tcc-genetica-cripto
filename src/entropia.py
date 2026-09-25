"""
Métricas de entropia para marcadores genéticos forenses.

Quantifica a imprevisibilidade de perfis STR/SNP,
insumo fundamental para avaliar a viabilidade de
derivação de material criptográfico.
"""

import math
from collections import Counter
from typing import Iterable


def entropia_shannon(valores: Iterable) -> float:
    """
    Calcula a entropia de Shannon (em bits) de uma coleção de valores.

    Parâmetros
    ----------
    valores : iterable
        Repetições de alelos/marcadores observados.

    Retorno
    -------
    float
        Entropia H(X) = -Σ p(x) * log2(p(x)), em bits.

    Exemplo
    -------
    >>> round(entropia_shannon([1, 1, 2, 2]), 4)
    1.0
    """
    contagem = Counter(valores)
    if not contagem:
        raise ValueError("Coleção vazia não possui entropia definida.")
    total = sum(contagem.values())
    return -sum(
        (n / total) * math.log2(n / total) for n in contagem.values()
    )


def entropia_minima(amostras: int) -> float:
    """Entropia máxima possível para 'amostras' símbolos distintos."""
    return math.log2(amostras) if amostras > 1 else 0.0
    