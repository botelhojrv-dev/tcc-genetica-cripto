RESUMO
A identificação humana constitui um dos pilares fundamentais da biomedicina forense, da segurança digital e das ciências da informação. Métodos biométricos convencionais  como impressões digitais, reconhecimento facial e padrões de íris  apresentam vulnerabilidades importantes: podem ser falsificados, reproduzidos artificialmente ou capturados sem consentimento. Diante desse cenário, este trabalho desenvolve um modelo computacional para gerar uma Chave Criptográfica Única (CKU) derivada de marcadores genéticos individuais, combinando a singularidade biológica do DNA com a irreversibilidade matemática de funções de derivação criptográfica memory-hard. O pipeline implementado emprega marcadores forenses consolidados (STRs, SNPs, INDELs) codificados em representação binária de comprimento fixo e processados por Argon2id com sal de contexto, substituindo formulações anteriores que empregavam funções hash de uso geral (SHA-256, SHA-3, BLAKE3). A análise quantitativa demonstra que um painel misto de 165 loci (20 STRs + 130 SNPs + 15 INDELs) projeta-se na faixa de 276 bits de entropia efetiva, enquanto a validação experimental com painel didático de 5 loci confirmou a viabilidade técnica: as três baterias estatísticas foram integralmente aprovadas (χ²(255) = 247,88; p = 0,614; proporção global de bits = 0,5017 com 2/256 posições fora do intervalo de 99%; efeito avalanche = 49,6%; σ = 9,5; n = 60). O custo médio de derivação foi de 247 ms em hardware modesto. Contudo, a entropia da fonte genética (~21,5 bits no painel de 5 loci) não alcança os patamares contemporâneos de segurança (128–256 bits); a qualidade estatística da saída não substitui o sigilo da entrada, pois o adversário pode obter amostra biológica diretamente. Recomenda-se, portanto, para aplicações críticas, o modelo híbrido que combina o perfil genético a um fator secreto adicional. O trabalho contribui metodologicamente para a intersecção entre genética forense e criptografia aplicada, estabelecendo tanto a viabilidade do pipeline quanto as limitações que impõem sua adoção responsável, em conformidade com a Lei Geral de Proteção de Dados (LGPD).
Palavras-chave: Chave Criptográfica Única; Genética Forense; Criptografia; Argon2id; LGPD; Autenticação Biométrica; Validação Estatística.

ABSTRACT
Human identification constitutes one of the fundamental pillars of forensic biomedicine, digital security, and information sciences. Conventional biometric methods , such as fingerprints, facial recognition, and iris patterns , present important vulnerabilities: they can be forged, artificially reproduced, or captured without consent. This work develops a computational model to generate a Unique Cryptographic Key (CKU) derived from individual genetic markers, combining the biological uniqueness of DNA with the mathematical irreversibility of memory-hard key derivation functions. The implemented pipeline employs consolidated forensic markers (STRs, SNPs, INDELs) encoded as fixed-length binary representation and processed by Argon2id with contextual salt, replacing earlier formulations that employed general-purpose hash functions (SHA-256, SHA-3, BLAKE3). Quantitative analysis demonstrates that a mixed panel of 165 loci (20 STRs + 130 SNPs + 15 INDELs) projects effective entropy in the range of 276 bits, while experimental validation with a didactic panel of 5 loci confirmed technical feasibility: three statistical batteries were fully approved (χ²(255) = 247,88; p = 0,614; global bit proportion = 0,5017 with 2/256 positions outside 99% CI; avalanche effect = 49,6%; σ = 9,5; n = 60). Mean derivation cost was 247 ms on modest hardware. However, the genetic source entropy (~21,5 bits in the 5-locus panel) does not reach contemporary security thresholds (128–256 bits); statistical quality of output does not replace secrecy of input, as an adversary may obtain biological sample directly. Therefore, for critical applications, a hybrid model combining the genetic profile with an additional secret factor is recommended. The work contributes methodologically to the intersection between forensic genetics and applied cryptography, establishing both the pipeline feasibility and the limitations that demand responsible adoption, in compliance with the Brazilian General Data Protection Law (LGPD).
Keywords: Unique Cryptographic Key; Forensic Genetics; Cryptography; Argon2id; LGPD; Biometric Authentication; Statistical Validation.

1. INTRODUÇÃO
A identificação humana é um dos pilares fundamentais da biomedicina forense, da segurança digital e das ciências da informação. Ao longo das últimas décadas, métodos biométricos como impressões digitais, reconhecimento facial e padrões de íris tornaram-se amplamente utilizados em sistemas de autenticação (JAIN; FLYNN; ROSS, 2011). Entretanto, tais métodos apresentam vulnerabilidades importantes: podem ser falsificados, reproduzidos artificialmente ou capturados sem consentimento. Nesse contexto, o DNA surge como o identificador biológico mais robusto, estável e individualizado disponível na atualidade (BUTLER, 2015).
A genética forense utiliza regiões altamente polimórficas do genoma humano  como Short Tandem Repeats (STRs), Single Nucleotide Polymorphisms (SNPs) e INDELs  para estabelecer perfis individuais com elevado poder discriminatório (BUTLER, 2015; HILLIS et al., 2021). Esses marcadores apresentam variações suficientes entre indivíduos para torná-los candidatos naturais à geração de identificadores digitais derivados de material genético.
Paralelamente, a criptografia moderna busca soluções cada vez mais seguras para autenticação, proteção de dados e prevenção de ataques cibernéticos. A literatura especializada distingue, nesse terreno, dois tipos de primitivas com papéis distintos: as funções hash de uso geral — como SHA-256, SHA-3 e BLAKE3 — projetadas para velocidade e uso amplo (NIST, 2015a; 2015b; O’CONNOR et al., 2020), e as funções de derivação de chaves memory-hard, como a Argon2id (BIRYUKOV; DINU; KHOVRATOVICH, 2017), vencedora da Password Hashing Competition de 2015 e projetada precisamente para o cenário em que a entrada possui baixa entropia, como é o caso, como se verá, dos perfis genéticos. Essa distinção é central para o desenho do presente trabalho.
Diante desse cenário, propõe-se a criação de uma Chave Criptográfica Única (CKU) derivada diretamente de marcadores genéticos individuais, sob a formalização CKU = Argon2id(S‖s), onde S é a codificação binária canônica do perfil genético e s é um salt de contexto. Essa abordagem combina a singularidade biológica do DNA com o custo computacional imposto pela função de derivação, resultando em um identificador digital de altíssima dificuldade de enumeração. Formulações anteriores deste modelo, baseadas em funções hash de uso geral, foram reformuladas neste trabalho em razão da vulnerabilidade dessas funções a ataques de enumeração em hardware massivamente paralelo, conforme analisado no referencial teórico (Capítulo 4).
Além de seu potencial tecnológico, a proposta exige análise rigorosa de aspectos éticos, legais e de privacidade, especialmente no contexto da Lei Geral de Proteção de Dados (LGPD), que classifica informações genéticas como dados sensíveis (BRASIL, 2018). Portanto, o desenvolvimento de uma chave criptográfica baseada em DNA deve garantir que o processo seja não reversível, evitando qualquer possibilidade de reconstrução do perfil genético original  requisito que, como este trabalho demonstra empiricamente, é atendido, mas que não esgota a análise de segurança: a possibilidade de obtenção direta de amostra biológica por um adversário constitui limitação estrutural que motiva a recomendação de um modelo híbrido para aplicações críticas.
Este trabalho organiza-se da seguinte forma: o Capítulo 2 apresenta a justificativa e relevância; o Capítulo 3 os objetivos; o Capítulo 4 o referencial teórico; o Capítulo 5 a metodologia; o Capítulo 6 o modelo matemático consolidado; o Capítulo 7 os resultados experimentais; o Capítulo 8 as aplicações; o Capítulo 10 as limitações; o Capítulo 11 a discussão; e o Capítulo 12 as conclusões e extensões futuras.

2. JUSTIFICATIVA E RELEVÂNCIA
A crescente digitalização de processos biomédicos, administrativos e jurídicos exige sistemas de autenticação cada vez mais robustos, capazes de proteger informações sensíveis contra ataques cibernéticos, falsificações e acessos não autorizados. Métodos tradicionais de identificação  como senhas, tokens, impressões digitais e reconhecimento facial apresentam vulnerabilidades significativas: senhas podem ser descobertas, padrões biométricos podem ser replicados artificialmente e dados pessoais podem ser capturados sem consentimento.
A genética forense oferece um conjunto de marcadores altamente polimórficos, com variação suficiente para distinguir indivíduos com elevado grau de precisão (KWON et al., 2021; MEI et al., 2021). Entretanto, seu potencial como fonte de material para sistemas criptográficos permanece pouco explorado na literatura, especialmente no que concerne a uma questão que este trabalho coloca em primeiro plano: o poder discriminatório de um painel genético — isto é, sua capacidade de distinguir indivíduos em uma população — não equivale ao sigilo criptográfico da fonte. Um painel com centenas de loci distingue bilhões de indivíduos entre si, mas isso não impede que um adversário que obtenha uma amostra biológica do titular reconstrua a entrada e, com ela, a chave. Essa distinção, frequentemente obscurecida em abordagens leigas ao tema, estrutura a análise de segurança desenvolvida neste trabalho e orienta suas recomendações.
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
A identificação humana por meio de material genético constitui um dos pilares da biomedicina forense contemporânea. Desde a introdução do DNA fingerprinting por Jeffreys e colaboradores em 1985 (JEFFREYS et al., 1985), a técnica foi aplicada pela primeira vez em investigação criminal em 1986, no caso que culminou na exclusão de um suspeito e, posteriormente, na identificação de Colin Pitchfork (NATIONAL LIBRARY OF MEDICINE, 2006). Desde então, a análise genética forense evoluiu para sistemas padronizados e amplamente utilizados. Os marcadores mais empregados são os Short Tandem Repeats (STRs), regiões do genoma humano compostas por repetições em tandem de unidades curtas de nucleotídeos, tipicamente de 2 a 6 pares de bases, cuja variação no número de repetições confere elevado poder discriminatório (BUTLER, 2012).
Além dos STRs, ganharam espaço na genética forense moderna os Single Nucleotide Polymorphisms (SNPs) — variações de um único nucleotídeo em posições específicas do genoma — e os INDELs (Insertions/Deletions), pequenas inserções ou deleções de bases. Enquanto os STRs são tipicamente codominantes, permitindo a distinção dos dois alelos em heterozigotos, SNPs e INDELs são frequentemente bialélicos e apresentam menor diversidade alélica por locus, embora possam ser analisados em grande número (HILLIS et al., 2021; PROMEGA, 2023).
O poder discriminatório de um painel genético é quantificado pela probabilidade de coincidência aleatória, isto é, pela chance de dois indivíduos não relacionados apresentarem exatamente o mesmo perfil genético. Painéis comerciais como o GlobalFiler e o PowerPlex Fusion analisam cerca de 23 a 24 loci, incluindo STRs autossômicos e, em alguns casos, marcadores adicionais, resultando em probabilidades de coincidência extremamente baixas — frequentemente na ordem de 10−2210^{-22}10−22 a 10−2810^{-28}10−28, conforme o painel, a população de referência e o modelo estatístico adotado (PROMEGA, 2023; STEFFEN et al., 2017).
Entretanto, há uma distinção crítica que este trabalho enfatiza desde o referencial teórico: o poder discriminatório populacional de um painel genético não equivale ao sigilo criptográfico da mesma informação. Um painel com alto poder discriminativo identifica um indivíduo entre milhões de outros, mas não impede que um adversário que obtenha amostra biológica direta (saliva em copo, fio de cabelo, pele descamada) reconstrua o perfil e derive a chave associada. Essa assimetria entre identificação e imprevisibilidade constitui a tensão central que estrutura o problema de segurança deste trabalho.
4.2 Fundamentos de Funções Hash Criptográficas
Funções hash criptográficas são primitivas matemáticas que mapeiam mensagens de tamanho arbitrário para saídas de tamanho fixo, com propriedades fundamentais para a segurança digital: preimage resistance — resistência à pré-imagem, isto é, dado um valor hash, é computacionalmente inviável encontrar uma mensagem que produza esse valor; second preimage resistance — resistência à segunda pré-imagem, isto é, dada uma mensagem, é inviável encontrar outra mensagem distinta que produza o mesmo hash; e collision resistance — resistência a colisões, isto é, é inviável encontrar duas mensagens distintas que produzam o mesmo hash (STALLINGS, 2021).
As funções hash de uso geral mais difundidas incluem:
SHA-256 (Secure Hash Algorithm 2, 256 bits), integrante da família SHA-2, desenvolvida pela NSA e publicada pelo NIST; sua especificação vigente consta do FIPS 180-4, revisado em 2015 (NIST, 2015a);
SHA-3, família de funções hash baseada na construção Keccak, selecionada como vencedora da competição SHA-3 do NIST em 2012 e padronizada em 2015 como alternativa estruturalmente distinta ao SHA-2 (NIST, 2015b);
BLAKE3, função moderna de altíssimo desempenho, projetada para explorar paralelismo em múltiplos núcleos (O’CONNOR et al., 2020).
Essas primitivas são projetadas para velocidade: em hardware convencional, podem processar gigabytes por segundo, com tempo de hash na ordem de microssegundos por bloco de 64 bytes. Para autenticação e integridade de dados, essa característica é desejável  permite verificação rápida de arquivos, transações e assinaturas digitais.
Contudo, quando aplicadas a entradas de baixa entropia  como senhas, PINs ou perfis genéticos  as funções hash rápidas tornam-se vulneráveis a ataques de enumeração em larga escala. Um atacante pode testar bilhões de candidatos por segundo usando GPUs especializadas, tornando viável a busca exaustiva sobre espaços de entrada pequenos. O problema é particularmente crítico em cenários de autenticação biométrica, onde o adversário conhece a distribuição populacional dos marcadores e pode enumerar candidatos plausíveis por ordem decrescente de frequência.
4.3 Do Hash Rápido à KDF Memory-Hard
Diante da vulnerabilidade das funções hash de uso geral a ataques de enumeração massivamente paralelos, desenvolveu-se uma classe especializada de primitivas: as funções de derivação de chaves memory-hard (KDFs memory-hard). Diferentemente das funções hash rápidas, as KDFs memory-hard foram projetadas para tornar economicamente inviável o ataque por enumeração, impondo dois custos simultâneos: custo computacional (tempo de processamento) e custo de memória (RAM dedicada por tentativa).
A Argon2id é a vencedor da Password Hashing Competition (PHC) de 2015, competição internacional organizada pela comunidade criptográfica para selecionar o algoritmo mais seguro para derivação de senhas (BIRYUKOV; DINU; KHOVRATOVICH, 2017). A variante id (híbrida) combina resistências herdadas do Argon2d (contra ataques de canal lateral) e do Argon2i (contra ataques de tempo-memória), sendo adequada para aplicações que exigem resistência a atacantes com acesso a hardware especializado.
Os parâmetros da Argon2id permitem calibrar o custo computacional:
time_cost (t): número de passes sobre a memória;
memory_cost (m): tamanho da memória em KiB consumida por derivação;
parallelism (p): número de threads paralelas;
hash_len (h): comprimento da saída em bytes.
No presente trabalho, adotaram-se os parâmetros t=3, m=64 MiB, p=1, hash_len=32 (256 bits), configurando uma operação que consome aproximadamente 247 ms por derivação em hardware modesto e 64 MiB de RAM dedicada. Esse custo eleva drasticamente o preço da enumeração: enquanto o SHA-256 processaria ~1 milhão de candidatos por segundo em hardware comum, a Argon2id processaria ~4 candidatos por segundo no mesmo hardware  um multiplicador de 250.000× no tempo de ataque.
A substituição da formulação inicial (CKU = H(S‖s), onde H é hash rápido) pela formulação final (CKU = Argon2id(S‖s)) não é meramente técnica: é a mudança de paradigma que diferencia um sistema vulnerável a enumeração em GPU de um sistema com resistência prática a ataques offline. As seções seguintes demonstram empiricamente essa diferença.
4.4 Entropia e Segurança Criptográfica
A segurança de um sistema baseado em chave derivada de biométrica depende fundamentalmente da entropia da fonte, isto é, da imprevisibilidade do material de entrada. A entropia de Shannon mede, em bits, a quantidade média de informação contida no resultado de uma variável aleatória:
[ H(X) = - \sum_{i} p(x_i) \cdot \log_2 p(x_i) ]
onde ( p(x_i) ) é a probabilidade do resultado ( x_i ).
Para marcadores genéticos, a entropia por locus depende do número de alelos e de sua distribuição de frequências. Sob distribuição uniforme (todos os alelos igualmente prováveis), a entropia máxima é ( \log_2 n ), onde ( n ) é o número de alelos. Sob distribuições reais, a entropia observada é sempre menor que a máxima.
A tabela abaixo apresenta a entropia teórica esperada para cada tipo de marcador, considerando dois modelos distintos: (i) modelo codominante, onde todos os genótipos possíveis são distinguishables (3 estados para marcadores bialélicos); e (ii) modelo dominante, onde apenas presença/ausência é observada (2 estados):
Tipo de Marcador
Estados Possíveis
Entropia Máxima (codominante)
Entropia Máxima (dominante)
STR (5 alelos)
15 genótipos
3,91 bits
—
SNP (bialélico)
3 genótipos
1,58 bits
1,00 bit
INDEL (bialélico)
3 genótipos
1,58 bits
1,00 bit
Em frequências populacionais realistas (não uniformes), as entropias efetivas são menores. Para frequências moderadas (p ≈ 0,3 para o alelo minoritário), a entropia de um SNP/INDEL bialélico no modelo codominante aproxima-se de ~1,34 bits. O trabalho do v5 utilizou valores aproximados de 1,4 bits/SNP e 0,97 bits/INDEL, que refletem modelos parcialmente codominantes com leve viés de frequência.
A entropia total de um painel misto de 165 loci (20 STRs + 130 SNPs + 15 INDELs) projeta-se na faixa de 276 bits, conforme estimativas da literatura. Contudo, é crucial distinguir duas interpretações dessa cifra:
Espaço de busca para enumeração: ~2^276 candidatos plausíveis na população inviável para ataque offline com hardware convencional;
Sigilo da fonte: um adversário com amostra biológica direta não precisa enumerar  tem a entrada nas mãos e aplica a mesma derivação que o sistema legítimo.
Essa segunda interpretação é a limitação estrutural que motiva o modelo híbrido: para aplicações críticas, o perfil genético deve ser combinado a um fator secreto adicional (senha, token, dispositivo), somando entropias independentes e transformando a automação biométrica em autenticação multifatorial.

5. METODOLOGIA
5.1 Desenho geral do estudo
O estudo possui caráter experimental e computacional, estruturado em duas fases articuladas:
Fase 1 (executada neste trabalho): validação do pipeline de derivação sobre um painel didático de 5 loci STR diplóides, com perfis sintéticos gerados sob frequências alélicas plausíveis, compreendendo a quantificação da entropia da fonte, a implementação e cronometragem do pipeline, e a validação estatística das chaves produzidas;
Fase 2 (projetada para desenvolvimento futuro): expansão do painel para o conjunto completo de marcadores (20 STRs + 130 SNPs + 15 INDELs, ~515 bits codificados), com frequências alélicas empíricas extraídas de bases públicas de população.
Essa arquitetura em duas fases é deliberada: o pipeline de derivação é locus-agnóstico  a canonização, a função de derivação e os critérios de validação independem do tamanho e da composição do painel —, de modo que a validação da engenharia na Fase 1 estabelece a fundação reutilizável da Fase 2 sem retrabalho metodológico.
5.2 Painel de marcadores e geração de perfis sintéticos
A Fase 1 utilizou perfis genotípicos sintéticos, simulados segundo frequências alélicas plausíveis para populações humanas, sob equilíbrio de Hardy-Weinberg, com loci independentes. O painel didático compreendeu cinco loci STR diplóides (D18S51, D21S11, D3S1358, D5S818 e TH01), representativos dos marcadores de identificação humana utilizados em genética forense. A geração aleatória foi ancorada em semente fixa (seed = 2024), garantindo que todos os experimentos sejam replicados de forma idêntica por qualquer interessado.
A opção por dados sintéticos atende a dois requisitos. Ético: a Lei Geral de Proteção de Dados classifica dados genéticos como dados pessoais sensíveis (BRASIL, 2018, Art. 5º, inciso II), impondo restrições ao uso de perfis reais  restrição que se aplicaria com força redobrada na Fase 2, mesmo com bases internacionais abertas, pois a finalidade do tratamento (geração de chaves criptográficas) é distinta da finalidade original de coleta. Metodológico: dados sintéticos eliminam variabilidade de coleta e permitem controle total dos parâmetros populacionais, isolando o comportamento do pipeline de interferências amostrais.
Foram gerados 5.000 perfis para análise populacional da fonte; a validação estatística das chaves (Seção 7) empregou uma subamostra de 400 perfis com salts independentes.
5.3 Codificação canônica do perfil genético
Antes da derivação, o genótipo é serializado em representação canônica unívoca, com três regras que garantem determinismo da entrada:
Loci em ordem alfabética fixa, eliminando dependência da ordem de iteração do dicionário de entrada;
Alelos ordenados por valor numérico dentro de cada locus (com fallback textual para alelos não numéricos, como marcadores de sexo), garantindo que o heterozigoto (a,b) e o (b,a) convirjam para a mesma representação;
Delimitadores unívocos (: entre locus e alelos, | entre loci), impedindo ambiguidades de concatenação (o par de alelos "1,15" não pode ser lido como "11,5").
A saída é uma cadeia UTF-8 determinística de ~61 bytes no painel didático (e ~86 bytes projetados para o painel completo de 165 loci). A canonização garante a propriedade estrutural verificada empiricamente: genótipos equivalentes, em qualquer ordem de entrada, produzem bytes idênticos e, portanto, a mesma chave — requisito de reprodutibilidade sem o qual o sistema seria inviável para descriptografia.
5.4 Salt e derivação
Acrescenta-se um salt aleatório de 16 bytes (128 bits), gerado por um gerador pseudoaleatório criptograficamente seguro (CSPRNG) e incorporado ao material de entrada da derivação. O salt previne ataques baseados em tabelas pré-computadas (rainbow tables) e permite a derivação de chaves independentes a partir do mesmo perfil genético, desde que seja único para cada operação de derivação. Por não constituir informação secreta, o salt pode ser armazenado junto à chave derivada ou aos metadados necessários à reprodução do processo (BIRYUKOV; DINU; KHOVRATOVICH, 2017; IETF, 2021).
A derivação emprega a função Argon2id, com parâmetros calibrados para hardware de baixo custo e execução single-thread. Embora o RFC 9106 recomende p = 4 para a configuração de referência, adotou-se p = 1 para maximizar a portabilidade e a compatibilidade com dispositivos com recursos computacionais limitados, mantendo 64 MiB de memória, três passos, salt de 128 bits e saída de 256 bits.
Parâmetro
Valor
Papel
time_cost (t)
3
Passes sobre a memória
memory_cost (m)
65.536 KiB (64 MiB)
Memória dedicada por derivação
parallelism (p)
1
Threads (compatibilidade universal)
hash_len
32 bytes
Saída compatível com AES-256
Salt
16 bytes
CSPRNG, único por derivação
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
dH(Argon2id(S,s), Argon2id(S′,s))≈2562=128 bits
onde d_H é a distância de Hamming e S′ difere de S em um bit. O critério de aprovação adotado foi a média de n = 60 pares dentro da faixa 128 ± tolerância, com desvio-padrão compatível com o valor teórico binomial (σ ≈ 8 bits). A validação experimental reportou média de 127,1 bits (49,6%), σ = 9,5 — dentro do critério (Seção 7.3).
6.4 Entropia do painel completo (projeção de Fase 2)
Para o painel projetado de 165 loci, a entropia efetiva estimada soma-se por tipo de marcador, com modelos de codificação explícitos:
Componente
Modelo de codificação
Entropia unitária
Loci
Subtotal
20 STRs
Codominante (genótipos completos, frequências forenses realistas)
~4,3 bits
20
~86 bits
130 SNPs
Codominante bialélico (p ≈ 0,3)
~1,34 bits
130
~174 bits
15 INDELs
Dominante (presença/ausência, 2 estados)
~1,00 bit
15
~15 bits
Total


165
~275 bits
O subtotal aproxima-se dos ~276 bits projetados na concepção do modelo, com duas ressalvas metodológicas necessárias. Primeira: os valores unitários são estimativas baseadas em frequências medianas da literatura; a calibração empírica com bases de população real (STRBase, ALFRED, 1000 Genomes) ,atividade da Fase 2  , poderá deslocar o total em alguns bits para qualquer direção. Segunda, e mais importante: como estabelecido no Referencial (Seção 4.4), essa cifra quantifica o espaço de enumeração — o custo de um atacante que busca o perfil a partir das frequências públicas —, e não o sigilo da fonte. Um adversário com acesso à amostra biológica dispõe da entrada completa e não enfrenta a enumeração.
6.5 Segurança do modelo híbrido
Para aplicações críticas, o modelo recomendado combina a CKU com fator secreto adicional f mantido pelo titular:
CKUhıˊbrida=Argon2id(φ(G) ∥ s ∥ f)
Sob independência estatística entre a fonte genética e o fator secreto, a entropia efetiva do sistema é aproximada pela soma: o painel didático da Fase 1 (~21,5 bits) combinado a uma frase-senha de ~40 bits eleva a segurança conjunta para a faixa de ~60 bits; o painel completo da Fase 2 (~275 bits), mesmo combinado a um fator modesto, supera com folga o patamar de 128 bits do padrão mínimo contemporâneo. O modelo híbrido adicionalmente desloca o ponto crítico de falha do segredo genético (irrevogável) para o fator auxiliar (revogável), mitigando o dilema da não-revocação da biometria  análise desenvolvida na Seção 10.



7. RESULTADOS EXPERIMENTAIS
Este capítulo reporta os resultados da Fase 1 do estudo, na ordem lógica do pipeline: primeiro a caracterização da fonte genética (7.1), depois o comportamento do operador de derivação (7.2), a validação estatística das chaves produzidas (7.3) e, por fim, o custo comparativo de enumeração entre a arquitetura adotada e as formulações anteriores com funções hash de uso geral (7.4).
7.1 Entropia da fonte genética
A Tabela 7.1 apresenta a entropia de Shannon observada por locus do painel didático simulado (N = 5.000 indivíduos, seed = 2024), a entropia máxima teórica (distribuição uniforme sobre os alelos do locus) e a razão entre ambas, definida como a eficiência do locus como fonte de imprevisibilidade.
Tabela 7.1 — Entropia de Shannon por locus do painel STR simulado.
Locus
Nº de alelos
H obs (bits)
H máx (bits)
Eficiência
D18S51
5
2,2320
2,3219
0,9613
D21S11
5
2,2770
2,3219
0,9806
D3S1358
5
2,2496
2,3219
0,9688
D5S818
4
1,7615
2,0000
0,8807
TH01
5
2,2325
2,3219
0,9615
Perfil (soma)
—
10,75
11,27
0,954
Fonte: dados do caderno experimental 01, elaborado pelo autor.
Os quatro loci de cinco alelos operaram com eficiência superior a 96%, refletindo frequências alélicas relativamente equilibradas no painel simulado. O locus D5S818 apresentou a menor eficiência (88,1%), consequência da dominância dos alelos 11 e 12, que juntos concentram 74% da frequência paramétrica  característica que o torna o candidato natural à exclusão em versões otimizadas do painel.
A entropia alélica agregada do painel é de 10,75 bits por conjunto haploide. Sob o modelo diplóide de Hardy-Weinberg, com loci independentes, a entropia do genótipo completo aproxima-se de 21,5 bits. Convém distinguir duas medidas distintas: a entropia do perfil como segredo (imprevisibilidade do genótipo face à população, ~21,5 bits) e a entropia interna média dos símbolos de cada perfil individual (2,95 bits, observada na distribuição individual), que quantifica a diversidade alélica dentro do indivíduo e não guarda relação com a resistência criptográfica da fonte.
Os valores obtidos confirmam o diagnóstico quantitativo antecipado na Justificativa: ainda que o painel identifique um indivíduo com elevada especificidade, a entropia disponível para derivação de chaves (~21,5 bits de genótipo) situa-se uma ordem de grandeza aquém dos 256 bits exigidos pelo AES-256  lacuna que motiva a função de derivação memory-hard (Seção 5.4) e o modelo híbrido recomendado na Discussão.
7.2 Derivação, dissimilaridade e determinismo
O pipeline descrito na Seção 5 foi executado sobre os perfis regenerados com a mesma semente (seed = 2024), com cronometragem de 100 derivações em série. O tempo médio foi de 247 ms por derivação (intervalo observado: 232–282 ms), com consumo de 64 MiB de memória dedicada por chamada — custo este que é o mecanismo central de defesa contra enumeração, conforme analisado na Seção 7.4.
Para caracterizar a dissimilaridade produzida pela derivação, foram medidas as distâncias de Hamming em nível de bit entre chaves em três cenários (Tabela 7.2). Dois avaliam o efeito avalanche sobre entradas distintas; o terceiro valida a propriedade determinística.
Tabela 7.2 — Distância de Hamming entre chaves derivadas, por cenário (256 bits por chave).
Cenário
Bits diferentes
% de alteração
Esperado
Perfis distintos, mesmo salt
119/256
46,5%
~128 (50%)
Mesmo perfil, salts distintos
130/256
50,8%
~128 (50%)
Mesmo perfil, mesmo salt
0/256
0%
0 exato
Fonte: dados dos cadernos experimentais 02 e da suíte de testes de determinismo, elaborado pelo autor.
As medidas dos dois primeiros cenários são observações pontuais (um par por cenário, para caracterização qualitativa do operador), cuja avaliação estatística formal  60 pares com média e desvio-padrão é reportada na Seção 7.3. O terceiro cenário confirma a propriedade determinística: derivações repetidas da mesma entrada canônica e mesmo salt convergem para chaves bit a bit idênticas, verificada por suíte automatizada de testes que inclui dez execuções consecutivas, a estabilidade em repetição e a invariância à ordem de inserção de loci e alelos no dicionário de entrada  propriedade garantida pela canonização descrita na Seção 5.3.
Em conjunto, as três medidas caracterizam o operador de derivação de forma completa: separa maximamente entradas distintas, preserva exatamente entradas idênticas e impõe custo computacional substancial a cada chamada.
7.3 Validação estatística das chaves
Para avaliar se as chaves atendem aos critérios estatísticos de material criptográfico legítimo, foram geradas 400 chaves independentes (variando-se perfil e salt), compondo 12.800 bytes agregados, submetidos às três baterias especificadas na Seção 5.6, sob nível de significância α = 0,05 (NIST, 2010).
Bateria 1  Uniformidade de distribuição de bytes. O teste qui-quadrado de aderência sobre os 12.800 bytes agregados (frequência esperada de 50 ocorrências por valor, 255 graus de liberdade) resultou em χ²(255) = 247,88, p = 0,614. A hipótese nula de distribuição uniforme não foi rejeitada: o valor de p situa-se muito acima do limiar, indicando que a frequência observada dos 256 valores de byte (faixa de 32 a 71 ocorrências) não desvia da expectativa uniforme de forma estatisticamente detectável. O estatístico ligeiramente inferior aos graus de liberdade (247,88 < 255) denota dispersão marginalmente menor que a esperada sob aleatoriedade perfeita comportamento compatível com flutuação amostral, não indício de estrutura nos dados.
Bateria 2  Equilíbrio posicional de bits. A proporção global de bits 1 nos 102.400 bits agregados foi de 0,5017 dentro do intervalo de confiança de 99% sob hipótese binomial (p = 0,5). Na avaliação posicional, com intervalos individuais de 99% para cada uma das 256 posições de bit (0,436–0,564 para n = 400 observações por posição), verificou-se que 2 posições situaram-se fora do intervalo — resultado consistente com a expectativa estatística de ~2,6 posições fora do intervalo por puro acaso. A bateria foi aprovada, sem indício de viés posicional detectável por um adversário.
Bateria 3   Efeito avalanche. As distâncias de Hamming entre chaves derivadas de pares de entrada diferindo em um único bit (inversão do bit menos significativo da representação canônica, mesmo salt) foram medidas em n = 60 pares, resultando em média de 127,1 bits alterados de 256 (49,6%), σ = 9,5 bits, faixa observada de 101 a 146. A média situa-se dentro do critério de aprovação centrado em 50%, e o desvio-padrão observado é compatível com o valor teórico sob difusão ideal (σ ≈ 8 bits).
Em síntese, as três baterias foram integralmente aprovadas: as chaves derivadas são estatisticamente indistinguíveis de material aleatório genuíno nas dimensões testadas. Importa sublinhar o alcance exato dessa conclusão  as baterias certificam a qualidade estatística da saída do pipeline, e não a entropia da fonte genética, que permanece limitada a ~21,5 bits conforme quantificado na Seção 7.1. A qualidade estatística não é transferível como segurança da chave, pois o adversário ataca o espaço de entrada, não a saída , distinção central para a Discussão.
7.4 Custo comparativo de enumeração
Para quantificar a vantagem da arquitetura memory-hard sobre as formulações anteriores do modelo (baseadas em funções hash de uso geral), foi executado benchmark comparativo no mesmo hardware, na mesma sessão e sobre o mesmo material canônico (65 bytes de perfil codificado + salt de 16 bytes), com aquecimento descartado. Os resultados estão persistidos no repositório (results/benchmark_hashes.json).
Tabela 7.3 — Custo por derivação e custo de enumeração do espaço de ~2^21,5 genótipos (~2,84 milhões).
Função
Tempo médio por derivação
Candidatos/s
Enumeração do espaço
SHA-256
1,7 µs
~595.800
~5 segundos
SHA3-256
1,9 µs
~531.000
~5,6 segundos
BLAKE3
2,3 µs
~429.600
~6,9 segundos
Argon2id
272 ms
~4
~9,4 dias
Fonte: dados do benchmark em mesma sessão (n = 1.000 para hashes; n = 10 para Argon2id), elaborado pelo autor.
Três leituras emergem da tabela. Primeira: sob qualquer função hash de uso geral, o espaço de genótipos do painel didático é enumerado por completo em segundos — a formulação original do modelo (CKU = H(S‖s)) ofereceria, na prática, proteção nula contra busca exaustiva offline. Segunda: a Argon2id eleva o custo da mesma enumeração para a ordem de nove dias no mesmo hardware, impondo multiplicador de ~162.000× sobre o tempo por tentativa — estimativa que, por ser medida em hardware modesto, constitui limite inferior do custo imposto a atacantes equipados de forma superior (Seção 5.5). Terceira: o consumo de 64 MiB de memória por tentativa neutraliza a vantagem de hardware massivamente paralelo, pois a RAM dedicada não escala com a mesma generosidade da computação bruta.
Duas notas metodológicas completam a leitura. O BLAKE3 mediu tempo superior ao SHA-256 (2,3 µs vs. 1,7 µs) — resultado atribuído ao custo de ligação (binding) da biblioteca em Python para entradas pequenas, e não ao algoritmo em si, cujo desempenho superior manifesta-se em entradas grandes e paralelismo multicore; a diferença é irrelevante para o argumento, pois no regime de enumeração de candidatos pequenos todas as funções rápidas operam na mesma ordem de grandeza. Adicionalmente, o tempo médio da Argon2id nesta sessão (272 ms, n = 10) contrasta com o benchmark do pipeline reportado na Seção 7.2 (247 ms, n = 100): a variação de ~10% entre sessões em estação de trabalho multitarefa é esperada e não compromete a ordem de grandeza de nenhum dos dois cenários; para fins de comparação interfunção, vale o par medido em mesma sessão.
O conjunto de resultados deste capítulo  entropia limitada, operador determinístico e estatisticamente sólido, custo de enumeração elevado  estabelece o quadro que a Discussão interpreta: viabilidade técnica demonstrada, com limitação estrutural na fonte que nenhum refinamento do operador de derivação elimina.
8. APLICAÇÕES
8.1 Saúde digital e prontuário eletrônico
A aplicação mais imediata da CKU situa-se na interoperabilidade de registros de saúde. O prontuário eletrônico do paciente (PEP) exige mecanismos de vinculação entre indivíduo e registro que sejam ao mesmo tempo únicos, persistentes e verificáveis. A CKU derivada do perfil genético oferece um identificador com vantagens estruturais frente às chaves convencionais: não pode ser esquecida (o titular nasce portando o material de derivação), não pode ser transferida (vinculação biológica direta) e não depende de terceiro emissor (ao contrário de CPF, RG ou certificados digitais).
Em arquiteturas típicas, a CKU funcionaria como chave de criptografia simétrica (AES-256) para o envelope criptográfico do prontuário, com o perfil genético atuando como material de derivação verificado no momento do atendimento por exemplo, na admissão hospitalar, mediante tipagem rápida do painel didático ou completo. Para aplicações críticas do setor (registros contendo dados sensíveis sob a LGPD), aplica-se o modelo híbrido da Seção 6.5, agregando fator secreto detido pelo titular.
8.2 Sistemas de alta segurança e controle de acesso
Ambientes que exigem autenticação de alta confiança  laboratórios forenses, instalações governamentais classificadas, infraestruturas críticas  podem empregar a CKU como fator de autenticação de algo que o usuário é, com especificidade superior às biometrias convencionais. Enquanto impressões digitais podem ser forjadas com moldes, faces replicadas por deepfakes e íris capturadas por fotografia de alta resolução, o perfil genético requer amostra biológica legítima do titular — elevando o custo do ataque de falsificação a patamares qualitativamente distintos.
O custo computacional de 247 ms por verificação (Seção 7.2), embora inviabilize processamento massivo, é plenamente compatível com autenticação interativa de usuário único — o cenário exato do controle de acesso físico ou lógico. O mesmo custo que limita o sistema legítimo é o que penaliza o atacante que tenta enumeração (Seção 7.4): o desenho beneficia deliberadamente o uso legítimo em detrimento do abuso.
8.3 Genética forense e cadeia de custódia
Na própria genética forense, a CKU oferece ferramenta de integridade de cadeia de custódia: vestígios biológicos coletados em local de crime podem ter seus perfis codificados e derivados como chaves de autenticação dos laudos associados, criando vínculo criptográfico entre amostra, perícia e conclusão. Qualquer adulteração do registro intermediário  troca de amostras, edição de laudo  resulta em chave inválida na verificação, tornando a manipulação detectável.
Aplicação correlata é a área de parentesco e identificação de desaparecidos, na qual bancos de perfis genéticos de vítimas de catástrofes ou de pessoas desaparecidas poderiam empregar chaves derivadas como índices de busca à prova de vazamento: um banco comprometido exporia chaves inúteis à reconstrução dos perfis originais (irreversibilidade, Seção 6.1), protegendo os dados sensíveis subjacentes mesmo em cenário de violação do repositório.
8.4 Gestão corporativa e assinatura de documentos
Em contexto corporativo  área da formação em Administração , a CKU presta-se à autenticação de atos de gestão de alta formalidade: assinatura de contratos, aprovação de transações sensíveis, deleção controlada de registros. A diferença conceitual frente à assinatura digital convencional é a natureza do fator: em vez de depender de posse (token) ou conhecimento (senha), ambos delegáveis ou roubáveis, o fator é inseparável do titular  propriedade valiosa em governança, onde a atribuição de responsabilidade individual é imperativa.
A limitação estrutural, contudo, impõe-se com particular relevância neste domínio: contrariamente à prática de assinaturas digitais, atos societários exigem eventualmente revogação de credenciais (exoneração de dirigente, por exemplo). A irreversibilidade do material genético torna imprescindível a arquitetura híbrida  o fator genético autentica o vínculo identitário; o fator secreto, revogável, autoriza a pratica do ato  decomposição analisada na Seção 10.
8.5 Conformidade com a LGPD
Todas as aplicações precedentes tem um fundamento regulatório comum. A Lei nº 13.709/2018 (LGPD) classifica dados genéticos como dados pessoais sensíveis (Art. 5º, II), submetendo seu tratamento a bases legais específicas e a princípios como finalidade, necessidade e segurança (BRASIL, 2018). A arquitetura da CKU dialoga com esses princípios em três frentes:
Minimização: a chave derivada não contém o perfil genético  a irreversibilidade da função de derivação significa que o dado sensível permanece apenas no processo de derivação, jamais no artefato armazenado ou transmitido;
Finalidade: o uso do perfil exclusivamente para derivação, com descarte do material após o processo, delimita a finalidade do tratamento de forma estrita  diferentemente de bancos de perfis completos, cuja reutilização para outras finalidades é tecnicamente possível;
Segurança: a adoção da função memory-hard constitui medida técnica proporcional ao risco, na linha do princípio da segurança (Art. 46), elevando o custo de ataques de enumeração em ordens de magnitude.
Cabe registrar, por honestidade regulatória, que a tipagem genética como etapa de autenticação constitui, ela própria, tratamento de dado sensível  de modo que a adoção da CKU não dispensa o consentimento ou base legal adequada para a coleta da amostra no ponto de verificação. A CKU mitiga os riscos de armazenamento, não os da coleta.
9. LIMITAÇÕES
Este trabalho apresenta limitações em dois planos distintos  estruturais, inerentes ao próprio conceito de derivação criptográfica a partir de fonte biológica, e empíricas, decorrentes do desenho experimental adotado na Fase 1.
9.1 Limitações estruturais
Gêmeos monozigóticos. A derivação da CKU pressupõe a unicidade do perfil genético  pressuposto violado para gêmeos monozigóticos, que compartilham o mesmo genoma em todos os loci cobertos pelo painel. Dois irmãos MZ gerariam, portanto, chaves idênticas quando submetidos ao mesmo procedimento de tipagem e ao mesmo salt. Trata-se de limitação insolúvel no nível do desenho atual: nenhum refinamento da função de derivação distingue material genético idêntico. Mitigações possíveis residem na CKU Ampliada  incorporação de marcadores somáticos e epigenéticos (padrões de metilação do DNA, rearranjos de receptores imunológicos, mosaicismos pós-zigóticos), que divergem entre MZ ao longo da vida  registrada como extensão futura (Seção 11). Para as aplicações críticas, a limitação reforça a necessidade do modelo híbrido: o fator secreto adicional distingue titulares mesmo sob identidade genética compartilhada.
Irrevogabilidade do material genético. Senhas comprometidas são substituídas; tokens perdidos, reemitidos; certificados digitais, revogados. O perfil genético não admite nenhuma dessas operações  o titular não pode trocar seu DNA. Comprometida a relação entre perfil e chave (por exemplo, pelo vazamento do material de derivação ou pela imposição coercitiva de fornecimento da amostra), a credencial está comprometida permanentemente. A arquitetura híbrida (Seção 6.5) desloca o ponto crítico de falha para o fator auxiliar, revogável  mitigação parcial, pois o componente genético permanece irrenunciável como elo identitário.
Obtenção direta de amostra biológica. O adversário que obtém amostra do titular (saliva residual em copo, fio de cabelo, material descamado) possui a entrada completa do sistema e a submete ao mesmo pipeline legítimo. Nenhuma quantidade de entropia do painel ou de endurecimento da função de derivação neutraliza esse vetor, pois o ataque contorna a enumeração  não a enfrenta. A consequência prática é a delimitação do modelo de ameaça: a CKU protege contra adversários que conhecem o espaço de perfis (frequências públicas, bases forenses), não contra adversários que possuem a amostra do titular. Vale notar que essa assimetria atenua a limitação em cenário real: a coleta de amostra requer proximidade física e conhecimento prévio do alvo, condição muito mais restritiva que o acesso remoto a bases de dados.
Entropia limitada da fonte (painel didático). Com ~21,5 bits de entropia de genótipo, o painel da Fase 1 situa-se muito aquém dos patamares contemporâneos (128 bits). A expansão para o painel completo (~275 bits projetados, Seção 6.4) atenua drasticamente a limitação, mas a mantém dependente do modelo de ameaça: a entropia quantifica o custo da enumeração, não o sigilo  distinção desenvolvida no Referencial (Seção 4.4) e que atravessa todo o trabalho.
9.2 Limitações empíricas da Fase 1
Simulação populacional. As frequências alélicas do painel didático são plausíveis, não empíricas. A calibração com frequências reais  STRBase, ALFRED, 1000 Genomes é atividade da Fase 2 e poderá deslocar os valores de entropia em qualquer direção, embora o argumento estrutural (gap frente aos 256 bits) seja insensível a essa troca.
Amplitude da validação estatística. As três baterias aplicadas (12.800 bytes, 400 chaves) foram integralmente aprovadas, mas constituem subconjunto mínimo da suíte do NIST SP 800-22, que compreende 15 subtestes e exige no mínimo 10⁶ bits. A bateria completa permanece como trabalho futuro  a Amostra da Fase 1 foi dimensionada para caracterização do pipeline, não para certificação exaustiva de aleatoriedade.
Medidas pontuais de dissimilaridade. As distâncias de Hamming entre perfis distintos e entre salts distintos (Tabela 7.2) baseiam-se em observação de par único por cenário; a avaliação estatística formal do efeito avalanche empregou n = 60 pares (Seção 7.3). A re-execução sistemática dos cenários de caracterização ampliaria a robustez do reporte.
Ausência da min-entropia. A entropia de Shannon superestima a resistência à enumeração gulosa  ataque que enumera genótipos por ordem decrescente de probabilidade. A min-entropia por locus (−log₂ max pᵢ) constitui limite inferior mais conservador e deverá integrar a análise da Fase 2, conforme registrado nos objetivos.
Hardware de referência. Os benchmarks foram medidos em estação de trabalho deliberadamente modesta (Seção 5.5), o que qualifica os tempos legítimos como limite superior e os custos ao atacante como limite inferior — prerrogativa metodológica consciente, mas que impede a generalização direta dos valores absolutos para ambientes de produção contemporâneos. O multiplicador de ~162.000× entre hash de uso geral e Argon2id, contudo, é propriedade da arquitetura, não do hardware específico.
Contingência operacional. A viabilidade pressupõe tipagem genômica confiável disponível no fluxo de autenticação  condição tecnológica e regulatória (LGPD) fora do escopo experimental deste estudo, examinada na dimensão de aplicações (Seção 8.5).
9.3 Síntese
As limitações estruturais não são defeitos de execução: são propriedades da fonte biológica como material criptográfico, mapeadas com antecedência e convertidas em critérios de desenho (modelo híbrido, delimitação do modelo de ameaça, CKU Ampliada como extensão). As limitações empíricas, por sua vez, delimitam o escopo validado da Fase 1 e definem a agenda da Fase 2. Em conjunto, elas definem o território honesto do trabalho: o que foi demonstrado, o que foi projetado e o que permanece aberto.

10. DISCUSSÃO
Os resultados experimentais da Fase 1, lidos em conjunto, compõem um quadro que exige interpretação em duas camadas: o que a arquitetura demonstrou e o que a fonte impõe. Esta seção articula as duas camadas e posiciona o trabalho frente à literatura de biometria criptográfica.
10.1 O gap de entropia como achado central
O resultado mais importante deste trabalho é também o mais desconfortável: a entropia genética disponível no painel STR estudado  aproximadamente 21,5 bits de genótipo (Seção 7.1)  corresponde a cerca de um sexto do patamar mínimo contemporâneo (128 bits) e a menos de um décimo dos 256 bits exigidos pela chave-alvo (AES-256). Traduzida ao espaço de busca, a diferença é dramática: um adversário enfrenta 2^106 vezes menos candidatos que os pressupostos pelo padrão mínimo, e 2^234 vezes menos que os do AES-256.
Essa lacuna não é defeito metodológico, mas característica intrínseca da fonte: a imprevisibilidade de um genótipo é limitada pelas frequências alélicas populacionais, que são públicas e amplamente documentadas. Um perfil STR identifica um indivíduo com especificidade extraordinária  bilhões para um mas identificar não é o mesmo que ser imprevisível: a especificidade advém da baixa probabilidade de coincidência entre dois perfis sorteados, enquanto a imprevisibilidade criptográfica exige a alta entropia do segredo face ao adversário. O adversário forense conhece as distribuições, sabe enumerar genótipos por ordem decrescente de probabilidade e dispõe, em cenários plausíveis, de informação genética parcial do alvo (parentes próximos, bancos forense-institucionais).
A distinção entre poder discriminatório e sigilo  posta em primeiro plano na Justificativa (Seção 2) e quantificada no Referencial (Seção 4.4)  constitui, portanto, o achado analítico central do trabalho: a projetada margem de ~275 bits do painel completo mede o custo da enumeração, não o sigilo da fonte, e nenhum refinamento do operador de derivação altera essa natureza.
10.2 O que a função de derivação compra — e o que não compra
O benchmark comparativo (Seção 7.4) permite quantificar com franqueza o papel da Argon2id na arquitetura. Sob funções hash de uso geral, o espaço de ~2^21,5 genótipos é enumerado por completo em ~5 segundos proteção nula contra busca exaustiva offline. Sob a Argon2id, a mesma enumeração custa ~9,4 dias no hardware de referência, com multiplicador de ~162.000× no tempo por tentativa e consumo de 64 MiB de memória dedicada por candidatura última característica decisiva, pois neutraliza a vantagem de hardware massivamente paralelo: a RAM dedicada não escala com a generosidade da computação bruta.
A função de derivação, portanto, compra custo: transforma 21,5 bits de entropia em um espaço de busca computacionalmente caro. O que ela não compra é entropia. Nenhuma KDF aumenta a imprevisibilidade da entrada e a distinção, embora elementar para a criptografia, merece ênfase neste contexto biométrico: formulações que sugerem que "passar o DNA por uma função forte" basta para produzir segurança de 256 bits são empiricamente refutadas pelos próprios resultados deste trabalho  chaves estatisticamente perfeitas (Seção 7.3) a partir de fonte com 21,5 bits. A qualidade estatística da saída não é transferível como segurança da chave, pois o adversário ataca o espaço de entrada, não a saída.
Essa leitura alimenta a recomendação central do trabalho: o componente criptográfico da arquitetura (Argon2id) e o componente de entropia (fonte genética + fator adicional) são eixos independentes, e a segurança do sistema é limitada pelo mais fraco em cada eixo. Otimizar apenas um deles  como fizeram as formulações anteriores do modelo com hashes rápidos sobre painel amplo  deixa o sistema vulnerável no outro.
10.3 Ataques de vizinhança genética
Cenário adversarial específico da fonte genética merece análise própria: parentes de primeiro grau compartilham, em média, metade de seus alelos. Um irmão do titular conhece, por consequência, metade do material de derivação  e poderia tentar enumeração apenas sobre a metade desconhecida, reduzindo substancialmente o espaço de busca.
Os resultados da Bateria 3 (Seção 7.3) fornecem a resposta a essa ameaça: a distância de Hamming média de 49,6% (σ = 9,5, n = 60) entre chaves derivadas de entradas que diferem em um único bit demonstra que meia entrada compartilhada não implica correlação aproveitável na saída  chaves de parentes próximos são tão dissimilares quanto chaves de indivíduos arbitrários. O efeito avalanche quebra estruturalmente a vizinhança genética: o atacante-parente não pode fatorar a busca em torno do que conhece, pois a função de derivação não preserva proximidade de entrada em proximidade de saída.
Essa propriedade precisa, contudo, ser lida com precisão: ela impede o ataque por vizinhança  inteligente, localizado mas não reduz o espaço de busca total. O irmão atacante ainda pode enumerar os ~2^21,5 genótipos plausíveis, incluindo os seus próprios e combinações de alelos familiares, pagando o custo integral da busca exaustiva. Em outras palavras, o avalanche converte um ataque inteligente em um ataque burro  mas o ataque burro permanece viável pela limitação de entropia da fonte, o que reforça a recomendação de arquitetura híbrida.
10.4 O modelo híbrido como síntese
Os resultados convergem para a arquitetura em camadas formalizada na Seção 6.5: o perfil genético e um fator secreto adicional, sob independência estatística, somam entropias  o painel didático (~21,5 bits) com uma frase-senha de ~40 bits alcança a faixa de ~60 bits; o painel completo (~275 bits) supera com folga o patamar de 128 bits mesmo com fator modesto.
A síntese das seções anteriores atribui a cada componente seu papel exato: o fator genético aporta o que a senha não tem (vinculação inseparável ao titular, resistência a phishing, impossibilidade de esquecimento); o fator secreto aporta o que o DNA não tem (entropia complementar, revogabilidade); e a Argon2id aporta o que nenhum dos dois tem (custo proibitivo à enumeração de qualquer combinação parcial de conhecimento). Três eixos, três propriedades distintas  e a segurança do conjunto é produto da composição, não de qualquer elemento isolado.
10.5 Posicionamento frente à biometria criptográfica clássica
O pipeline proposto difere das abordagens clássicas em um aspecto estrutural: ele não enfrenta, na etapa de derivação, o problema da variação intraclasse. O Fuzzy Vault (JUELS; SUDAN, 2006) e os fuzzy extractors (DODIS et al., 2008) foram concebidos para biometrias ruidosas — como impressões digitais e íris —, cujas leituras sucessivas podem diferir e exigem mecanismos de correção de erro capazes de recuperar a mesma chave a partir de amostras imperfeitas. O dado STR, após tipagem laboratorial e canonização do genótipo, apresenta comportamento particularmente estável nesse contexto: trata-se de uma representação discreta do genótipo, e não de uma medida fenotípica continuamente variável. Essa estabilidade permite dispensar, no pipeline de derivação, a maquinaria de tolerância a ruído e, com ela, vetores de ataque associados a esses mecanismos, como a análise dos pontos chaff de um vault ou a exploração de informações auxiliares públicas em fuzzy extractors, que podem revelar parcialmente informações sobre o segredo biométrico.
Frente ao BioHashing (TEOH et al., 2004), a distinção é de papel, não de mecanismo: o BioHashing projeta a biometria em um domínio pseudoaleatório parametrizado por um token secreto, perseguindo revogabilidade; o presente trabalho adota um caminho conceitualmente mais simples — a separação entre fonte de identidade (perfil genético) e fator secreto (modelo híbrido) —, alcançando um análogo pragmático de revogabilidade sem recorrer ao domínio projetado, ao custo reconhecido de exigir do titular a guarda de um fator adicional.
Nenhuma dessas famílias de técnicas, note-se, resolve o problema central quantificado neste trabalho: a entropia limitada da fonte de identidade genética. Elas o administram de maneiras distintas, cada qual com seus custos; o presente estudo contribui precisamente ao quantificar, com validação experimental, as implicações de cada escolha arquitetural.
10.6 Síntese da discussão
O conjunto interpreta-se assim: a Fase 1 demonstrou que o pipeline é tecnicamente viável  determinístico, estatisticamente sólido, computacionalmente adequado e com custo de enumeração elevado por construção. Demonstrou igualmente que a viabilidade técnica não se traduz automaticamente em segurança: a fonte genética impõe tetos que nenhum refinamento do operador remove. A resposta arquitetural a essa tensão  o modelo híbrido  não é concessão de fraqueza, mas desenho de engenharia consciente: cada componente contribui com a propriedade que os demais não podem fornecer. Nesse sentido, o trabalho cumpre os objetivos de desenvolver o modelo, validá-lo experimentalmente e, com igual rigor, delimitar honestamente o que ele pode prometer.

11. CONCLUSÃO

Este trabalho investigou a viabilidade de gerar uma Chave Criptográfica Única (CKU) derivada de marcadores genéticos individuais, mediante um pipeline determinístico e integralmente reprodutível que une genética forense e criptografia aplicada, sob a formalização CKU = Argon2id(S‖s). A resposta obtida tem duas faces, ambas sustentadas por evidência experimental.
No plano técnico, a viabilidade foi demonstrada. O pipeline canonização unívoca do genótipo, derivação via Argon2id com parâmetros calibrados (t = 3, m = 64 MiB, p = 1)  produziu chaves estatisticamente indistinguíveis de material aleatório genuíno nas três baterias de validação aplicadas: uniformidade de distribuição de bytes (χ²(255) = 247,88; p = 0,614), equilíbrio posicional de bits (proporção global de 0,5017; 2 de 256 posições fora do intervalo de 99%, contra ~2,6 esperadas por acaso) e efeito avalanche (49,6% de bits alterados; σ = 9,5; n = 60). A propriedade determinística foi verificada por suíte de testes automatizada, incluindo a invariância à ordem de entrada de loci e alelos. O custo computacional de 247 ms por derivação em hardware deliberadamente modesto situa o método em regime compatível com operações interativas, enquanto o benchmark comparativo demonstrou o preço da arquitetura ao atacante: um multiplicador de ~162.000× sobre funções hash de uso geral, elevando a enumeração do espaço de genótipos de ~5 segundos para a ordem de nove dias de computação contínua.
No plano da segurança, contudo, a conclusão exige franqueza. A entropia genética do painel estudado (~21,5 bits de genótipo) situa-se muito aquém dos patamares contemporâneos, e a qualidade estatística da saída não modifica esse quadro, pois o adversário ataca o espaço de entrada, não a saída. O poder discriminatório de um painel genético  mesmo o painel completo projetado, com ~275 bits  quantifica o custo da enumeração, não o sigilo da fonte, e nenhum refinamento do operador de derivação altera essa natureza. Recomenda-se, portanto, para aplicações críticas, o modelo híbrido que combina o perfil genético a um fator secreto adicional, somando entropias independentes e deslocando o ponto crítico de falha para o componente revogável, ao custo reconhecido de exigir do titular a guarda de um fator adicional.
Como extensões futuras, apontam-se quatro direções. Primeira, a expansão do painel para o conjunto completo de marcadores (20 STRs + 130 SNPs + 15 INDELs), com frequências alélicas empíricas de bases públicas de população, elevando a entropia da fonte para a casa dos 275 bits. Segunda, o reporte da min-entropia por locus, medida conservadora mais adequada à análise de enumeração gulosa. Terceira, a execução da bateria completa do NIST SP 800-22 (15 subtestes, mínimo de 10⁶ bits). Quarta, a investigação da CKU Ampliada com marcadores somáticos e epigenéticos, direcionada à discriminação de gêmeos monozigóticos  a fronteira residual da unicidade genética como pressuposto criptográfico.
O trabalho contribui, assim, metodologicamente para a interseção entre a biomedicina forense e a criptografia aplicada, estabelecendo tanto o que a abordagem oferece  um pipeline reprodutível, determinístico e estatisticamente validado, executável em hardware acessível quanto, com igual rigor, aquilo que ela não pode prometer. Nesse equilíbrio entre demonstração e delimitação reside, entende-se, a condição de maturidade científica da proposta: não afirmar mais do que os dados sustentam, nem menos do que os dados comprovam.

REFERÊNCIAS

BIRYUKOV, A.; DINU, D.; KHOVRATOVICH, D. Argon2: the memory-hard function for password hashing and other applications. Luxembourg: University of Luxembourg, 2017. (White paper, Password Hashing Competition).
BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). Diário Oficial da União: seção 1, Brasília, DF, 15 ago. 2018.
BUTLER, J. M. Advanced topics in forensic DNA typing: interpretation. San Diego: Academic Press, 2015.
DODIS, Y.; OSTROVSKY, R.; REYZIN, L.; SMITH, A. Fuzzy extractors: how to generate strong keys from biometrics and other noisy data. SIAM Journal on Computing, v. 38, n. 1, p. 97-139, 2008. DOI: https://doi.org/10.1137/060651380.
INTERNET ENGINEERING TASK FORCE. Argon2 memory-hard function for password hashing and proof-of-work applications: RFC 9106. [S. l.]: IETF, 2021. DOI: https://doi.org/10.17487/RFC9106.
JAIN, Anil K.; FLYNN, Patrick; ROSS, Arun A. (org.). Handbook of biometrics. New York: Springer, 2007.
JEFFREYS, A. J.; WILSON, V.; THEIN, S. L. Individual-specific “fingerprints” of human DNA. Nature, v. 316, p. 76-79, 1985.
JUELS, A.; SUDAN, M. A fuzzy vault scheme. Designs, Codes and Cryptography, v. 38, n. 2, p. 237-257, 2006. DOI: https://doi.org/10.1007/s10623-005-6343-z.
KWON, Y. L. et al. Massively parallel sequencing of 25 autosomal STRs including SE33 in four population groups for forensic applications. Scientific Reports, v. 11, art. 4701, 2021. DOI: https://doi.org/10.1038/s41598-021-82814-z.
NATIONAL LIBRARY OF MEDICINE. Visible proofs: forensic views of the body: the Jeffreys case. Bethesda: National Library of Medicine, 2006. Disponível em: https://www.nlm.nih.gov/exhibition/visibleproofs/galleries/cases/jeffreys.html. Acesso em: 23 out. 2026.
NIST. SP 800-22 Rev. 1a: a statistical test suite for random and pseudorandom number generators for cryptographic applications. Gaithersburg: National Institute of Standards and Technology, 2010.
NIST. FIPS 180-4: Secure Hash Standard (SHS). Gaithersburg: National Institute of Standards and Technology, 2015a.
NIST. FIPS 202: SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions. Gaithersburg: National Institute of Standards and Technology, 2015b.
O’CONNOR, J.; AUMASSON, J.-P.; NEVES, S.; WILCOX-O’HEARN, Z. BLAKE3: one function, fast everywhere. 2020. Disponível em: https://github.com/BLAKE3-team/BLAKE3-specs/blob/master/blake3.pdf. Acesso em: 23 out. 2026.
PROMEGA CORPORATION. PowerPlex® Fusion 6C System: technical manual. Madison: Promega, 2023.
STALLINGS, W. Cryptography and network security: principles and practice. 8. ed. Harlow: Pearson, 2021.
TEOH, A. B. J.; NGO, D. C. L.; GOH, A. Biohashing: two factor authentication featuring fingerprint data and tokenised random number. Pattern Recognition, v. 37, n. 11, p. 2245-2255, 2004. DOI: https://doi.org/10.1016/j.patcog.2004.04.011.

APÊNDICE A — PROTÓTIPO COMPUTACIONAL (CÓDIGO-FONTE  CORRIGIDO)

Introdução de apêndice antes do código:

    Apresenta-se a seguir o código-fonte do protótipo computacional do modelo CKU, na versão corrigida para os fins deste trabalho. O protótipo original, escrito para a formulação com funções hash de uso geral, serviu de banco de provas conceitual das versões anteriores do modelo (fase pré-Argon2id). As correções aplicadas foram três: importação do módulo random (ausente, causando erro de nomeação na primeira execução), validação explícita da função hash recebida pelo construtor (eliminando a aceitação silenciosa de valores inválidos) e recuo dos comandos de saída para o bloco de guarda if __name__ (impedindo execução em importação do módulo).

#!/usr/bin/env python3
"""
Protótipo do modelo CKU (Chave Criptográfica Única).
Versão histórica: formulação com funções hash de uso geral.
A arquitetura de produção do trabalho emprega Argon2id (ver Apêndice A.2).

Correções aplicadas sobre a versão anterior:
  1. import random adicionado (NameError na primeira execução);
  2. validação explícita de funções hash no construtor;
  3. comandos de saída recolhidos ao bloco de guarda.
"""
import hashlib
import random          # Correção 1: import ausente na versão original
import secrets
import statistics
import time
from typing import Any, Dict, List, Tuple

FUNCOES_VALIDAS = ('SHA-256', 'SHA-3', 'BLAKE3')   # Correção 2


def perfil_canonico(perfil: Dict[str, Tuple[str, str]]) -> bytes:
    """Serializa o perfil em representação canônica determinística."""
    partes = []
    for locus in sorted(perfil.keys()):
        alelos = sorted(perfil[locus],
                        key=lambda a: float(a) if a.replace('.', '', 1)
                        .isdigit() else float('inf'))
        partes.append(f"{locus}:{alelos[0]}:{alelos[1]}")
    return '|'.join(partes).encode('utf-8')


class GeradorCKU:
    """Gera CKUs a partir de perfis genéticos e salts."""

    def __init__(self, funcao_hash: str = 'SHA-256') -> None:
        self.funcao_hash = funcao_hash.upper()
        if self.funcao_hash not in FUNCOES_VALIDAS:
            raise ValueError(f'Função hash desconhecida: {funcao_hash}')
        if self.funcao_hash == 'BLAKE3':
            import blake3
            self._blake3 = blake3

    def derivar(self, perfil: Dict[str, Tuple[str, str]],
                salt: bytes) -> bytes:
        """Deriva a CKU de 256 bits: CKU = H(perfil_canônico || salt)."""
        material = perfil_canonico(perfil) + salt
        if self.funcao_hash == 'SHA-256':
            return hashlib.sha256(material).digest()
        if self.funcao_hash == 'SHA-3':
            return hashlib.sha3_256(material).digest()
        return self._blake3.blake3(material).digest()


def gerar_genotipo_simulado(id_individuo: int,
                            painel: Dict[str, List[str]]
                            ) -> Dict[str, Tuple[str, str]]:
    """Gera genótipo sintético com RNG determinístico por indivíduo."""
    rng = random.Random(id_individuo)
    return {locus: tuple(sorted(rng.sample(alelos, 2)))
            for locus, alelos in painel.items()}


def main() -> None:
    painel = {
        'D18S51': ['12', '13', '14', '15', '16', '17'],
        'D21S11': ['28', '29', '30', '31', '31.2', '32'],
        'D3S1358': ['14', '15', '16', '17', '18'],
        'D5S818': ['10', '11', '12', '13'],
        'TH01': ['6', '7', '8', '9', '9.3'],
    }
    gerador = GeradorCKU('SHA-256')
    tempos: List[float] = []

    for i in range(100):
        perfil = gerar_genotipo_simulado(i, painel)
        salt = secrets.token_bytes(16)
        t0 = time.perf_counter()
        chave = gerador.derivar(perfil, salt)
        tempos.append(time.perf_counter() - t0)
        assert len(chave) == 32

    print(f'Chaves geradas: 100')
    print(f'Tempo médio por hash: {statistics.fmean(tempos)*1e6:.1f} µs')
    print(f'Amplitude: {(max(tempos)-min(tempos))*1e6:.1f} µs')
    print('PROCESSAMENTO COMPLETO')


if __name__ == '__main__':
    main()          # Correção 3: execução sob guarda

    Nota histórica: este protótipo integra a função de derivação com geração de perfis e cronometragem. O benchmark comparativo definitivo entre este modelo e a arquitetura Argon2id — que motivou a substituição formalizada na Seção 6 — encontra-se em scripts/benchmark_hashes.py e nos resultados reportados na Seção 7.4.

APÊNDICE B — DIAGRAMA DO PIPELINE (MERMAID)

Introdução:

    O diagrama abaixo representa o fluxo do pipeline de derivação da CKU na arquitetura consolidada deste trabalho, conforme implementado e validado experimentalmente (Fases 1 e 2).

flowchart LR
    A[Amostra de DNA] --> B[Extração e tipagem<br/>STRs · SNPs · INDELs]
    B --> C[Seleção de marcadores<br/>20 STR + 130 SNP + 15 INDEL]
    C --> D[Codificação binária canônica<br/>6+6 bits / 2 bits / 1 bit]
    D --> E[Sequência S<br/>515 bits]
    E --> F[Adição de salt<br/>S′ = S ‖ s]
    F --> G[Derivação Argon2id<br/>t=3 · m=64 MiB · p=1]
    G --> H[CKU<br/>256 bits · 64 hex]



E uma versão conceitual da arquitetura híbrida — vale como Figura de fechamento :
flowchart LR
    P[Perfil genético<br/>irrevogável · vinculante] --> D[Argon2id<br/>S ‖ s ‖ f]
    F[Fator secreto f<br/>revogável · portador de entropia] --> D
    S[Salt s<br/>CSPRNG · único por derivação] --> D
    D --> K[CKU híbrida<br/>256 bits]

APÊNDICE C — COMANDOS DE REPRODUÇÃO

Pequeno e valioso — ensina a reproduzir tudo 

    A reprodução integral dos resultados requer apenas Python 3.12 e o ambiente declarado:
    git clone https://github.com/botelhojrv-dev/tcc-genetica-cripto
    cd tcc-genetica-cripto
    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    make test                    # suíte: 18 casos (inclui determinismo)
    python scripts/benchmark_hashes.py   # Tabela 7.3



