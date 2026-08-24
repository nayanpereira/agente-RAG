# 🛒 Agente Inteligente - Mercado Central 24h

Este projeto consiste em um assistente virtual corporativo baseado em Inteligência Artificial (RAG - Retrieval-Augmented Generation). O agente é capaz de responder dúvidas de funcionários e gestores com base em documentos internos da empresa (manuais, FAQs, políticas de atendimento e balanços financeiros), garantindo respostas precisas e sem alucinações.

---

## 📸 Sistema em Funcionamento

Abaixo está a interface web do agente rodando localmente e integrada ao modelo de linguagem:

![Funcionamento do Sistema](./imagem/funcionamento.png)

---

## 🛠️ O Que Foi Criado (Estrutura do Projeto)

O projeto foi estruturado em módulos para separar a ingestão de dados, o processamento de IA e a interface de usuário:

* **`processador_pdf.py`**: Responsável por ler os documentos em PDF da pasta base, fatiá-los em pedaços menores (*chunks*) e prepará-los para a vetorização.
* **`indexador.py`**: Converte os textos fatiados em vetores matemáticos usando embeddings e os armazena no banco de dados vetorial local.
* **`agente.py`**: Contém o motor principal do agente, configurando a busca semântica avançada (com MMR para diversidade de fontes), o *prompt* do sistema e a conexão com o modelo **Google Gemini (Gemini 2.5 Flash)** via LangChain.
* **`app.py`**: Constrói a interface de chat interativa e amigável utilizando **Streamlit**.
* **`requirements.txt`**: Lista com todas as bibliotecas Python necessárias para rodar o projeto (LangChain, ChromaDB, Streamlit, etc.).
* **`Dockerfile` & `.dockerignore`**: Arquivos de configuração para empacotar toda a aplicação em um container isolado.
* **`.env`**: Arquivo seguro para armazenar variáveis de ambiente, como a chave de API do Google (não versionado no Git).

---

## 🚀 Como Executar o Projeto Localmente

1. **Clone o repositório e acesse a pasta:**
   ```bash
   git clone <seu-repositorio>
   cd <sua-pasta>


## 2. Criar e Ativar o Ambiente Virtual (venv)

É altamente recomendável isolar as dependências do projeto usando um ambiente virtual:

**No Windows (CMD ou PowerShell):**

```bash
python -m venv venv
venv\Scripts\activate
```

**No Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Instalar as Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias listadas no projeto:

```bash
pip install -r requirements.txt
```

## 4. Configurar as Variáveis de Ambiente (.env)

Na raiz do projeto, crie um arquivo chamado `.env` e adicione a sua chave da API do Google:

```
GOOGLE_API_KEY=sua_chave_aqui_sem_aspas
```

## 5. Indexar a Base de Conhecimento

Certifique-se de que a pasta contendo os seus arquivos PDF (documentos base) está configurada no projeto. Em seguida, execute o script de indexação para gerar o banco vetorial local:

```bash
python indexador.py
```

## 6. Iniciar a Aplicação Web

Com o banco vetorial pronto, inicie o servidor local do Streamlit:

```bash
streamlit run app.py
```

O navegador abrirá automaticamente a interface do chat em: `http://localhost:8501`

---

## 🐳 Containerização com Docker

Se preferir rodar a aplicação isolada em um container (sem precisar gerenciar versões do Python na máquina local):

**1. Construir a imagem Docker:**

```bash
docker build -t agente-mercado-central .
```

**2. Executar o container (injetando o arquivo `.env` para segurança):**

```bash
docker run -p 8501:8501 --env-file .env agente-mercado-central
```

Acesse a aplicação no navegador em: `http://localhost:8501`
