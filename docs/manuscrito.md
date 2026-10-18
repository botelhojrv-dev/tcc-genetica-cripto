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
Sob essa premissa, os tempos reportados configuram limite superior da latência legítima do método, ao passo que o custo computacional imposto a potenciais atacantes deve ser interpretado como limite inferior, dado que infraestruturas contemporâneas reduziriam ambos."

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
3.2 Derivação e Performance

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
