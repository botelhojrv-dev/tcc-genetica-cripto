# [Manuscrito em rascunho] Derivação de Chaves Criptográficas a partir de
Perfis STR Forenses: Pipeline Reprodutível com Argon2id e Validação Estatística

> **Estado:** esqueleto IMRaD — preencher seção por seção
> **Formato alvo:** artigo de iniciação científica (submissão a congresso/revista a definir)

---

## Título (candidaturas)

1. "Geração de chaves criptográficas a partir de perfis STR forenses:
   viabilidade, limites e validação estatística"
2. "Da genética à criptografia: derivação de chaves AES-256 a partir de
   marcadores STR com Argon2id"
3. *(alternativa a definir com o orientador)*

## Autores e afiliação

- José Ricardo Vega Botelho — [curso de Biomedicina; afiliação a completar]
- *(coautores/orientador a incluir após contato — ver Etapa C)*

## Abstract (~200 palavras) — RASCUNHO EXISTENTE

→ Base: `docs/resumo_executivo.md` (versão expandida, parágrafo 1)
→ Incluir: contexto, método, 3 números-chave (χ² p=0,614; avalanche 49,6%;
247 ms), conclusão honesta do gap de entropia
→ Palavras-chave: genética forense; criptografia; STR; Argon2; KDF;
validação estatística; reprodutibilidade

---

### 1. INTRODUÇÃO

A autenticação biométrica tornou-se onipresente: impressões digitais desbloqueiam
telefones, o reconhecimento facial autoriza pagamentos e a íris controla
acessos restritos. Paralelamente, a criptografia moderna exige chaves de
alto grau de imprevisibilidade — no mínimo 128 bits para os padrões
contemporâneos (AES-128), com 256 bits recomendados (AES-256). A união
dessas duas frentes, contudo, esbarra num obstáculo fundamental: dados
biométricos não são segredos. Ao contrário de uma senha, a característica
biométrica está permanentemente "exposta ao mundo" — pode ser coletada
sem consentimento (uma digital em um copo, DNA em saliva residual) e não
pode ser trocada caso comprometida. Essa assimetria fez surgir um campo
próprio de pesquisa, a biometria criptográfica, com propostas originais 
comoFuzzy Vault (JUELS; SUDAN, 2006) e os fuzzy extractors (DODIS; OSTROVSKY; REYZIN; SMITH, 2008).

Dentre as modalidades biométricas, o DNA ocupa posição singular: é o
identificador humano mais discriminante conhecido, inalterável ao longo
da vida, e — no contexto forense — já estruturado em infraestrutura
normatizada mundialmente. Os marcadores STR (Short Tandem Repeats) são o
padrão-ouro da identificação genética forense, utilizados nos bancos
de dados nacionais (como o CODIS norte-americano) e nos kits comerciais
de tipagem (GlobalFiler, PowerPlex Fusion). Um perfil STR típico
identifica um indivíduo com probabilidade de coincidência de ordem de
bilhões a um — o que levanta naturalmente a pergunta: se o perfil STR
distingue com tanta segurança uma pessoa de todas as outras, poderia ele
servir de fonte para derivação de chaves criptográficas?

Essa pergunta, contudo, enfrenta um desafio quantitativo imediato.
Identificação e imprevisibilidade criptográfica são propriedades
distintas: um perfil pode ser único na população e ainda assim conter
poucos bits de entropia efetiva, pois os genótipos possíveis são
limitados pelas frequências alélicas populacionais — que são públicas.
A literatura de criptografia é categórica sobre o risco: chaves
derivadas de material de baixa entropia são vulneráveis a ataques de
busca exaustiva, nos quais o adversário enumera os candidatos plausíveis
da fonte em vez de todo o espaço de chaves. Para dados biométricos, cuja
entropia dificilmente ultrapassa algumas dezenas de bits, a mitigação
clássica combina duas estratégias: funções de derivação que elevam o
custo computacional de cada tentativa, e fatores secretos adicionais
que complementam a entropia da fonte.

Nesse cenário, este trabalho investiga sistematicamente a viabilidade
de derivar chaves AES-256 a partir de perfis STR forenses, respondendo
a três perguntas específicas: (i) quanta entropia um painel STR fornece
de fato como material criptográfico; (ii) em que medida uma função de
derivação memory-hard — a Argon2id, vencedora da Password Hashing
Competition (Biryukov, Dinu e Khovratovich, 2016) — é capaz de elevar o
custo de ataques de força bruta sobre esse espaço reduzido; e (iii) se
as chaves resultantes atendem aos critérios estatísticos de
aleatoriedade esperados de material criptográfico legítimo.

A contribuição do trabalho é fourfold. Primeiro, quantificamos
empiricamente a entropia de um painel de cinco loci STR diplóides
simulados segundo frequências plausíveis (≈22 bits por perfil). Segundo,
especificamos um pipeline completo e determinístico de transformação —
canonização unívoca do genótipo, derivação via Argon2id com parâmetros
calibrados em hardware modesto — implementado como software livre,
testado automaticamente e integralmente reprodutível. Terceiro,
submetemos as chaves derivadas a três baterias de validação estatística
(uniformidade qui-quadrado, equilíbrio posicional de bits e efeito
avalanche), todas aprovadas. Quarto, discutimos com franqueza os limites
da abordagem: a entropia genética isolada não alcança os patamares de
segurança modernos, o que nos leva a recomendar, para aplicações
críticas, um modelo híbrido que combine o perfil genético a um fator
secreto adicional.

O restante deste artigo está organizado da seguinte forma: a Seção 2
detalha a metodologia, do painel sintético aos critérios estatísticos;
a Seção 3 reporta os resultados de entropia, desempenho e validação;
a Seção 4 discute implicações de segurança, comparação com propostas
afins (Fuzzy Vault, BioHashing) e limitações; a Seção 5 conclui e
aponta extensões futuras.

### 1.1 Contexto — biometria e criptografia
- Crescimento de aplicações biométricas em autenticação
- Paradigma: dado biométrico não é segredo (está "no mundo"), logo não
  pode alimentar criptografia diretamente — problema clássico da área
  (citar Juels & Sudan 2006; Dodis et al. 2008)

### 1.2 Os STRs como fonte de identificação
- Marcadores padrão-ouro forense (CODIS; kits GlobalFiler/PowerPlex)
- Propriedades: polimorfismo, estabilidade, banques de dados existentes
- Pergunta de pesquisa: *quanta entropia os STRs realmente oferecem
  para fins criptográficos, e essa entropia é "esticável" com KDF?*

### 1.3 Contribuições deste trabalho
1. Quantificação empírica da entropia de painel STR (NB01)
2. Pipeline completo reprodutível: canonização → Argon2id → chave (NB02)
3. Validação estatística em 3 baterias (NB03)
4. Discussão honesta dos limites e recomendação de modelo híbrido
   (`docs/discussao_gap_entropia.md`)

---

## 2. METODOLOGIA — MATERIAL PARCIALMENTE EXISTENTE

### 2.1 Dados sintéticos e reprodutibilidade
→ Base: README (seção nota de ética) + NB01 células 3–4
→ Painel de 5 loci, frequências plausíveis, Hardy-Weinberg, seed=2024
→ Justificativa ética: LGPD Art. 5º, II; nenhum dado real

### 2.2 Quantificação de entropia
→ Base: NB01 + `src/entropia.py`
→ Shannon por locus, agregação, eficiência (D5S818 88% → candidato a exclusão)

### 2.3 Canonização e derivação
→ Base: NB02 + `src/derivacao.py` (docstrings já são texto metodológico!)
→ Figura: `docs/fluxograma.md` (exportar SVG via mermaid.live)
→ Parâmetros Argon2id: t=3, m=64 MiB, p=1, salt 16 bytes

### 2.4 Validação estatística
→ Base: NB03 células 5–10
→ χ² uniformidade; equilíbrio de bits + IC 99%; avalanche (n=60)
→ Nota: teste caseiro inspirado em NIST SP 800-22 (limitação a admitir)

---

## 3. RESULTADOS — MATERIAL EXISTENTE, SÓ ORGANIZAR

### 3.1 Entropia da fonte
→ Tabela por locus (5 linhas) + Figura 1 (`01_entropia_str.png`)
→ ~10,75 bits/alelo; ~22 bits/genótipo; 2,95 bits observados/perfil

### 3.2 Derivação e performance
→ 247 ms médio (232–282); 64 MiB; ~11–12 dias força bruta serial
→ Hamming: perfis distintos 119/256; salts distintos 130/256

### 3.3 Validação estatística
→ Figura 2 (`03_validacao_chaves.png`)
→ χ²(255)=247,88, p=0,614; bits 0,5017 (2/256 fora do IC);
avalanche 49,6% (σ=9,5, n=60)

---

## 4. DISCUSSÃO — RASCUNHO EXISTENTE (refinar)

→ Base integral: `docs/discussao_gap_entropia.md`
- 4.1 O gap 22 vs. 256 bits
- 4.2 O que o Argon2id compra e o que não compra
- 4.3 Ataques de vizinhança genética (parentes) — avalanche mitiga?
- 4.4 Recomendação de modelo híbrido (fator secreto adicional)
- 4.5 Comparação com Fuzzy Vault / BioHashing / secure sketch
- 4.6 Limitações: n amostral, bateria NIST completa, painel de 5 loci

---

## 5. CONCLUSÃO
→ Base: §6 de `docs/discussao_gap_entropia.md`
→ Viabilidade técnica demonstrada + honestidade científica sobre limites
→ Trabalhos futuros: painel 24 loci, SNPs, bateria NIST completa

## REFERÊNCIAS (iniciais — expandir com pesquisa bibliográfica)

- Juels, A.; Sudan, M. (2006). A Fuzzy Vault Scheme. * Designs, Codes and Cryptography*
- Dodis, Y.; Ostrovsky, R.; Reyzin, L.; Smith, A. (2008). Fuzzy Extractors.
- Teoh, A.B.J. et al. (2004). BioHashing.
- Biryukov, A.; Dinu, D.; Khovratovich, D. (2016). Argon2: the memory-hard
  function for password hashing (PHC winner).
- NIST SP 800-22 rev. 1a (2010). A Statistical Test Suite for RNG.
- LGPD — Lei nº 13.709/2018, Art. 5º, II.
- *(completar: livros de genética forense — Butler "Forensic DNA Typing"?)*

## Agradecimentos / Suporte financeiro
→ (a definir — iniciação científica? instituição?)
