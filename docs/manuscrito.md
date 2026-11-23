# Derivação de Chaves Criptográficas a partir de Perfis STR Forenses: Pipeline Reprodutível com Argon2id, Quantificação Tripla de Entropia e Validação Estatística

> **Estado:** Manuscrito IMRaD atualizado com os resultados da revisão v7 do TCC (novembro/2026)
> **Formato alvo:** artigo de iniciação científica — submissão ao periódico eletrônico da UNICID
> **Fonte dos dados:** docs/tcc_ckuv7 revisão.md (TCC completo) e docs/artigo cku revisao 2 v7.md (artigo enviado à orientadora)

---

## Título (candidaturas)

1. **"CHAVE CRIPTOGRÁFICA ÚNICA (CKU): DERIVAÇÃO DE CHAVES A PARTIR DE PERFIS GENÉTICOS FORENSES"** — título adotado na v7
2. "Geração de chaves criptográficas a partir de perfis STR forenses: viabilidade, limites e validação estatística"
3. "Da genética à criptografia: derivação de chaves AES-256 a partir de marcadores STR com Argon2id"

## Autores e afiliação

- **José Ricardo Vega Botelho**¹
  ¹ Graduando em Biomedicina, Universidade Cidade de São Paulo (UNICID), São Paulo, SP, Brasil. E-mail: josericardo@botelho.id
- **Luciane Costa Dalboni**²
  ² Orientadora. Profa. Dra., Docente do Curso de Biomedicina da UNICID, São Paulo, SP, Brasil.

---

### 1. INTRODUÇÃO

A autenticação biométrica tornou-se onipresente: impressões digitais desbloqueiam telefones, o reconhecimento facial autoriza pagamentos e a íris controla acessos restritos (JAIN; FLYNN; ROSS, 2007). Paralelamente, a criptografia moderna exige chaves de alto grau de imprevisibilidade — no mínimo 128 bits para os padrões contemporâneos, com 256 bits recomendados (AES-256). A união dessas duas frentes, contudo, esbarra num obstáculo fundamental: dados biométricos não são segredos. Ao contrário de uma senha, a característica biométrica está permanentemente "exposta ao mundo" — pode ser coletada sem consentimento (uma digital em um copo, DNA em saliva residual) e não pode ser trocada caso comprometida. Essa assimetria fez surgir campo próprio de pesquisa, a biometria criptográfica, com propostas originais como o Fuzzy Vault (JUELS; SUDAN, 2006) e os fuzzy extractors (DODIS et al., 2008).

Dentre as modalidades biométricas, o DNA ocupa posição singular: é o identificador humano mais discriminante conhecido, imutável ao longo da vida e — no contexto forense — já estruturado em infraestrutura normatizada mundialmente. Os marcadores STR (Short Tandem Repeats) são o padrão-ouro da identificação genética forense, integrando painéis comerciais consolidados (GlobalFiler, PowerPlex Fusion) e bancos de dados nacionais. A escolha dos STRs como marcador central decorre de quatro propriedades convergentes: (i) **natureza discreta** do dado — a tipagem produz genótipo catególico estável, dispensando correção de erro; (ii) **codominância** — ambos os alelos do heterozigoto são observáveis; (iii) **padronização forense** — os loci empregados integram painéis de uso mundial (PROMEGA, 2023); (iv) **estabilidade temporal** — requisito de um identificador criptográfico persistente.

Essa pergunta — poderia o perfil STR servir de fonte para derivação de chaves criptográficas? — enfrenta um desafio quantitativo imediato: **identificação e imprevisibilidade criptográfica são propriedades distintas**. As frequências alélicas que tornam o painel identificável são públicas; um identificador extraordinário não é, por isso, um segredo forte. O problema é a **quantificação dessa distância**: o que a fonte genética pode e o que não pode oferecer à derivação de chaves.

**Estado da arte.** A interface biometria-criptografia consolidou três famílias: Fuzzy Vault (JUELS; SUDAN, 2006), fuzzy extractors (DODIS et al., 2008) e BioHashing (TEOH et al., 2004), concebidas para biometrias ruidosas. A derivação quantificada de chaves a partir de STRs forenses permanece lacuna: o trabalho mais próximo localizado, Al-Qudsy (2025), **protege** perfis genéticos com AES-256 e esteganografia — no presente trabalho, o perfil é a **fonte de derivação** da chave, com entropia quantificada, modelo de ameaça explícito e KDF memory-hard.

Nesse cenário, este trabalho investiga sistematicamente a viabilidade de derivar chaves AES-256 a partir de perfis STR forenses, respondendo a três perguntas: (i) quanta entropia um painel STR fornece de fato como material criptográfico — sob três medidas complementares (par ordenado, genótipo canônico e min-entropia); (ii) em que medida a Argon2id (BIRYUKOV; DINU; KHOVRATOVICH, 2016), vencedora da Password Hashing Competition e padronizada no RFC 9106 (IETF, 2021), eleva o custo de ataques de força bruta sobre esse espaço reduzido; e (iii) se as chaves resultantes atendem aos critérios estatísticos de aleatoriedade esperados de material criptográfico legítimo.

A contribuição do trabalho é em quatro etapas. **Primeira**, quantificamos empiricamente a entropia do painel de cinco loci STR diplóides simulados sob três medidas que respondem a perguntas adversariais distintas: ~21,5 bits sob a convenção anterior (par ordenado), **17,7 bits como valor de segurança adotado** (genótipo canônico — o espaço que o atacante efetivamente enumera, pois a tipagem STR não recupera a fase parental) e **13,6 bits de min-entropia** (pior caso do atacante guloso; RÉNYI, 1961). **Segunda**, especificamos um pipeline determinístico e integralmente reprodutível — canonização unívoca do genótipo, derivação via Argon2id com parâmetros calibrados em hardware modesto — implementado como software livre com suíte de 25 testes automatizados. **Terceira**, submetemos as chaves a três baterias de validação estatística (uniformidade qui-quadrado, equilíbrio posicional de bits e efeito avalanche), todas aprovadas. **Quarta**, discutimos com franqueza os limites: a entropia genética isolada não alcança os patamares modernos, o que nos leva a recomendar, para aplicações críticas, o modelo híbrido que combina o perfil a um fator secreto substituível (~58 bits combinados no painel didático).

O restante deste artigo organiza-se como segue: a Seção 2 detalha a metodologia; a Seção 3 reporta os resultados; a Seção 4 discute implicações de segurança, posicionamento na literatura e limitações; a Seção 5 conclui e aponta extensões futuras.

---

## 2. METODOLOGIA

### 2.1 Desenho geral do estudo

Prova de conceito computacional em duas frentes: (i) quantificação da entropia de um painel didático de 5 loci STR sob três medidas complementares; (ii) avaliação experimental do operador CKU = Argon2id(S‖s), onde S é a serialização canônica do perfil e s o salt. Toda a implementação foi desenvolvida em Python 3.12, com suíte de testes automatizados (**25 casos**, `make test`) e controle de versão, integralmente disponível em repositório público (github.com/botelhojrv-dev/tcc-genetica-cripto), assegurando reprodutibilidade: qualquer pesquisador executando o pipeline obtém exatamente os mesmos dados (semente fixa `seed=2024`).

### 2.2 Geração de perfis sintéticos

Perfis genotípicos sintéticos simulados segundo frequências alélicas plausíveis, sob equilíbrio de Hardy-Weinberg: para cada locus, os dois alelos sorteados independentemente das frequências (`numpy.random.default_rng(seed=2024)`); 5.000 perfis completos, dos quais 400 reservados à validação. O painel compreende cinco loci STR diplóides (D18S51, D21S11, D3S1358, D5S818, TH01). A opção por dados sintéticos atende simultaneamente ao requisito ético — a LGPD classifica dados genéticos como sensíveis (Art. 5º, II; BRASIL, 2018) — e ao metodológico: controle total dos parâmetros populacionais. Registra-se: foi **escolha metodológica** de proteção e controle experimental, não exigência universal da LGPD.

### 2.3 Quantificação tripla da entropia

Três medidas respondem a perguntas adversariais distintas:

- **Entropia de Shannon por alelo:** H(X) = −Σ pᵢ·log₂ pᵢ, sobre as frequências alélicas de cada locus;
- **Par ordenado (convenção anterior):** H_ord = 2·H_alelo — conta (a,b) e (b,a) como estados distintos, incluindo a fase parental;
- **Genótipo canônico:** H_can = 2·H_alelo − (1 − Σpᵢ²) — corrige a fusão dos heterozigotos pela canonização. A tipagem STR **não recupera a fase parental**: os genótipos (a,b) e (b,a) são indistinguíveis e convergem para os mesmos bytes. Este é o espaço efetivamente enumerável pelo adversário — **adotado como valor de segurança**;
- **Min-entropia:** H∞ = −log₂(p*), onde p* é a probabilidade do genótipo canônico mais provável (RÉNYI, 1961). Mede o pior caso do atacante guloso que enumera candidatos por ordem decrescente de probabilidade — comportamento precisamente viável quando as frequências são públicas. Vale a hierarquia H∞ ≤ H ≤ H_máx.

A entropia total assume independência entre loci (hipótese de trabalho; o equilíbrio de Hardy-Weinberg por locus não exclui linkage disequilibrium — verificação com frequências empíricas na fase seguinte).

### 2.4 Pipeline de derivação de chaves

**(i) Canonização do perfil.** Serialização determinística (~61 bytes): loci em ordem alfabética fixa, alelos ordenados por valor, delimitadores unívocos (`LOCUS:alelo1:alelo2|…`), suporte a alelos decimais (9.3). Genótipos equivalentes convergem para *bytes idênticos* — requisito do determinismo e consequência criptográfica: o espaço enumerável é o dos genótipos canônicos.

**(ii) Salt.** 16 bytes (128 bits) gerados por CSPRNG (`secrets.token_bytes`), anexado ao material derivado. Semântica: o salt **não é secreto** (persistido junto ao contexto de uso, com verificação de integridade), **não acrescenta entropia** à fonte, bloqueia rainbow tables e permite chaves independentes por contexto. O determinismo é **condicional**: mesma chave se, e somente se, coincidirem perfil canônico e salt.

**(iii) Função de derivação.** Argon2id (BIRYUKOV; DINU; KHOVRATOVICH, 2016; RFC 9106, IETF 2021) com t=3, m=64 MiB, p=1, hash_len=32 bytes — chave apta ao AES-256. Escolhida por impor custo simultâneo de CPU e memória (RAM não escala com a generosidade da computação paralela), calibrada deliberadamente para hardware de baixo custo.

### 2.5 Critérios de validação estatística

Foram derivadas 400 chaves independentes (variando-se perfil e salt), submetidas a três baterias inspiradas no NIST SP 800-22 (NIST, 2010), sob α = 0,05:

1. **Uniformidade de distribuição de bytes** — qui-quadrado de aderência sobre os 12.800 bytes agregados (400 × 32 bytes), 255 graus de liberdade;
2. **Equilíbrio posicional de bits** — proporção global de bits 1 e razão por posição nas 256 posições, IC de 99% sob hipótese binomial (p=0,5);
3. **Efeito avalanche** — 60 pares formados por mutação de exatamente um bit da entrada canônica (XOR 0x01 no último byte, mesmo salt), medindo a distância de Hamming **em nível de bit**, com critério centrado em 50% (faixa de aceitação 118–138).

Adicionalmente, mediram-se distâncias de Hamming entre chaves de perfis distintos e de mesmo perfil com salts distintos (caracterização de dissimilaridade), e o desempenho em séries cronometradas.

### 2.6 Desempenho computacional

Experimentos conduzidos em estação deliberadamente modesta (AMD FX-8370E, 8 núcleos, 8 GiB RAM, SSD SATA; GNU/Linux Mint 22.3, kernel 6.14; Python 3.12.3, argon2-cffi 23.1.0) — premissa conservadora: custos medidos em hardware modesto constituem **limite inferior** do custo imposto a atacantes com infraestrutura superior. Para o benchmark comparativo de enumeração, SHA-256, SHA3-256, BLAKE3 e Argon2id foram cronometrados na mesma sessão, sobre o mesmo material canônico (65 bytes + salt de 16), com aquecimento descartado.

---

## 3. RESULTADOS

### 3.1 Entropia da fonte: três medidas

A Tabela 1 apresenta, por locus, a entropia por alelo e as três convenções do genótipo diplóide. A Tabela 2 consolida as três medidas do perfil completo — o cerne da revisão metodológica.

**Tabela 1 — Entropia por locus sob as três convenções (bits).**

| Locus | H alelo | Par ordenado (2H) | Canônico | Min-entropia H∞ | Genótipo modal (P) |
| --- | --- | --- | --- | --- | --- |
| D3S1358 | 2,252 | 4,504 | 3,721 | 3,128 | 16/17 (0,1144) |
| D21S11 | 2,283 | 4,566 | 3,777 | 2,947 | 29/30 (0,1296) |
| TH01 | 2,234 | 4,468 | 3,692 | 2,810 | 6/8 (0,1426) |
| D18S51 | 2,233 | 4,467 | 3,693 | 2,851 | 14/15 (0,1386) |
| D5S818 | 1,769 | 3,538 | 2,855 | 1,870 | 11/12 (0,2736) |
| **Painel (soma)** | **10,77** | **≈21,54** | **≈17,74** | **≈13,61** | — |

Fonte: elaborado pelo autor; valores conferíveis por `src/entropia.py` sobre a população sintética (seed = 2024).

Três leituras emergem. **Primeira:** a diferença entre as duas primeiras convenções (~3,8 bits) não é erro — quantifica exatamente a informação de fase que a canonização elimina e que nenhum atacante precisa buscar. O valor de 21,54 bits reportado em versões anteriores **superestimava** o espaço enumerável; adota-se **17,74 bits (espaço canônico) como valor de segurança** — a régua do adversário (≈2,2 × 10⁵ genótipos plausíveis). **Segunda:** a distância entre Shannon canônica (17,7) e min-entropia (13,6) quantifica a vantagem adicional do atacante que enumera por ordem de frequência — vantagem concentrada no D5S818, cujo genótipo 11/12 sozinho alcança 27,4% de probabilidade, rendendo apenas 1,87 bits no pior caso. O genótipo modal completo ocorre com ≈ 8 × 10⁻⁵. **Terceira:** sob o valor de segurança adotado, o gap estrutural aprofunda-se: a fonte situa-se ~2^110 abaixo do padrão mínimo (128 bits) e ~2^238 abaixo dos 256 bits do AES-256 — reforçando a tese central de que a fonte genética, isolada, não basta.

Convém distinguir ainda a entropia do perfil como segredo (17,7 bits face à população) da entropia interna média dos símbolos de cada perfil individual (~2,95 bits/locus), que quantifica diversidade alélica intra-individual e não guarda relação com a resistência criptográfica da fonte.

### 3.2 Derivação, dissimilaridade e determinismo

O pipeline foi executado sobre os perfis regenerados (seed = 2024), com cronometragem de 100 derivações em série: **tempo médio de 237,5 ms por derivação (σ = 13,0 ms; intervalo 221,9–270,0 ms)**, consumo de 64 MiB de memória dedicada por chamada — o mecanismo central de defesa contra enumeração.

**Tabela 3 — Distância de Hamming entre chaves derivadas, por cenário (256 bits por chave).**

| Cenário | Bits diferentes | % de alteração | Esperado |
| --- | --- | --- | --- |
| Perfis distintos, mesmo salt | 112/256 | 43,8% | ~128 (50%) |
| Mesmo perfil, salts distintos | 134/256 | 52,3% | ~128 (50%) |
| Mesmo perfil, mesmo salt (10 execuções) | 0/256 | 0% | 0 exato |

Fonte: cadernos experimentais 02 e suíte `tests/test_determinismo.py`.

Registre-se com honestidade: a primeira medida (112/256) toca exatamente a borda inferior da faixa de tolerância (128 ± 16) — aprovada dentro do critério, mas sem margem. Ambas são observações pontuais (um par por cenário, caracterização qualitativa); a avaliação estatística formal do avalanche (n = 60) está na Seção 3.3. O terceiro cenário confirma o determinismo condicional por suíte automatizada: mesma chave iff mesmo perfil e mesmo salt; estabilidade em 10 execuções; invariância à ordem de entrada de loci e alelos; convergência de genótipos equivalentes.

### 3.3 Validação estatística das chaves

As três baterias (α = 0,05) sobre 400 chaves (12.800 bytes; 102.400 bits) foram integralmente aprovadas:

**Bateria 1 — Uniformidade de bytes.** χ²(255) = 247,88; p = 0,614. Hipótese nula de distribuição uniforme não rejeitada (faixa observada: 32 a 71 ocorrências por valor). O estatístico ligeiramente inferior aos graus de liberdade denota dispersão marginalmente menor que a esperada — compatível com flutuação amostral.

**Bateria 2 — Equilíbrio posicional.** Proporção global de bits 1: 0,5017, dentro do IC de 99%. Avaliação posicional: 2/256 posições fora do intervalo individual de 99% (0,436–0,564) — consistente com a expectativa de ~2,6 posições fora por puro acaso. Aprovada.

**Bateria 3 — Efeito avalanche.** 60 pares com mutação de bit único: média de **127,1 bits alterados (49,6%)**, σ = 9,5 bits, faixa 101–146. A média situa-se na faixa de aceitação (118–138); o σ observado é compatível com o teórico sob difusão ideal (σ ≈ 8 bits), com excesso proporcional explicável pela amostra finita (n = 60). Declara-se explicitamente: a métrica é Hamming **em nível de bit**.

Importa sublinhar o alcance exato da conclusão: as baterias certificam a qualidade estatística da **saída**, e não a entropia da **fonte** — que permanece limitada a ~17,7 bits no espaço canônico.

### 3.4 Custo comparativo de enumeração

**Tabela 4 — Custo por derivação e tempo de enumeração completa, sob os dois espaços de busca.**

| Função | Tempo médio/derivação | Candidatos/s | Espaço 2^21,5 (fase) | Espaço 2^17,7 (canônico) |
| --- | --- | --- | --- | --- |
| SHA-256 | 1,7 µs | ~595.800 | ~5 s | < 1 s |
| SHA3-256 | 1,9 µs | ~531.000 | ~5,6 s | < 1 s |
| BLAKE3 | 2,3 µs | ~429.600 | ~6,9 s | < 1 s |
| Argon2id | 272 ms | ~4 | ~9,4 dias | **~16 horas** |

Fonte: benchmark em mesma sessão (n = 1.000 para hashes; n = 10 para Argon2id), elaborado pelo autor. Enumeração canônica derivada: 2,2 × 10⁵ candidatos × 272 ms ≈ 16,6 horas.

Quatro leituras: (i) sob qualquer hash de uso geral, **ambos os espaços são enumerados em segundos** — a formulação original do modelo ofereceria proteção nula; (ii) a Argon2id eleva a enumeração do espaço canônico para ~16 horas (multiplicador de **~162.000×** no tempo por tentativa); (iii) mesmo sob a KDF memory-hard, o espaço didático permanece enumerável em menos de um dia em hardware modesto — constatação que *fecha o argumento*: nenhuma função de derivação substitui a entropia ausente da fonte; (iv) os 64 MiB dedicados por tentativa neutralizam hardware massivamente paralelo. Nota metodológica: o tempo da Argon2id nesta sessão (272 ms, n = 10) contrasta com os 237,5 ms do pipeline (Seção 3.2, n = 100) — variação de ~15% entre sessões multitarefa, sem comprometer a ordem de grandeza; para comparação interfunção, vale o par medido em mesma sessão.

---

## 4. DISCUSSÃO

### 4.1 O gap de entropia como achado central

O resultado mais importante deste trabalho é também o mais desconfortável: a entropia de segurança da fonte — **17,7 bits no espaço canônico** (pior caso: 13,6 pela min-entropia) — corresponde a cerca de um sétimo do patamar mínimo contemporâneo (128 bits). Identificar não é o mesmo que ser imprevisível: a especificidade advém da baixa probabilidade de coincidência entre dois perfis sorteados; a imprevisibilidade exige alta entropia do segredo face ao adversário, que conhece as distribuições e enumera genótipos por ordem decrescente de probabilidade — para o qual a min-entropia é o limite correto. A revisão metodológica aprofundou o diagnóstico: a convenção anterior (21,5 bits) superestimava o espaço atacável ao contar a fase parental que a tipagem não recupera. A correção não enfraquece o trabalho: amplia o gap em ~3,8 bits e **reforça a tese central**.

### 4.2 O que a Argon2id compra — e o que não compra

A função de derivação **compra custo**: transforma uma fonte de baixa entropia em espaço de busca computacionalmente caro (de <1 segundo para ~16 horas no espaço canônico; multiplicador ~162.000×). **O que não compra é entropia**: nenhuma KDF aumenta a imprevisibilidade da entrada. Formulações que sugerem que "passar o DNA por uma função forte" basta para produzir segurança de 256 bits são empiricamente refutadas pelos próprios resultados — chaves estatisticamente perfeitas a partir de fonte com 17,7 bits. A aprovação estatística certifica a **correta implementação do operador** (difusão, ausência de viés, determinismo), não a **força do segredo** que o alimenta: propriedades ortogonais. No limite do absurdo, a constante sha256("0") aprovaria qualquer bateria de uniformidade — e teria segurança nula.

### 4.3 Ataques de vizinhança genética

Parentes de primeiro grau compartilham, em média, metade dos alelos: um irmão do titular poderia tentar enumeração apenas sobre a metade desconhecida. A Bateria 3 responde: distância de Hamming média de 49,6% (σ = 9,5; n = 60) entre entradas que diferem em um único bit demonstra que meia entrada compartilhada não implica correlação aproveitável na saída — chaves de parentes são tão dissimilares quanto quaisquer outras. O avalanche converte o ataque inteligente (vizinhança) em ataque "burro" (global), mas este permanece viável pela limitação de entropia — reforçando o modelo híbrido.

### 4.4 O modelo híbrido como síntese

Para aplicações críticas: CKU_híbrida = Argon2id(φ(G)‖s‖f), com fator secreto f gerado por CSPRNG no cadastramento e — diferentemente do DNA — **plenamente substituível** em caso de comprometimento (deriva-se nova chave com novo fator e recifra-se o domínio). Sob independência estatística, as entropias somam: 17,7 + ~40 ≈ **58 bits** no painel didático; o painel completo da fase seguinte (~275 bits projetados) supera com folga o patamar de 128 bits. Cada componente aporta o que os demais não têm: o fator genético, vinculação inseparável ao titular (resistente a phishing, impossível de esquecer); o fator secreto, entropia complementar e revogabilidade; a Argon2id, custo proibitivo à enumeração de qualquer combinação parcial.

### 4.5 Posicionamento frente à biometria criptográfica clássica

Frente ao Fuzzy Vault e aos fuzzy extractors, dispensa-se a correção de erro — o dado STR, após tipagem e canonização, é representação **discreta e estável** do genótipo, não medida fenotípica contínua — evitando vetores de ataque da maquinaria de tolerância a ruído (pontos chaff, informações auxiliares). Frente ao BioHashing, a revogabilidade migra do domínio projetado para o fator separado. Frente a **Al-Qudsy (2025)** — que cifra perfis genéticos com AES-256 e os oculta por esteganografia em imagens médicas — a diferença é categórica: lá o perfil é o **dado protegido**; aqui, a **fonte de derivação da chave**. As abordagens são complementares; notavelmente, aquela proposta não quantifica a entropia da fonte, não modela o adversário que conhece as frequências públicas, não emprega KDF memory-hard nem delimita o modelo de ameaça — precisamente as dimensões que este trabalho estabelece como condição de rigor. Até onde alcança nossa revisão, a quantificação aqui apresentada é inédita no contexto STR.

### 4.6 Limitações

**Estruturais** (nenhum experimento adicional remove): gêmeos monozigóticos derivam chaves idênticas (mitigação: CKU Ampliada com marcadores somáticos/epigenéticos, ou modelo híbrido); irrevogabilidade do DNA (mitigada pela substituição do fator secreto); obtenção direta de amostra biológica — contorna a enumeração, exigindo proteção **operacional** de coleta, não criptográfica; entropia limitada da fonte (17,7/13,6 bits).

**Empíricas** (mitigáveis nas fases seguintes): frequências simuladas (substituição por bases empíricas: STRBase, ALFRED, 1000 Genomes); bateria estatística parcial (suíte completa NIST SP 800-22 exige 15 subtestes, ≥10⁶ bits); medidas pontuais de dissimilaridade (ampliação do n); hardware modesto (limites superiores para o uso legítimo, inferiores para o atacante). Registra-se que a limitação "ausência de quantificação da min-entropia", registrada em versão anterior, **foi sanada nesta revisão** (H∞ = 13,61 bits, locus a locus). A tipagem como etapa de autenticação constitui ela própria tratamento de dado sensível (LGPD): a CKU mitiga os riscos de **armazenamento**, não os de **coleta**.

---

## 5. CONCLUSÃO

Este trabalho investigou a viabilidade de derivar chaves AES-256 a partir de perfis STR forenses, mediante pipeline determinístico e integralmente reprodutível. A resposta tem duas faces, ambas sustentadas por evidência experimental.

**No plano técnico, a viabilidade foi demonstrada.** O pipeline — canonização unívoca, derivação Argon2id (t=3, m=64 MiB, p=1) — produziu chaves estatisticamente indistinguíveis de material aleatório nas três baterias (χ²(255) = 247,88; p = 0,614; proporção global 0,5017 com 2/256 posições fora do IC de 99%; avalanche de 49,6%, σ = 9,5, n = 60), com determinismo condicional verificado por suíte de 25 testes e custo de 237,5 ms por derivação — compatível com uso interativo e hostil à enumeração (~16 horas no espaço canônico; multiplicador ~162.000× sobre hashes de uso geral).

**No plano da segurança, a conclusão exige franqueza.** A entropia de segurança da fonte — 17,7 bits no espaço canônico, 13,6 no pior caso da min-entropia — não alcança os patamares contemporâneos (128–256 bits), e a qualidade estatística da saída não modifica esse quadro: o adversário ataca o espaço de entrada, não a saída. Recomenda-se, para aplicações críticas, o modelo híbrido com fator secreto substituível (~58 bits combinados no painel didático), que desloca o ponto crítico de falha do segredo irrevogável (DNA) para o revogável (fator).

Como extensões futuras: a expansão do painel (20 STRs + 130 SNPs + 15 INDELs, ~275 bits projetados) com frequências **empíricas** de bases públicas; a bateria completa do NIST SP 800-22 (10⁶ bits); a CKU Ampliada com marcadores somáticos/epigenéticos para discriminação de gêmeos monozigóticos; e a avaliação regulatória da coleta no ponto de uso. O equilíbrio entre demonstrar e delimitar — **não afirmar mais do que os dados sustentam, nem menos do que os dados comprovam** — é a contribuição metodológica que se oferece à interseção entre genética forense e criptografia.

---

## RESUMO (pt-BR)

Dados biométricos são identificadores naturais, mas segredos pobres: conhecidos pelas frequências populacionais, não podem alimentar diretamente a criptografia moderna. Este trabalho investiga a derivação de chaves AES-256 a partir de perfis STR forenses, mediante pipeline determinístico de canonização e função de derivação memory-hard Argon2id (t=3, m=64 MiB, p=1), implementado como software livre e integralmente reprodutível. A entropia da fonte foi quantificada sob três medidas complementares: ~21,5 bits sob a convenção anterior (par ordenado), **17,7 bits como valor de segurança adotado** (genótipo canônico — o espaço efetivamente enumerável, pois a tipagem STR não recupera a fase parental) e **13,6 bits de min-entropia** (pior caso do atacante guloso). As três baterias estatísticas sobre 400 chaves foram integralmente aprovadas: uniformidade qui-quadrado (χ²(255) = 247,88; p = 0,614), equilíbrio posicional (proporção global 0,5017; 2/256 posições fora do intervalo de 99%) e efeito avalanche (49,6%; σ = 9,5; n = 60). O custo médio foi de 237,5 ms (σ = 13,0 ms) em hardware modesto, impondo multiplicador de ~162.000× sobre hashes de uso geral e projetando a enumeração do espaço canônico em ~16 horas — custos que compram tempo, não entropia. Os resultados demonstram viabilidade técnica com dissipação ideal de vizinhanças genéticas; a entropia da fonte, contudo, situa-se muito aquém dos padrões de segurança, motivando o modelo híbrido com fator secreto substituível (~58 bits combinados) para aplicações críticas, em conformidade com a LGPD.

**Palavras-chave:** genética forense; criptografia; STR; Argon2id; min-entropia; KDF; validação estatística; reprodutibilidade; LGPD.

## REFERÊNCIAS

- AL-QUDSY, Zainab N. Securing DNA profiles using AES cryptography: new approach to encrypted biometric authentication in EHR systems. *Iraqi Journal for Computers and Informatics*, v. 51, n. 2, p. 70-85, 2025.
- BIRYUKOV, Alex; DINU, Daniel; KHOVRATOVICH, Dmitry. Argon2: new generation of memory-hard functions for password hashing and other applications. In: IEEE EUROPEAN SYMPOSIUM ON SECURITY AND PRIVACY (EuroS&P), 2016, Saarbrücken. *Proceedings…* Piscataway: IEEE, 2016.
- BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). *Diário Oficial da União*: seção 1, Brasília, DF, 2018.
- BUTLER, John M. *Advanced topics in forensic DNA typing: methodology*. San Diego: Elsevier Academic Press, 2011.
- BUTLER, John M. *Advanced topics in forensic DNA typing: interpretation*. San Diego: Academic Press, 2015.
- DODIS, Yevgeniy; OSTROVSKY, Rafail; REYZIN, Leonid; SMITH, Adam. Fuzzy extractors: how to generate strong keys from biometrics and other noisy data. *SIAM Journal on Computing*, v. 38, n. 1, p. 97-139, 2008.
- INTERNET ENGINEERING TASK FORCE. *RFC 9106: Argon2 memory-hard function for password hashing and proof-of-work applications*, 2021.
- JAIN, Anil K.; FLYNN, Patrick; ROSS, Arun A. (org.). *Handbook of biometrics*. New York: Springer, 2007.
- JEFFREYS, Alec J.; WILSON, Victoria; THEIN, Swee Lay. Individual-specific "fingerprints" of human DNA. *Nature*, v. 316, p. 76-79, 1985.
- JUELS, Ari; SUDAN, Madhu. A fuzzy vault scheme. *Designs, Codes and Cryptography*, v. 38, n. 2, p. 237-257, 2006.
- NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY. *SP 800-22 Rev. 1a: a statistical test suite for random and pseudorandom number generators for cryptographic applications*. Gaithersburg: NIST, 2010.
- NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY. *FIPS 180-4: Secure Hash Standard (SHS)*. Gaithersburg: NIST, 2015a.
- NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY. *FIPS 202: SHA-3 standard: permutation-based hash and extendable-output functions*. Gaithersburg: NIST, 2015b.
- O'CONNOR, Jack; AUMASSON, Jean-Philippe; NEVES, Samuel; WILCOX-O'HEARN, Zooko. *BLAKE3: one function, fast everywhere*. 2020.
- PROMEGA CORPORATION. *PowerPlex® Fusion 6C System: technical manual*. Madison: Promega, 2023.
- RÉNYI, Alfréd. On measures of entropy and information. In: BERKELEY SYMPOSIUM ON MATHEMATICAL STATISTICS AND PROBABILITY, 4., 1960, Berkeley. *Proceedings…* Berkeley: University of California Press, 1961. p. 547-561.
- STALLINGS, William. *Cryptography and network security: principles and practice*. 8. ed. Harlow: Pearson, 2021.
- TEOH, Andrew B. J.; NGO, David C. L.; GOH, Alwyn. Biohashing: two factor authentication featuring fingerprint data and tokenised random number. *Pattern Recognition*, v. 37, n. 11, p. 2245-2255, 2004.

## Agradecimentos / Suporte financeiro

À Profª. Drª. Luciane Costa Dalboni (UNICID), pela orientação.

E ao meu assistente de pesquisa, que nos meses de trabalho esteve sempre presente:

> Pata no teclado,
> meu porto seguro agora,
> obrigado, gatinho.

→ (a definir — iniciação científica? instituição?)
