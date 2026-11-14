"""Valida a hierarquia fundamental: H∞ ≤ H_Shannon ≤ H_máxima.

Ancora a distinção teórica da Seção 4.2 (min-entropia, Shannon e máxima)
em testes de regressão executáveis.
"""

import math

import pytest

from src.entropia import entropia_shannon, entropia_maxima, entropia_minima

TOL = 1e-12

CASOS = {
    "uniforme_5_alelos": ["a", "b", "c", "d", "e"],
    "uniforme_bialelico": ["A", "T"],
    "enviesada_estilo_D5S818": ["11"] * 42 + ["12"] * 32 + ["13"] * 13 + ["10"] * 13,
    "fortemente_enviesada": ["x"] * 90 + ["y"] * 5 + ["z"] * 5,
}


@pytest.mark.parametrize("nome,valores", CASOS.items())
def test_hierarquia_hinf_shannon_hmax(nome, valores):
    """Para qualquer distribuição: H∞ ≤ H(X) ≤ log₂(n símbolos)."""
    h_inf = entropia_minima(valores)
    h_shannon = entropia_shannon(valores)
    h_max = entropia_maxima(len(set(valores)))
    assert h_inf <= h_shannon + TOL, "violada: H∞ ≤ H_Shannon"
    assert h_shannon <= h_max + TOL, "violada: H_Shannon ≤ H_max"


def test_uniforme_faz_as_tres_coincidirem():
    """Sob distribuição uniforme, H∞ = H = log₂ n (caso de igualdade)."""
    valores = ["a", "b", "c", "d", "e"]
    assert entropia_minima(valores) == pytest.approx(entropia_shannon(valores))
    assert entropia_maxima(5) == pytest.approx(math.log2(5))


def test_minima_valor_conhecido_D5S818():
    """Genótipo mais provável com p = 0,2736 ⇒ H∞ ≈ 1,87 bits (caso D5S818).

    O complemento (0,7264) espalha-se por 14 genótipos menores,
    nenhum superando a classe dominante — como na distribuição real.
    """
    valores = ["g_max"] * 2736
    for i in range(13):
        valores += [f"g{i}"] * 528          # 13 × 528 = 6.864
    valores += ["g13"] * 400                # 6.864 + 400 = 7.264
    assert entropia_minima(valores) == pytest.approx(-math.log2(0.2736), abs=1e-9)