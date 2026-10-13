# Resumo Executivo — TCC Genética Forense + Criptografia

## Versão curta (1 parágrafo)

Esta pesquisa investiga a viabilidade de transformar perfis genéticos STR forenses
em chaves criptográficas utilizáveis. Demonstramos que 5 loci diplóides fornecem
~22 bits de entropia — insuficientes para padrões modernos (AES-256 exige 256 bits),
mas viáveis quando combinados com função de derivação memory-hard (Argon2id). O
pipeline proposto inclui canonização determinística do perfil (~61 bytes UTF-8),
derivação via Argon2id (247 ms por chave, 64 MiB de memória), e validação estatística
rigorosa. Resultados confirmam comportamento de aleatoriedade ideal (χ²(255)=247,88;
p=0,614; proporção de bits=0,5017; avalanche=49,6%). Reconhecemos explicitamente que a
entropia genética isolada não atinge segurança moderna, recomendando fator secreto
adicional em aplicações críticas.

## Versão expandida (2 parágrafos)

Os marcadores STR forenses, amplamente utilizados para identificação humana em
investigação criminal e testes de paternidade, possuem propriedades que despertam
interesse para aplicações criptográficas: unicidade individual, estabilidade ao longo
da vida, e disponibilidade em bancos de dados genéticos. Contudo, sua entropia
intrínseca (~22 bits por perfil com 5 loci) é ordens de magnitude inferior à exigida
por protocolos criptográficos contemporâneos (≥128–256 bits). Esta tese investiga se
funções de derivação de chave (KDFs) memory-hard podem "estender" o custo de ataques
de força bruta, compensando parcialmente a lacuna de entropia.

Desenvolvemos um pipeline completo de transformação de perfil STR em chave AES-256
pronta, implementando serialização determinística do genótipo, derivação via Argon2id
(vencedora da Password Hashing Competition, 2015), e validação estatística abrangente.
Experimentos com 5.000 perfis sintéticos regenerados reproduzivelmente revelaram:
(1) uniformidade de distribuição dos bytes derivados (χ²(255)=247,88, p=0,614); (2)
equilíbrio de bits globais (0,5017) e ausência de viés posicional; (3) avalanche effect
ideal (49,6% dos bits alterados por mudança de um bit na entrada). O tempo médio de
derivação foi 247 ms no hardware local (desktop modesto), com consumo de 64 MiB por
tentativa — custos que inviabilizam paralelização massiva em GPUs/ASICs. Concluímos
que a abordagem é tecnicamente viável, mas recomenda-se fator secreto adicional
(senha/salt privado) para aplicações que demandem >128 bits de segurança.

## Tópicos-chave (bullet points)

- **Problema**: 5 loci STR fornecem ~22 bits de entropia vs. 256 bits exigidos por AES-256
- **Solução proposta**: canonização determinística + Argon2id memory-hard KDF
- **Viabilidade técnica confirmada**: 400 chaves derivadas passam em todos os testes estatísticos
- **Performance**: 247 ms/chave, 64 MiB de memória (hardware modesto)
- **Limitação reconhecida**: entropia insuficiente para segurança >128 bits sem fator adicional
- **Contribuição original**: pipeline reproducible, código testado (15/15 testes), figura dupla de validação
- **Aplicabilidade**: autenticação biométrica híbrida, vinculação legal de documentos, gestão de identidade