RESUMO

A identificação humana constitui um dos pilares fundamentais da biomedicina forense, da segurança digital e das ciências da informação. Métodos biométricos convencionais — como impressões digitais, reconhecimento facial e padrões de íris — apresentam vulnerabilidades importantes: podem ser falsificados, reproduzidos artificialmente ou capturados sem consentimento. Diante desse cenário, este trabalho desenvolve um modelo computacional para gerar uma Chave Criptográfica Única (CKU) derivada de marcadores genéticos individuais, combinando a singularidade biológica do DNA com a irreversibilidade matemática de funções de derivação criptográfica memory-hard. O pipeline implementado emprega marcadores forenses consolidados (STRs, SNPs, INDELs) codificados em representação binária de comprimento fixo e processados por Argon2id com sal de contexto, substituindo formulações anteriores que empregavam funções hash de uso geral (SHA-256, SHA-3, BLAKE3). A análise quantitativa demonstra que um painel misto de 165 loci (20 STRs + 130 SNPs + 15 INDELs) projeta-se na faixa de 276 bits de entropia efetiva, enquanto a validação experimental com painel didático de 5 loci confirmou a viabilidade técnica: as três baterias estatísticas foram integralmente aprovadas (χ²(255) = 247,88; p = 0,614; proporção global de bits = 0,5017 com 2/256 posições fora do intervalo de 99%; efeito avalanche = 49,6%; σ = 9,5; n = 60). O custo médio de derivação foi de 247 ms em hardware modesto. Contudo, a entropia da fonte genética (~21,5 bits no painel de 5 loci) não alcança os patamares contemporâneos de segurança (128–256 bits); a qualidade estatística da saída não substitui o sigilo da entrada, pois o adversário pode obter amostra biológica diretamente. Recomenda-se, portanto, para aplicações críticas, o modelo híbrido que combina o perfil genético a um fator secreto adicional. O trabalho contribui metodologicamente para a intersecção entre genética forense e criptografia aplicada, estabelecendo tanto a viabilidade do pipeline quanto as limitações que impõem sua adoção responsável, em conformidade com a Lei Geral de Proteção de Dados (LGPD).

Palavras-chave: Chave Criptográfica Única; Genética Forense; Criptografia; Argon2id; LGPD; Autenticação Biométrica; Validação Estatística.
ABSTRACT

Human identification constitutes one of the fundamental pillars of forensic biomedicine, digital security, and information sciences. Conventional biometric methods — such as fingerprints, facial recognition, and iris patterns — present important vulnerabilities: they can be forged, artificially reproduced, or captured without consent. This work develops a computational model to generate a Unique Cryptographic Key (CKU) derived from individual genetic markers, combining the biological uniqueness of DNA with the mathematical irreversibility of memory-hard key derivation functions. The implemented pipeline employs consolidated forensic markers (STRs, SNPs, INDELs) encoded as fixed-length binary representation and processed by Argon2id with contextual salt, replacing earlier formulations that employed general-purpose hash functions (SHA-256, SHA-3, BLAKE3). Quantitative analysis demonstrates that a mixed panel of 165 loci (20 STRs + 130 SNPs + 15 INDELs) projects effective entropy in the range of 276 bits, while experimental validation with a didactic panel of 5 loci confirmed technical feasibility: three statistical batteries were fully approved (χ²(255) = 247,88; p = 0,614; global bit proportion = 0,5017 with 2/256 positions outside 99% CI; avalanche effect = 49,6%; σ = 9,5; n = 60). Mean derivation cost was 247 ms on modest hardware. However, the genetic source entropy (~21,5 bits in the 5-locus panel) does not reach contemporary security thresholds (128–256 bits); statistical quality of output does not replace secrecy of input, as an adversary may obtain biological sample directly. Therefore, for critical applications, a hybrid model combining the genetic profile with an additional secret factor is recommended. The work contributes methodologically to the intersection between forensic genetics and applied cryptography, establishing both the pipeline feasibility and the limitations that demand responsible adoption, in compliance with the Brazilian General Data Protection Law (LGPD).

Keywords: Unique Cryptographic Key; Forensic Genetics; Cryptography; Argon2id; LGPD; Biometric Authentication; Statistical Validation.

1. INTRODUÇÃO

A identificação humana é um dos pilares fundamentais da biomedicina forense, da segurança digital e das ciências da informação. Ao longo das últimas décadas, métodos biométricos como impressões digitais, reconhecimento facial e padrões de íris tornaram-se amplamente utilizados em sistemas de autenticação (JAIN; FLYNN; ROSS, 2011). Entretanto, tais métodos apresentam vulnerabilidades importantes: podem ser falsificados, reproduzidos artificialmente ou capturados sem consentimento. Nesse contexto, o DNA surge como o identificador biológico mais robusto, estável e individualizado disponível na atualidade (BUTLER, 2015).

A genética forense utiliza regiões altamente polimórficas do genoma humano — como Short Tandem Repeats (STRs), Single Nucleotide Polymorphisms (SNPs) e INDELs — para estabelecer perfis individuais com elevado poder discriminatório (BUTLER, 2015; HILLIS et al., 2021). Esses marcadores apresentam variações suficientes entre indivíduos para torná-los candidatos naturais à geração de identificadores digitais derivados de material genético.

Paralelamente, a criptografia moderna busca soluções cada vez mais seguras para autenticação, proteção de dados e prevenção de ataques cibernéticos. A literatura especializada distingue, nesse terreno, dois tipos de primitivas com papéis distintos: as funções hash de uso geral (SHA-256, SHA-3, BLAKE3), projetadas para velocidade (NIST, 2015a; 2015b; O'CONNOR et al., 2020), e as funções de derivação de chaves memory-hard, como a Argon2id (BIRYUKOV; DINU; KHOVRATOVICH, 2017), vencedora da Password Hashing Competition de 2015 e projetada precisamente para o cenário em que a entrada tem baixa entropia — o caso, como se verá, dos perfis genéticos. Essa distinção é central para o desenho do presente trabalho.

Diante desse cenário, propõe-se a criação de uma Chave Criptográfica Única (CKU) derivada diretamente de marcadores genéticos individuais, sob a formalização CKU = Argon2id(S‖s), onde S é a codificação binária canônica do perfil genético e s é um salt de contexto. Essa abordagem combina a singularidade biológica do DNA com o custo computacional imposto pela função de derivação, resultando em um identificador digital de altíssima dificuldade de enumeração. Formulações anteriores deste modelo, baseadas em funções hash de uso geral, foram reformuladas neste trabalho em razão da vulnerabilidade dessas funções a ataques de enumeração em hardware massivamente paralelo, conforme analisado no referencial teórico (Capítulo 4).

Além de seu potencial tecnológico, a proposta exige análise rigorosa de aspectos éticos, legais e de privacidade, especialmente no contexto da Lei Geral de Proteção de Dados (LGPD), que classifica informações genéticas como dados sensíveis (BRASIL, 2018). Portanto, o desenvolvimento de uma chave criptográfica baseada em DNA deve garantir que o processo seja não reversível, evitando qualquer possibilidade de reconstrução do perfil genético original — requisito que, como este trabalho demonstra empiricamente, é atendido, mas que não esgota a análise de segurança: a possibilidade de obtenção direta de amostra biológica por um adversário constitui limitação estrutural que motiva a recomendação de um modelo híbrido para aplicações críticas.

Este trabalho organiza-se da seguinte forma: o Capítulo 2 apresenta a justificativa e relevância; o Capítulo 3 os objetivos; o Capítulo 4 o referencial teórico; o Capítulo 5 a metodologia; o Capítulo 6 o modelo matemático consolidado; o Capítulo 7 os resultados experimentais; o Capítulo 8 as aplicações; o Capítulo 10 as limitações; o Capítulo 11 a discussão; e o Capítulo 12 as conclusões e extensões futuras.


2. JUSTIFICATIVA E RELEVÂNCIA

A crescente digitalização de processos biomédicos, administrativos e jurídicos exige sistemas de autenticação cada vez mais robustos, capazes de proteger informações sensíveis contra ataques cibernéticos, falsificações e acessos não autorizados. Métodos tradicionais de identificação — como senhas, tokens, impressões digitais e reconhecimento facial — apresentam vulnerabilidades significativas: senhas podem ser descobertas, padrões biométricos podem ser replicados artificialmente e dados pessoais podem ser capturados sem consentimento.

A genética forense oferece um conjunto de marcadores altamente polimórficos, com variação suficiente para distinguir indivíduos com elevado grau de precisão (HILLIS et al., 2021; PROMEGA, 2023). Entretanto, seu potencial como fonte de material para sistemas criptográficos permanece pouco explorado na literatura, especialmente no que concerne a uma questão que este trabalho coloca em primeiro plano: o poder discriminatório de um painel genético — sua capacidade de distinguir indivíduos em uma população — não equivale ao sigilo criptográfico da fonte. Um painel com centenas de loci distingue bilhões de indivíduos entre si, mas isso não impede que um adversário que obtenha amostra biológica do titular reconstrua a entrada e, com ela, a chave. Essa distinção, freqüentemente obscurecida em abordagens leigas ao tema, estrutura a análise de segurança desenvolvida neste trabalho e orienta suas recomendações.

A proposta de gerar uma CKU derivada de marcadores genéticos une duas áreas críticas: a biomedicina, que fornece o identificador biológico mais confiável disponível, e a análise de sistemas, que oferece as ferramentas matemáticas e computacionais para transformá-lo em uma chave digital segura. As vantagens centrais da abordagem são a unicidade prática (probabilidade de colisão desprezível entre indivíduos distintos), a irreversibilidade (impossibilidade de reconstrução do perfil genético a partir da chave), a estabilidade temporal dos marcadores e a amplitude de aplicações (segurança digital, prontuários médicos, sistemas forenses e ambientes de alta segurança).

O tema é ainda relevante no contexto da LGPD, que classifica informações genéticas como dados sensíveis (BRASIL, 2018). A necessidade de métodos seguros, éticos e não reversíveis para manipulação de dados biomédicos torna esta pesquisa não apenas inovadora, mas socialmente necessária. Ademais, o trabalho se situa deliberadamente na interseção de três formações — Biomedicina, Análise e Desenvolvimento de Sistemas e Administração —, articulando o conteúdo biológico dos marcadores, a engenharia computacional do pipeline e as implicações de adoção em larga escala.

3. OBJETIVOS
3.1 Objetivo geral

Desenvolver um modelo computacional capaz de gerar uma Chave Criptográfica Única (CKU) derivada de marcadores genéticos individuais, utilizando princípios da genética forense e funções de derivação criptográfica memory-hard (Argon2id), garantindo unicidade prática, irreversibilidade e segurança dos dados genéticos, em conformidade com a Lei Geral de Proteção de Dados (LGPD).
3.2 Objetivos específicos

    Identificar marcadores genéticos forenses com alto poder discriminatório (STRs, SNPs, INDELs) adequados para uso como fonte de entropia criptográfica;

    Quantificar a entropia de Shannon do painel de marcadores, distinguidindo entropia máxima teórica (sob distribuição uniforme) da entropia efetiva populacional (sob frequências alélicas reais);

    Definir uma codificação binária canônica de comprimento fixo para o perfil genético, independente de estatísticas populacionais;

    Formalizar o modelo CKU = Argon2id(S ‖ s) e comparar sua segurança e desempenho frente a formulações alternativas que empregam funções hash de uso geral (SHA-256, SHA-3, BLAKE3), avaliando resistência a ataques de enumeração, efeito avalanche e irreversibilidade;

    Desenvolver um pipeline computacional que integre carregamento, codificação, derivação e geração da CKU, com implementação de referência em Python;

    Validar a robustez da chave por testes de unicidade (colisões em N indivíduos), efeito avalanche (média de bits alterados entre chaves distintas), estabilidade (reprodutibilidade em execuções repetidas) e isolamento de salt;

    Analisar implicações éticas e legais (LGPD) do uso de dados genéticos sensíveis, incluindo irreversibilidade, finalidade específica e consentimento explícito;

    Propor aplicações práticas da CKU e estratégias de mitigação arquitetural para suas limitações estruturais, incluindo o modelo híbrido (perfil genético + fator secreto adicional) para aplicações críticas;

    Estabelecer extensões futuras para o projeto, incluindo a expansão para painéis forenses completos (20–24 loci STRs + 130+ SNPs + 15+ INDELs), a validação empírica com dados do 1000 Genomes Project e a investigação da CKU Ampliada para discriminação de gêmeos monozigóticos (marcadores somáticos/epigenéticos).

4. REFERENCIAL TEÓRICO
4.1 Genética Forense

A identificação humana por meio de material genético constitui um dos pilares da biomedicina forense contemporânea. Desde o primeiro caso de uso forense do DNA, em 1986, quando Jeffreys identificou o assassino Colin Pitchfork com base no perfil genético (JEFFREYS et al., 1985), a técnica evoluiu para um sistema padronizado e globalmente normatizado. Os marcadores mais utilizados atualmente são os Short Tandem Repeats (STRs), regiões do genoma humano compostas por repetições de sequências curtas de nucleotídeos (tipicamente 2–6 bases), cuja variação numérica entre indivíduos confere elevado poder discriminatório (BUTLER, 2015).

Além dos STRs, ganharam espaço na genética forense moderna os Single Nucleotide Polymorphisms (SNPs) — variações de um único nucleotídeo em posições específicas do genoma — e os INDELs (Insertions/Deletions) — pequenas inserções ou deleções de bases. Enquanto os STRs são tipicamente codominantes, oferecendo três genótipos possíveis por locus (homozigoto A/A, heterozigoto A/B, homozigoto B/B), SNPs e INDELs são frequentemente bialélicos, apresentando dois ou três estados dependendo do modelo de codificação (HILLIS et al., 2021; PROMEGA, 2023).

O poder discriminatório de um painel genético é quantificado pela probabilidade de coincidência, isto é, a chance de dois indivíduos distintos possuírem exatamente o mesmo perfil genético. Painéis comerciais como o GlobalFiler e PowerPlex Fusion analisam 20–24 loci STRs, resultando em probabilidades de coincidência na ordem de um em vários bilhões, o que os torna adequados para identificação criminal e testes de paternidade.

Entretanto, há uma distinção crítica que este trabalho enfatiza desde o referencial teórico: o poder discriminatório populacional de um painel genético não equivale ao sigilo criptográfico da mesma informação. Um painel com alto poder discriminativo identifica um indivíduo entre milhões de outros, mas não impede que um adversário que obtenha amostra biológica direta (saliva em copo, fio de cabelo, pele descamada) reconstrua o perfil e derive a chave associada. Essa assimetria entre identificação e imprevisibilidade constitui a tensão central que estrutura o problema de segurança deste trabalho.
4.2 Fundamentos de Funções Hash Criptográficas

Funções hash criptográficas são primitivas matemáticas que mapeiam mensagens de tamanho arbitrário para saídas de tamanho fixo, com propriedades fundamentais para a segurança digital: preimage resistance (dado um hash, é computacionalmente inviável encontrar a mensagem original), second preimage resistance (dada uma mensagem, é inviável encontrar outra que produza o mesmo hash) e colision resistance (é inviável encontrar duas mensagens quaisquer que produzam o mesmo hash) (STALLINGS, 2021).

As funções hash de uso geral mais difundidas incluem:

    SHA-256 (Secure Hash Algorithm 2, 256 bits), parte da família SHA-2 desenvolvida pela NSA e padronizada pelo NIST em 2015 (NIST, 2015a);
    SHA-3, primeira alternativa competitiva ao SHA-2, baseada na construção Keccak, também padronizada pelo NIST em 2015 (NIST, 2015b);
    BLAKE3, função moderna de altíssimo desempenho, otimizada para paralelismo em múltiplos núcleos (O'CONNOR et al., 2020).

Essas primitivas são projetadas para velocidade: em hardware convencional, podem processar gigabytes por segundo, com tempo de hash na ordem de microssegundos por bloco de 64 bytes. Para autenticação e integridade de dados, essa característica é desejável — permite verificação rápida de arquivos, transações e assinaturas digitais.

Contudo, quando aplicadas a entradas de baixa entropia — como senhas, PINs ou perfis genéticos — as funções hash rápidas tornam-se vulneráveis a ataques de enumeração em larga escala. Um atacante pode testar bilhões de candidatos por segundo usando GPUs especializadas, tornando viável a busca exaustiva sobre espaços de entrada pequenos. O problema é particularmente crítico em cenários de autenticação biométrica, onde o adversário conhece a distribuição populacional dos marcadores e pode enumerar candidatos plausíveis por ordem decrescente de frequência.

4.3 Do Hash Rápido à KDF Memory-Hard

Diante da vulnerabilidade das funções hash de uso geral a ataques de enumeração massivamente paralelos, desenvolveu-se uma classe especializada de primitivas: as funções de derivação de chaves memory-hard (KDFs memory-hard). Diferentemente das funções hash rápidas, as KDFs memory-hard foram projetadas para tornar economicamente inviável o ataque por enumeração, impondo dois custos simultâneos: custo computacional (tempo de processamento) e custo de memória (RAM dedicada por tentativa).

A Argon2id é a vencedor da Password Hashing Competition (PHC) de 2015, competição internacional organizada pela comunidade criptográfica para selecionar o algoritmo mais seguro para derivação de senhas (BIRYUKOV; DINU; KHOVRATOVICH, 2017). A variante id (híbrida) combina resistências herdadas do Argon2d (contra ataques de canal lateral) e do Argon2i (contra ataques de tempo-memória), sendo adequada para aplicações que exigem resistência a atacantes com acesso a hardware especializado.

Os parâmetros da Argon2id permitem calibrar o custo computacional:

    time_cost (t): número de passes sobre a memória;
    memory_cost (m): tamanho da memória em KiB consumida por derivação;
    parallelism (p): número de threads paralelas;
    hash_len (h): comprimento da saída em bytes.

No presente trabalho, adotaram-se os parâmetros t=3, m=64 MiB, p=1, hash_len=32 (256 bits), configurando uma operação que consome aproximadamente 247 ms por derivação em hardware modesto e 64 MiB de RAM dedicada. Esse custo eleva drasticamente o preço da enumeração: enquanto o SHA-256 processaria ~1 milhão de candidatos por segundo em hardware comum, a Argon2id processaria ~4 candidatos por segundo no mesmo hardware — um multiplicador de 156.000× no tempo de ataque.

A substituição da formulação inicial (CKU = H(S‖s), onde H é hash rápido) pela formulação final (CKU = Argon2id(S‖s)) não é meramente técnica: é a mudança de paradigma que diferencia um sistema vulnerável a enumeração em GPU de um sistema com resistência prática a ataques offline. As seções seguintes demonstram empiricamente essa diferença.


4.4 Entropia e Segurança Criptográfica

A segurança de um sistema baseado em chave derivada de biométrica depende fundamentalmente da entropia da fonte, isto é, da imprevisibilidade do material de entrada. A entropia de Shannon mede, em bits, a quantidade média de informação contida no resultado de uma variável aleatória:

[ H(X) = - \sum_{i} p(x_i) \cdot \log_2 p(x_i) ]

onde ( p(x_i) ) é a probabilidade do resultado ( x_i ).

Para marcadores genéticos, a entropia por locus depende do número de alelos e de sua distribuição de frequências. Sob distribuição uniforme (todos os alelos igualmente prováveis), a entropia máxima é ( \log_2 n ), onde ( n ) é o número de alelos. Sob distribuições reais, a entropia observada é sempre menor que a máxima.

A tabela abaixo apresenta a entropia teórica esperada para cada tipo de marcador, considerando dois modelos distintos: (i) modelo codominante, onde todos os genótipos possíveis são distinguishables (3 estados para marcadores bialélicos); e (ii) modelo dominante, onde apenas presença/ausência é observada (2 estados):
Tipo de Marcador	Estados Possíveis	Entropia Máxima (codominante)	Entropia Máxima (dominante)
STR (5 alelos)	15 genótipos	3,91 bits	—
SNP (bialélico)	3 genótipos	1,58 bits	1,00 bit
INDEL (bialélico)	3 genótipos	1,58 bits	1,00 bit

Em frequências populacionais realistas (não uniformes), as entropias efetivas são menores. Para frequências moderadas (p ≈ 0,3 para o alelo minoritário), a entropia de um SNP/INDEL bialélico no modelo codominante aproxima-se de ~1,34 bits. O trabalho do v5 utilizou valores aproximados de 1,4 bits/SNP e 0,97 bits/INDEL, que refletem modelos parcialmente codominantes com leve viés de frequência.

A entropia total de um painel misto de 165 loci (20 STRs + 130 SNPs + 15 INDELs) projeta-se na faixa de 276 bits, conforme estimativas da literatura. Contudo, é crucial distinguir duas interpretações dessa cifra:

    Espaço de busca para enumeração: ~2^276 candidatos plausíveis na população — inviável para ataque offline com hardware convencional;
    Sigilo da fonte: um adversário com amostra biológica direta não precisa enumerar — tem a entrada nas mãos e aplica a mesma derivação que o sistema legítimo.

Essa segunda interpretação é a limitação estrutural que motiva o modelo híbrido: para aplicações críticas, o perfil genético deve ser combinado a um fator secreto adicional (senha, token, dispositivo), somando entropias independentes e transformando a automação biométrica em autenticação multifatorial.

5. METODOLOGIA

5.1 Desenho geral do estudo

O estudo possui caráter experimental e computacional, estruturado em duas fases articuladas:

Fase 1 (executada neste trabalho): validação do pipeline de derivação sobre um painel didático de 5 loci STR diplóides, com perfis sintéticos gerados sob frequências alélicas plausíveis, compreendendo a quantificação da entropia da fonte, a implementação e cronometragem do pipeline, e a validação estatística das chaves produzidas;

Fase 2 (projetada para desenvolvimento futuro): expansão do painel para o conjunto completo de marcadores (20 STRs + 130 SNPs + 15 INDELs, ~515 bits codificados), com frequências alélicas empíricas extraídas de bases públicas de população.

Essa arquitetura em duas fases é deliberada: o pipeline de derivação é locus-agnóstico — a canonização, a função de derivação e os critérios de validação independem do tamanho e da composição do painel —, de modo que a validação da engenharia na Fase 1 estabelece a fundação reutilizável da Fase 2 sem retrabalho metodológico.
5.2 Painel de marcadores e geração de perfis sintéticos

A Fase 1 utilizou perfis genotípicos sintéticos, simulados segundo frequências alélicas plausíveis para populações humanas, sob equilíbrio de Hardy-Weinberg, com loci independentes. O painel didático compreendeu cinco loci STR diplóides (D18S51, D21S11, D3S1358, D5S818 e TH01), representativos dos marcadores de identificação humana utilizados em genética forense. A geração aleatória foi ancorada em semente fixa (seed = 2024), garantindo que todos os experimentos sejam replicados de forma idêntica por qualquer interessado.

A opção por dados sintéticos atende a dois requisitos. Ético: a Lei Geral de Proteção de Dados classifica dados genéticos como dados pessoais sensíveis (BRASIL, 2018, Art. 5º, inciso II), impondo restrições ao uso de perfis reais — restrição que se aplicaria com força redobrada na Fase 2, mesmo com bases internacionais abertas, pois a finalidade do tratamento (geração de chaves criptográficas) é distinta da finalidade original de coleta. Metodológico: dados sintéticos eliminam variabilidade de coleta e permitem controle total dos parâmetros populacionais, isolando o comportamento do pipeline de interferências amostrais.

Foram gerados 5.000 perfis para análise populacional da fonte; a validação estatística das chaves (Seção 7) empregou uma subamostra de 400 perfis com salts independentes.
5.3 Codificação canônica do perfil genético

Antes da derivação, o genótipo é serializado em representação canônica unívoca, com três regras que garantem determinismo da entrada:

    Loci em ordem alfabética fixa, eliminando dependência da ordem de iteração do dicionário de entrada;
    Alelos ordenados por valor numérico dentro de cada locus (com fallback textual para alelos não numéricos, como marcadores de sexo), garantindo que o heterozigoto (a,b) e o (b,a) convirjam para a mesma representação;
    Delimitadores unívocos (: entre locus e alelos, | entre loci), impedindo ambiguidades de concatenação (o par de alelos "1,15" não pode ser lido como "11,5").

A saída é uma cadeia UTF-8 determinística de ~61 bytes no painel didático (e ~86 bytes projetados para o painel completo de 165 loci). A canonização garante a propriedade estrutural verificada empiricamente: genótipos equivalentes, em qualquer ordem de entrada, produzem bytes idênticos e, portanto, a mesma chave — requisito de reprodutibilidade sem o qual o sistema seria inviável para descriptografia.
5.4 Salt e derivação

Acrescenta-se salt aleatório de 16 bytes (128 bits), gerado por gerador criptograficamente seguro (CSPRNG), anexado ao material de derivação. O salt previne ataques com tabelas pré-computadas (rainbow tables) e permite a derivação de chaves independentes a partir do mesmo perfil, sendo armazenado junto à chave (não é secreto).

A derivação emprega a função Argon2id (BIRYUKOV; DINU; KHOVRATOVICH, 2017), com parâmetros calibrados para hardware de baixo custo:
Parâmetro	Valor	Papel
time_cost (t)	3	Passes sobre a memória
memory_cost (m)	65.536 KiB (64 MiB)	Memória dedicada por derivação
parallelism (p)	1	Threads (compatibilidade universal)
hash_len	32 bytes	Saída compatível com AES-256
Salt	16 bytes	CSPRNG, único por derivação

O modelo formal consolidado é CKU = Argon2id(S‖s), onde S é a codificação canônica do perfil e s o salt de contexto. Formulações anteriores baseadas em funções hash de uso geral (SHA-256, SHA-3, BLAKE3) foram mantidas apenas como baseline comparativo na análise de custo de enumeração (Seção 4.3), tendo sido substituídas pela KDF memory-hard em razão de sua vulnerabilidade a ataques massivamente paralelos.
5.5 Ambiente computacional e reprodutibilidade

Os experimentos foram conduzidos em estação de trabalho deliberadamente representativa de hardware de baixo custo (AMD FX-8370E, 8 núcleos, 3,3 GHz; 8 GiB de RAM; SSD SATA; GNU/Linux Mint 22.3, kernel 6.14; Python 3.12.3) — premissa metodológica conservadora sob a qual os tempos reportados configuram limite superior da latência legítima, ao passo que o custo imposto a atacantes deve ser interpretado como limite inferior.

O desenvolvimento utilizou ambiente virtual isolado (venv) com as bibliotecas argon2-cffi (23.1.0), numpy, pandas, matplotlib e scipy; a validação de software empregou suíte automatizada (pytest) cobrindo determinismo, invariância de canonização e estabilidade de repetição. Todo o código, os cadernos experimentais e os resultados encontram-se sob controle de versão (Git) e disponíveis em repositório público (https://github.com/botelhojrv-dev/tcc-genetica-cripto), assegurando reprodutibilidade integral mediante a semente fixa e os parâmetros registrados.
5.6 Critérios de validação

As chaves produzidas foram submetidas a três baterias estatísticas, inspiradas nos procedimentos do NIST SP 800-22 (NIST, 2010), sob nível de significância α = 0,05:

    Uniformidade de distribuição de bytes — teste qui-quadrado de aderência sobre os 12.800 bytes agregados (400 chaves × 32 bytes), com 255 graus de liberdade;
    Equilíbrio posicional de bits — proporção global de bits 1 e razão por posição nas 256 posições, com intervalos de confiança de 99% sob hipótese binomial (p = 0,5);
    Efeito avalanche — distância de Hamming entre chaves derivadas de entradas que diferem em um único bit (n = 60 pares), com critério de aprovação centrado em 50%.

Adicionalmente, foram medidas as distâncias de Hamming entre chaves de perfis distintos e de um mesmo perfil com salts distintos (caracterização de dissimilaridade), a propriedade determinística (suíte automatizada com 10 execuções repetidas e invariância à ordem de entrada), e o desempenho (cronometragem de 100 derivações em série, reportando média e intervalo observado).

O desempenho de funções hash de uso geral (SHA-256, SHA-3, BLAKE3) foi cronometrado separadamente como baseline comparativo do custo de enumeração, quantificando a vantagem da KDF memory-hard sobre as formulações de gerações anteriores do modelo.

6. MODELO MATEMÁTICO CONSOLIDADO

6.1 Definição formal

Seja G = {(m₁, g₁), …, (mₙ, gₙ)} o perfil genético de um indivíduo, onde mᵢ identifica o marcador (STR, SNP ou INDEL) e gᵢ ∈ Γ(mᵢ) o genótipo observado nesse locus. O modelo opera sobre três funções:

Codificação canônica. A função φ(G) serializa o perfil em cadeia de bytes determinística, com loci em ordem alfabética fixa, alelos ordenados por valor e delimitadores unívocos (Seção 5.3). A função é injetiva por construção: φ(G₁) = φ(G₂) ⟺ G₁ = G₂ (geneticamente equivalentes). A propriedade de injetividade foi verificada empiricamente na suíte de testes de canonização.

Derivação com salt. A CKU é definida por:

CKU=Argon2id(t=3, m=64 MiB, p=1)(φ(G) ∥ s)∈{0,1}256

onde s é salt de 128 bits gerado por CSPRNG. A derivação é determinística (mesma entrada e salt produzem chave idêntica) e unidirecional (a chave não permite recuperar o perfil genético).

Independência de chaves. Para salts distintos s₁ ≠ s₂ aplicados ao mesmo perfil, as chaves resultantes comportam-se como independentes — verificado pela distância de Hamming de 130/256 bits (~50,8%) observada na caracterização de dissimilaridade (Seção 7).

6.2 Probabilidade de colisão

A probabilidade de dois indivíduos distintos produzirem a mesma CKU combina dois eventos independentes: a coincidência dos perfis genéticos (evento raro, ditado pela genética populacional) e a coincidência das saídas da função de derivação para entradas distintas (evento ditado pela função hash subjacente).

Para o primeiro evento, com N indivíduos na população, a probabilidade de coincidência de pares segue o paradoxo do aniversário:

P(colisa˜o)≈N22⋅2256

Para N = 10¹⁸ (um quintilhão de indivíduos — dez milhões de vezes a população humana atual):

P≈(1018)22⋅2256≈10362,3×1077≈4,3×10−42

valor desprezível para qualquer finalidade prática.

Para o segundo evento, as propriedades da função de derivação garantem que entradas distintas produzam saídas com distribuição indistinguível de aleatória — resultado este que não precisa ser presumido, pois foi validado empiricamente pelas três baterias estatísticas da Seção 7.

6.3 Efeito avalanche

A propriedade de difusão do modelo exige que alteração de um único bit da entrada altere, em média, 50% dos bits de saída:

dH(Argon2id(S,s), Argon2id(S′,s))≈2562=128 bits

onde d_H é a distância de Hamming e S′ difere de S em um bit. O critério de aprovação adotado foi a média de n = 60 pares dentro da faixa 128 ± tolerância, com desvio-padrão compatível com o valor teórico binomial (σ ≈ 8 bits). A validação experimental reportou média de 127,1 bits (49,6%), σ = 9,5 — dentro do critério (Seção 7.3).


6.4 Entropia do painel completo (projeção de Fase 2)

Para o painel projetado de 165 loci, a entropia efetiva estimada soma-se por tipo de marcador, com modelos de codificação explícitos:
Componente	Modelo de codificação	Entropia unitária	Loci	Subtotal
20 STRs	Codominante (genótipos completos, frequências forenses realistas)	~4,3 bits	20	~86 bits
130 SNPs	Codominante bialélico (p ≈ 0,3)	~1,34 bits	130	~174 bits
15 INDELs	Dominante (presença/ausência, 2 estados)	~1,00 bit	15	~15 bits
Total			165	~275 bits

O subtotal aproxima-se dos ~276 bits projetados na concepção do modelo, com duas ressalvas metodológicas necessárias. Primeira: os valores unitários são estimativas baseadas em frequências medianas da literatura; a calibração empírica com bases de população real (STRBase, ALFRED, 1000 Genomes) — atividade da Fase 2 — poderá deslocar o total em alguns bits para qualquer direção. Segunda, e mais importante: como estabelecido no Referencial (Seção 4.4), essa cifra quantifica o espaço de enumeração — o custo de um atacante que busca o perfil a partir das frequências públicas —, e não o sigilo da fonte. Um adversário com acesso à amostra biológica dispõe da entrada completa e não enfrenta a enumeração.


6.5 Segurança do modelo híbrido

Para aplicações críticas, o modelo recomendado combina a CKU com fator secreto adicional f mantido pelo titular:

CKUhıˊbrida=Argon2id(φ(G) ∥ s ∥ f)

Sob independência estatística entre a fonte genética e o fator secreto, a entropia efetiva do sistema é aproximada pela soma: o painel didático da Fase 1 (~21,5 bits) combinado a uma frase-senha de ~40 bits eleva a segurança conjunta para a faixa de ~60 bits; o painel completo da Fase 2 (~275 bits), mesmo combinado a um fator modesto, supera com folga o patamar de 128 bits do padrão mínimo contemporâneo. O modelo híbrido adicionalmente desloca o ponto crítico de falha do segredo genético (irrevogável) para o fator auxiliar (revogável), mitigando o dilema da não-revocação da biometria — análise desenvolvida na Seção 10.

7. RESULTADOS EXPERIMENTAIS

Este capítulo reporta os resultados da Fase 1 do estudo, na ordem lógica do pipeline: primeiro a caracterização da fonte genética (7.1), depois o comportamento do operador de derivação (7.2), a validação estatística das chaves produzidas (7.3) e, por fim, o custo comparativo de enumeração entre a arquitetura adotada e as formulações anteriores com funções hash de uso geral (7.4).
7.1 Entropia da fonte genética

A Tabela 7.1 apresenta a entropia de Shannon observada por locus do painel didático simulado (N = 5.000 indivíduos, seed = 2024), a entropia máxima teórica (distribuição uniforme sobre os alelos do locus) e a razão entre ambas, definida como a eficiência do locus como fonte de imprevisibilidade.

Tabela 7.1 — Entropia de Shannon por locus do painel STR simulado.
Locus	Nº de alelos	H obs (bits)	H máx (bits)	Eficiência
D18S51	5	2,2320	2,3219	0,9613
D21S11	5	2,2770	2,3219	0,9806
D3S1358	5	2,2496	2,3219	0,9688
D5S818	4	1,7615	2,0000	0,8807
TH01	5	2,2325	2,3219	0,9615
Perfil (soma)	—	10,75	11,27	0,954

Fonte: dados do caderno experimental 01, elaborado pelo autor.

Os quatro loci de cinco alelos operaram com eficiência superior a 96%, refletindo frequências alélicas relativamente equilibradas no painel simulado. O locus D5S818 apresentou a menor eficiência (88,1%), consequência da dominância dos alelos 11 e 12, que juntos concentram 74% da frequência paramétrica — característica que o torna o candidato natural à exclusão em versões otimizadas do painel.

A entropia alélica agregada do painel é de 10,75 bits por conjunto haploide. Sob o modelo diplóide de Hardy-Weinberg, com loci independentes, a entropia do genótipo completo aproxima-se de 21,5 bits. Convém distinguir duas medidas distintas: a entropia do perfil como segredo (imprevisibilidade do genótipo face à população, ~21,5 bits) e a entropia interna média dos símbolos de cada perfil individual (2,95 bits, observada na distribuição individual), que quantifica a diversidade alélica dentro do indivíduo e não guarda relação com a resistência criptográfica da fonte.

Os valores obtidos confirmam o diagnóstico quantitativo antecipado na Justificativa: ainda que o painel identifique um indivíduo com elevada especificidade, a entropia disponível para derivação de chaves (~21,5 bits de genótipo) situa-se uma ordem de grandeza aquém dos 256 bits exigidos pelo AES-256 — lacuna que motiva a função de derivação memory-hard (Seção 5.4) e o modelo híbrido recomendado na Discussão.
7.2 Derivação, dissimilaridade e determinismo

O pipeline descrito na Seção 5 foi executado sobre os perfis regenerados com a mesma semente (seed = 2024), com cronometragem de 100 derivações em série. O tempo médio foi de 247 ms por derivação (intervalo observado: 232–282 ms), com consumo de 64 MiB de memória dedicada por chamada — custo este que é o mecanismo central de defesa contra enumeração, conforme analisado na Seção 7.4.

Para caracterizar a dissimilaridade produzida pela derivação, foram medidas as distâncias de Hamming em nível de bit entre chaves em três cenários (Tabela 7.2). Dois avaliam o efeito avalanche sobre entradas distintas; o terceiro valida a propriedade determinística.

Tabela 7.2 — Distância de Hamming entre chaves derivadas, por cenário (256 bits por chave).
Cenário	Bits diferentes	% de alteração	Esperado
Perfis distintos, mesmo salt	119/256	46,5%	~128 (50%)
Mesmo perfil, salts distintos	130/256	50,8%	~128 (50%)
Mesmo perfil, mesmo salt	0/256	0%	0 exato

Fonte: dados dos cadernos experimentais 02 e da suíte de testes de determinismo, elaborado pelo autor.

As medidas dos dois primeiros cenários são observações pontuais (um par por cenário, para caracterização qualitativa do operador), cuja avaliação estatística formal — 60 pares com média e desvio-padrão — é reportada na Seção 7.3. O terceiro cenário confirma a propriedade determinística: derivações repetidas da mesma entrada canônica e mesmo salt convergem para chaves bit a bit idênticas, verificada por suíte automatizada de testes que inclui dez execuções consecutivas, a estabilidade em repetição e a invariância à ordem de inserção de loci e alelos no dicionário de entrada — propriedade garantida pela canonização descrita na Seção 5.3.

Em conjunto, as três medidas caracterizam o operador de derivação de forma completa: separa maximamente entradas distintas, preserva exatamente entradas idênticas e impõe custo computacional substancial a cada chamada.
7.3 Validação estatística das chaves

Para avaliar se as chaves atendem aos critérios estatísticos de material criptográfico legítimo, foram geradas 400 chaves independentes (variando-se perfil e salt), compondo 12.800 bytes agregados, submetidos às três baterias especificadas na Seção 5.6, sob nível de significância α = 0,05 (NIST, 2010).

Bateria 1 — Uniformidade de distribuição de bytes. O teste qui-quadrado de aderência sobre os 12.800 bytes agregados (frequência esperada de 50 ocorrências por valor, 255 graus de liberdade) resultou em χ²(255) = 247,88, p = 0,614. A hipótese nula de distribuição uniforme não foi rejeitada: o valor de p situa-se muito acima do limiar, indicando que a frequência observada dos 256 valores de byte (faixa de 32 a 71 ocorrências) não desvia da expectativa uniforme de forma estatisticamente detectável. O estatístico ligeiramente inferior aos graus de liberdade (247,88 < 255) denota dispersão marginalmente menor que a esperada sob aleatoriedade perfeita — comportamento compatível com flutuação amostral, não indício de estrutura nos dados.

Bateria 2 — Equilíbrio posicional de bits. A proporção global de bits 1 nos 102.400 bits agregados foi de 0,5017 — dentro do intervalo de confiança de 99% sob hipótese binomial (p = 0,5). Na avaliação posicional, com intervalos individuais de 99% para cada uma das 256 posições de bit (0,436–0,564 para n = 400 observações por posição), verificou-se que 2 posições situaram-se fora do intervalo — resultado consistente com a expectativa estatística de ~2,6 posições fora do intervalo por puro acaso. A bateria foi aprovada, sem indício de viés posicional detectável por um adversário.

Bateria 3 — Efeito avalanche. As distâncias de Hamming entre chaves derivadas de pares de entrada diferindo em um único bit (inversão do bit menos significativo da representação canônica, mesmo salt) foram medidas em n = 60 pares, resultando em média de 127,1 bits alterados de 256 (49,6%), σ = 9,5 bits, faixa observada de 101 a 146. A média situa-se dentro do critério de aprovação centrado em 50%, e o desvio-padrão observado é compatível com o valor teórico sob difusão ideal (σ ≈ 8 bits).

Em síntese, as três baterias foram integralmente aprovadas: as chaves derivadas são estatisticamente indistinguíveis de material aleatório genuíno nas dimensões testadas. Importa sublinhar o alcance exato dessa conclusão — as baterias certificam a qualidade estatística da saída do pipeline, e não a entropia da fonte genética, que permanece limitada a ~21,5 bits conforme quantificado na Seção 7.1. A qualidade estatística não é transferível como segurança da chave, pois o adversário ataca o espaço de entrada, não a saída — distinção central para a Discussão.
7.4 Custo comparativo de enumeração

Para quantificar a vantagem da arquitetura memory-hard sobre as formulações anteriores do modelo (baseadas em funções hash de uso geral), foi executado benchmark comparativo no mesmo hardware, na mesma sessão e sobre o mesmo material canônico (65 bytes de perfil codificado + salt de 16 bytes), com aquecimento descartado. Os resultados estão persistidos no repositório (results/benchmark_hashes.json).

Tabela 7.3 — Custo por derivação e custo de enumeração do espaço de ~2^21,5 genótipos (~2,84 milhões).
Função	Tempo médio por derivação	Candidatos/s	Enumeração do espaço
SHA-256	1,7 µs	~595.800	~5 segundos
SHA3-256	1,9 µs	~531.000	~5,6 segundos
BLAKE3	2,3 µs	~429.600	~6,9 segundos
Argon2id	272 ms	~4	~9,4 dias

Fonte: dados do benchmark em mesma sessão (n = 1.000 para hashes; n = 10 para Argon2id), elaborado pelo autor.

Três leituras emergem da tabela. Primeira: sob qualquer função hash de uso geral, o espaço de genótipos do painel didático é enumerado por completo em segundos — a formulação original do modelo (CKU = H(S‖s)) ofereceria, na prática, proteção nula contra busca exaustiva offline. Segunda: a Argon2id eleva o custo da mesma enumeração para a ordem de nove dias no mesmo hardware, impondo multiplicador de ~162.000× sobre o tempo por tentativa — estimativa que, por ser medida em hardware modesto, constitui limite inferior do custo imposto a atacantes equipados de forma superior (Seção 5.5). Terceira: o consumo de 64 MiB de memória por tentativa neutraliza a vantagem de hardware massivamente paralelo, pois a RAM dedicada não escala com a mesma generosidade da computação bruta.

Duas notas metodológicas completam a leitura. O BLAKE3 mediu tempo superior ao SHA-256 (2,3 µs vs. 1,7 µs) — resultado atribuído ao custo de ligação (binding) da biblioteca em Python para entradas pequenas, e não ao algoritmo em si, cujo desempenho superior manifesta-se em entradas grandes e paralelismo multicore; a diferença é irrelevante para o argumento, pois no regime de enumeração de candidatos pequenos todas as funções rápidas operam na mesma ordem de grandeza. Adicionalmente, o tempo médio da Argon2id nesta sessão (272 ms, n = 10) contrasta com o benchmark do pipeline reportado na Seção 7.2 (247 ms, n = 100): a variação de ~10% entre sessões em estação de trabalho multitarefa é esperada e não compromete a ordem de grandeza de nenhum dos dois cenários; para fins de comparação interfunção, vale o par medido em mesma sessão.

O conjunto de resultados deste capítulo — entropia limitada, operador determinístico e estatisticamente sólido, custo de enumeração elevado — estabelece o quadro que a Discussão interpreta: viabilidade técnica demonstrada, com limitação estrutural na fonte que nenhum refinamento do operador de derivação elimina.


