.PHONY: setup notebook test lint docker clean help

# Cria ambiente virtual e instala dependências
setup:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	@echo "✓ Ambiente pronto. Ativar com: source .venv/bin/activate"

# Sobe o JupyterLab local
notebook:
	.venv/bin/jupyter lab

# Roda os testes
test:
	.venv/bin/pytest tests/ -v

# Formata o código
lint:
	.venv/bin/black src/ tests/

# Docker
docker:
	docker compose build
	docker compose up -d jupyter
	@echo "✓ JupyterLab em http://localhost:8888"

# Limpeza
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .ipynb_checkpoints

help:
	@echo "Comandos disponíveis:"
	@echo "  make setup    - cria ambiente virtual e instala dependências"
	@echo "  make notebook - sobe o JupyterLab"
	@echo "  make test     - executa a suíte de testes"
	@echo "  make lint     - formata código com black"
	@echo "  make docker   - build e sobe ambiente Docker"
	@echo "  make clean    - limpa caches temporários"
	