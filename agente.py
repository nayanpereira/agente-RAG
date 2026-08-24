import os
import warnings
import logging

# Suprime avisos de bibliotecas para um terminal limpo
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Carrega a chave do arquivo .env
load_dotenv()

def iniciar_agente():
    print("[*] Conectando ao Banco Vetorial...")
    # Mesmo modelo de embedding usado no indexador.py — precisa ser idêntico
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
    banco = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

    # MMR para garantir diversidade e não ficar preso só em documentos repetidos (ex: FAQ)
    retriever = banco.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 10,           # Quantos documentos entregar para o LLM
            "fetch_k": 30,     # Quantos documentos buscar no banco antes de filtrar
            "lambda_mult": 0.5 # 0.5 equilibra relevância e diversidade
        }
    )

    print("[*] Inicializando LLM...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Você é o assistente virtual do Mercado Central 24h.\n"
         "Responda EXCLUSIVAMENTE com base no contexto abaixo. Não use conhecimento externo.\n"
         "Se a resposta não estiver literalmente no contexto, diga: 'Não encontrei essa informação nos documentos.'\n\n"
         "Contexto:\n{context}"),
        ("human", "{input}")
    ])

    def formatar_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Sintaxe moderna (LCEL) garantida
    rag_chain = (
        {"context": retriever | formatar_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain, retriever

# Oculta mensagens extensas de log da API do Google no terminal
logging.getLogger("google_genai").setLevel(logging.ERROR)

if __name__ == "__main__":
    agente, retriever = iniciar_agente()

    print("\n" + "="*50)
    print("🚀 Agente Mercado Central 24h - ONLINE")
    print("="*50)

    pergunta = "Como funciona o pagamento de horas extras em feriados?"
    print(f"\n[Usuário]: {pergunta}\n\nProcessando...")

    try:
        resposta = agente.invoke(pergunta)
        print(f"\n[Agente]: {resposta}")

        print("\n[!] Fontes Consultadas:")
        for doc in retriever.invoke(pergunta):
            origem = doc.metadata.get('source', 'Desconhecida')
            pagina = doc.metadata.get('page', 'N/A')
            print(f"  - {origem} (Página {pagina})")

    except Exception as e:
        print(f"\n[ERRO CRÍTICO NA API DO GOOGLE]")
        print(f"Detalhe técnico: {e}")