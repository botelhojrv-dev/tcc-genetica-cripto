# tests/test_determinismo.py
import secrets

from src.derivacao import derivar_chave, perfil_canonico

# Perfil representativo dos 5 loci, na forma real esperada pela função
PERFIL = {
    "D18S51": ("15", "17"),
    "D21S11": ("29", "31.2"),
    "D3S1358": ("15", "16"),
    "D5S818": ("11", "13"),
    "TH01": ("6", "9.3"),
}

SALT_FIXO = bytes.fromhex("00112233445566778899aabbccddeeff")


class TestDeterminismo:
    """Propriedade determinística: mesmo perfil + mesmo salt → mesma chave."""

    def test_mesmo_perfil_mesmo_salt_mesma_chave(self):
        salt = secrets.token_bytes(16)

        chave_1 = derivar_chave(PERFIL, salt)
        chave_2 = derivar_chave(PERFIL, salt)

        assert chave_1 == chave_2, (
            "Falha de determinismo: mesma entrada produziu chaves distintas"
        )
        assert len(chave_1) == 32, "Chave deveria ter 32 bytes (AES-256)"

    def test_repeticoes_multiplas_estaveis(self):
        """10 execuções confirmam estabilidade além do acaso."""
        chaves = {derivar_chave(PERFIL, SALT_FIXO) for _ in range(10)}

        assert len(chaves) == 1, (
            f"Determinismo violado: {len(chaves)} chaves distintas em 10 execuções"
        )

    def test_ordem_de_insercao_e_alelos_nao_afetam(self):
        """Canonização: ordem de loci e de alelos deve ser irrelevante."""
        perfil_reordenado = {
            "TH01": ("9.3", "6"),
            "D5S818": ("13", "11"),
            "D3S1358": ("16", "15"),
            "D21S11": ("31.2", "29"),
            "D18S51": ("17", "15"),
        }

        assert derivar_chave(PERFIL, SALT_FIXO) == derivar_chave(
            perfil_reordenado, SALT_FIXO
        ), "Canonização falhou: perfis equivalentes geraram chaves distintas"


def test_canonizacao_invariante():
    """Teste unitário direto da canonização, sem custo de KDF."""
    p1 = {"TH01": ("9", "7"), "D21S11": ("30", "29")}
    p2 = {"TH01": ("7", "9"), "D21S11": ("29", "30")}

    assert perfil_canonico(p1) == perfil_canonico(p2)
    assert perfil_canonico(p1) == b"D21S11:29:30|TH01:7:9"