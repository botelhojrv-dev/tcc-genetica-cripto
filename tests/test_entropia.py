"""Testes do módulo de entropia."""

import pytest
from src.entropia import entropia_shannon, entropia_minima


class TestEntropiaShannon:
    def test_distribuicao_uniforme(self):
        """Duas classes equilibradas => exatamente 1 bit."""
        assert entropia_shannon(["A", "A", "T", "T"]) == pytest.approx(1.0)

    def test_deterministico_tem_entropia_zero(self):
        """Um único valor possível => zero bits de imprevisibilidade."""
        assert entropia_shannon([7, 7, 7, 7]) == 0.0

    def test_quanto_mais_classes_maior_entropia(self):
        h_binaria = entropia_shannon([1, 2])
        h_ternaria = entropia_shannon([1, 2, 3])
        assert h_ternaria > h_binaria

    def test_lanca_erro_em_lista_vazia(self):
        with pytest.raises(ValueError):
            entropia_shannon([])


# Corrige o comportamento com lista vazia adicionando validação:
# (inclua no módulo: if not contagem: raise ValueError("Coleção vazia)")
