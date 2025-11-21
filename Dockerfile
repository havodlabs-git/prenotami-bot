# Usar imagem base Python com Chromium
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do bot
COPY prenotami_bot.py .
COPY discord_bot.py .
COPY cli.py .
COPY monitor.py .

# Criar diretório para arquivos temporários
RUN mkdir -p /app/data

# Definir variáveis de ambiente padrão
ENV PYTHONUNBUFFERED=1
ENV HEADLESS_MODE=true

# Comando para iniciar o bot Discord
CMD ["python", "discord_bot.py"]
