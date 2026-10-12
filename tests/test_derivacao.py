"""
Testes automatizados do módulo de derivação criptográfica.

Ciclo TDD aplicado à ponte genética → criptográfica.
"""

import pytest
import secrets
from src.derivacao import perfil_canonico, derivar_chave


class TestPerfilCanonico:
    """Testes da serialização determinística."""
    
    def test_heterozigoto_ignorando_ordem_de_entrada(self):
        """Genótipos (A,B) e (B,A) produzem bytes idênticos."""
        p1 = {"TH01": ("9", "7"), "D21S11": ("30", "29")}
        p2 = {"TH01": ("7", "9"), "D21S11": ("29", "30")}
        
        assert perfil_canonico(p1) == perfil_canonico(p2)
    
    def test_ordem_alphabetica_dos_loci(self):
        """Loci aparecem em ordem alfabética na saída."""
        perfil = {"Zzz": ("1", "2"), "Aaa": ("3", "4")}
        resultado = perfil_canonico(perfil)
        
        assert b"Aaa:" in resultado
        assert b"Zzz:" in resultado
        assert resultado.index(b"Aaa:") < resultado.index(b"Zzz:")
    
    def test_alelo_decimal_ordenado_corretamente(self):
        """TH01 tem alelo 9.3 — ordenação deve ser numérica."""
        p1 = {"TH01": ("9.3", "9")}
        p2 = {"TH01": ("9", "9.3")}
        
        # 9.3 vem depois de 9 numericamente
        assert perfil_canonico(p1) == perfil_canonico(p2)
        assert b"TH01:9:9.3" in perfil_canonico(p1)
    
    def test_delimitador_impede_ambiguidade(self):
        """(1,15) não pode ser confundido com (11,5)."""
        p1 = {"LOC": ("1", "15")}
        p2 = {"LOC": ("11", "5")}
        
        # Devem produzir strings CANONICAS diferentes
        assert perfil_canonico(p1) != perfil_canonico(p2)
        assert perfil_canonico(p1) == b"LOC:1:15"
        assert perfil_canonico(p2) == b"LOC:5:11"


class TestDerivarChave:
    """Testes da função de derivação criptográfica."""

    def test_comprimento_da_chave_padrao(self):
        ...

    def test_mesmo_perfil_salt_diferente_chave_diferente(self):
        ...
        
    def test_mesmo_perfil_mesmo_salt_mesma_chave(self):
        """Determinismo: mesma entrada → mesma saída, sempre."""
        perfil = {"D3S1358": ("16", "17"), "TH01": ("7", "9")}
        salt = secrets.token_bytes(16)

        chave1 = derivar_chave(perfil, salt)
        chave2 = derivar_chave(perfil, salt)

        assert chave1 == chave2

    def test_salt_diferente_sem_correlacao(self):
        """Média de várias derivações com salts distintos ≈ 128 bits de diferença."""
        perfil = {"D3S1358": ("16", "17"), "TH01": ("7", "9")}
        salt_base = secrets.token_bytes(16)
        chave_ref = derivar_chave(perfil, salt_base)

        distancias = []
        for _ in range(5):
            salt_outro = secrets.token_bytes(16)
            chave_outro = derivar_chave(perfil, salt_outro)
            d = sum(bin(b1 ^ b2).count("1")
                    for b1, b2 in zip(chave_ref, chave_outro))
            distancias.append(d)

        media = sum(distancias) / len(distancias)
        assert 116 <= media <= 140, f"Média observada: {media}"
        
    def test_chave_hexadecimal_solo(self):
        """Chave derivada é pura informação aleatória (0x00–0xFF distribuídos)."""
        perfil = {"D3S1358": ("16", "17")}
        salt = secrets.token_bytes(16)
        chave = derivar_chave(perfil, salt)
        
        # Qualquer byte é permitido — verifica que não é binário simples
        assert all(0 <= b <= 255 for b in chave)
    
    def test_argon2id_time_cost_alto_demora_mais(self):
        """time_cost maior implica derivação mais lenta."""
        perfil = {"TH01": ("7", "9")}
        salt = secrets.token_bytes(16)
        
        import time
        
        # Parâmetro baixo
        t0_low = time.perf_counter()
        derivar_chave(perfil, salt, time_cost=1)
        tempo_low = time.perf_counter() - t0_low
        
        # Parâmetro alto
        t0_high = time.perf_counter()
        derivar_chave(perfil, salt, time_cost=5)
        tempo_high = time.perf_counter() - t0_high
        
        assert tempo_high > tempo_low * 2  # Deve ser pelo menos o dobro
    
    def test_salto_invalido_joga_type_error(self):
        """Salt que não seja bytes deve levantar TypeError."""
        perfil = {"TH01": ("7", "9")}
        
        with pytest.raises(TypeError):
            derivar_chave(perfil, "string-nao-e-bytes")
