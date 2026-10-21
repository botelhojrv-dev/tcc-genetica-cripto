# scripts/benchmark_hashes.py
"""
Benchmark comparativo: funções hash de uso geral vs. Argon2id.

Quantifica a justificativa da Seção 4.3 (troca de hash rápido por KDF
memory-hard): tempo médio por derivação de cada função sobre o MESMO
material canônico, no MESMO hardware, na MESMA sessão.

Uso:
    cd ~/Projetos/tcc-genetica-cripto
    source .venv/bin/activate
    python scripts/benchmark_hashes.py
"""
import hashlib
import json
import statistics
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from argon2.low_level import hash_secret_raw, Type
from src.derivacao import perfil_canonico

# ---- Material: perfil canônico real do pipeline + salt fixo --------
PERFIL = {
    "D18S51": ("15", "17"),
    "D21S11": ("29", "31.2"),
    "D3S1358": ("15", "16"),
    "D5S818": ("11", "13"),
    "TH01": ("6", "9.3"),
}
SALT = bytes.fromhex("00112233445566778899aabbccddeeff")
MATERIAL = perfil_canonico(PERFIL) + SALT  # mesma concatenação do modelo

# BLAKE3 é opcional (não está na stdlib); o teste pula se ausente
try:
    import blake3
    TEM_BLAKE3 = True
except ImportError:
    TEM_BLAKE3 = False

def medir(funcao, n_iter, rotulo):
    """Roda e cronometra uma função; descarta aquecimento e reporta estatísticas."""
    # Aquecimento: 1ª execução paga custos de import/cache
    funcao(MATERIAL)
    tempos = []
    for _ in range(n_iter):
        t0 = time.perf_counter()
        funcao(MATERIAL)
        tempos.append(time.perf_counter() - t0)
    media = statistics.fmean(tempos)
    resultado = {
        "funcao": rotulo,
        "n_iter": n_iter,
        "media_us": media * 1e6,
        "min_us": min(tempos) * 1e6,
        "max_us": max(tempos) * 1e6,
    }
    print(f"{rotulo:<12} média: {media*1e6:9.1f} µs  "
          f"(min {min(tempos)*1e6:8.1f} | máx {max(tempos)*1e6:8.1f} | n={n_iter})")
    return resultado

def main():
    print(f"Material canônico: {len(perfil_canonico(PERFIL))} bytes + salt 16 bytes\n")

    resultados = [
        medir(lambda m: hashlib.sha256(m).digest(), 1000, "SHA-256"),
        medir(lambda m: hashlib.sha3_256(m).digest(), 1000, "SHA3-256"),
    ]
    if TEM_BLAKE3:
        resultados.append(medir(lambda m: blake3.blake3(m).digest(), 1000, "BLAKE3"))
    else:
        print("BLAKE3      (módulo blake3 não instalado — pulado)")
    resultados.append(medir(
        lambda m: hash_secret_raw(m, SALT, time_cost=3, memory_cost=65536,
                                  parallelism=1, hash_len=32, type=Type.ID),
        10, "Argon2id"))

    # ---- Derivados de segurança (espaço de enumeração 2^21,5 ≈ 2,84 M) ----
    ESPACO_BUSCA = 2 ** 21.5
    print("\n--- Custos de enumeração sobre ~2^21,5 genótipos (2,84 milhões) ---")
    for r in resultados:
        cand_s = 1 / (r["media_us"] / 1e6)
        dias = (ESPACO_BUSCA * r["media_us"] / 1e6) / 86400
        r["cand_por_seg"] = cand_s
        r["dias_enum_espaco"] = dias
        print(f"{r['funcao']:<12} {cand_s:>14,.0f} candidatos/s | "
              f"enumeração completa: {dias:.4g} dias")

    sha = next(r for r in resultados if r["funcao"] == "SHA-256")
    argon = next(r for r in resultados if r["funcao"] == "Argon2id")
    mult = argon["media_us"] / sha["media_us"]
    print(f"\nMultiplicador Argon2id vs SHA-256: {mult:,.0f}x")

    # Persiste em results/ para citar no manuscrito com rastreabilidade
    saida = {
        "hardware": "AMD FX-8370E, 8 GiB RAM, Linux Mint 22.3, kernel 6.14",
        "material_bytes": len(MATERIAL),
        "espaco_busca_genotipos": ESPACO_BUSCA,
        "multiplicador_vs_sha256": mult,
        "resultados": resultados,
    }
    arquivo = RAIZ / "results" / "benchmark_hashes.json"
    arquivo.write_text(json.dumps(saida, indent=2, ensure_ascii=False))
    print(f"\nSalvo: {arquivo}")

if __name__ == "__main__":
    main()
    