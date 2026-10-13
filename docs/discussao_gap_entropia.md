# Discussão: O Gap de Entropia entre Perfis STR e Chaves Criptográficas

## 1. O Problema Central

Os marcadores STR forenses, embora eficazes para identificação humana individual,
apresentam entropia insuficiente para geração direta de chaves criptográficas modernas.
Nossa análise revelou entropia agregada de ~10,75 bits por alelo ou ~22 bits por perfil
completo (5 loci diplóides). Para fins comparativos, o padrão AES-256 exige 256 bits de
imprevisibilidade na fonte, e mesmo AES-128 requer ≥128 bits — uma lacuna de 6 a 12 vezes
superior à disponibilidade genética.

## 2. Mitigação via Funções Memory-Hard (Argon2id)

A função de derivação Argon2id (vencedora da Password Hashing Competition, 2015) não
*cria* entropia — ela amplifica o **custo computacional** de exploração do espaço de
chaves. Com parâmetros calibrados (t=3, m=64 MiB, p=1), cada tentativa de ataque de força
bruta custa ~247 ms no hardware local e demanda 64 MiB de memória dedicada.

**Implicação prática:** explorar exhaustivamente o espaço de ~4 milhões de perfis
genéticos possíveis (~22 bits) levaria ~11–12 dias de CPU serial em hardware modesto.
O consumo de memória por tentativa inviabiliza paralelização massiva em GPUs/ASICs,
que tipicamente compartilham recursos limitados entre milhares de núcleos.

## 3. Limitações da Abordagem Atual

Apesar da mitigação, duas vulnerabilidades permanecem:

**3.1. Espaço reduzido de candidatos.** O conhecimento público das frequências
populacionais permite ao atacante enumerar apenas os genótipos plausíveis, em vez
de testar o espaço completo de 2²⁵⁶ combinações. Embora o Argon2id torne cada
tentativa custosa, um adversário com recursos dedicados pode, em tese, testar
todas as 4 milhões de possibilidades em tempo viável (~12 dias).

**3.2. Dependência da qualidade da fonte.** A KDF não aumenta a entropia intrínseca:
se dois indivíduos compartilham ~50% dos alelos (parentes próximos), suas chaves
derivadas são distintas, mas a redução do espaço de busca permanece proporcional
à entropia original. Ataques de "vizinhança genética" — tentativa de derivar chaves
a partir de perfis de familiares — são teoricamente viáveis se o atacante tiver
acesso a amostras biológicas de parentescidade próxima.

## 4. Recomendação: Fator Secreto Adicional

Para aplicações que exigem >128 bits de segurança, recomendamos adotar o modelo
*híbrido*: perfil genético + salt secreto (senha/PIN). Neste esquema:

- O perfil genético fornece "identificação vinculante" (somente portador autorizado)
- O salt secreto adiciona entropia suplementar (ex.: senha de 8 dígitos = ~26 bits;
  12 dígitos = ~40 bits)
- A combinação resulta em entropia total: 22 bits (STR) + 40 bits (senha) = 62 bits,
  ainda abaixo de 128, mas significativamente mais resistente

Esta abordagem é coerente com protocolos existentes de biometria criptográfica,
como o **Fuzzy Vault** (Juels & Sudan, 2006) e **BioHashing** (Teoh et al., 2004),
que também combinam características biométricas públicas com fatores secretos.

## 5. Perspectivas Futuras

Duas direções ampliam a viabilidade criptográfica:

**5.1. Ampliação do painel genético.** Kits comerciais modernos (GlobalFiler,
PowerPlex Fusion) analisam 24+ loci STR, aumentando a entropia proporcionalmente.
Adição de SNPs (milhares de posições polimórficas) elevaria exponencialmente o
espaço de perfis possíveis.

**5.2. Integração com protocolos existentes.** A canalização proposta pode ser
substituída por esquemas de *secure sketch* ou *fuzzy extractor* (Dodis et al., 2008),
que toleram variações ruidosas na biometria enquanto mantêm propriedades criptográficas.

## 6. Conclusão

A presente pesquisa estabelece a viabilidade técnica de transformar perfil STR em
chave criptográfica utilizável, validando estatisticamente que as chaves derivadas
possuem comportamento de aleatoriedade ideal (uniformidade, equilíbrio de bits,
avalanche effect). Contudo, reconhece-se explicitamente que a entropia genética
isolada não atinge o patamar de segurança moderna — recomendando-se fator adicional
em aplicações críticas. Este trabalho representa contribuição metodológica para
a intersecção entre genética forense e criptografia aplicada.