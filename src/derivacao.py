"""
Módulo de derivação de chave criptográfica a partir de perfis STR forenses.

Transforma perfis genéticos em material criptográfico (32 bytes)
via Argon2id memory-hard KDF, com serialização determinística.

Autor: Ricardo
Data: Setembro 2026
"""

from typing import Dict

import argon2
from argon2.low_level import hash_secret_raw, Type


def perfil_canonico(perfil: Dict[str, tuple]) -> bytes:
    """
    Serializa um perfil STR em bytes canônicos.

    Garante que o mesmo genótipo produza sempre a mesma representação
    de bytes, independentemente da ordem de iteração ou sorteio.

    Regras de canonização:
    1. Loci ordenados alfabeticamente
    2. Alelos dentro de cada locus ordenados numericamente
    3. Delimitadores unívocos para evitar ambiguidade (ex: 1,15 ≠ 11,5)

    Parâmetros
    ----------
    perfil : dict
        Dicionário {locus: (alelo1, alelo2)}, ex:
        {"D3S1358": ("16", "17"), "TH01": ("7", "9")}

    Retorno
    -------
    bytes
        String de bytes em UTF-8, ex: b'D21S11:29:30|TH01:7:9'

    Exemplo
    -------
    >>> p1 = {"TH01": ("9", "7"), "D21S11": ("30", "29")}
    >>> p2 = {"TH01": ("7", "9"), "D21S11": ("29", "30")}
    >>> perfil_canonico(p1) == perfil_canonico(p2)
    True
    """
    partes = []
    for locus in sorted(perfil.keys()):
        a1, a2 = perfil[locus]
        # Ordenação: tenta numérica (TH01 tem 9.3), recorre à textual
        try:
            par_ordenado = sorted([a1, a2], key=float)
        except ValueError:
            par_ordenado = sorted([a1, a2])
        partes.append(f"{locus}:{par_ordenado[0]}:{par_ordenado[1]}")
    return "|".join(partes).encode("utf-8")


def derivar_chave(
    perfil: Dict[str, tuple],
    salt: bytes,
    time_cost: int = 3,
    memory_cost: int = 65536,
    parallelism: int = 1,
    hash_len: int = 32,
    argon_type: Type = Type.ID,
) -> bytes:
    """
    Deriva uma chave criptográfica de 32 bytes a partir do perfil STR.

    Usa Argon2id (vencedora da Password Hashing Competition 2015) com
    parâmetros memory-hard para dificultar ataques paralelos massivos.

    Propriedades de segurança:
    - Memory-hard: consome ~64 MiB por derivação, inviabilizando GPU/ASIC barato
    - Determinística: mesmo perfil + mesmo salt → mesma chave
    - Unidirecional: chave não permite recuperar o perfil original

    Parâmetros
    ----------
    perfil : dict
        Dicionário de genótipos, ex: {"D3S1358": ("16", "17"), ...}
    salt : bytes
        Sal aleatório de 16–32 bytes (armazenar junto com a chave, não é secreto)
    time_cost : int
        Número de passes sobre a memória (default: 3)
    memory_cost : int
        Tamanho da memória em KiB (default: 65536 = 64 MiB)
    parallelism : int
        Número de threads paralelas (default: 1, compatível universal)
    hash_len : int
        Comprimento da saída em bytes (default: 32 = AES-256)
    argon_type : Type
        Variante Argon2 (default: Type.ID = híbrida)

    Retorno
    -------
    bytes
        Chave criptográfica de `hash_len` bytes

    Raises
    ------
    TypeError
        Se salt não for bytes ou perfil não for dicionário válido

    Example
    -------
    >>> import secrets
    >>> perfil = {"TH01": ("7", "9")}
    >>> salt = secrets.token_bytes(16)
    >>> chave = derivar_chave(perfil, salt)
    >>> len(chave)
    32
    """
    if not isinstance(salt, bytes):
        raise TypeError("Salt must be bytes")
    
    material = perfil_canonico(perfil)
    
    return hash_secret_raw(
        secret=material,
        salt=salt,
        time_cost=time_cost,
        memory_cost=memory_cost,
        parallelism=parallelism,
        hash_len=hash_len,
        type=argon_type,
    )


if __name__ == "__main__":
    # Teste rápido standalone
    import time
    import secrets
    
    perfil_demo = {"D3S1358": ("16", "17"), "TH01": ("7", "9")}
    salt_demo = secrets.token_bytes(16)
    
    t0 = time.perf_counter()
    chave = derivar_chave(perfil_demo, salt_demo)
    elapsed = time.perf_counter() - t0
    
    print(f"Chave derivada: {chave.hex()}")
    print(f"Tempo: {elapsed:.3f}s")
    print(f"Comprimento: {len(chave)} bytes")