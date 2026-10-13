# Fluxograma da Metodologia

Pipeline de geração de chaves criptográficas a partir de perfis STR forenses.

```mermaid
flowchart TD
    A[Perfil STR forense<br/>5 loci · diplóide] --> B[Canonização<br/>loci alfabéticos · alelos ordenados]
    B --> C[Material de entrada<br/>~61 bytes UTF-8 determinístico]
    C --> D[Argon2id KDF<br/>t=3 · m=64MiB · p=1]
    E[Salt aleatório<br/>16 bytes · não secreto] --> D
    D --> F[Chave criptográfica<br/>32 bytes · AES-256 ready]

    G[Análise de entropia<br/>NB 01 · ~22 bits/genótipo] -.->|justifica parâmetros| D
    F -.-> H[Validação estatística<br/>NB 03 · chi-quadrado · avalanche]

    style A fill:#e8f5e9,stroke:#2e7d32
    style F fill:#fff3e0,stroke:#ef6c00
    style D fill:#fce4ec,stroke:#c2185b
```

## Legenda do fluxo

| Etapa | Função | Onde está implementada |
|---|---|---|
| Perfil STR | Matéria-prima genética (~22 bits de entropia) | `notebooks/01` |
| Canonização | Serialização determinística sem ambiguidade | `src/derivacao.py` → `perfil_canonico()` |
| Salt | Impede rainbow tables; armazenado junto à chave | `secrets.token_bytes(16)` |
| Argon2id | Estica o custo de força bruta (CPU + memória) | `src/derivacao.py` → `derivar_chave()` |
| Chave 32B | Material pronto para AES-256 | saída `hash_secret_raw` |
| Validação | Uniformidade estatística das chaves em massa | `notebooks/02` (Hamming) · `notebooks/03` (planejado) |

## Parâmetros de segurança (hardware modesto)

- Tempo médio de derivação: **247 ms**
- Custo de memória por tentativa: **64 MiB**
- Implicação: busca exaustiva do espaço de genótipos ≈ **11–12 dias** de CPU serial