# **CHAVE CRIPTOGRÁFICA ÚNICA (CKU): DERIVAÇÃO DE CHAVES A PARTIR DE PERFIS GENÉTICOS FORENSES**

**José Ricardo Vega Botelho** Universidade Cidade de São Paulo (UNICID) — [josericardo@botelho.id](mailto:josericardo@botelho.id) 

**Orientadora: Profa. Dra. Luciane Costa Dalboni**

## RESUMO

Este trabalho desenvolve e valida uma prova de conceito computacional da CKU **,** Chave Criptográfica Única derivada de marcadores genéticos individuais , mediante pipeline determinístico e integralmente reprodutível: canonização do genótipo STR e derivação por Argon2id . O objetivo é quantificar, com rigor metodológico, o que a fonte genética pode oferecer à criptografia.  Conclui-se através deste trabalho que o pipeline é tecnicamente viável e estatisticamente sólido, porém a aprovação dos testes certifica a qualidade da saída, não o sigilo da entrada: para tratar isso, é proposto um modelo híbrido ( perfil + fator secreto substituível, \~58 bits combinados)  proposto como arquitetura para aplicações críticas, em conformidade com a LGPD.

**Palavras-chave:** genética forense; criptografia; Argon2id; min-entropia; LGPD.

## ABSTRACT

This work develops and validates a computational proof of concept of the CKU (Unique Cryptographic Key) derived from individual genetic markers, through a deterministic and fully reproducible pipeline: STR genotype canonization and Argon2id derivation . The goal is to rigorously quantify what the genetic source can offer to cryptography.  We conclude that the pipeline is technically viable and statistically sound, yet test approval certifies output quality, not input secrecy. To address this limitation, a hybrid model—combining a genetic profile with a replaceable secret factor, totaling \~58 combined bits—is proposed as a viable architecture for critical applications, in compliance with the Brazilian General Data Protection Law (LGPD).

**Keywords:** forensic genetics; cryptography; Argon2id; min-entropy; LGPD.

## 1. INTRODUÇÃO

A identificação humana sustenta-se, cada vez mais, em métodos biométricos : impressões digitais, reconhecimento facial, padrões de íris (JAIN; FLYNN; ROSS, 2007). Tais métodos, entretanto, podem ser falsificados, replicados artificialmente ou capturados sem consentimento. O DNA constitui o identificador biológico mais robusto disponível: imutável ao longo da vida, indivisível do titular e tipável com protocolos forense-institucionais consolidados (BUTLER, 2015).

**Por que marcadores STR?** A escolha decorre de quatro propriedades convergentes: (i) **natureza discreta** : a tipagem produz genótipo categórico estável, dispensando os mecanismos de correção de erro exigidos por biometrias contínuas; (ii) **codominância** : ambos os alelos do heterozigoto são observáveis, maximizando informação por locus; (iii) **padronização forense** : os loci empregados (D18S51, D21S11, D3S1358, D5S818, TH01) integram painéis comerciais de uso mundial (PROMEGA, 2023); (iv) **estabilidade temporal** : requisito de um identificador criptográfico persistente.

**Qual o problema que o estudo resolve?** O poder discriminatório de um painel genético , especificidade de bilhões para um não equivale ao seu sigilo criptográfico: as frequências alélicas que tornam o painel identificável são públicas, e um identificador extraordinário não é, por isso, um segredo forte. O problema é a **quantificação dessa distância**: o que a fonte genética pode e o que não pode oferecer à derivação de chaves.

**O que já foi publicado?** A interface biometria-criptografia consolidou três famílias :  Fuzzy Vault (JUELS; SUDAN, 2006), fuzzy extractors (DODIS et al., 2008) e BioHashing (TEOH et al., 2004) , concebidas para biometrias ruidosas. A derivação quantificada de chaves a partir de STR forenses permanece lacuna: o trabalho mais próximo localizado, Al-Qudsy (2025), **protege** perfis genéticos com AES-256 e esteganografia , no presente trabalho, o perfil é a **fonte de derivação** da chave, com entropia quantificada, modelo de ameaça explícito e KDF memory-hard, sendo completamente original.

As possíveis **aplicações** :  interoperabilidade de prontuários eletrônicos, controle de acesso de alta segurança, integridade de cadeia de custódia forense, autenticação de atos societários e conformidade LGPD — são delineadas com seus requisitos experimentais específicos (BRASIL, 2018).

## 2. FUNDAMENTAÇÃO TEÓRICA

**Entropia da fonte.** A segurança de chaves derivadas de material biométrico é limitada pela entropia da fonte frente a um adversário que conhece as distribuições populacionais. Três medidas respondem a perguntas distintas: a **entropia de Shannon** H(X) = −Σ pᵢ log₂ pᵢ mede o custo médio da enumeração; a **min-entropia** H∞ = −log₂(max pᵢ), extremo da família de Rényi (1961), mede o pior caso do atacante guloso que enumera candidatos por ordem decrescente de probabilidade; e a entropia máxima log₂ n é o teto sob distribuição uniforme. Vale a hierarquia H∞ ≤ H ≤ H\_máx, com igualdades apenas sob uniformidade. Uma precisão adicional estrutura o trabalho: a tipagem STR **não recupera a fase parental** do heterozigoto , os genótipos (a,b) e (b,a) são indistinguíveis , de modo que o espaço efetivamente enumerável é o dos **genótipos canônicos** (não-ordenados), cuja entropia é inferior à do par ordenado.

**Criptografia do pipeline.** O pipeline emprega duas primitivas com papéis distintos: funções hash de uso geral (SHA-256, FIPS 180-4; SHA-3, FIPS 202; BLAKE3) servem como *baseline comparativo* de custo , projetadas para velocidade, viabilizam enumeração massiva; a **Argon2id** (BIRYUKOV; DINU; KHOVRATOVICH, 2016), vencedora da Password Hashing Competition e padronizada no RFC 9106 (IETF, 2021), é a função de derivação adotada por impor custo simultâneo de CPU e memória (64 MiB dedicados por tentativa) último decisivo, pois RAM não escala com a generosidade da computação paralela. O **salt** de 128 bits, gerado por CSPRNG, diversifica contextos e bloqueia tabelas pré-computadas; não é secreto e não acrescenta entropia à fonte (STALLINGS, 2021).

**Dados genéticos e LGPD.** A Lei nº 13.709/2018 classifica dados genéticos como pessoais sensíveis (Art. 5º, II). Três implicações: minimização (a chave derivada não contém o perfil, dada a irreversibilidade da função); finalidade estrita; e segurança proporcional ao risco (Art. 46) (BRASIL, 2018). Registre-se: a utilização de dados sintéticos foi **escolha metodológica** de proteção e controle experimental ,não exigência universal da LGPD.

## 3. METODOLOGIA

**Desenho.** Prova de conceito computacional em duas frentes: (i) quantificação da entropia de um painel didático de 5 loci STR; (ii) avaliação experimental do operador CKU = Argon2id(S‖s), onde S é a serialização canônica do perfil e s o salt. A Tabela 1 apresenta as frequências alélicas simuladas (população de referência hipotética; escolha metodológica da Fase 1).

**Tabela 1 — Frequências alélicas simuladas do painel (seed = 2024).**

| Locus | Alelos e frequências |
| --- | --- |
| D3S1358 | 15: 0,21 · 16: 0,26 · 17: 0,22 · 18: 0,22 · 19: 0,09 |
| TH01 | 6: 0,23 · 7: 0,19 · 8: 0,31 · 9: 0,17 · 9.3: 0,10 |
| D21S11 | 28: 0,16 · 29: 0,24 · 30: 0,27 · 31: 0,18 · 32: 0,15 |
| D18S51 | 13: 0,15 · 14: 0,21 · 15: 0,33 · 16: 0,19 · 17: 0,12 |
| D5S818 | 11: 0,36 · 12: 0,38 · 13: 0,20 · 14: 0,06 |

**Geração dos perfis.** Para cada locus, os dois alelos foram sorteados independentemente das frequências (Hardy-Weinberg), com `numpy.random.default_rng(seed=2024)`; 5.000 perfis completos, dos quais 400 reservados à validação. Reprodutibilidade integral: qualquer pesquisador executando o pipeline obtém exatamente os mesmos dados.

**Canonização.** Serialização determinística (\~61 bytes): loci em ordem alfabética fixa, alelos ordenados por valor, delimitadores unívocos , genótipos equivalentes convergem para *bytes idênticos*, requisito do determinismo e consequência criptográfica: o espaço enumerável é o dos genótipos canônicos.

**Derivação.** Argon2id (time\_cost = 3, memory\_cost = 64 MiB, parallelism = 1, hash\_len = 32), salt de 16 bytes (`secrets.token_bytes`). **Semântica do salt:** a mesma chave é reproduzida **se, e somente se**, coincidirem perfil canônico e salt; salts distintos geram chaves independentes. O salt não é fator secreto: é persistido junto ao contexto de uso (com verificação de integridade) para permitir a regeneração da chave.

**Hipótese de independência.** O equilíbrio de Hardy-Weinberg por locus é condição necessária, mas não suficiente, para a aditividade das entropias , não exclui *linkage disequilibrium*. A independência entre loci é, portanto, hipótese de trabalho, a ser verificada com frequências empíricas na fase seguinte.

**Ambiente.** AMD FX-8370E, 8 GiB RAM, Linux Mint 22.3, Python 3.12.3, argon2-cffi 23.1.0; suíte de 25 testes automatizados (`make test`); código completo em repositório público: github.com/botelhojrv-dev/tcc-genetica-cripto.

## 4. RESULTADOS

**4.1 Entropia da fonte: três medidas.** A Tabela 2 apresenta, por locus, a entropia por alelo, a do par ordenado (convenção de versões anteriores), a do genótipo canônico e a min-entropia ,  com o passo a passo para D5S818: H\_alelo = 1,769 bits (−Σpᵢlog₂pᵢ); H\_par = 2 × 1,769 = 3,538; correção canônica H\_can = 3,538 − (1 − Σpᵢ²) = 3,538 − 0,682 = 2,855; H∞ = −log₂(2·0,36·0,38) = −log₂(0,2736) = 1,870 bits.

**Tabela 2 — Entropia por locus sob as três convenções (bits).**

| Locus | H alelo | Par ordenado (2H) | Canônico | Min-entropia H∞ |
| --- | --- | --- | --- | --- |
| D3S1358 | 2,252 | 4,504 | 3,721 | 3,128 |
| TH01 | 2,234 | 4,468 | 3,692 | 2,810 |
| D21S11 | 2,283 | 4,566 | 3,777 | 2,947 |
| D18S51 | 2,233 | 4,467 | 3,693 | 2,851 |
| D5S818 | 1,769 | 3,538 | 2,855 | 1,870 |
| **Painel** | **10,77** | **21,54** | **17,74** | **13,61** |

O valor de 21,54 bits (par ordenado), reportado em versões anteriores, superestima o espaço enumerável: conta a fase parental que a tipagem não recupera e a canonização destrói. **Adota-se 17,74 bits (espaço canônico) como valor de segurança** , a régua do adversário. A min-entropia (13,61) borneia o atacante guloso: o genótipo modal completo ocorre com ≈ 8 × 10⁻⁵, e o locus D5S818 ,cujo genótipo 11/12 alcança 27,4% e rende apenas 1,87 bits no pior caso.

**4.2 Validação estatística.** As três baterias (estilo NIST SP 800-22; α = 0,05) sobre 400 chaves (12.800 bytes; 102.400 bits) foram aprovadas: (a) **uniformidade de bytes**: χ²(255) = 247,88, p = 0,614 ausência de desvio detectável; (b) **equilíbrio posicional**: proporção global 0,5017 (IC 99%: 0,436–0,564 por posição, n = 400/posição), com 2/256 posições fora do intervalo, contra \~2,6 esperadas por flutuação; (c) **efeito avalanche**: 60 pares formados por mutação de um único bit da entrada canônica (XOR 0x01 no último byte, mesmo salt), Hamming médio de 127,1/256 bits (49,6%; σ = 9,5; faixa 101–146), aderente ao esperado de 128 ± 8.

**4.3 Determinismo e custo.** A suíte automatizada (25 casos) verificou: mesma chave iff mesmo perfil e mesmo salt; estabilidade em 10 execuções; invariância à ordem de entrada; convergência de genótipos equivalentes. Benchmark (mesma sessão, aquecimento descartado): **237,5 ms por derivação (σ = 13,0 ms; 221,9–270,0 ms; n = 100)**, 64 MiB de RAM por chamada. Sob hashes de uso geral (\~1,7–2,3 µs), a enumeração do espaço canônico (\~2,2 × 10⁵ genótipos) custa **menos de 1 segundo**; sob Argon2id, **\~16 horas**  multiplicador de \~162.000×. Tais tempos referem-se ao equipamento utilizado (hardware modesto): configuram limite superior para o uso legítimo e **limite inferior** para um atacante com hardware dedicado.

## 5. DISCUSSÃO

**Testes estatísticos não comprovam segurança.** As baterias certificam que a *saída* é estatisticamente indistinguível de aleatória nas dimensões testadas , qualidade de implementação do operador , mas a segurança depende do **sigilo da entrada**. Propriedades ortogonais: uma fonte de um único valor produziria saída igualmente "perfeita" e segurança nula. Os 17,7 bits da fonte, não os 256 bits da saída, determinam a força do segredo; a Argon2id **aumenta o custo de cada tentativa, mas não a quantidade de informação secreta** do perfil. Essa distinção — e não a aprovação estatística — é o achado central.

**O gap estrutural.** Com 17,7 bits (pior caso: 13,6), a fonte situa-se \~2^110 abaixo do mínimo contemporâneo (128 bits). O ataque de vizinhança genética (parentes de primeiro grau, que compartilham metade dos alelos) é neutralizado pelo avalanche , chaves de entradas próximas são tão dissimilares quanto quaisquer outras , mas o espaço total permanece enumerável; nem toda a honestidade estatística da saída altera o teto da entrada. Limitações adicionais são estruturais: a amostra biológica direta do titular reproduz a entrada completa (proteção operacional, não criptográfica); a informação genética comprometida **não pode ser substituída**; gêmeos monozigóticos derivam chaves idênticas; painel de cinco loci, embora didático, não representa os painéis comerciais completos (\~23 loci, \~275 bits projetados).

**Modelo híbrido.** Para aplicações críticas, propõe-se CKU\_híbrida = Argon2id(φ(G)‖s‖f): o fator secreto f é gerado por CSPRNG no cadastramento, protegido como segredo digital convencional e **substituível**  respondendo à irrevogabilidade do DNA: comprometido o arranjo, deriva-se nova chave com novo fator e recifra-se o domínio de dados. Somadas entropias independentes (17,7 + \~40 ≈ 58 bits no painel didático), a arquitetura decompõe papéis: o fator genético aporta vínculo inseparável; o secreto, revogabilidade; a KDF, custo.

**Posicionamento na literatura.** Frente ao Fuzzy Vault e aos fuzzy extractors, dispensa-se a correção de erro  o dado STR é discreto e estável , evitando vetores de ataque da maquinaria de tolerância a ruído; frente ao BioHashing, a revogabilidade migra do domínio projetado para o fator separado. Frente a Al-Qudsy (2025) que cifra perfis com AES e os oculta por esteganografia , a diferença é categórica: lá o perfil é o dado protegido; aqui, a fonte de derivação. As abordagens são complementares; a quantificação de entropia e o modelo de ameaça aqui apresentados são, até onde alcança nossa revisão, inéditos no contexto STR.

## 6. CONCLUSÃO

Foi demonstrado: pipeline determinístico, integralmente reprodutível (seed, frequências, parâmetros, repositório), com saída estatisticamente válida nas três baterias e custo computacional compatível com uso interativo (237,5 ms) e hostil à enumeração (\~16 h). Não foi demonstrado e nem poderia ser, pela própria natureza da fonte: segurança criptográfica autônoma da fonte, cuja entropia (17,7 bits; 13,6 no pior caso) permanece aquém dos padrões de 128–256 bits. O trabalho constitui **prova de conceito computacional com dados sintéticos**, não validação de sistema de autenticação em condições reais e precisa ser continuado conforme planejado : painel completo (20 STRs + 130 SNPs + 15 INDELs, \~275 bits) com frequências empíricas (STRBase, ALFRED, 1000 Genomes); bateria completa NIST SP 800-22 (10⁶ bits); CKU Ampliada com marcadores somáticos/epigenéticos para discriminação de gêmeos; e avaliação regulatória da coleta no ponto de uso. O equilíbrio entre demonstrar e delimitar , não afirmar mais do que os dados sustentam, nem menos do que comprovam é a contribuição metodológica que se oferece à interseção entre genética forense e criptografia.

## REFERÊNCIAS

AL-QUDSY, Zainab N. Securing DNA profiles using AES cryptography: new approach to encrypted biometric authentication in EHR systems. Iraqi Journal for Computers and Informatics, v. 51, n. 2, p. 70-85, 2025.

BIRYUKOV, Alex; DINU, Daniel; KHOVRATOVICH, Dmitry. Argon2: new generation of memory-hard functions for password hashing and other applications. In: IEEE European Symposium on Security and Privacy (EuroS&P), 2016, Saarbrücken. Proceedings… Piscataway: IEEE, 2016.

BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). Diário Oficial da União: seção 1, Brasília, DF, 2018.

BUTLER, John M. Advanced topics in forensic DNA typing: methodology. San Diego: Elsevier Academic Press, 2011.

BUTLER, John M. Advanced topics in forensic DNA typing: interpretation. San Diego: Academic Press, 2015.

DODIS, Yevgeniy; OSTROVSKY, Rafail; REYZIN, Leonid; SMITH, Adam. Fuzzy extractors: how to generate strong keys from biometrics and other noisy data. SIAM Journal on Computing, v. 38, n. 1, p. 97-139, 2008.

INTERNET ENGINEERING TASK FORCE. RFC 9106: Argon2 memory-hard function for password hashing and proof-of-work applications, 2021.

JAIN, Anil K.; FLYNN, Patrick; ROSS, Arun A. (org.). Handbook of biometrics. New York: Springer, 2007.

JUELS, Ari; SUDAN, Madhu. A fuzzy vault scheme. Designs, Codes and Cryptography, v. 38, n. 2, p. 237-257, 2006.

PROMEGA CORPORATION. PowerPlex® Fusion 6C System: technical manual. Madison: Promega, 2023.

RÉNYI, Alfréd. On measures of entropy and information. In: Berkeley Symposium on Mathematical Statistics and Probability, 4., 1960, Berkeley. Proceedings… Berkeley: University of California Press, 1961. p. 547-561.

STALLINGS, William. Cryptography and network security: principles and practice. 8. ed. Harlow: Pearson, 2021.

TEOH, Andrew B. J.; NGO, David C. L.; GOH, Alwyn. Biohashing: two factor authentication featuring fingerprint data and tokenised random number. Pattern Recognition, v. 37, n. 11, p. 2245-2255, 2004.