# **CHAVE CRIPTOGRÁFICA ÚNICA DERIVADA DE MARCADORES GENÉTICOS INDIVIDUAIS**




José Ricardo Vega Botelho¹ ; Luciane Costa Dalboni²

¹Graduando em Biomedicina, Universidade Cidade de São Paulo (UNICID), São Paulo, SP, Brasil. E-mail: josericardo@botelho.id

² Orientadora. Profa. Dra., Docente do Curso de Biomedicina da Universidade Cidade de São Paulo (UNICID), São Paulo, SP, Brasil.

**Versão:** Rascunho para revisão (Novembro/2026)

RESUMO

A identificação humana constitui um dos pilares fundamentais da biomedicina forense, da segurança digital e das ciências da informação. Métodos biométricos convencionais como impressões digitais, reconhecimento facial e padrões de íris apresentam vulnerabilidades importantes: podem ser falsificados, reproduzidos artificialmente ou capturados sem consentimento. Diante desse cenário, este trabalho desenvolve um modelo computacional para gerar uma Chave Criptográfica Única (CKU) derivada de marcadores genéticos individuais, combinando a singularidade biológica do DNA com o custo computacional imposto por funções de derivação memory-hard. O pipeline emprega marcadores forenses consolidados (STRs, SNPs, INDELs) codificados em representação canônica determinística e processados por Argon2id com salt de contexto, substituindo formulações anteriores que empregavam funções hash de uso geral (SHA-256, SHA-3, BLAKE3). A contribuição central do trabalho é dupla e deliberadamente honesta: quantificar com rigor a entropia efetiva da fonte genética sob três medidas complementares , 21,5 bits sob a convenção anterior (par ordenado), **17,7 bits como valor de segurança adotado** (genótipo canônico) e **13,6 bits de min-entropia**  , e validar experimentalmente a engenharia de derivação.O custo médio de derivação foi de 237,5 ms (σ = 13,0 ms) em hardware modesto, impondo custo de enumeração \~162.000× superior ao de hashes rápidos e projetando a busca exaustiva do espaço canônico em \~16 horas , custos que compram tempo, não entropia. Contudo, a entropia da fonte genética não alcança os patamares contemporâneos de segurança (128–256 bits): a aprovação estatística da saída não equivale ao sigilo da entrada, pois o adversário pode obter amostra biológica diretamente , e o modelo híbrido, que soma o perfil genético a um fator secreto adicional (\~58 bits combinados no painel didático), constitui a resposta estrutural a essa limitação. O trabalho contribui metodologicamente para a intersecção entre genética forense e criptografia aplicada, estabelecendo tanto a viabilidade do pipeline quanto as fronteiras que impõem sua adoção responsável, em conformidade com a Lei Geral de Proteção de Dados (LGPD).

**Palavras-chave:** Chave Criptográfica Única; Genética Forense; Criptografia; Argon2id; Min-entropia; LGPD; Autenticação Biométrica; Validação Estatística.

## ABSTRACT

Human identification constitutes one of the fundamental pillars of forensic biomedicine, digital security, and information sciences. Conventional biometric methods, such as fingerprints, facial recognition, and iris patterns, present important vulnerabilities: they can be forged, artificially reproduced, or captured without consent. Against this backdrop, this work develops a computational model to generate a Unique Cryptographic Key (CKU) derived from individual genetic markers, combining the biological uniqueness of DNA with the computational cost imposed by memory-hard key derivation functions. The pipeline employs consolidated forensic markers (STRs, SNPs, INDELs) encoded in a deterministic canonical representation and processed by Argon2id with a contextual salt, replacing earlier formulations that employed general-purpose hash functions (SHA-256, SHA-3, BLAKE3). The work's central contribution is twofold and deliberately honest: it rigorously quantifies the effective entropy of the genetic source under three complementary measures , 21.5 bits under the former ordered-pair convention, **17.7 bits as the adopted security value** (canonical genotype), and **13.6 bits of min-entropy** and it experimentally validates the derivation engineering. Mean derivation cost was 237.5 ms (σ = 13.0 ms) on modest hardware, imposing an enumeration cost \~162,000× higher than that of fast hashes and projecting exhaustive search of the canonical space at \~16 hours , costs that buy time, not entropy. However, the genetic source entropy does not reach contemporary security thresholds (128–256 bits): statistical approval of the output does not substitute for secrecy of the input, as an adversary may obtain a biological sample directly — and the hybrid model, combining the genetic profile with an additional secret factor (\~58 combined bits in the didactic panel), constitutes the structural answer to this limitation. The work contributes methodologically to the intersection of forensic genetics and applied cryptography, establishing both the pipeline feasibility and the boundaries that demand responsible adoption, in compliance with the Brazilian General Data Protection Law (LGPD).

**Keywords:** Unique Cryptographic Key; Forensic Genetics; Cryptography; Argon2id; Min-entropy; LGPD; Biometric Authentication; Statistical Validation.

## 1. INTRODUÇÃO

A identificação humana é um dos pilares fundamentais da biomedicina forense, da segurança digital e das ciências da informação. Ao longo das últimas décadas, métodos biométricos como impressões digitais, reconhecimento facial e padrões de íris tornaram-se amplamente utilizados em sistemas de autenticação (JAIN; FLYNN; ROSS, 2007). Entretanto, tais métodos apresentam vulnerabilidades importantes: podem ser falsificados, reproduzidos artificialmente ou capturados sem consentimento. Nesse contexto, o DNA surge como o identificador biológico mais robusto, estável e individualizado disponível na atualidade (BUTLER, 2015).

A genética forense utiliza regiões altamente polimórficas do genoma humano , Short Tandem Repeats (STRs), Single Nucleotide Polymorphisms (SNPs) e INDELs ,para estabelecer perfis individuais com elevado poder discriminatório (BUTLER, 2015). A escolha dos Short Tandem Repeats como marcador central deste trabalho não é arbitrária, mas decorre de quatro propriedades que os tornam singulares como fonte de material de derivação. *Primeira, a natureza discreta do dado:* a tipagem STR produz um genótipo categórico , um par de alelos por locus, determinado sem ambiguidade , ao contrário de biometrias contínuas (íris, face), cujas leituras variam entre capturas e exigem mecanismos de correção de erro; a discretude elimina a variação intraclasse do lado da fonte (distinção desenvolvida na Seção 10.6). *Segunda, a padronização forense:* os STRs autossômicos compõem os painéis comerciais consolidados (GlobalFiler, PowerPlex Fusion), com protocolos de tipagem regulados, reagentes disponíveis e cadeia de custódia institucionalizada , infraestrutura laboratorial que qualquer aplicação real da proposta herdaria sem custo adicional de desenvolvimento. *Terceira, a estabilidade temporal:* o genótipo STR é imutável ao longo da vida do titular, ao contrário de biometrias suscetíveis a envelhecimento, cicatrizes ou desgaste. *Quarta, a informatividade documentada:* as frequências alélicas populacionais dos STRs forenses são publicadas e auditadas há décadas, o que permite quantificar com precisão a entropia da fonte , inclusive sua limitação, que este trabalho mede e confronta em vez de pressupor.

Paralelamente, a criptografia moderna distingue duas primitivas com papéis distintos: as funções hash de uso geral : SHA-256, SHA-3, BLAKE3 , projetadas para velocidade (NIST, 2015a; 2015b; O'CONNOR et al., 2020), e as funções de derivação de chaves memory-hard, como a Argon2id (BIRYUKOV; DINU; KHOVRATOVICH, 2016), vencedora da Password Hashing Competition de 2015 e projetada precisamente para o cenário em que a entrada possui baixa entropia  como é o caso, como se verá, dos perfis genéticos. Essa distinção é central para o desenho do presente trabalho.

**Estado da arte.** A interface entre biometria e criptografia constitui campo estabelecido, com três famílias dominantes de técnicas: o Fuzzy Vault (JUELS; SUDAN, 2006) e os fuzzy extractors (DODIS et al., 2008), concebidos para biometrias ruidosas mediante correção de erro; e o BioHashing (TEOH et al., 2004), que projeta a biometria em domínio pseudoaleatório parametrizado por token, perseguindo revogabilidade. A derivação de chaves a partir de material genético, porém, permanece pouco explorada na literatura em comparação à maturidade dessas famílias  e, até onde alcança nossa revisão, o estudo mais próximo localizado (AL-QUDSY, 2025) cifra o perfil genético com AES-256 e esteganografia, mas não o emprega como fonte de derivação de chaves nem quantifica sua entropia, mede o custo de enumeração sob KDF memory-hard ou delimita o modelo de ameaça correspondente. A lacuna que este trabalho ocupa é precisamente a de quantificação honesta: aplicação de bateria estatística completa, reporte das três medidas de entropia (máxima, Shannon, mínima) e delimitação explícita do que a aprovação estatística certifica , e do que não certifica. O posicionamento detalhado frente a cada técnica ocupa a Seção 10.6.

Diante desse cenário, propõe-se a criação de uma Chave Criptográfica Única (CKU) derivada diretamente de marcadores genéticos individuais, sob a formalização CKU = Argon2id(S‖s), onde S é a codificação binária canônica do perfil genético e s é um salt de contexto. As aplicações da proposta são articuladas no Capítulo 8: interoperabilidade de prontuários eletrônicos de saúde (vinculação biológica inseparável, dispensando terceiro emissor), controle de acesso em ambientes de alta segurança (fator "algo que o usuário é" com especificidade estrutural), integridade de cadeia de custódia forense (vínculo criptográfico entre amostra, laudo e conclusão), autenticação de atos societários (fator não delegável, valioso em governança) e conformidade com a LGPD (dados genéticos como categoria sensível  BRASIL, 2018). Em todas elas, o custo de 237,5 ms por verificação (σ = 13,0 ms, Seção 7.2) é compatível com o uso interativo individual, ao passo que penaliza deliberadamente a enumeração massiva.

 O trabalho aporta três novidades articuladas confirmando sua originalidade . *Primeira:* a quantificação experimental, em um pipeline integralmente reprodutível (seed = 2024, repositório público, suíte automatizada de 25 testes), do que uma fonte genética forense pode e não pode oferecer à criptografia , as três baterias estatísticas aprovadas coexistem com uma entropia de segurança de 17,7 bits (min-entropia: 13,6), e essa coexistência é ela mesma o achado: viabilidade técnica não equivale a segurança, e nenhum estudo anterior quantificou essa tensão com validação experimental em painel STR. *Segunda:* a arquitetura de derivação Argon2id aplicada a fonte genética, com canonização unívoca do genótipo como etapa criptográfica explícita, elevando o custo da enumeração de menos de um segundo para \~16 horas no espaço canônico (\~9,4 dias no espaço de fase)  multiplicador de \~162.000× medido sobre funções hash de uso geral. *Terceira:* a distinção metodológica entre três medidas de entropia : máxima, de Shannon e mínima , e a adoção explícita da convenção canônica (17,7 bits) como valor de segurança, corrigindo a superestimativa da convenção de par ordenado (21,5 bits) que contava fase parental irrecuperável pela tipagem;Os  testes de regressão executáveis, transforma uma sutileza teórica em critério de projeto verificável.

Além de seu potencial tecnológico, a proposta exige análise rigorosa de aspectos éticos, legais e de privacidade, especialmente no contexto da Lei Geral de Proteção de Dados (LGPD), que classifica informações genéticas como dados sensíveis (BRASIL, 2018). Portanto, o desenvolvimento de uma chave criptográfica baseada em DNA deve garantir que o processo seja não reversível, evitando qualquer possibilidade de reconstrução do perfil genético original , requisito que, como este trabalho demonstra empiricamente, é atendido, mas que não esgota a análise de segurança: a possibilidade de obtenção direta de amostra biológica por um adversário constitui limitação estrutural que motiva a recomendação de um modelo híbrido (perfil genético + fator secreto adicional) para aplicações críticas.

Este trabalho organiza-se da seguinte forma: o Capítulo 2 apresenta a justificativa e relevância; o Capítulo 3 os objetivos; o Capítulo 4 o referencial teórico; o Capítulo 5 a metodologia; o Capítulo 6 o modelo matemático consolidado; o Capítulo 7 os resultados experimentais; o Capítulo 8 as aplicações; o Capítulo 9 as limitações; o Capítulo 10 a discussão; e o Capítulo 11 as conclusões e extensões futuras.

## 2. JUSTIFICATIVA E RELEVÂNCIA

A crescente digitalização de processos biomédicos, administrativos e jurídicos exige sistemas de autenticação cada vez mais robustos. Senhas são reutilizadas, esquecidas e furtadas por phishing; tokens físicos são perdidos, clonados ou delegáveis a terceiros; e as biometrias convencionais , impressões digitais, reconhecimento facial, padrões de íris , embora amplamente implantadas, podem ser falsificadas com moldes de silicone, replicadas por deepfakes ou capturadas sem consentimento do titular. Nenhum desses mecanismos oferece, isoladamente, as três propriedades que um identificador de alta confiabilidade idealmente reuniria: unicidade prática, impossibilidade de delegação e estabilidade ao longo de toda a vida do titular.

A genética forense oferece um conjunto de marcadores altamente polimórficos , os Short Tandem Repeats (STRs) e, mais recentemente, SNPs e INDELs , capazes de distinguir indivíduos com elevado grau de precisão (KWON et al., 2021). Esses marcadores sustentam, há décadas, a identificação humana em contextos criminais e de parentesco, com protocolos de tipagem padronizados, reagentes comerciais disponíveis e cadeia de custódia institucionalizada ,  infraestrutura que qualquer aplicação criptográfica herdaria sem custo adicional de desenvolvimento. O presente trabalho parte, contudo, de uma distinção que estrutura todo o seu desenho: o poder discriminatório de um painel genético , a baixíssima probabilidade de coincidência entre dois indivíduos não relacionados ,  **não equivale ao sigilo criptográfico da fonte**. As frequências alélicas que tornam o painel identificável são públicas; um identificador extraordinário não é, por isso, um segredo forte. A pergunta que motiva o trabalho é precisamente a de quantificar essa distância , e de estabelecer, com números, o que a fonte genética pode e o que não pode oferecer à criptografia.

A união entre biomedicina forense e análise de sistemas proposta aqui explora quatro vantagens estruturais do material genético como fundamento de derivação de chaves: a unicidade prática (perfis distinguíveis com especificidade de bilhões para um em painéis comerciais); a irreversibilidade da função de derivação (a chave derivada não permite reconstruir o perfil que a originou); a estabilidade temporal (o genótipo é imutável ao longo da vida); e a amplitude de aplicações : do prontuário eletrônico à cadeia de custódia forense, ao controle de acesso e à conformidade regulatória (Capítulo 8). Todas essas aplicações operam, ademais, sob um regime legal específico: a Lei Geral de Proteção de Dados classifica dados genéticos como pessoais sensíveis, impondo medidas técnicas proporcionais ao risco (BRASIL, 2018)  e um pipeline que não armazena o dado sensível, apenas a chave dele derivada, dialoga diretamente com esses princípios.

Relevância adicional decorre da própria natureza interdisciplinar da proposta: o trabalho conflui as três formações do autor : Biomedicina (a fonte: genética forense e tipagem STR), Análise e Desenvolvimento de Sistemas (o instrumento: pipeline computacional, derivação criptográfica e validação estatística) e Administração (o contexto: aplicações corporativas, governança e conformidade regulatória) , numa única prova de conceito executável. Por fim, registra-se o enquadramento programático: este trabalho constitui a Fase 1 de um programa de pesquisa contínuo . Fase 2: frequências alélicas empíricas e painel ampliado; Fase 3: painel completo (20 STRs, 130 SNPs, 15 INDELs) e CKU Ampliada , de modo que as delimitações aqui documentadas funcionam como agenda explícita das etapas seguintes, não como pontos finais.

## 3. OBJETIVOS

Os objetivos abaixo delimitam a Fase 1 do programa de pesquisa: uma prova de conceito computacional integralmente reprodutível sobre um painel didático de cinco loci STR, com dados sintéticos de frequência plausível.

### 3.1 Objetivo geral

Desenvolver um modelo computacional capaz de gerar uma Chave Criptográfica Única (CKU) derivada de marcadores genéticos individuais, mediante canonização determinística do genótipo e derivação por função memory-hard (Argon2id), caracterizando , e não presumindo , a unicidade prática, a irreversibilidade da derivação e os limites de segurança da fonte, em conformidade com a LGPD (BRASIL, 2018).

### 3.2 Objetivos específicos

1. **Identificar** marcadores genéticos forenses (STRs, SNPs, INDELs) adequados como fonte de material de derivação, justificando a escolha dos STRs como marcador central;
2. **Quantificar** as três medidas de entropia da fonte , máxima teórica, de Shannon (nas convenções de par ordenado e de genótipo canônico) e mínima , distinguindo identificação populacional de sigilo criptográfico;
3. **Calcular a min-entropia por locus**, identificando os loci mais vulneráveis à enumeração gulosa por um atacante que conhece as frequências públicas;
4. **Definir** a codificação binária canônica do perfil (ordenação de loci e alelos, delimitadores unívocos, comprimento fixo \~61 bytes), como etapa criptográfica de preparação de entrada;
5. **Formalizar** a derivação CKU = Argon2id(S‖s) e compará-la, em custo de enumeração, avalanche e irreversibilidade, com formulações baseadas em hashes de uso geral (SHA-256, SHA-3, BLAKE3);
6. **Implementar** o pipeline em Python, integralmente reprodutível (semente fixa, repositório público, suíte automatizada de testes);
7. **Validar** o determinismo condicional (mesmo perfil e mesmo salt ⇒ mesma chave), a canonização (invariância à ordem de entrada), o efeito avalanche e o isolamento estatístico entre salts distintos;
8. **Analisar** as implicações éticas e legais da proposta no quadro da LGPD (BRASIL, 2018);
9. **Delinear** as classes de aplicação (Capítulo 8) e o modelo híbrido com fator secreto substituível (Seção 6.7), como resposta arquitetural à limitação de entropia e à irrevogabilidade do material genético;
10. **Apontar** as extensões futuras do programa de pesquisa: painel completo (\~275 bits projetados), frequências alélicas empíricas (STRBase, ALFRED, 1000 Genomes), bateria completa do NIST SP 800-22 e CKU Ampliada para discriminação de gêmeos monozigóticos.

## 4. REFERENCIAL TEÓRICO

### 4.1 Genética forense e marcadores moleculares de identificação

A identificação humana por meio de material genético constitui um dos pilares da biomedicina forense contemporânea. Desde a introdução do DNA fingerprinting por Jeffreys e colaboradores (JEFFREYS et al., 1985), a técnica foi aplicada pela primeira vez em investigação criminal em 1986, no caso que culminou na exclusão de um suspeito e, posteriormente, na identificação de Colin Pitchfork (NATIONAL LIBRARY OF MEDICINE, 2006). Desde então, a análise genética forense evoluiu para sistemas padronizados e amplamente utilizados.

Os marcadores mais empregados são os Short Tandem Repeats (STRs), regiões do genoma humano compostas por repetições em tandem de unidades curtas de nucleotídeos, tipicamente de 2 a 6 pares de bases, cuja variação no número de repetições confere elevado poder discriminatório (BUTLER, 2011). Além dos STRs, ganharam espaço na genética forense moderna os Single Nucleotide Polymorphisms (SNPs) , variações de um único nucleotídeo em posições específicas do genoma ,  e os INDELs (Insertions/Deletions), pequenas inserções ou deleções de bases. Enquanto os STRs são tipicamente codominantes, permitindo a distinção dos dois alelos em heterozigotos, SNPs e INDELs são frequentemente bialélicos e apresentam menor diversidade alélica por locus, embora possam ser analisados em grande número (BUTLER, 2015; PROMEGA, 2023).

**Justificativa da escolha de STRs como fonte do painel.** A opção por STRs como marcadores do presente estudo decorre de quatro propriedades convergentes: (i) representação **discreta** , a tipagem STR produz genótipos categóricos e estáveis, ao contrário de medidas fenotípicas contínuas sujeitas a variação intraclasse; (ii) codominância : ambos os alelos do heterozigoto são observáveis, maximizando a informação por locus; (iii) padronização forense consolidada : loci como D18S51, D21S11, D3S1358, D5S818 e TH01 integram painéis comerciais de uso mundial (PROMEGA, 2023), com protocolos e nomenclatura universalmente estabelecidos; e (iv) estabilidade temporal : o genótipo STR é invariante ao longo da vida do titular, requisito essencial para um identificador criptográfico persistente. Essas propriedades tornam o STR o marcador de menor atrito para derivação determinística de chaves: não exige correção de ruído nem mecanismos de tolerância a leituras imperfeitas, simplificando estruturalmente o pipeline (análise comparativa com biometrias ruidosas na Seção 10.6).

O poder discriminatório de um painel genético é quantificado pela probabilidade de coincidência aleatória, isto é, pela chance de dois indivíduos não relacionados apresentarem exatamente o mesmo perfil. Painéis comerciais como o GlobalFiler e o PowerPlex Fusion analisam cerca de 23 a 24 loci, resultando em probabilidades de coincidência frequentemente na ordem de 10⁻²² a 10⁻²⁸, conforme o painel, a população de referência e o modelo estatístico adotado (PROMEGA, 2023).

Entretanto, há uma distinção crítica que este trabalho enfatiza desde o referencial teórico: **o poder discriminatório populacional de um painel genético não equivale ao sigilo criptográfico da mesma informação.** Um painel com alto poder discriminativo identifica um indivíduo entre milhões, mas não impede que um adversário que obtenha amostra biológica direta (saliva em copo, fio de cabelo, pele descamada) reconstrua o perfil e derive a chave associada. Essa assimetria entre identificação e imprevisibilidade constitui a tensão central que estrutura o problema de segurança deste trabalho.

### 4.2 Entropia da informação e métricas de imprevisibilidade

A segurança de um sistema baseado em chave derivada de fonte biológica depende fundamentalmente da **entropia da fonte** , a imprevisibilidade do material de entrada diante de um adversário que conhece as distribuições populacionais. Este trabalho opera com três medidas distintas, cada uma respondendo a uma pergunta adversarial diferente.

**Entropia de Shannon.** Mede, em bits, a quantidade média de informação de uma variável aleatória:

H(X) = − Σᵢ p(xᵢ) · log₂ p(xᵢ)

onde p(xᵢ) é a probabilidade do resultado xᵢ. Sob distribuição uniforme sobre n símbolos, a **entropia máxima** é log₂ n; sob frequências reais, a entropia observada é sempre menor que a máxima (STALLINGS, 2021).

**Min-entropia.** Definida como H∞ = −log₂(max pᵢ), corresponde ao extremo da família de entropias de Rényi e mede a imprevisibilidade do **evento mais provável**. Trata-se da medida correta para bornear o sucesso de um único palpite otimizado e, por extensão, do **atacante guloso** que enumera candidatos por ordem decrescente de probabilidade , comportamento precisamente viável quando as frequências alélicas são públicas, como no caso forense (a utilização de min-entropia como limite conservador de fontes biométricas é estabelecida na literatura de fuzzy extractors; DODIS et al., 2008). Para qualquer distribuição vale a hierarquia:

H∞ ≤ H(X) ≤ log₂ n

com igualdades somente sob distribuição uniforme. Essa hierarquia, embora elementar, é frequentemente negligenciada em formulações que associam a saída de funções criptográficas a "segurança de 256 bits" a partir de fontes com entropia muito inferior ,  a distinção que os resultados deste trabalho quantificam empiricamente (Seções 7.1 e 10).

**Genótipo diplóide: par ordenado e genótipo canônico.** Para marcadores codominantes, a entropia por locus depende do número de alelos e de suas frequências. A tabela a seguir apresenta as entropias máximas esperadas por tipo de marcador, sob dois modelos: (i) codominante, onde todos os genótipos são distinguíveis; e (ii) dominante, onde apenas presença/ausência é observada.

| Tipo de marcador | Estados possíveis | H máx (codominante) | H máx (dominante) |
| --- | --- | --- | --- |
| STR (5 alelos) | 15 genótipos | 3,91 bits | — |
| SNP (bialélico) | 3 genótipos | 1,58 bits | 1,00 bit |
| INDEL (bialélico) | 3 genótipos | 1,58 bits | 1,00 bit |

Em frequências populacionais realistas, as entropias efetivas são menores: para frequência moderada (p ≈ 0,3 no alelo minoritário), a entropia de um marcador bialélico no modelo codominante aproxima-se de \~1,34 bits.

Impõe-se aqui uma precisão conceitual que estrutura as Seções 6 e 7. Sob Hardy-Weinberg com alelos sorteados independentemente, a entropia do genótipo como **par ordenado de sorteios** (fase parental incluída) aproxima-se do dobro da entropia haploide. Todavia, a **tipagem STR não observa a fase**: os genótipos (a,b) e (b,a) são indistinguíveis no laboratório e convergem, pela canonização deste pipeline (Seção 5.3), para a mesma representação de bytes. A entropia relevante para a análise de enumeração é, portanto, a do **genótipo canônico** (não-ordenado) , inferior à do par ordenado. As três medidas (par ordenado, genótipo canônico e min-entropia) são quantificadas experimentalmente na Seção 7.1.2, que adota o genótipo canônico como valor de segurança da fonte.

**Distância de Hamming.** Definida como o número de posições em que duas sequências binárias de igual comprimento diferem, a distância de Hamming é a métrica com que este trabalho avalia o **efeito avalanche:&#32;** a propriedade exigida do operador de derivação de que entradas minimamente distintas produzam saídas maximalmente dissimilares (≈ 50% dos bits de saída alterados). Declara-se desde já que a métrica é operada **em nível de bit**: a expectativa teórica de 50% vale para bits, e a medida compõe, com as baterias estatísticas, o quadro de validação do operador (Seção 7.3). É importante notar o papel distinto dessa métrica: o avalanche avalia a **difusão da função de derivação**, não a entropia da fonte .  a média de 50% garante que entradas próximas não gerem chaves correlacionadas, mas não amplia a imprevisibilidade do espaço de entrada.

### 4.3 Fundamentos criptográficos do pipeline

Esta seção apresenta os conceitos criptográficos mobilizados pelo pipeline, com a justificativa da escolha de cada método , critério de seleção: resistência ao modelo de ameaça específico de uma fonte de baixa entropia e pública.

#### 4.3.1 Criptografia simétrica e AES-256

O padrão AES (Advanced Encryption Standard), na variante de chave de 256 bits, é o padrão dominante de criptografia simétrica contemporânea (STALLINGS, 2021). A chave-alvo do pipeline é definida em 256 bits por ser o tamanho compatível com AES-256 , e é exatamente esse patamar que serve de régua para o diagnóstico central do trabalho: a fonte genética do painel didático situará sua entropia de segurança na casa das dezenas de bits (Seção 7.1), de modo que a função de derivação não pode ser tratada como fonte de segurança por si só.

#### 4.3.2 Funções hash de uso geral: SHA-256, SHA-3 e BLAKE3

Funções hash criptográficas mapeiam mensagens de tamanho arbitrário para saídas de tamanho fixo, com três propriedades de segurança: *preimage resistance* (dado o digest, é inviável encontrar mensagem que o produza), *second preimage resistance* (dada uma mensagem, é inviável encontrar outra distinta com o mesmo digest) e *collision resistance* (é inviável encontrar duas mensagens distintas com o mesmo digest) (STALLINGS, 2021). As funções consideradas neste trabalho são: SHA-256, da família SHA-2, especificada no FIPS 180-4 (NIST, 2015a); SHA-3, baseada na construção Keccak, vencedora da competição do NIST em 2012 e padronizada no FIPS 202 (NIST, 2015b); e BLAKE3, função moderna de altíssimo desempenho projetada para paralelismo multicore (O'CONNOR et al., 2020).

**Justificativa do papel no trabalho.** Essas primitivas são projetadas para velocidade , processam gigabytes por segundo em hardware convencional, na casa dos microssegundos por bloco. Para integridade e autenticação de dados, isso é desejável; para derivação de chaves a partir de **entradas de baixa entropia**, é exatamente o oposto: a velocidade viabiliza enumeração em larga escala, com bilhões de candidatos testados por segundo em GPUs especializadas. Por isso, as formulações anteriores deste modelo (CKU = H(S‖s), com hash de uso geral) foram **substituídas** pela KDF memory-hard; os hashes rápidos permanecem no trabalho apenas como *baseline comparativo* de custo de enumeração (Seção 7.4), papel metodológico que justifica sua presença no referencial.

#### 4.3.3 Funções de derivação de chaves memory-hard e Argon2id

Diante da vulnerabilidade das funções rápidas ao ataque massivamente paralelo, desenvolveu-se uma classe especializada: as funções de derivação de chaves (*key derivation functions*, KDFs) **memory-hard**, que impõem simultaneamente custo computacional e custo de memória (RAM dedicada por tentativa) , último custo decisivo, pois a memória não escala com a generosidade da computação bruta em hardware paralelo.

A Argon2id é a vencedora da Password Hashing Competition (2015), competição internacional para seleção do algoritmo de derivação de senhas (BIRYUKOV; DINU; KHOVRATOVICH, 2016), padronizada posteriormente no RFC 9106 (IETF, 2021). A variante *id* (híbrida) combina resistências herdadas do Argon2d (contra ataques de canal lateral) e do Argon2i (contra ataques de tempo-memória), sendo adequada para aplicações que exigem resistência a atacantes com acesso a hardware especializado.

**Justificativa da escolha e dos parâmetros.** A Argon2id foi adotada por ser o estado da arte em KDFs memory-hard, com calibração por quatro parâmetros: *time\_cost* (t, passes sobre a memória), *memory\_cost* (m, memória em KiB por derivação), *parallelism* (p, threads) e *hash\_len* (comprimento da saída). O presente trabalho adota t = 3, m = 64 MiB, p = 1 e hash\_len = 32 (256 bits), configurando derivação de \~238 ms em hardware modesto e compatível com dispositivos de baixo custo — calibração deliberada que favorece portabilidade sem sacrificar o custo imposto ao atacante (o desvio de p = 1 frente à configuração de referência do RFC 9106, p = 4, é justificado na Seção 5.4).

#### 4.3.4 Salt e geração pseudoaleatória criptograficamente segura

O salt é um valor aleatório único por derivação, incorporado ao material de entrada da função de derivação. Sua geração exige um gerador pseudoaleatório **criptograficamente seguro** (CSPRNG) . Geradores estatísticos comuns produzem sequências previsíveis por adversários informados do estado interno, o que neutralizaria a função do salt. Três propriedades delimitam o conceito: o salt **não é secreto** (pode ser armazenado junto aos metadados da chave; BIRYUKOV; DINU; KHOVRATOVICH, 2016; IETF, 2021); **não acrescenta entropia** à fonte (sua função é de diversificação, não de segredo); e seu determinismo é **condicional** , mesmo perfil e mesmo salt produzem a mesma chave (requisito de descriptografia), enquanto salts distintos produzem chaves estatisticamente independentes do mesmo perfil. O salt previne ataques com tabelas pré-computadas (rainbow tables) e viabiliza a derivação de chaves independentes a partir do mesmo perfil genético; a semântica operacional completa (armazenamento, recuperação, ciclo de vida) está na Seção 5.4.

#### 4.3.5 Ataques por enumeração e o modelo de custo

O ataque por enumeração (busca exaustiva offline) percorre sistematicamente o espaço de candidatos plausíveis da fonte, submetendo cada um à função de derivação e comparando o resultado com o material observado. Seu custo total é o produto de dois fatores independentes: o **tamanho do espaço de busca**, ditado pela entropia da fonte (2^H candidatos na expectativa , ou 2^(H∞) no pior caso do defensor), e o **custo por tentativa**, ditado pela dureza da função de derivação. A implicação estrutural orienta todo o desenho deste trabalho: a segurança é limitada pelo produto dos dois fatores, e **nenhum fator substitui o outro** , a função mais dura do mundo não compensa uma fonte de entropia desprezível, e a fonte mais imprevisível é derrotada por uma derivação instantânea. As frequências alélicas forenses serem públicas agrava o primeiro fator: o adversário conhece a distribuição e pode enumerar por ordem decrescente de probabilidade, contexto em que a min-entropia (4.2) é o limite correto.

#### 4.3.6 Canonização como etapa criptográfica de preparação de entrada

Sistemas criptográficos determinísticos exigem que **entradas geneticamente equivalentes sejam byte a byte idênticas**: qualquer variação trivial de representação (ordem de inserção, ordem dos alelos do heterozigoto, delimitadores ambíguos) produziria chaves distintas para o mesmo titular, inviabilizando a descriptografia. A canonização (Seção 5.3) cumpre esse requisito por uma serialização injetiva e determinística , loci em ordem alfabética fixa, alelos ordenados por valor, delimitadores unívocos , verificada empiricamente pela suíte de testes (invariância à ordem de entrada). Note-se o papel duplo da etapa: do lado da **usabilidade**, garante reprodutibilidade; do lado da **segurança**, ela também *destrói a informação de fase* (a ordem parental dos alelos), reduzindo o espaço que o atacante precisa enumerar ,consequência quantificada na Seção 7.1.2 e assumida conscientemente no valor de segurança adotado.

### 4.4 Proteção legal de dados genéticos: LGPD e dados sensíveis

A Lei nº 13.709/2018 (LGPD) classifica dados genéticos como dados pessoais sensíveis (Art. 5º, inciso II), submetendo seu tratamento a bases legais específicas e aos princípios da finalidade, necessidade, adequação e segurança (BRASIL, 2018). Três implicações diretas condicionam o desenho deste trabalho. Primeira, a decisão de operar com **dados sintéticos** na Fase 1 atende simultaneamente ao requisito ético (elimina o tratamento de dados reais fora de finalidade lícita específica) e ao requisito metodológico (permite controle total dos parâmetros populacionais). Segunda, o próprio objetivo do pipeline , gerar chaves das quais o perfil não seja recuperável , dialoga com o princípio da minimização: o artefato armazenado não contém o dado sensível. Terceira, a adoção de função de derivação memory-hard constitui medida técnica proporcional ao risco, na linha do princípio da segurança (Art. 46). A análise completa de conformidade das aplicações, incluindo a ressalva de que a tipagem genética na autenticação constitui ela própria tratamento de dado sensível, é desenvolvida na Seção 8.5.

## 5. METODOLOGIA

### 5.1 Desenho geral

O estudo foi conduzido como prova de conceito computacional em duas frentes: (i) quantificação da entropia de um painel didático de cinco marcadores STR; e (ii) avaliação experimental do operador de derivação CKU sobre perfis sintéticos. O painel didático , D3S1358, TH01, D21S11, D18S51 e D5S818 , foi definido com cinco alelos por locus (exceto D5S818, com quatro), frequências alélicas compatíveis com as ordens de grandeza reportadas na literatura forense. Esta é a Fase 1 de um programa de pesquisa em três etapas: a Fase 2 substituirá as frequências simuladas por frequências empíricas de bases públicas (STRBase, ALFRED, 1000 Genomes) e ampliará o painel; a Fase 3 avaliará o painel completo (20 STR + 130 SNP + 15 INDEL).

### 5.2 Geração dos perfis sintéticos

Os perfis foram gerados por simulação estocástica com semente fixa (`seed=2024`, `numpy.random.default_rng`), assegurando reprodutibilidade integral: qualquer pessoa executando o pipeline obtém exatamente o mesmo conjunto de dados.

1. Para cada locus, os dois alelos do genótipo foram sorteados de forma **independente** a partir das frequências alélicas da Tabela 5.1 (`rng.choice(size=2, p=frequências)`), simulando a fase germinativa do par paterno/materno;
2. Foram gerados 5.000 perfis completos, dos quais 400 foram reservados para a bateria de validação estatística;
3. Cada perfil foi submetido à canonização (Seção 5.3) e serializado para a derivação.

**Declaração de origem das frequências:** as frequências da Tabela 5.1 são **simuladas** (população de referência hipotética, painel didático). Escolha metodológica deliberada da Fase 1 — proteção de dados e foco no pipeline — e **não exigência da LGPD**. Substituição por frequências empíricas: Fase 2.

**Tabela 5.1 — Frequências alélicas simuladas do painel didático** *(valores extraídos de&#32;`PAINEL_STR`, Notebook 02)*

| Locus | Alelos e frequências (simuladas) |
| --- | --- |
| D3S1358 | 15: 0,21 · 16: 0,26 · 17: 0,22 · 18: 0,22 · 19: 0,09 |
| TH01 | 6: 0,23 · 7: 0,19 · 8: 0,31 · 9: 0,17 · 9.3: 0,10 |
| D21S11 | 28: 0,16 · 29: 0,24 · 30: 0,27 · 31: 0,18 · 32: 0,15 |
| D18S51 | 13: 0,15 · 14: 0,21 · 15: 0,33 · 16: 0,19 · 17: 0,12 |
| D5S818 | 11: 0,36 · 12: 0,38 · 13: 0,20 · 14: 0,06 |

*(Todos os vetores somam 1,00.)*

### 5.3 Canonização e serialização canônica

A função `perfil_canonico(·)` transforma o perfil genético em uma sequência de bytes canônica (\~61 bytes no painel didático):

- **Ordem fixa de loci** : ordenação alfabética estrita (o mesmo dicionário Python pode iterar em ordens diferentes entre contextos);
- **Alelos ordenados** :o genótipo é serializado com os alelos em ordem numérica crescente: `(16,17)` e `(17,16)` produzem **exatamente os mesmos bytes**;
- **Delimitadores unívocos** : formato `LOCUS:alelo1:alelo2` com separador `|`, impedindo que "(1,15)" seja lido como "(11,5)"; alelos decimais (9.3) suportados.

**Consequência formal:** como a canonização funde as duas fases do heterozigoto em uma única representação, o espaço efetivamente enumerável pelo atacante é o dos **genótipos canônicos** (n·(n+1)/2 combinações por locus), e não o de pares ordenados. A tipagem STR de fragmentos não recupera a fase , a ordem paterna/materna é fisicamente irrecuperável. A entropia do espaço canônico é, portanto, o valor de segurança relevante (Seção 6.4).

A canonização garante a invariância à ordem de inserção de loci e alelos  verificada por teste de unidade dedicado (suíte `tests/test_determinismo.py`).

### 5.4 Salt e geração pseudoaleatória

Salt de 16 bytes (128 bits) gerado por CSPRNG (`secrets.token_bytes`). Semântica:

1. **Determinismo condicional** : a mesma chave é reproduzida se, e somente se, forem usados o mesmo perfil canônico **e** o mesmo salt;
2. **Não-secretividade** : o salt não é fator secreto (armazenado junto ao contexto de uso; o Notebook 02 o persiste junto à chave);
3. **Insignificância entrópica** : o salt não aumenta a entropia da fonte;
4. **Função** : chaves independentes por contexto/domínio; bloqueio de tabelas pré-computadas (*rainbow tables*) dirigidas ao painel;
5. **Recuperação** : a regeneração da chave exige a recuperação fiel do salt original, persistido com verificação de integridade.

### 5.5 Hipótese de independência entre loci

O cálculo da entropia total assume independência entre os cinco loci (entropias aditivas). O equilíbrio de Hardy-Weinberg por locus é condição **necessária, mas não suficiente**: não exclui associação entre loci (*linkage disequilibrium*). A independência é hipótese de trabalho; verificação empírica com frequências reais na Fase 2.

### 5.6 Procedimento de validação (Notebook 03)

Três baterias estatísticas no estilo NIST SP 800-22, α = 0,05, sobre 400 chaves derivadas (12.800 bytes, 102.400 bits):

- **Uniformidade de bytes** : qui-quadrado de bondade de ajuste sobre a frequência dos 256 valores de byte (esperado ≈ 50 por valor);
- **Equilíbrio de bits** : proporção global de bits 1 e análise posicional (IC 99% por posição);
- **Efeito avalanche** : 60 pares de chaves formados por mutação de **um único bit** no material canônico (XOR 0x01 no último byte), **mesmo salt**, medindo a distância de Hamming em bits.

Esses testes avaliam características estatísticas da saída e **não comprovam, isoladamente, a segurança criptográfica** do esquema (Seção 10).

### 5.7 Ambiente computacional e reprodutibilidade

| Item | Especificação |
| --- | --- |
| Processador | AMD FX-8370E (hardware de referência modesto) |
| Memória | 8 GiB RAM |
| Sistema | Linux Mint 22.3 |
| Python | 3.12.3 |
| Bibliotecas | argon2-cffi 23.1.0, numpy, pandas, scipy, matplotlib |
| Parâmetros Argon2id | time\_cost=3, memory\_cost=65536 (64 MiB), parallelism=1, hash\_len=32 (Type.ID) |
| RNG | `numpy.random.default_rng(seed=2024)` (dados); `secrets` (salts, CSPRNG) |
| Testes | pytest, suíte de 25 casos (`make test`) |
| Repositório | github.com/botelhojrv-dev/tcc-genetica-cripto |

## 6. MODELO MATEMÁTICO

### 6.1 Definições

**Entropia de Shannon por alelo:** H(X) = − Σᵢ pᵢ · log₂ pᵢ, sobre as frequências alélicas pᵢ do locus.

**Convenção do par ordenado :** H\_gen(ord) = 2·H\_alelo ,  conta (a,b) e (b,a) como resultados distintos. Sob independência e Hardy-Weinberg, esse valor coincide com a entropia de Shannon do genótipo *antes* da fusão de fases.

**Entropia do espaço canônico:** H\_gen(canon) = 2·H\_alelo − (1 − Σ pᵢ²) : corrige a fusão dos heterozigotos pela canonização (redução de 1 bit por massa de probabilidade de par heterozigoto).

**Min-entropia:** H∞ = −log₂ p\*, onde p\* = 2·p\_a·p\_b é a probabilidade do genótipo canônico mais provável (dois alelos mais frequentes, heterozigoto, se 2·p\_a·p\_b > p\_a²). A fundamentação formal é a entropia de Rényi de ordem infinita (RÉNYI, 1961).

### 6.2 Tabela consolidada por locus

| Locus | n alelos | H alelo (bits) | H par ordenado (bits) | H canônico (bits) | Genótipo mais provável | P (gen.) | H∞ (bits) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D3S1358 | 5 | 2,252 | 4,504 | 3,721 | 16/17 | 0,1144 | 3,128 |
| TH01 | 5 | 2,234 | 4,468 | 3,692 | 6/8 | 0,1426 | 2,810 |
| D21S11 | 5 | 2,283 | 4,566 | 3,777 | 29/30 | 0,1296 | 2,947 |
| D18S51 | 5 | 2,233 | 4,467 | 3,693 | 14/15 | 0,1386 | 2,851 |
| D5S818 | 4 | 1,769 | 3,538 | 2,855 | 11/12 | 0,2736 | 1,870 |
| **Total** | — | 10,77 | **≈ 21,54** | **≈ 17,74** | — | — | **≈ 13,61** |

### 6.3 Demonstração passo a passo: locus D5S818

**Passo 1 : entropia do alelo.** Com p = (0,36; 0,38; 0,20; 0,06): H = −(0,36·log₂0,36 + 0,38·log₂0,38 + 0,20·log₂0,20 + 0,06·log₂0,06) = −(0,36·(−1,4739) + 0,38·(−1,3959) + 0,20·(−2,3219) + 0,06·(−4,0589)) = 0,5306 + 0,5304 + 0,4644 + 0,2435 = **1,769 bits/alelo**.

**Passo 2 : par ordenado.** H\_ord = 2 × 1,769 = **3,538 bits**. Este é o valor da convenção original do TCC; o locus atinge 3,538/4,00 = **88,4%** da eficiência máxima de 4 alelos.

**Passo 3 : correção canônica.** Σp² = 0,36² + 0,38² + 0,20² + 0,06² = 0,3176. H\_canon = 3,538 − (1 − 0,3176) = 3,538 − 0,682 = **2,855 bits** — o espaço que um atacante enumera contra a representação canônica (10 genótipos possíveis, teto log₂10 = 3,32 bits).

**Passo 4 : min-entropia.** Genótipo mais provável: 11/12, P = 2·0,36·0,38 = 0,2736. H∞ = −log₂ 0,2736 = **1,870 bits**  menos da metade da entropia média: um atacante que testa os genótipos por ordem de frequência acerta este locus com pouco mais de 1 bit de esforço esperado no pior caso.

### 6.4 Entropia total do painel : os três números do trabalho

Sob independência entre loci, as entropias somam. Este trabalho apresenta explicitamente os **três valores, com papéis distintos**:

1. **≈ 21,5 bits**  convenção do par ordenado (2·ΣH\_alelo = 21,54). Valor do TCC original; **superestima** o espaço enumerável, pois conta as fases do heterozigoto que a tipagem STR não recupera e que a canonização funde;
2. **≈ 17,7 bits**  entropia de Shannon do **espaço canônico** (2·ΣH\_alelo − Σ\_loci (1−Σp²) = 17,74). Corresponde ao espaço efetivamente enumerável contra a representação serializada — **é o valor de segurança adotado neste trabalho**;
3. **≈ 13,6 bits** min-entropia do painel: −log₂(0,1144·0,1426·0,1296·0,1386·0,2736) = −log₂(8,1×10⁻⁵) = 13,61. Pior caso para enumeração guiada por frequência (atacante ótimo que testa os genótipos mais prováveis primeiro).

A adoção do valor canônico transforma a correção em evidência de rigor metodológico: a fase do heterozigoto é fisicamente irrecuperável pela tipagem de fragmentos STR, e medir com a régua do adversário exige contar apenas o que ele efetivamente percorre. A lacuna para os 128 bits mínimos é, portanto, ainda maior que a reportada nas versões anteriores (fator ≈ 7×, contra ≈ 6×), **reforçando a tese central**: **a fonte genética, isolada, não basta como segredo criptográfico.**

### 6.5 Probabilidade de colisão (painel completo, Fase 3)

Para N = 10¹⁸ derivações e k = 256 bits de saída: P ≈ N²/2^(k+1) = (10¹⁸)²/2²⁵⁷ ≈ **4,3 × 10⁻⁴²** — desprezível.

### 6.6 Efeito avalanche :  previsão e medição

Um KDF seguro deve inverter, em média, metade dos bits de saída diante de uma mutação mínima na entrada. Esperado: Hamming ≈ 128/256, σ teórico = √(256·0,25) = 8 bits. **Medição (Notebook 03):** 60 mutações de bit único (XOR 0x01 no último byte da representação canônica, mesmo salt) produziram média de **127,1 bits alterados (49,6%)**, σ = 9,5, faixa 101–146  aderente à previsão (faixa de aceitação adotada: 118–138). O σ observado levemente superior ao teórico reflete o tamanho amostral (n = 60).

### 6.7 Modelo híbrido e substituição do fator secreto

**CKU\_híbrida = Argon2id(φ(G) ‖ s ‖ f)**

O fator f é gerado por CSPRNG no cadastramento, protegido como segredo digital convencional e diferentemente do DNA  **plenamente substituível** em caso de comprometimento: deriva-se nova chave com novo fator e recifra-se o domínio de dados. A substituibilidade operacional responde à irrevogabilidade do DNA: o fator genético (17,7 bits no espaço canônico) somado a um fator secreto de \~40 bits situa o arranjo na faixa de \~58 bits , abaixo ainda do patamar de 128 bits no painel didático, mas superado com folga no painel completo da Fase 2 (\~275 bits projetados).

## 7. RESULTADOS EXPERIMENTAIS

Este capítulo reporta os resultados da Fase 1 na ordem lógica do pipeline: a caracterização da fonte genética sob três medidas de entropia (7.1), o comportamento do operador de derivação (7.2), a validação estatística das chaves produzidas (7.3) e o custo comparativo de enumeração (7.4).

### 7.1 Entropia da fonte genética

A Tabela 7.1 apresenta a entropia de Shannon por alelo de cada locus, calculada a partir das frequências paramétricas do painel simulado (`PAINEL_STR`, caderno experimental 01), a entropia máxima teórica sob distribuição uniforme e a eficiência resultante.

**Tabela 7.1 — Entropia de Shannon por alelo, por locus (valores teóricos do painel paramétrico).**

| Locus | Nº de alelos | H por alelo (bits) | H máx (bits) | Eficiência |
| --- | --- | --- | --- | --- |
| D3S1358 | 5 | 2,252 | 2,3219 | 0,970 |
| D21S11 | 5 | 2,283 | 2,3219 | 0,983 |
| TH01 | 5 | 2,234 | 2,3219 | 0,962 |
| D18S51 | 5 | 2,233 | 2,3219 | 0,962 |
| D5S818 | 4 | 1,769 | 2,0000 | 0,884 |
| **Painel (soma haploide)** | — | **10,77** | **11,27** | **0,954** |

Fonte: elaborado pelo autor a partir do caderno experimental 01.

Os valores teóricos foram confirmados empiricamente na população simulada (N = 5.000, seed = 2024): a soma haploide observada foi de 10,75 bits, com desvio individual por locus inferior a 0,01 bit em todos os casos (D5S818: 1,7615 bits observados contra 1,769 teóricos; eficiência empírica de 88,1%). O locus D5S818 permanece o menos eficiente do painel, consequência da dominância dos alelos 11 e 12, que concentram 74% da frequência paramétrica  característica que o torna candidato natural à exclusão em versões otimizadas do painel.

#### 7.1.1 As três medidas da entropia do perfil

Um dos pontos centrais desta revisão é a apresentação explícita de três medidas de entropia do genótipo diplóide, que respondem a perguntas adversariais distintas : identificação, custo médio de enumeração e pior caso de adivinhação.

**(a) Convenção de par ordenado (fase): ≈ 21,5 bits.** Sob Hardy-Weinberg com alelos sorteados independentemente, a entropia do genótipo como *par ordenado de sorteios* aproxima-se do dobro da entropia haploide: 2 × 10,77 ≈ **21,54 bits**. Nesta convenção, os genótipos (16,17) e (17,16) contam como estados distintos. É o valor reportado nas versões anteriores do trabalho e permanece correto *como medida de imprevisibilidade do evento de tipagem* , a fase (origem parental de cada alelo) existe biologicamente, ainda que não seja observável pela tipagem STR.

**(b) Entropia do espaço canônico: ≈ 17,7 bits.** A canonização descrita na Seção 5.3 ordena os alelos de cada locus por valor antes da serialização: (16,17) e (17,16) convergem para *bytes idênticos* e, portanto, para a mesma chave. Um atacante que enumera strings canônicas não precisa testar as duas ordens , a fase é destruída pelo próprio pipeline que ele ataca. A entropia de Shannon do espaço efetivamente enumerável é, assim, a do genótipo não-ordenado: ≈ **17,74 bits** (≈ 2,2 × 10⁵ genótipos canônicos plausíveis). **Este trabalho adota 17,7 bits como o valor de segurança da fonte**, por ser a medida alinhada ao espaço que o adversário efetivamente percorre.

**(c) Min-entropia (pior caso): ≈ 13,6 bits.** A min-entropia H∞ = −log₂(max pᵢ) mede a previsibilidade do evento *mais provável*: o genótipo modal do painel (D3S1358 16/17 · TH01 6/8 · D21S11 29/30 · D18S51 14/15 · D5S818 11/12) ocorre com probabilidade ≈ 8 × 10⁻⁵, correspondendo a H∞ ≈ **13,61 bits**. É o limite correto para bornear o sucesso de um único palpite otimizado e o atacante guloso que enumera por ordem decrescente de frequência.

**Tabela 7.2 — Entropia do perfil por locus sob as três convenções (bits).**

| Locus | Par ordenado (2H) | Genótipo canônico | Min-entropia H∞ |
| --- | --- | --- | --- |
| D3S1358 | 4,504 | 3,721 | 3,128 |
| D21S11 | 4,566 | 3,777 | 2,947 |
| TH01 | 4,468 | 3,692 | 2,81 |
| D18S51 | 4,467 | 3,693 | 2,851 |
| D5S818 | 3,538 | 2,855 | 1,870 |
| **Perfil (soma)** | **21,54** | **17,74** | **13,61** |

Fonte: elaborado pelo autor; valores conferíveis por `src/entropia.py` (funções `entropia_shannon` e `entropia_minima`) sobre a população sintética (seed = 2024).

Três leituras emergem da tabela. Primeira: a diferença entre as duas primeiras colunas (\~3,8 bits) não é erro quantifica exatamente a informação de fase que a canonização elimina e que nenhum atacante precisa buscar. Segunda: a distância entre Shannon canônica (17,7) e min-entropia (13,6) quantifica a vantagem adicional do atacante que abandona a enumeração ingênua em favor da ordenação por frequência  vantagem concentrada sobretudo no D5S818, cujo genótipo 11/12 sozinho alcança 27,4% de probabilidade, rendendo ao locus apenas 1,87 bits no pior caso: um atacante inteligente "quebra" esse locus quase de graça. Terceira: as três medidas são computáveis sobre o *mesmo* conjunto de dados, bastando contar os genótipos sob as três convenções **&#32;o que torna a análise integralmente auditável no repositório público.**

#### 7.1.2 O gap frente aos patamares contemporâneos

Sob o valor de segurança adotado (17,7 bits), o gap estrutural identificado nas versões anteriores aprofunda-se: a fonte situa-se \~110 bits abaixo do padrão mínimo contemporâneo (128 bits) e \~238 bits abaixo dos 256 bits exigidos pela chave-alvo (AES-256). O adversário enfrenta ≈ 2,2 × 10⁵ candidatos plausíveis  espaço que, como quantifica a Seção 7.4, é percorrido em horas mesmo sob a função de derivação memory-hard. Esse aprofundamento não enfraquece o trabalho: ele *reforça* a tese central de que a fonte genética não basta sozinha e de que a arquitetura híbrida (Seção 6.7) é requisito, não opcional. Convém ainda distinguir a entropia do perfil como segredo (\~17,7 bits) da entropia interna média dos símbolos de cada perfil individual (\~2,95 bits por locus), que quantifica diversidade alélica intra-individual e não guarda relação com a resistência criptográfica da fonte.

### 7.2 Derivação, dissimilaridade e determinismo

O pipeline descrito na Seção 5 foi executado sobre os perfis regenerados com a mesma semente (seed = 2024), com cronometragem de 100 derivações em série: tempo médio de **237,5 ms por derivação** (σ = 13,0 ms; intervalo observado: 221,9–270,0 ms), consumo de 64 MiB de memória dedicada por chamada , custo que é o mecanismo central de defesa contra enumeração (Seção 7.4). O tempo médio é plenamente compatível com operações interativas individuais.

Para caracterizar a dissimilaridade produzida pela derivação, mediram-se distâncias de Hamming em nível de bit entre chaves em três cenários (Tabela 7.3).

**Tabela 7.3 — Distância de Hamming entre chaves derivadas, por cenário (256 bits por chave).**

| Cenário | Bits diferentes | % de alteração | Esperado |
| --- | --- | --- | --- |
| Perfis distintos, mesmo salt | 112/256 | 43,8% | \~128 (50%) |
| Mesmo perfil, salts distintos | 134/256 | 52,3% | \~128 (50%) |
| Mesmo perfil, mesmo salt (10 execuções) | 0/256 | 0% | 0 exato |

Fonte: cadernos experimentais 02 e suíte de testes de determinismo (`tests/test_determinismo.py`).

Registre-se com honestidade a posição do primeiro cenário: 112/256 bits toca exatamente a borda inferior da faixa de tolerância adotada (128 ± 16)  aprovado dentro do critério, mas sem margem. As medidas dos dois primeiros cenários são observações pontuais (um par por cenário, para caracterização qualitativa do operador); a avaliação estatística formal, com n = 60 pares, está na Seção 7.3 e constitui a referência de validação do efeito avalanche (49,6%; σ = 9,5). O terceiro cenário confirma a propriedade determinística por suíte automatizada de testes: (i) mesmo perfil e mesmo salt produzem chave idêntica; (ii) estabilidade ao longo de dez execuções consecutivas; (iii) invariância à ordem de inserção de loci e alelos no dicionário de entrada; (iv) validação da canonização (genótipos equivalentes convergem para a mesma representação de bytes). Em conjunto, as medidas caracterizam o operador de forma completa: separa maximamente entradas distintas, preserva exatamente entradas idênticas e impõe custo computacional substancial a cada chamada.

### 7.3 Validação estatística das chaves

Foram geradas 400 chaves independentes (variando-se perfil e salt), compondo 12.800 bytes agregados, submetidos às três baterias especificadas na Seção 5.6, sob α = 0,05 (NIST, 2010).

**Bateria 1 : Uniformidade de distribuição de bytes.** O teste qui-quadrado de aderência sobre os 12.800 bytes agregados (frequência esperada de 50 ocorrências por valor, 255 graus de liberdade) resultou em χ²(255) = 247,88, p = 0,614. A hipótese nula de distribuição uniforme não foi rejeitada: a frequência observada dos 256 valores de byte (faixa de 32 a 71 ocorrências) não desvia da expectativa uniforme de forma estatisticamente detectável. O estatístico ligeiramente inferior aos graus de liberdade (247,88 < 255) denota dispersão marginalmente menor que a esperada , comportamento compatível com flutuação amostral.

**Bateria 2 : Equilíbrio posicional de bits.** A proporção global de bits 1 nos 102.400 bits agregados foi de 0,5017, dentro do intervalo de confiança de 99% sob hipótese binomial (p = 0,5). Na avaliação posicional, com intervalos individuais de 99% para cada uma das 256 posições (0,436–0,564 para n = 400 observações por posição), 2 posições situaram-se fora do intervalo , resultado consistente com a expectativa de \~2,6 posições fora por puro acaso. A bateria foi aprovada, sem indício de viés posicional detectável.

**Bateria 3 : Efeito avalanche.** O protocolo foi o seguinte: para cada par, a representação canônica do perfil foi mutada em exatamente um bit (inversão do bit menos significativo do último byte, via XOR com 0x01), mantendo-se o mesmo salt; a distância de Hamming entre as duas chaves foi medida em nível de bit. Foram n = 60 pares, resultando em média de 127,1 bits alterados de 256 (49,6%), σ = 9,5 bits, faixa observada de 101 a 146. A média situa-se dentro do critério centrado em 50%, e o desvio-padrão observado é compatível com o valor teórico sob difusão ideal (σ ≈ 8 bits para 256 bits de saída), com o excesso proporcional explicável pela amostra finita (n = 60). Declara-se explicitamente que a métrica de avalanche é Hamming **em nível de bit** , a expectativa teórica de 50% vale para bits, não para bytes.

Em síntese, as três baterias foram integralmente aprovadas: as chaves derivadas são estatisticamente indistinguíveis de material aleatório genuíno nas dimensões testadas. Importa sublinhar o alcance exato dessa conclusão: as baterias certificam a qualidade estatística da *saída* do pipeline, e não a entropia da *fonte* genética, que permanece limitada a \~17,7 bits no espaço canônico (Seção 7.1). A qualidade estatística não é transferível como segurança da chave, pois o adversário ataca o espaço de entrada, não a saída ,distinção central para a Discussão.

### 7.4 Custo comparativo de enumeração

Para quantificar a vantagem da arquitetura memory-hard sobre formulações com funções hash de uso geral, executou-se benchmark comparativo no mesmo hardware (Seção 5.7), na mesma sessão e sobre o mesmo material canônico (65 bytes de perfil codificado + salt de 16 bytes), com aquecimento descartado. Os resultados estão persistidos no repositório (`results/benchmark_hashes.json`).

**Tabela 7.4 — Custo por derivação e tempo de enumeração completa, sob os dois espaços de busca.**

| Função | Tempo médio/derivação | Candidatos/s | Espaço 2^21,5 (convenção fase) | Espaço 2^17,7 (canônico) |
| --- | --- | --- | --- | --- |
| SHA-256 | 1,7 µs | \~595.800 | \~5 s | < 1 s |
| SHA3-256 | 1,9 µs | \~531.000 | \~5,6 s | < 1 s |
| BLAKE3 | 2,3 µs | \~429.600 | \~6,9 s | < 1 s |
| Argon2id | 272 ms | \~4 | \~9,4 dias | **\~16 horas** |

Fonte: benchmark em mesma sessão (n = 1.000 para hashes; n = 10 para Argon2id), elaborado pelo autor. Tempos de enumeração do espaço canônico derivados: 2,2 × 10⁵ candidatos × 272 ms ≈ 6,0 × 10⁴ s ≈ 16,6 horas.

**Figura 7.1 — Tempo de enumeração completa do espaço de busca, por função de derivação** *(gráfico em escala logarítmica; no repositório, a versão Vega-Lite gera a figura para o .docx)*.



SHA-256SHA3-256BLAKE3Argon2idFunção de derivaçãoTempo de enumeração (s, escala log)Canônico (2^17,7)Fase (2^21,5)Espaço de buscaTempo de enumeração completa do espaçoArgon2id eleva a busca de segundos para \~9,4 dias (espaço de fase) ou \~16 h (espaço canônico); escala logarítmica.

Quatro leituras emergem. Primeira: sob qualquer função hash de uso geral, *ambos* os espaços , o de fase e o canônico : são enumerados por completo em segundos; a formulação original do modelo ofereceria proteção nula contra busca exaustiva offline. Segunda: a Argon2id eleva a enumeração do espaço canônico (o que o atacante efetivamente percorre) para a ordem de **16 horas** no hardware de referência  e a do espaço de fase para a ordem de nove dias  impondo multiplicador de \~162.000× sobre o tempo por tentativa. Terceira: mesmo sob a KDF memory-hard, o espaço didático permanece enumerável em menos de um dia de computação contínua em hardware modesto constatação que, longe de constranger o trabalho, *fecha o argumento* com autonomia: nenhuma função de derivação substitui a entropia ausente da fonte, e o painel completo da Fase 2 (\~275 bits projetados) somado ao fator secreto do modelo híbrido é o caminho para o patamar de 128 bits. Quarta: o consumo de 64 MiB de memória dedicada por tentativa neutraliza a vantagem de hardware massivamente paralelo, pois a RAM dedicada não escala com a generosidade da computação bruta.

Duas notas metodológicas completam a leitura. O BLAKE3 mediu tempo superior ao SHA-256 (2,3 µs vs. 1,7 µs)  resultado atribuído ao custo de ligação (binding) da biblioteca Python para entradas pequenas, e não ao algoritmo em si, cujo desempenho superior manifesta-se em entradas grandes e paralelismo multicore; no regime de enumeração de candidatos pequenos, todas as funções rápidas operam na mesma ordem de grandeza. Adicionalmente, o tempo médio da Argon2id nesta sessão (272 ms, n = 10) contrasta com o cronometragem do pipeline na Seção 7.2 (237,5 ms, n = 100): variação de \~15% entre sessões em estação multitarefa é esperada e não compromete a ordem de grandeza; para comparação interfunção, vale o par medido em mesma sessão. Todos os tempos foram medidos em hardware deliberadamente modesto (Seção 5.7): os tempos legítimos configuram limite superior e os custos ao atacante, limite inferior  o multiplicador de \~162.000×, porém, é propriedade da arquitetura, não do hardware específico.

O conjunto de resultados deste capítulo : entropia tripla quantificada, operador determinístico e estatisticamente sólido, custo de enumeração elevado por construção , estabelece o quadro que a Discussão interpreta: viabilidade técnica demonstrada, com limitação estrutural na fonte que nenhum refinamento do operador de derivação elimina.

## 8. APLICAÇÕES

O pipeline validado na Fase 1 não é uma curiosidade de laboratório: cada propriedade demonstrada empiricamente , correspondem a requisitos concretos de classes de aplicação reais. Esta seção delineia as cinco classes em que a CKU encontra aplicação direta, indicando, em cada uma, qual resultado experimental a sustenta e qual limitação estrutural a condiciona. *Até onde alcança nossa revisão da literatura, a derivação quantificada de chaves criptográficas a partir de STR forenses com validação estatística completa não havia sido reportada como pipeline reprodutível integral ,o que posiciona as aplicações abaixo como consequências originais do modelo, e não transposição de resultados alheios.*

### 8.1 Saúde digital e prontuário eletrônico

A aplicação mais imediata da CKU situa-se na interoperabilidade de registros de saúde. O prontuário eletrônico do paciente (PEP) exige mecanismos de vinculação entre indivíduo e registro que sejam ao mesmo tempo únicos, persistentes e verificáveis. A CKU derivada do perfil genético oferece um identificador com vantagens estruturais frente às chaves convencionais: não pode ser esquecida (o titular nasce portando o material de derivação), não pode ser transferida (vinculação biológica direta) e não depende de terceiro emissor (ao contrário de CPF, RG ou certificados digitais).

Em arquiteturas típicas, a CKU funcionaria como chave de criptografia simétrica (AES-256) para o envelope criptográfico do prontuário, com o perfil genético atuando como material de derivação verificado no momento do atendimento  por exemplo, na admissão hospitalar, mediante tipagem rápida do painel didático ou completo. Dois resultados experimentais sustentam essa arquitetura: o custo de derivação medido (237,5 ms) é plenamente compatível com o fluxo interativo de admissão hospitalar; e as três baterias estatísticas aprovadas (Seção 7.3) garantem que envelopes distintos, derivados com salts distintos, não exibam correlação explorável. Para aplicações críticas do setor  registros contendo dados sensíveis sob a LGPD , aplica-se o modelo híbrido da Seção 6.7, agregando fator secreto detido pelo titular.

### 8.2 Sistemas de alta segurança e controle de acesso

Ambientes que exigem autenticação de alta confiança : laboratórios forenses, instalações governamentais classificadas, infraestruturas críticas  podem empregar a CKU como fator de autenticação de "algo que o usuário é", com especificidade superior às biometrias convencionais. Enquanto impressões digitais podem ser forjadas com moldes, faces replicadas por deepfakes e íris capturadas por fotografia de alta resolução, o perfil genético requer amostra biológica legítima do titular  elevando o custo do ataque de falsificação a patamares qualitativamente distintos.

O custo computacional de 237,5 ms por verificação (Seção 7.2), embora inviabilize processamento massivo, é plenamente compatível com autenticação interativa de usuário único , o cenário exato do controle de acesso físico ou lógico. O mesmo custo que limita o sistema legítimo é o que penaliza o atacante que tenta enumeração (Seção 7.4): o desenho beneficia deliberadamente o uso legítimo em detrimento do abuso. A limitação estrutural da entropia da fonte (Seção 7.1), aqui como em toda aplicação, condiciona o modelo de ameaça: a proteção valida contra adversários que conhecem o espaço de perfis, não contra adversários que possuem a amostra do titular razão pela qual ambientes de máxima criticidade devem combinar a CKU ao fator secreto adicional (modelo híbrido).

### 8.3 Genética forense e cadeia de custódia

Na própria genética forense, a CKU oferece ferramenta de integridade de cadeia de custódia: vestígios biológicos coletados em local de crime podem ter seus perfis codificados e derivados como chaves de autenticação dos laudos associados, criando vínculo criptográfico entre amostra, perícia e conclusão. Qualquer adulteração do registro intermediário  troca de amostras, edição de laudo  resulta em chave inválida na verificação, tornando a manipulação detectável. O determinismo verificado pela suíte de testes (Seção 7.2) é o requisito que sustenta esse vínculo: a mesma amostra, tipada e canonizada em qualquer laboratório, reproduz a mesma chave.

Aplicação correlata é a área de parentesco e identificação de desaparecidos, na qual bancos de perfis genéticos de vítimas de catástrofes ou de pessoas desaparecidas poderiam empregar chaves derivadas como índices de busca **à prova de vazamento**: um banco comprometido exporia chaves inúteis à reconstrução dos perfis originais (irreversibilidade, Seção 10.2), protegendo os dados sensíveis subjacentes mesmo em cenário de violação do repositório. Essa propriedade é convergente com a LGPD na medida em que reduz o dano potencial de vazamentos de bases que, hoje, expõem perfis completos.

### 8.4 Gestão corporativa e assinatura de documentos

Em contexto corporativo , a CKU presta-se à autenticação de atos de gestão de alta formalidade: assinatura de contratos, aprovação de transações sensíveis, deleção controlada de registros. A diferença conceitual frente à assinatura digital convencional é a natureza do fator: em vez de depender de posse (token) ou conhecimento (senha), ambos delegáveis ou roubáveis, o fator é inseparável do titular , propriedade valiosa em governança, onde a atribuição de responsabilidade individual é imperativa.

A limitação estrutural, contudo, impõe-se com particular relevância neste domínio: contrariamente à prática de assinaturas digitais, atos societários exigem eventualmente revogação de credenciais (exoneração de dirigente, por exemplo). A irreversibilidade do material genético torna imprescindível a arquitetura híbrida :  o fator genético autentica o vínculo identitário; o fator secreto, revogável, autoriza a prática do ato (decomposição analisada na Seção 10.5). Cumpre notar que a entropia combinada desse arranjo  painel didático (17,7 bits no espaço canônico) somada a um fator secreto de \~40 bits , situa-se na faixa de \~58 bits, adequada à proteção de atos que não representem alvo de enumeração dedicada; para atos de maior criticidade, o painel completo da Fase 2 é o caminho indicado.

### 8.5 Conformidade com a LGPD

Todas as aplicações precedentes têm um fundamento regulatório comum. A Lei nº 13.709/2018 (LGPD) classifica dados genéticos como dados pessoais sensíveis (Art. 5º, II), submetendo seu tratamento a bases legais específicas e a princípios como finalidade, necessidade e segurança (BRASIL, 2018). A arquitetura da CKU dialoga com esses princípios em três frentes:

- **Minimização:** a chave derivada não contém o perfil genético — a irreversibilidade da função de derivação significa que o dado sensível permanece apenas no processo de derivação, jamais no artefato armazenado ou transmitido;
- **Finalidade:** o uso do perfil exclusivamente para derivação, com descarte do material após o processo, delimita a finalidade do tratamento de forma estrita  diferentemente de bancos de perfis completos, cuja reutilização para outras finalidades é tecnicamente possível;
- **Segurança:** a adoção da função memory-hard constitui medida técnica proporcional ao risco, na linha do princípio da segurança (Art. 46), elevando o custo de ataques de enumeração em ordens de magnitude.

Cabe registrar, por honestidade regulatória, que a tipagem genética como etapa de autenticação constitui, ela própria, tratamento de dado sensível  de modo que a adoção da CKU não dispensa o consentimento ou base legal adequada para a coleta da amostra no ponto de verificação. A CKU mitiga os riscos de armazenamento, não os da coleta.

## 9. LIMITAÇÕES

As limitações do presente trabalho distribuem-se em dois planos qualitativamente distintos, cuja separação estruturará a Discussão (Capítulo 10) e a Conclusão (Seção 11.2): as **estruturais**, que nenhum experimento adicional remove, e as **empíricas**, que fases subsequentes do programa de pesquisa podem mitigar. Distingui-las com clareza é, em si, parte do rigor que a proposta defende.

### 9.1 Limitações estruturais

**Gêmeos monozigóticos.** Gêmeos idênticos compartilham o mesmo genoma (salvo mosaicismos pós-zigóticos raros) e, portanto, derivam chaves idênticas de qualquer painel germinal. Nenhuma função de derivação distingue material geneticamente idêntico , limitação insolúvel no âmbito da arquitetura proposta, cuja mitigação ultrapassa os objetivos da Fase 1: a CKU Ampliada, baseada em marcadores somáticos e epigenéticos (Fase 3), ou o modelo híbrido com fator secreto adicional (Seção 6.7).

**Irrevogabilidade do material genético.** O titular não pode trocar seu DNA: comprometida a chave, a fonte permanece. A resposta arquitetural é a substituição do fator complementar no modelo híbrido  o fator secreto é substituível, o genético não.

**Obtenção direta de amostra biológica.** Um adversário que adquira amostra biológica do titular (saliva em utensílio, fio de cabelo, células descamadas) tipa o perfil e reproduz a entrada completa da derivação , o ataque contorna a enumeração, que é a única barreira quantificada neste trabalho. A proteção contra esse vetor é operacional (guarda da amostra, cadeia de coleta), não criptográfica , razão pela qual aplicações críticas exigem o fator secreto adicional.

**Entropia limitada da fonte.** A entropia de segurança do painel didático é de **17,7 bits no espaço canônico** (convenção adotada; Seção 7.1.1), com pior caso de **13,6 bits pela min-entropia** — a ordem de 10⁷–10¹⁰ vezes menos candidatos que os patamares contemporâneos de 128–256 bits (Seção 7.1.2). Nem a qualidade estatística da saída nem a dureza da KDF modificam esse teto: o painel completo da Fase 2 (\~275 bits projetados) somado ao fator secreto é o caminho para os padrões mínimos.

### 9.2 Limitações empíricas

**Simulação populacional.** As frequências alélicas do painel são plausíveis, não empíricas , população de referência hipotética, escolha metodológica deliberada da Fase 1 (Seção 5.2). Todas as medidas de entropia herdam essa condição; a substituição por frequências de bases públicas (STRBase, ALFRED, 1000 Genomes) é o primeiro passo da Fase 2.

**Amplitude da validação estatística.** As três baterias aplicadas (uniformidade de bytes, equilíbrio posicional, avalanche) são subconjunto da suíte completa do NIST SP 800-22 (15 subtestes, mínimo de 10⁶ bits por sequência), executadas sobre 400 chaves agregadas (12.800 bytes; 102.400 bits). A aprovação certifica a qualidade estatística da saída nessas dimensões e não a segurança da fonte (distinção central da Seção 10.3).

**Medidas pontuais de dissimilaridade.** Os contrastes de chaves reportados na Tabela 7.3 (perfis distintos sob mesmo salt; mesmo perfil sob salts distintos) são observações pontuais de caracterização ,  a avaliação estatística formal é a bateria avalanche com n = 60 pares (Seção 7.3). Ampliar o n das medidas pontuais é melhoria trivial de custo computacional, agendada para a Fase 2.

**Hardware de referência modesto.** Todos os tempos foram medidos em estação de baixo custo (Seção 5.7), configurando limite superior para o uso legítimo e **limite inferior para o atacante** — um adversário com hardware dedicado enumera mais rápido. O multiplicador de \~162.000× é propriedade da comparação interfunção em mesma sessão, não do hardware específico (Seção 7.4), mas a vantagem absoluta do atacante com recursos abundantes permanece.

**Contingência regulatória da coleta.** A tipagem genética como etapa de autenticação constitui, ela própria, tratamento de dado sensível (LGPD): a CKU mitiga os riscos de armazenamento, não os da coleta (Seção 8.5). A adoção operacional exige base legal e salvaguardas no ponto de verificação , condicionante extratecnológico, não eliminável por desenho de pipeline.

**Registro de limite cumprido.** A limitação "ausência de quantificação da min-entropia", registrada na versão anterior, **foi sanada nesta revisão**: H∞ = 13,61 bits, reportada locus a locus (Seção 7.1.1, Tabela 7.2). Restringe-se agora à condição de frequências simuladas acima — a extensão a frequências empíricas acompanha a Fase 2.

### 9.3 Quadro-resumo: limitação → mitigação → horizonte

| Limitação | Mitigação (arquitetura ou programa) | Horizonte |
| --- | --- | --- |
| Gêmeos monozigóticos | CKU Ampliada (marcadores somáticos/epigenéticos); modelo híbrido | Fase 3 / presente |
| Irrevogabilidade do DNA | Substituição do fator secreto no modelo híbrido (Seção 6.7) | Presente |
| Amostra biológica direta | Salvaguardas operacionais de coleta + fator secreto adicional | Contínua |
| Entropia da fonte (17,7 / 13,6 bits) | Painel completo (\~275 bits) + fator secreto (\~40 bits) | Fase 2 |
| Frequências simuladas | Bases empíricas (STRBase, ALFRED, 1000 Genomes) | Fase 2 |
| Bateria estatística parcial | Suíte completa NIST SP 800-22 (10⁶ bits) | Fase 2 |
| Medidas pontuais de dissimilaridade | Ampliação do n (bateria avalanche formal) | Fase 2 |
| Hardware modesto | Benchmarks multiplataforma e adversariais | Fase 2 |
| Coleta = tratamento de dado sensível | Base legal e salvaguardas no ponto de coleta | Contínua |

O quadro delimita o território honesto do trabalho: o que foi demonstrado, o que foi projetado e o que permanece aberto  e atribui a cada abertura um endereço: uma seção da arquitetura presente ou uma fase do programa de pesquisa.

## 10. DISCUSSÃO

Os resultados experimentais da Fase 1, lidos em conjunto, compõem um quadro que exige interpretação em duas camadas: o que a arquitetura demonstrou e o que a fonte impõe. Esta seção articula as duas camadas, posiciona o trabalho frente à literatura de biometria criptográfica e explicita os limites do que a validação estatística pode afirmar.

### 10.1 O gap de entropia como achado central

O resultado mais importante deste trabalho é também o mais desconfortável: a entropia de segurança da fonte genética disponível no painel didático , **17,7 bits no espaço canônico** (valor adotado neste trabalho, Seção 7.1.1), com pior caso de **13,6 bits pela min-entropia** , corresponde a cerca de um sétimo do patamar mínimo contemporâneo (128 bits) e a menos de um décimo dos 256 bits exigidos pela chave-alvo (AES-256). Traduzida ao espaço de busca, a diferença é dramática: um adversário enfrenta 2^110 vezes menos candidatos que os pressupostos pelo padrão mínimo e 2^238 vezes menos que os do AES-256.

Essa lacuna não é defeito metodológico, mas característica intrínseca da fonte: a imprevisibilidade de um genótipo é limitada pelas frequências alélicas populacionais, que são públicas e amplamente documentadas. Um perfil STR identifica um indivíduo com especificidade extraordinária , bilhões para um , mas **identificar não é o mesmo que ser imprevisível**: a especificidade advém da baixa probabilidade de coincidência entre dois perfis sorteados, enquanto a imprevisibilidade criptográfica exige alta entropia do segredo face ao adversário. O adversário forense conhece as distribuições, sabe enumerar genótipos por ordem decrescente de probabilidade , comportamento para o qual a min-entropia (13,6 bits) é o limite correto, e não a média de Shannon e dispõe, em cenários plausíveis, de informação genética parcial do alvo (parentes próximos, bancos forense-institucionais).

A revisão metodológica desta versão aprofundou o diagnóstico: a convenção anterior (21,5 bits, par ordenado) **superestimava** o espaço que o atacante percorre, pois contava a fase parental dos heterozigotos , informação que a tipagem STR não recupera e que a canonização, por construção, destrói. A correção não enfraquece o trabalho: amplia o gap em \~3,8 bits e **reforça a tese central**, distinguindo, também na medida, o que a fonte pode prometer.

### 10.2 O que a função de derivação compra  e o que não compra

O benchmark comparativo (Seção 7.4) permite quantificar com franqueza o papel da Argon2id na arquitetura. Sob funções hash de uso geral, o espaço canônico de \~2^17,7 genótipos é enumerado por completo **em menos de um segundo** , proteção nula contra busca exaustiva offline. Sob a Argon2id, a mesma enumeração custa a ordem de **16 horas** no hardware de referência (9,4 dias para o espaço de fase), com multiplicador de \~162.000× no tempo por tentativa e consumo de 64 MiB de memória dedicada por candidatura última característica decisiva, pois neutraliza a vantagem de hardware massivamente paralelo: a RAM dedicada não escala com a generosidade da computação bruta.

A função de derivação, portanto, **compra custo: transforma uma fonte de baixa entropia em um espaço de busca computacionalmente caro**. O que ela não compra é entropia. Nenhuma KDF aumenta a imprevisibilidade da entrada  e a distinção, embora elementar para a criptografia, merece ênfase neste contexto biométrico: formulações que sugerem que "passar o DNA por uma função forte" basta para produzir segurança de 256 bits são empiricamente refutadas pelos próprios resultados deste trabalho  chaves estatisticamente perfeitas (Seção 7.3) a partir de fonte com 17,7 bits. Ao mesmo tempo, a mesma propriedade estabelece a irreversibilidade prática da derivação: a saída de 256 bits não contém informação utilizável para reconstruir a entrada  o que fundamenta o armazenamento à prova de vazamento da Seção 8.3. Essa leitura alimenta a recomendação central: o componente criptográfico (Argon2id) e o componente de entropia (fonte genética + fator adicional) são eixos independentes, e a segurança do sistema é limitada pelo mais fraco em cada eixo.

### 10.3 Aprovação estatística não é segurança criptográfica

Merece destaque próprio o alcance exato das três baterias aprovadas e ponto nuclear da revisão. As baterias atestam que a *saída* do pipeline é estatisticamente indistinguível de material aleatório nas dimensões testadas: uniformidade de bytes, equilíbrio de bits, avalanche. São, porém, **testes de qualidade da saída**, e a segurança de uma chave depende do **sigilo da entrada** propriedades ortogonais. Uma fonte determinística de um único valor, submetida ao mesmo pipeline, produziria saída igualmente "perfeita" nos testes e segurança nula; no limite do absurdo, a constante sha256("0") aprovaria qualquer bateria de uniformidade. A aprovação, portanto, certifica a *correta implementação* do operador de derivação  difusão, ausência de viés, determinismo , não a *força do segredo* que o alimenta. Confundir os dois planos é o erro de raciocínio que este trabalho documenta e refuta com seus próprios números: o adversário ataca o espaço de entrada, não a saída.

### 10.4 Ataques de vizinhança genética

Cenário adversarial específico da fonte genética merece análise própria: parentes de primeiro grau compartilham, em média, metade de seus alelos. Um irmão do titular conhece, por consequência, metade do material de derivação e poderia tentar enumeração apenas sobre a metade desconhecida, reduzindo substancialmente o espaço de busca. Os resultados da Bateria 3 (Seção 7.3) fornecem a resposta a essa ameaça: a distância de Hamming média de 49,6% (σ = 9,5, n = 60) entre chaves derivadas de entradas que diferem em um único bit demonstra que meia entrada compartilhada não implica correlação aproveitável na saída , chaves de parentes próximos são tão dissimilares quanto chaves de indivíduos arbitrários. O efeito avalanche quebra estruturalmente a vizinhança genética: o atacante-parente não pode fatorar a busca em torno do que conhece, pois a função de derivação não preserva proximidade de entrada em proximidade de saída.

Essa propriedade precisa, contudo, ser lida com precisão: ela impede o ataque inteligente por vizinhança localizado , mas **não reduz o espaço de busca total**. O irmão atacante ainda pode enumerar os \~2^17,7 genótipos plausíveis do espaço canônico, incluindo os seus próprios e combinações de alelos familiares, pagando o custo integral da busca exaustiva. Em outras palavras, o avalanche converte um ataque inteligente em um ataque "burro" , mas o ataque burro permanece viável pela limitação de entropia da fonte, o que reforça a recomendação de arquitetura híbrida.

### 10.5 O modelo híbrido como síntese

Os resultados convergem para a arquitetura em camadas formalizada na Seção 6.7: o perfil genético e um fator secreto adicional, sob independência estatística, somam entropias o painel didático (17,7 bits canônicos) com uma frase-senha de \~40 bits alcança a faixa de **\~58 bits**; o painel completo da Fase 2 (\~275 bits) supera com folga o patamar de 128 bits mesmo com fator modesto. A síntese das seções anteriores atribui a cada componente seu papel exato:

- o **fator genético** aporta o que a senha não tem: vinculação inseparável ao titular, resistência a phishing, impossibilidade de esquecimento;
- o **fator secreto** aporta o que o DNA não tem: entropia complementar e revogabilidade  inclusive a substituição operacional em caso de comprometimento (Seção 6.7);
- a **Argon2id** aporta o que nenhum dos dois tem: custo proibitivo à enumeração de qualquer combinação parcial de conhecimento.

Três eixos, três propriedades distintas  e a segurança do conjunto é produto da composição, não de qualquer elemento isolado. O modelo híbrido não é concessão de fraqueza, mas desenho de engenharia consciente.

### 10.6 Posicionamento frente à biometria criptográfica clássica

O pipeline proposto difere das abordagens clássicas em um aspecto estrutural: ele não enfrenta, na etapa de derivação, o problema da variação intraclasse. O Fuzzy Vault (JUELS; SUDAN, 2006) e os fuzzy extractors (DODIS et al., 2008) foram concebidos para biometrias ruidosas  impressões digitais, íris , cujas leituras sucessivas podem diferir e exigem correção de erro capaz de recuperar a mesma chave a partir de amostras imperfeitas. O dado STR, após tipagem laboratorial e canonização, é uma **representação discreta e estável do genótipo** , não uma medida fenotípica continuamente variável. Essa estabilidade permite dispensar a maquinaria de tolerância a ruído e, com ela, vetores de ataque associados: a análise dos pontos chaff de um vault ou a exploração de informações auxiliares públicas em fuzzy extractors, que podem revelar parcialmente o segredo biométrico. Frente a tais técnicas, o presente trabalho desfruta de simplicidade conceitual relativa  e essa dispensa não é acidente, mas consequência direta da escolha de marcadores discretos justificada na Seção 4.1.

Frente ao BioHashing (TEOH et al., 2004), a distinção é de papel, não de mecanismo: o BioHashing projeta a biometria em um domínio pseudoaleatório parametrizado por token secreto, perseguindo revogabilidade; este trabalho adota caminho conceitualmente mais simples , a separação entre fonte de identidade (perfil genético) e fator secreto (modelo híbrido) , alcançando análogo pragmático de revogabilidade sem domínio projetado, ao custo reconhecido de exigir do titular a guarda de um fator adicional.

Registra-se, por fim, o trabalho identificado como o mais próximo do presente na literatura recente: Al-Qudsy (2025) propõe extrair STRs e SNPs de perfis de DNA, codificá-los em binário, protegê-los com AES-256 e ocultá-los por esteganografia em imagens médicas (transformada DCT), para autenticação biométrica em prontuários eletrônicos. A despeito da proximidade aparente do material genético, a diferença estrutural é categórica: naquele trabalho, o perfil genético é o **dado protegido** ,o objeto da cifra, com chave convencional , ao passo que, no presente trabalho, o perfil genético é a **fonte de derivação da chave**. As duas abordagens são, de fato, complementares: uma protege o perfil; a outra o emprega como segredo. Notavelmente, aquela proposta não quantifica a entropia da fonte genética, não modela o adversário que conhece as frequências públicas de alelos, não emprega KDF memory-hard e não delimita o modelo de ameaça , precisamente as dimensões que este trabalho estabelece como condição de rigor para qualquer sistema que pretenda derivar chaves de material biológico, e cuja ausência ilustra, na prática, a confusão entre proteger o dado genético e derivar segurança dele.

Nenhuma dessas famílias de técnicas, note-se, resolve o problema central quantificado neste trabalho: a entropia limitada da fonte de identidade genética. Elas o administram de maneiras distintas, cada qual com seus custos; o presente estudo contribui precisamente ao quantificar, com validação experimental, as implicações de cada escolha arquitetural.

### 10.7 Síntese da discussão

O conjunto interpreta-se assim: a Fase 1 demonstrou que o pipeline é tecnicamente viável — determinístico, estatisticamente sólido, computacionalmente adequado (237,5 ± 13,0 ms por derivação) e com custo de enumeração elevado por construção (\~16 horas no espaço canônico, contra menos de um segundo sob hash de uso geral). Demonstrou igualmente que a viabilidade técnica não se traduz automaticamente em segurança: a fonte genética impõe tetos ,17,7 bits de segurança média, 13,6 no pior caso , que nenhum refinamento do operador remove. A resposta arquitetural a essa tensão , o modelo híbrido ,não é concessão de fraqueza, mas desenho consciente: cada componente contribui com a propriedade que os demais não podem fornecer. Nesse sentido, o trabalho cumpre os objetivos de desenvolver o modelo, validá-lo experimentalmente e, com igual rigor, delimitar honestamente o que ele pode prometer.

## 11. CONCLUSÃO

Este trabalho investigou a viabilidade de gerar uma Chave Criptográfica Única (CKU) derivada de marcadores genéticos individuais, mediante um pipeline determinístico e integralmente reprodutível que une genética forense e criptografia aplicada, sob a formalização CKU = Argon2id(S‖s). A resposta obtida tem duas faces, ambas sustentadas por evidência experimental e é na natureza exata de cada face que reside a contribuição do trabalho.

Como extensões futuras, apontam-se quatro direções, em continuidade direta com o programa de pesquisa delineado na Fase 2. **Primeira**, a expansão do painel para o conjunto completo de marcadores (20 STRs + 130 SNPs + 15 INDELs) com frequências alélicas **empíricas** extraídas de bases públicas de população (STRBase, ALFRED, 1000 Genomes), elevando a entropia da fonte para a casa dos 275 bits e liberando o trabalho da premissa simulada da Fase 1. **Segunda**, a execução da bateria completa do NIST SP 800-22 sobre o volume amostral exigido (10⁶ bits), transformando a caracterização atual em certificação de amplo espectro. **Terceira**, a investigação da CKU Ampliada com marcadores somáticos e epigenéticos (padrões de metilação, rearranjos de receptores imunológicos, mosaicismos pós-zigóticos), direcionada à discriminação de gêmeos monozigóticos , a fronteira residual da unicidade genética como pressuposto criptográfico. **Quarta**, a avaliação da viabilidade operacional da tipagem como fator de autenticação no ponto de uso, articulando as dimensões tecnológica e regulatória (LGPD) que a Fase 1 manteve fora do escopo experimental.

O trabalho contribui, assim, metodologicamente para a interseção entre a biomedicina forense e a criptografia aplicada, estabelecendo tanto o que a abordagem oferece  um pipeline reprodutível, determinístico e estatisticamente validado, executável em hardware acessível quanto, com igual rigor, aquilo que ela não pode prometer. Nesse equilíbrio entre demonstração e delimitação reside, entende-se, a condição de maturidade científica da proposta: **não afirmar mais do que os dados sustentam, nem menos do que os dados comprovam.**

## REFERÊNCIAS

AL-QUDSY, Zainab N. Securing DNA profiles using AES cryptography: new approach to encrypted biometric authentication in EHR systems. Iraqi Journal for Computers and Informatics, v. 51, n. 2, p. 70-85, 2025. DOI: [https://doi.org/10.25195/ijci.v51i2.598](https://doi.org/10.25195/ijci.v51i2.598).

BIRYUKOV, Alex; DINU, Daniel; KHOVRATOVICH, Dmitry. Argon2: new generation of memory-hard functions for password hashing and other applications. In: IEEE EUROPEAN SYMPOSIUM ON SECURITY AND PRIVACY (EuroS&P), 2016, Saarbrücken. *Proceedings…* Piscataway: IEEE, 2016. DOI: [https://doi.org/10.1109/EuroSP.2016.31](https://doi.org/10.1109/EuroSP.2016.31).

BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). Diário Oficial da União: seção 1, Brasília, DF, 15 ago. 2018.

BUTLER, John M. Advanced topics in forensic DNA typing: methodology. San Diego: Elsevier Academic Press, 2011.

BUTLER, John M. Advanced topics in forensic DNA typing: interpretation. San Diego: Academic Press, 2015.

DODIS, Yevgeniy; OSTROVSKY, Rafail; REYZIN, Leonid; SMITH, Adam. Fuzzy extractors: how to generate strong keys from biometrics and other noisy data. SIAM Journal on Computing, v. 38, n. 1, p. 97-139, 2008. DOI: [https://doi.org/10.1137/060651380](https://doi.org/10.1137/060651380).

INTERNET ENGINEERING TASK FORCE. Argon2 memory-hard function for password hashing and proof-of-work applications: RFC 9106. [S. l.]: IETF, 2021. DOI: [https://doi.org/10.17487/RFC9106](https://doi.org/10.17487/RFC9106).

JAIN, Anil K.; FLYNN, Patrick; ROSS, Arun A. (org.). Handbook of biometrics. New York: Springer, 2007.

JEFFREYS, Alec J.; WILSON, Victoria; THEIN, Swee Lay. Individual-specific "fingerprints" of human DNA. Nature, v. 316, p. 76-79, 1985.

JUELS, Ari; SUDAN, Madhu. A fuzzy vault scheme. Designs, Codes and Cryptography, v. 38, n. 2, p. 237-257, 2006. DOI: [https://doi.org/10.1007/s10623-005-6343-z](https://doi.org/10.1007/s10623-005-6343-z).

KWON, Young L. et al. Massively parallel sequencing of 25 autosomal STRs including SE33 in four population groups for forensic applications. Scientific Reports, v. 11, art. 4701, 2021. DOI: [https://doi.org/10.1038/s41598-021-82814-z](https://doi.org/10.1038/s41598-021-82814-z).

NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY. SP 800-22 Rev. 1a: a statistical test suite for random and pseudorandom number generators for cryptographic applications. Gaithersburg: NIST, 2010.

NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY. FIPS 180-4: Secure Hash Standard (SHS). Gaithersburg: NIST, 2015a.

NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY. FIPS 202: SHA-3 standard: permutation-based hash and extendable-output functions. Gaithersburg: NIST, 2015b.

NATIONAL LIBRARY OF MEDICINE. Visible proofs: forensic views of the body: the Jeffreys case. Bethesda: National Library of Medicine, 2006. Disponível em: [https://www.nlm.nih.gov/exhibition/visibleproofs/galleries/cases/jeffreys.html](https://www.nlm.nih.gov/exhibition/visibleproofs/galleries/cases/jeffreys.html). Acesso em: 23 out. 2026.

O'CONNOR, Jack; AUMASSON, Jean-Philippe; NEVES, Samuel; WILCOX-O'HEARN, Zooko. BLAKE3: one function, fast everywhere. 2020. Disponível em: [https://github.com/BLAKE3-team/BLAKE3-specs/blob/master/blake3.pdf](https://github.com/BLAKE3-team/BLAKE3-specs/blob/master/blake3.pdf). Acesso em: 23 out. 2026.

PROMEGA CORPORATION. PowerPlex® Fusion 6C System: technical manual. Madison: Promega, 2023.

RÉNYI, Alfréd. On measures of entropy and information. In: BERKELEY SYMPOSIUM ON MATHEMATICAL STATISTICS AND PROBABILITY, 4., 1960, Berkeley. *Proceedings…* Berkeley: University of California Press, 1961. p. 547-561.

STALLINGS, William. Cryptography and network security: principles and practice. 8. ed. Harlow: Pearson, 2021.

TEOH, Andrew B. J.; NGO, David C. L.; GOH, Alwyn. Biohashing: two factor authentication featuring fingerprint data and tokenised random number. Pattern Recognition, v. 37, n. 11, p. 2245-2255, 2004. DOI: [https://doi.org/10.1016/j.patcog.2004.04.011](https://doi.org/10.1016/j.patcog.2004.04.011).