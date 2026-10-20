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

- José Ricardo Vega Botelho¹
¹ Universidade Cidade de São Paulo (UNICID)
   Curso de Biomedicina — São Paulo, SP, Brasil
   Correspondência: josericardo@botelho.id

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

## 2. METODOLOGIA

### 2.1 Desenho geral do estudo

O estudo possui caráter experimental e computacional, estruturado em três
etapas sequenciais: (i) quantificação da entropia disponível em um painel
de loci STR; (ii) especificação e implementação de um pipeline
determinístico de derivação de chaves criptográficas a partir de perfis
genotípicos; e (iii) validação estatística das chaves produzidas. Toda a
implementação foi desenvolvida em Python 3.12, com suíte de testes
automatizados (15 casos) e controle de versão, e encontra-se integralmente
disponível em repositório público (https://github.com/botelhojrv-dev/
tcc-genetica-cripto), assegurando reprodutibilidade integral dos
resultados.

### 2.2 Geração de perfis sintéticos

Foram utilizados perfis genotípicos sintéticos, simulados segundo
frequências alélicas plausíveis para populações humanas, sob equilíbrio
de Hardy-Weinberg. O painel compreendeu cinco loci STR diplóides
(D18S51, D21S11, D3S1358, D5S818 e TH01), representativos dos marcadores
de identificação humana utilizados em genética forense. A geração
aleatória foi ancorada em semente fixa (seed=2024), garantindo que todos
os experimentos sejam replicados de forma idêntica.

A opção por dados sintéticos atende a dois requisitos: ético — a Lei Geral
de Proteção de Dados (BRASIL, 2018) classifica dados genéticos como dados
pessoais sensíveis (Art. 5º, inciso II), impondo restrições ao uso de
perfis reais — e metodológico, ao eliminar variabilidade de coleta e
permitir controle total dos parâmetros populacionais.

### 2.3 Quantificação de entropia

A entropia de Shannon foi calculada por locus com base nas frequências
genotípicas esperadas, conforme:

H = − Σ p(i) · log₂ p(i)

em que p(i) denota a probabilidade do genótipo i no locus considerado. A
entropia do perfil completo foi estimada pela soma das contribuições dos
cinco loci, sob a hipótese de independência entre loci (pressuposição
padrão em cálculos forenses de perfil combinado). Foram reportadas ainda
a entropia máxima teórica de cada locus e a razão entre entropia
observada e máxima (eficiência do locus como fonte de imprevisibilidade).

### 2.4 Pipeline de derivação de chaves

O pipeline de transformação do perfil genotípico em chave criptográfica
compreendeu três estágios:

**(i) Canonização do perfil.** O genótipo diplóide de cada locus foi
serializado em representação canônica unívoca (alelos ordenados por valor
numérico), concatenada em ordem fixa de loci, produzindo cadeia UTF-8
determinística de aproximadamente 61 bytes. A canonização garante que
genótipos equivalentes (mesmos alelos, ordem arbitrária) convergem para
entrada idêntica na função de derivação.

**(ii) Sal.** Foi acrescido salt aleatório de 16 bytes (128 bits), gerado
por CSPRNG, anexado ao material derivado, prevenindo ataques com tabelas
pré-computadas (rainbow tables) e permitindo derivação de chaves
independentes a partir do mesmo perfil.

**(iii) Função de derivação.** A derivação foi realizada com Argon2id
(BIRYUKOV; DINU; KHOVRATOVICH, 2016), vencedora da Password Hashing
Competition, na configuração t=3 (três iterações), m=64 MiB de memória
e p=1 (paralelismo), produzindo chave de 32 bytes apta ao uso com
AES-256. A Argon2id foi escolhida por combinar resistência a ataques
massivamente paralelos em GPU/ASIC (custo de memória) com desempenho
adequado em hardware de baixo custo.

### 2.5 Critérios de validação estatística

Foram derivadas 400 chaves independentes (variando-se perfil e salt),
submetidas a três baterias de testes, inspiradas nos procedimentos do
NIST SP 800-22 (NIST, 2010):

1. **Uniformidade de distribuição de bytes** — teste qui-quadrado de
   aderência sobre os 12.800 bytes agregados (400 chaves × 256 bytes),
   com 255 graus de liberdade, avaliando a hipótese nula de distribuição
   uniforme;

2. **Equilíbrio posicional de bits** — proporção global de bits 1 e
   razão bit a bit nas 256 posições, com intervalos de confiança de 99%
   sob hipótese binomial (p=0,5);

3. **Efeito avalanche** — distância de Hamming entre chaves derivadas de
   entradas que diferem em um único bit (n=60 pares), com critério de
   aprovação centrado em 50% de bits alterados (128/256 ± tolerância,
   avaliada pela média de 5 medições para reduzir variância).

Adicionalmente, foram medidas as distâncias de Hamming entre chaves de
perfis distintos e entre chaves do mesmo perfil com salts distintos,
para caracterizar a dissimilaridade produzida pela derivação.

### 2.6 Desempenho computacional

O tempo de derivação foi cronometrado em séries de execuções, reportando-
se média e desvio-padrão. Os experimentos foram conduzidos em estação de
trabalho convencional (AMD FX-8370E, 8 núcleos, arquitetura Piledriver,
3,3 GHz; 8 GiB de RAM; armazenamento SSD SATA; sistema operacional GNU/
Linux Mint 22.3, kernel 6.14; Python 3.12), deliberadamente representativa
de hardware de baixo custo, datável de meados da década de 2010 — premissa
metodológica conservadora: custos medidos em hardware modesto constituem
limite inferior do custo imposto a eventuais atacantes.
Sob essa premissa, os tempos reportados configuram limite superior da latência legítima do método, ao passo que o custo computacional imposto a potenciais atacantes deve ser interpretado como limite inferior, dado que infraestruturas contemporâneas reduziriam ambos.

---

## 3. RESULTADOS — MATERIAL EXISTENTE, SÓ ORGANIZAR

### 3.1 Entropia de Fonte Genética 

A Tabela 2 apresenta a entropia de Shannon observada por locus do painel STR simulado, a entropia máxima teórica (distribuição uniforme sobre os alelos do locus) e a razão entre ambas, definida como a eficiência do locus como fonte de imprevisibilidade.

Tabela 2 — Entropia de Shannon por locus do painel STR simulado (N = 5.000 indivíduos, seed = 2024).
Locus	Nº de alelos	H obs (bits)	H máx (bits)	Eficiência
D18S51	5	2,2320	2,3219	0,9613
D21S11	5	2,2770	2,3219	0,9806
D3S1358	5	2,2496	2,3219	0,9688
D5S818	4	1,7615	2,0000	0,8807
TH01	5	2,2325	2,3219	0,9615
Perfil (soma)	—	10,75	11,27	0,954

Fonte: dados do notebook 01, elaborado pelo autor.

A Figura 1 ilustra o comportamento dos cinco loci. Os quatro loci de cinco alelos operaram com eficiência superior a 96%, refletindo frequências alélicas relativamente equilibradas no painel simulado. O locus D5S818 apresentou a menor eficiência (88,1%), consequência da dominância dos alelos 11 e 12, que juntos concentram 74% da frequência paramétrica — característica que o torna o candidato natural à exclusão em eventuais versões otimizadas do painel.

A entropia alélica agregada do painel é de 10,75 bits por conjunto haploide. Sob o modelo diplóide de Hardy-Weinberg, com loci independentes, a entropia do genótipo completo aproxima-se de 21,5 bits — valor coerente com a estimativa teórica de ~22 bits que fundamenta a discussão de segurança deste trabalho (Seção 4). Convém distinguir, contudo, duas medidas distintas: a entropia do perfil como segredo (imprevisibilidade do genótipo face à população, ~21,5 bits) e a entropia interna média dos símbolos de cada perfil individual (2,95 bits, observada no painel B da Figura 1), que quantifica a diversidade alélica dentro do indivíduo e não guarda relação com a resistência criptográfica da fonte.

Os valores obtidos confirmam o diagnóstico quantitativo antecipado na Introdução: ainda que o painel STR identifique um indivíduo com elevada especificidade, a entropia disponível para derivação de chaves (~21,5 bits de genótipo) situa-se uma ordem de grandeza aquém dos 256 bits exigidos pelo AES-256 — lacuna que motiva a adoção da função de derivação memory-hard (Seção 2.4) e o modelo híbrido recomendado na Discussão (Seção 4).

### 3.2 Derivação e performance

O pipeline descrito na Seção 2.4 foi executado sobre os perfis sintéticos regenerados com a mesma semente do experimento de entropia (seed = 2024, Seção 2.2), com cronometragem de 100 derivações em série. A Tabela 3 resume as métricas de desempenho observadas.

Tabela 3 — Desempenho do pipeline de derivação Argon2id (n = 100 derivações; hardware descrito na Seção 2.6).
Métrica	Valor
Tempo médio por derivação	247 ms
Intervalo observado	232 – 282 ms
Consumo de memória por derivação	64 MiB
Nº de derivações cronometradas	100

Fonte: dados do notebook 02, elaborado pelo autor.

O tempo médio de 247 ms por derivação situa o método em faixa compatível com operações interativas isoladas (autenticação de usuário único, desbloqueio de cofre local) — embora inviabilize, por construção, o processamento massivo. Esse comportamento não é defeito, mas desenho: o custo de memória de 64 MiB por chamada é precisamente o mecanismo pelo qual a Argon2id eleva o preço de ataques de enumeração. Estimando o espaço de genótipos plausíveis em ~2^21,5 (Seção 3.1), um atacante que optasse por busca exaustiva serial gastaria da ordem de 11–12 dias de computação contínua no mesmo hardware — sem considerar o custo de aquisição prévia dos dados genéticos.

Para caracterizar a dissimilaridade produzida pela derivação, foram medidas as distâncias de Hamming em nível de bit entre chaves em três cenários distintos (Tabela 4). Dois deles avaliam o efeito avalanche — difusão entre entradas distintas — e o terceiro valida a propriedade determinística do pipeline.

Tabela 4 — Distância de Hamming entre chaves derivadas, por cenário (256 bits por chave).
Cenário	Bits diferentes	% de alteração	Esperado
Perfis distintos, mesmo salt	119/256	46,5%	~128 (50%)
Mesmo perfil, salts distintos	130/256	50,8%	~128 (50%)
Mesmo perfil, mesmo salt	0/256	0%	0 exato

Fonte: dados dos notebooks 02 e da suíte de testes (tests/test_determinismo.py, 4 casos aprovados), elaborado pelo autor.

Os dois primeiros cenários demonstram comportamento preliminar de avalanche: alterações na entrada — no genótipo ou no salt — propagam-se para cerca de metade dos bits de saída. Cabe registrar que essas medidas do notebook 02 são observações pontuais (um par por cenário, para caracterização qualitativa do operador), enquanto a avaliação estatística formal do efeito avalanche — 60 pares, com média e desvio-padrão — é reportada na Seção 3.3. O terceiro cenário confirma a propriedade determinística: derivações repetidas da mesma entrada canônica e mesmo salt convergem para chaves bit a bit idênticas, verificada por suíte dedicada que inclui dez execuções consecutivas e a invariância à ordem de inserção de loci e alelos — propriedade garantida pela canonização descrita na Seção 2.4.

Em conjunto, as três medidas caracterizam o operador de derivação de forma completa: ele separa maximamente entradas distintas, preserva exatamente entradas idênticas e impõe custo computacional substancial a cada chamada — as propriedades conjuntas exigidas de um pipeline reprodutível apto à derivação de chaves.

### 3.3 Validação Estatística das Chaves
Para avaliar se as chaves derivadas atendem aos critérios estatísticos de material criptográfico legítimo, foram geradas 400 chaves independentes (variando-se perfil e salt), compondo 12.800 bytes agregados, submetidos às três baterias de testes especificadas na Seção 2.5, sob nível de significância α = 0,05, conforme recomendação do NIST SP 800-22. A Figura 2 sintetiza os resultados.

Bateria 1 — Uniformidade de distribuição de bytes. O teste qui-quadrado de aderência sobre os 12.800 bytes agregados (frequência esperada de 50 ocorrências por valor, 255 graus de liberdade) resultou em χ²(255) = 247,88, p = 0,614. A hipótese nula de distribuição uniforme não foi rejeitada: o valor de p situa-se muito acima do limiar de significância, indicando que a frequência observada dos 256 valores de byte (faixa de 32 a 71 ocorrências) não desvia da expectativa uniforme de forma estatisticamente detectável. O estatístico ligeiramente inferior aos graus de liberdade (247,88 < 255) denota dispersão marginalmente menor que a esperada sob aleatoriedade perfeita — comportamento plenamente compatível com flutuação amostral, não indício de estrutura nos dados.

Bateria 2 — Equilíbrio posicional de bits. A proporção global de bits 1 nos 102.400 bits agregados foi de 0,5017 — dentro do intervalo de confiança de 99% sob hipótese binomial (p = 0,5). Na avaliação posicional, com intervalos individuais de 99% para cada uma das 256 posições de bit (0,436 – 0,564 para n = 400 observações por posição), verificou-se que 2 posições situaram-se fora do intervalo — resultado consistente com a expectativa estatística de ~2,6 posições fora do intervalo por puro acaso. A bateria foi, portanto, aprovada, sem indício de viés posicional detectável por um adversário.

Bateria 3 — Efeito avalanche. As distâncias de Hamming entre chaves derivadas de pares de entrada diferindo em um único bit (inversão do bit menos significativo da representação canônica, mesmo salt) foram medidas em n = 60 pares, resultando em média de 127,1 bits alterados de 256 (49,6%), σ = 9,5 bits, faixa observada de 101 a 146. A média situa-se dentro do critério de aprovação centrado em 50% (128/256 ± tolerância), e o desvio-padrão observado é compatível com o valor teórico sob difusão ideal (σ ≈ 8 bits), conferindo estabilidade à medida. Esses resultados quantificam estatisticamente o comportamento preliminarmente caracterizado na Tabela 4 (Seção 3.2), fechando o ciclo entre observação pontual e validação amostral.

Em síntese, as três baterias foram integralmente aprovadas: as chaves derivadas são estatisticamente indistinguíveis de material aleatório genuíno nas dimensões testadas. Importa sublinhar, contudo, o alcance exato dessa conclusão — as baterias certificam a qualidade estatística da saída do pipeline (uniformidade, equilíbrio e difusão), e não a entropia da fonte genética, que permanece limitada a ~21,5 bits conforme quantificado na Seção 3.1. A distinção é central para a discussão de segurança desenvolvida na Seção 4: a Argon2id produz chaves com excelentes propriedades estatísticas a partir de entrada de entropia restrita, propriedades que não substituem, mas complementam, a análise de custo de ataques de enumeração.


---

## 4. DISCUSSÃO 

### 4.1 O gap de entropia: 22 bits diante de 256

O resultado mais importante deste trabalho é também o mais desconfortável: a entropia genética disponível no painel STR estudado — aproximadamente 21,5 bits de genótipo (Seção 3.1) — corresponde a cerca de um sexto do patamar mínimo contemporâneo (128 bits) e a menos de um décimo dos 256 bits exigidos pela chave-alvo (AES-256). Traduzida ao espaço de busca, a diferença é dramática: um adversário enfrenta 2^106 vezes menos candidatos que os pressupostos pelo padrão mínimo, e 2^234 vezes menos que os do AES-256.  Essa lacuna não é defeito metodológico do presente estudo, mas característica intrínseca da fonte: a imprevisibilidade de um genótipo é limitada pelas frequências alélicas populacionais, que são públicas e amplamente documentadas (Seção 2.3). Um perfil STR identifica um indivíduo com especificidade extraordinária — bilhões para um — mas identificar não é o mesmo que ser imprevisível: a especificidade advém da baixa probabilidade de coincidência entre dois perfis sorteados, enquanto a imprevisibilidade criptográfica exige a alta entropia do segredo face ao adversário. O adversário forense conhece as distribuições; sabe enumerar genótipos por ordem decrescente de probabilidade; e dispõe, em cenários plausíveis, de informação genética parcial do alvo (parentes próximos, bancos forense-institucionais).

### 4.2 O que a Argon2id compra — e o que não compra

Os resultados da Seção 3.2 permitem quantificar com franqueza o papel da função de derivação. Com tempo médio de 247 ms por derivação no hardware de referência, a busca exaustiva serial sobre o espaço de ~2^21,5 genótipos custa da ordem de 11–12 dias de computação contínua — estimativa que constitui, conforme argumentado na Seção 2.6, um limite inferior do custo real imposto a atacantes com hardware superior. A Argon2id, portanto, compra tempo: eleva o custo por tentativa em três a quatro ordens de grandeza frente a uma derivação leve (SHA-256 pura, por exemplo, processaria o mesmo espaço em segundos). O mecanismo memory-hard é essencial nessa conta, pois neutraliza a vantagem de hardware massivamente paralelo (GPU/ASIC), mantendo o custo do ataque aproximadamente linear em memória — recurso que não segue a lei de Moore com a mesma generosidade que a computação.

O que a função de derivação não compra é entropia. Nenhuma KDF, por construção ou sofisticação, aumenta a imprevisibilidade da entrada: o que ela faz é dilatar o custo de cada enumeração, transformando 21,5 bits de entropia em um espaço de busca computacionalmente caro, mas ainda finito e conhecido. A distinção, embora elementar para a criptografia, merece ênfase neste contexto biométrico: a literatura de aplicações leigas por vezes sugere que "passar o DNA por uma função forte" basta para produzir segurança de 256 bits — os resultados aqui apresentados (chaves estatisticamente perfeitas, fonte com 21,5 bits) demonstram precisamente o contrário: a qualidade estatística da saída (Seção 3.3) não é transferível como segurança da chave, pois o adversário ataca o espaço de entrada, não a saída.

### 4.3 Ataques de vizinhança genética: o que o avalanche mitiga


Cenário adversarial específico da fonte genética: parentes de primeiro grau compartilham, em média, 50% de seus alelos. Um irmão do titular da chave conhece, por consequência, metade do material de derivação — e poderia tentar enumeração apenas sobre a metade desconhecida, reduzindo o espaço de busca em fator exponencial (~2^11). Os resultados da Bateria 3 (Seção 3.3) fornecem a resposta a essa ameaça: a distância de Hamming média de 49,6% (σ = 9,5, n = 60) entre chaves derivadas de entradas que diferem em um único bit demonstra que meia entrada compartilhada não implica nenhuma correlação aproveitável na saída — chaves de parentes próximos são tão dissimilares quanto chaves de indivíduos arbitrários. O efeito avalanche, portanto, quebra estruturalmente a vizinhança genética: o atacante-parente não pode fatorar a busca em torno do que conhece, pois a função de derivação não preserva proximidade de entrada em proximidade de saída.

Essa propriedade, contudo, precisa ser lida com precisão: ela impede o ataque por vizinhança, mas não reduz o espaço de busca total — o irmão atacante ainda pode enumerar os ~2^21,5 genótipos plausíveis (incluindo os seus próprios, os de outros parentes, e combinações de alelos familiares), pagando o custo integral da busca exaustiva. Em outras palavras, o avalanche transforma um ataque inteligente (localizado na vizinhança) num ataque burro (global), mas este último continua viável pela limitação de entropia da fonte — argumento que reforça a recomendação de modelo híbrido desenvolvida a seguir.


### 4.4 Recomendação de modelo híbrido


Os resultados das seções anteriores convergem para uma arquitetura de segurança em camadas, que denominamos modelo híbrido: a chave final de 256 bits derivada como XOR (ou concatenação seguida de segunda derivação) de duas fontes independentes — o perfil STR e um fator secreto adicional detido pelo usuário (frase-senha, chave de hardware, segredo memorizado). A composição preserva as virtudes de cada componente: o perfil genético oferece um fator que não pode ser esquecido nem obtido por phishing (está, literalmente, no corpo do titular), enquanto o fator secreto adicional aporta a entropia que a fonte genética não pode fornecer. Sob o pressuposto de independência estatística entre os fatores, a entropia efetiva do modelo híbrido aproxima-se da soma das contribuições — uma frase-senha modesta de 40 bits, combinada ao painel de ~21,5 bits, eleva a segurança conjunta para para a faixa de 60 bits, já proibitivos para ataques de enumeração offline realizáveis com hardware convencional, mesmo com o custo por tentativa ampliado pela Argon2id.

O modelo híbrido resolve, adicionalmente, o dilema da irrevogabilidade biométrica: comprometido o fator secreto, ele pode ser substituído sem que o perfil genético precise ser abandonado como material de derivação. Em termos de modelo de ameaça, a arquitetura desloca o ponto crítico de falha do segredo genético (que não se troca) para o segredo auxiliar (que se troca) — inversão que prescinde de qualquer novidade técnica, mas cuja viabilidade só se sustenta porque o pipeline-base demonstrou ser determinístico, estatisticamente sólido e computacionalmente adequado (Seções 3.2 e 3.3).


### 4.5 Posicionamento frente a Fuzzy Vault, BioHashing e secure sketches


O pipeline proposto difere das abordagens clássicas de biometria criptográfica em um aspecto estrutural: ele não enfrenta o problema da variação intra-classe. O Fuzzy Vault (Juels; Sudan, 2006) e os fuzzy extractors (Dodis et al., 2008) foram concebidos para biometrias ruidosas — impressões digitais e íris cujas leituras sucessivas diferem, exigindo mecanismos de correção de erro (Chaffing, secure sketches, códigos de Gray) capazes de recuperar a mesma chave a partir de amostras imperfeitas. O dado STR, nesse contexto, é excepcionalmente bem-comportado: a tipagem laboratorial de um mesmo indivíduo reproduz o genótipo com exatidão determinística (trata-se de leitura de genótipo, não de fenótipo variável), o que eliminou do presente pipeline toda a maquinaria de tolerância — e, com ela, os vetores de ataque típicos desses mecanismos, como a análise dos pontos chaff de um vault ou a exploração da informação auxiliar pública dos fuzzy extractors, que pode vazar parcialmente o segredo biométrico.

Já frente ao BioHashing (Teoh et al., 2004), a distinção é de papel, não de mecanismo : o BioHashing projeta a biometria sobre um domínio pseudo-aleatório parametrizado por um token secreto, perseguindo revocabilidade; o presente trabalho adota caminho conceitualmente mais simples — a separação entre fonte pública de identidade (perfil) e fator secreto (modelo híbrido) — alcançando análogo pragmático de revocabilidade sem a sofisticação do domínio projetado, ao custo reconhecido de exigir do usuário a guarda de um fator adicional. Nenhuma dessas famílias de técnicas, note-se, resolve o problema central quantificado neste trabalho: a entropia limitada da fonte biométrica — elas o administram de maneiras distintas, cada qual com seu custo.

### 4.6 Limitações


Os resultados devem ser lidos sob seis limitações explícitas. Primeira, o tamanho do painel: cinco loci Diplóides fornecem ~21,5 bits; painéis forenses contemporâneos de 20 a 24 loci (GlobalFiler, PowerPlex Fusion) elevariam a entropia para a casa de 100 bits — crescimento expressivo, mas ainda inferior aos 128 bits do padrão mínimo. Segunda, o espaço amostral da validação: 400 chaves e 12.800 bytes aprovam as três baterias aplicadas, mas a bateria completa do NIST SP 800-22 (15 subtestes) requer no mínimo 10⁶ bits, permanecendo como trabalho futuro. Terceira, as medidas de dissimilaridade pontuais: as distâncias de Hamming da Tabela 4 (perfis distintos, salts distintos) baseiam-se em observação de par único, embora o efeito avalanche tenha sido confirmado estatisticamente com n = 60 (Seção 3.3); a re-execução sistemática desses cenários ampliaria a robustez do reporte. Quarta, a simulação populacional: as frequências alélicas do painel são plausíveis, não empíricas; resultados com dados de população real (NIST STRBase, bases brasileiras) podem diferir quantitativamente, embora o argumento estrutural — gap frente a 256 bits — seja insensível a essa troca. Quinta, a ausência de min-entropia reportada: a entropia de Shannon superestima a resistência à enumeração gulosa; a min-entropia por locus (−log₂ max pᵢ) constituiria limite inferior mais conservador e deverá integrar versões futuras. Sexta, o cenário de laboratório: a viabilidade operacional pressupõe tipagem genômica confiável disponível no fluxo de autenticação, contingência tecnológica e regulatória fora do escopo deste estudo.


---

## 5. CONCLUSÃO

Este trabalho investigou a viabilidade de derivar chaves criptográficas AES-256 a partir de perfis STR forenses, mediante um pipeline determinístico e integralmente reprodutível. A resposta obtida tem duas faces, ambas sustentadas por evidência experimental.

No plano técnico, a viabilidade foi demonstrada. O pipeline — canonização unívoca do genótipo, derivação via Argon2id com parâmetros calibrados (t=3, m=64 MiB, p=1) — produziu chaves estatisticamente indistinguíveis de material aleatório genuíno nas três baterias de validação aplicadas: uniformidade de distribuição de bytes (χ²(255) = 247,88; p = 0,614), equilíbrio posicional de bits (proporção global de 0,5017; 2/256 posições fora do intervalo de 99%, contra ~2,6 esperadas por acaso) e efeito avalanche (49,6% de bits alterados; σ = 9,5; n = 60). A propriedade determinística foi verificada por suíte de testes automatizada, incluindo a invariância à ordem de entrada de loci e alelos. O custo computacional de 247 ms por derivação em hardware modesto situa o método em regime compatível com operações interativas, simultaneamente impondo custo substancial à enumeração por atacantes (~11–12 dias para o espaço completo de genótipos, em limite inferior conservador).

No plano da segurança, contudo, a conclusão exige franqueza: a entropia genética do painel estudado (~21,5 bits de genótipo) não alcança os patamares contemporâneos — 128 bits no mínimo — nem a qualidade estatística da saída modifica esse quadro, pois o adversário ataca o espaço de entrada, não a saída. Recomenda-se, portanto, para aplicações críticas, o modelo híbrido que combina o perfil genético a um fator secreto adicional, somando entropias independentes e preservando a irrevogabilidade do componente biométrico como fator de vinculação do titular.

Como extensões futuras, apontam-se quatro direções: a ampliação do painel para os 20–24 loci dos kits comerciais contemporâneos, elevando a entropia para a casa de 100 bits; a incorporação de SNPs como fonte complementar; a execução da bateria completa do NIST SP 800-22 (15 subtestes, ≥10⁶ bits); e o reporte da min-entropia por locus, medida conservadora mais adequada à análise de enumeração gulosa. O trabalho contribui, assim, metodologicamente para a intersecção entre genética forense e criptografia aplicada, estabelecendo tanto o que a abordagem oferece quanto — com igual rigor — aquilo que ela não pode prometer.
Abstract (~200 palavras)

Dados biométricos são identificadores naturais, mas segredos pobres: conhecidos pelas frequências populacionais, não podem alimentar diretamente a criptografia moderna. Este trabalho investiga a derivação de chaves AES-256 a partir de perfis STR forenses, mediante pipeline determinístico de canonização e função de derivação memory-hard Argon2id (t=3, m=64 MiB, p=1), implementado como software livre e integralmente reprodutível. Foram quantificadas a entropia do painel de cinco loci diplóides simulados (10,75 bits por conjunto haploide; ~21,5 bits de genótipo) e submetidas à validação estatística 400 chaves derivadas. As três baterias foram integralmente aprovadas: uniformidade qui-quadrado de bytes (χ²(255) = 247,88; p = 0,614), equilíbrio posicional de bits (proporção global 0,5017; 2/256 posições fora do intervalo de 99%) e efeito avalanche (49,6% ± 9,5 bits; n = 60). O custo médio de derivação foi de 247 ms em hardware modesto. Os resultados demonstram viabilidade técnica do pipeline, com dissipação ideal de vizinhanças genéticas; a entropia da fonte (~21,5 bits), contudo, situa-se muito aquém dos padrões de segurança, motivando modelo híbrido com fator secreto adicional para aplicações críticas.

Palavras-chave: genética forense; criptografia; STR; Argon2id; KDF; validação estatística; reprodutibilidade.

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
