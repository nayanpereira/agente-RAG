# 1. Usa uma imagem oficial do Python (versão leve)
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Atualiza o sistema e instala dependências básicas do SO
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# 4. Copia apenas o arquivo de dependências primeiro (otimiza o cache do Docker)
COPY requirements.txt .

# 5. Instala as bibliotecas do Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia todo o resto do seu código (e a pasta chroma_db) para dentro do container
COPY . .

# 7. Expõe a porta padrão que o Streamlit usa
EXPOSE 8501

# 8. Comando para iniciar o Streamlit quando o container subir
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]