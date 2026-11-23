# Geração de Chaves Criptográficas a partir de Dados de Genética Forense

Pesquisa de iniciação científica com fins de TCC, dissertação de mestrado
e tese doutoral. Investiga a viabilidade de derivar material criptográfico
(chaves AES-256) a partir de marcadores genéticos forenses (STR).

## Estado atual do projeto

| Componente | Status | Detalhes |
|---|---|---|
| Notebook 01 — Entropia dos STRs | ✅ Concluído | Três medidas: 21,5 (fase) · **17,74 canônica (valor de segurança)** · 13,61 min-entropia |
| Notebook 02 — Derivação Argon2id | ✅ Concluído | 237,5 ms/chave (σ = 13,0 ms), 64 MiB |
| Notebook 03 — Validação estatística | ✅ Concluído | 3 baterias aprovadas |
| `src/entropia.py` | ✅ Testado | 10/10 testes (Shannon + hierarquia H∞ ≤ H ≤ Hmáx) |
| `src/derivacao.py` | ✅ Testado | 11/11 testes |
| `tests/test_determinismo.py` | ✅ Testado | 4/4 testes (determinismo condicional + canonização) |
| Suíte completa | 🟢 **25/25** | ~7 s |
| Manuscrito v7 (artigo + TCC) | ✅ | `docs/manuscrito.md`, `docs/artigo cku revisao 2 v7.md`, `docs/tcc_ckuv7 revisão.md` |
| Fluxograma da metodologia | ✅ | `docs/fluxograma.md` (Mermaid) |
| Discussão do gap de entropia | ✅ | `docs/discussao_gap_entropia.md` |
| Resumo executivo | ✅ | `docs/resumo_executivo.md` |

## Resultados principais

1. **Entropia da fonte** (três medidas, v7): 10,75 bits/alelo; **17,74 bits**
   por perfil diplóide no espaço canônico (valor de segurança adotado),
   21,54 bits na convenção de par ordenado (superestimada) e 13,61 bits
   de min-entropia (pior caso) — ver [`notebooks/01_exploracao.ipynb`]
2. **Derivação**: Argon2id (t=3, m=64 MiB, p=1) → chave de 32 bytes
   AES-256-ready, média de 237,5 ms (σ = 13,0 ms) em hardware modesto
3. **Validação estatística** (400 chaves, 12.800 bytes):
   - Uniformidade de bytes: χ²(255) = 247,88; p = 0,614 ✓
   - Equilíbrio de bits: 0,5017 global; 2/256 posições fora do IC 99% ✓
   - Avalanche effect: 49,6% (127,1/256 bits; σ = 9,5; n = 60 pares) ✓
   - Hamming entre perfis distintos: 112/256 bits; entre salts: 134/256 ✓

Figuras do artigo em `results/figures/`:
- `01_entropia_str.png` — entropia por locus + histograma por perfil
- `03_validacao_chaves.png` — distribuição de bytes + avalanche

## ⚠️ Nota de ética e segurança

Dados genéticos são dados pessoais sensíveis (LGPD, Art. 5º, II).
O diretório `data/raw/` é EXCLUÍDO do controle de versão via `.gitignore`.
Nenhuma sequência real deve ser enviada a repositório remoto —
todos os resultados foram obtidos com **perfis sintéticos** gerados
reproduzivelmente (semente fixa seed=2024).

**Limitação de segurança reconhecida**: 17,74 bits de entropia genética
(canônica; pior caso min-entropia 13,61) não são suficientes para os
128 bits de segurança contemporâneos sem fator secreto adicional
(modelo híbrido, ~58 bits).
Ver `docs/discussao_gap_entropia.md` para a análise completa.

## Estrutura do projeto

```
data/
    raw/         -> dados brutos originais (IMUTÁVEIS, fora do Git)
    interim/      -> dados em processamento intermediário
    processed/    -> dados prontos para análise
notebooks/       -> cadernos Jupyter de exploração numerados
src/              -> módulos Python da metodologia (código estável)
tests/            -> testes automatizados (pytest)
results/figures/  -> figuras geradas (Matplotlib)
docs/             -> documentação, fluxograma, discussões
```

## Setup rápido

### Opção 1 — Ambiente local (Python 3.12)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make test      # 25/25 verdes
make notebook  # JupyterLab em http://localhost:8888
```

### Opção 2 — Docker (reprodutibilidade total)

```bash
docker compose up -d jupyter   # JupyterLab em http://localhost:8888
```

## Metodologia (resumo)

```
Perfil STR forense (5 loci, diplóide)
        │
        ▼
Canonização determinística (~61 bytes UTF-8)
        │                        Salt aleatório (16 bytes)
        ▼                              │
   Argon2id KDF ◄─────────────────────┘
   (t=3 · m=64MiB · p=1)
        │
        ▼
Chave AES-256 (32 bytes)
```

1. Extração de marcadores STR de perfis forenses (sintéticos)
2. Quantificação da entropia de Shannon (`src/entropia.py`)
3. Canonização do perfil + Argon2id (`src/derivacao.py`)
4. Validação estatística: chi-quadrado, equilíbrio de bits, avalanche

Fluxograma completo: `docs/fluxograma.md` · Discussão de segurança: `docs/discussao_gap_entropia.md`

## Hardware de referência

Todos os benchmarks foram medidos em desktop modesto (Linux Mint 22.3,
Python 3.12.3) — princípio: *se custa caro em hardware modesto, o argumento
de robustez vale a fortiori para qualquer atacante.*