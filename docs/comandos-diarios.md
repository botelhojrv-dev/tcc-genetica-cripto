# Comandos Diários — Projeto TCC Genética + Criptografia

Guia de rotina para iniciar, trabalhar e finalizar sessões de desenvolvimento.

---

## 🟢 INICIAR UMA SESSÃO

### 1. Abrir o terminal e acessar o projeto

```bash
cd ~/Projetos/tcc-genetica-cripto
2. Ativar o ambiente virtual (obrigatório para cada sessão nova)
source .venv/bin/activate

    Nota: o prompt muda para (.venv) ricardo@.... Se não mudar, repita o comando.

3. Escolher o modo de trabalho
Modo	Comando	Quando usar
JupyterLab	make notebook	Trabalhar em notebooks, análise interativa
Shell direto	.venv/bin/python src/modulo.py	Rodar scripts prontos
Testes	make test	Após alterar código em src/
🔴 FINALIZAR UMA SESSÃO
1. Parar o servidor Jupyter (se estiver rodando)

No terminal onde o make notebook foi iniciado:
# Pressione Ctrl + C
# Quando perguntar: "Shutdown all kernels? [y/N]" → digite y e Enter
2. Registrar mudanças no Git
git add .
git commit -m "Descreva brevemente o que foi feito"

    Exemplos de mensagens válidas:

        "Adiciona módulo de entropia com testes"
        "Notebook 02: derivação de chave via Argon2"
        "Corrige bug na representação canônica"

3. Desativar o ambiente (opcional)
deactivate
🔧 COMANDOS ÚTEIS DO MAKEFILE
Comando	O que faz
make setup	Cria .venv/ e instala dependências (rodar APENAS na primeira vez)
make notebook	Inicia JupyterLab em http://localhost:8888
make test	Executa a suíte de testes do pytest
make lint	Formata código com Black
make docker	Builda e sobe o ambiente Docker
make clean	Remove caches temporários
🧰 CHECKLIST DE TROUBLESHOOTING RÁPIDO
Sintoma	Provável causa	Solução
ModuleNotFoundError: src	Ambiente não ativado ou Jupyter rodando fora da pasta	Ative .venv/bin/activate e rode make notebook na raiz
IndentationError	Mistura de TAB com espaços	No VS Code, configure "Indent Using Spaces" = 4
Permission denied ao rodar Docker	Usuário sem grupo docker	sudo usermod -aG docker $USER, reinicie sessão
pip: no such option: ---	Linhas decorativas copiadas acidentalmente	Verifique que requirements.txt só tem nomes de pacotes
Failed to resolve 'files.pythonhosted.org'	DNS caiu	Troque para 1.1.1.1, 8.8.8.8 nas configurações de rede
Jupyter não abre navegador	Firewall ou política local	Copie o link http://localhost:8888/?token=... manualmente
📁 ESTRUTURA DO PROJETO — LEITURA RÁPIDA
Pasta/Arquivo	Conteúdo
data/raw/	Dados brutos — NUNCA editar e NUNCA submeter ao Git
notebooks/	Cadernos Jupyter de exploração numerados (01_, 02_)
src/	Módulos Python estáveis (código de produção da tese)
tests/	Testes automatizados com pytest
results/figures/	Gráficos gerados (prontos para artigo)
docs/	Documentação formal, metodologias, fluxogramas
requirements.txt	Dependências pinadas para reprodutibilidade
Makefile	Atalhos de comandos centralizados
Dockerfile + docker-compose.yml	Ambiente reproduzível em qualquer máquina
🔄 FLUXO IDEAL DURANTE UMA SESSÃO
1. cd ~/Projetos/tcc-genetica-cripto
2. source .venv/bin/activate
3. make notebook (ou make test, ou editar código)
   ...trabalho...
4. make test (após qualquer alteração em src/)
5. Ctrl+C para parar Jupyter (se tiver usado)
6. git add .
7. git commit -m "mensagem descritiva"
🛡️ REGRAS DE OURO

    NUNCA altere dados em data/raw/ — eles são imutáveis
    NUNCA faça commit de arquivos grandes de dados genéticos reais
    Sempre ative o ambiente antes de rodar scripts
    Sempre commit com mensagem descritiva (evite "fix", "update")
    Mantenha testes passando (make test deve sair 4/4 verdes)
    Use small commits — melhor 5 commits focados que 1 gigante

    Versão do documento: 1.0
    Última atualização: Setembro 2026
    Mantido por: Ricardo
