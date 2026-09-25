FROM python:3.12-slim

# Evita buffering de saída (logs em tempo real)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependências primeiro (aproveita cache de camadas do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Resto do projeto
COPY . .

# Usuário não-root (boa prática)
RUN useradd --create-home researcher && chown -R researcher:researcher /app
USER researcher

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
