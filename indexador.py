import os
# Desativa avisos de paralelismo da biblioteca tokenizers para manter o terminal limpo
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from processador_pdf import processar_base_conhecimento

def criar_banco_vetorial():
    print("\n[*] --- ETAPA DE INDEXAÇÃO VETORIAL ---")

    # 1. Puxa os chunks gerados a partir dos PDFs
    chunks = processar_base_conhecimento()

    # 2. Configura o modelo de Embeddings (multilíngue, com bom suporte a PT-BR)
    print("\n[*] Carregando modelo de Embeddings (isso pode levar alguns segundos na primeira vez)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

    # 3. Define onde o banco de dados será salvo no seu projeto
    pasta_banco = "./chroma_db"
    print(f"[*] Transformando texto em vetores e salvando no banco em: {pasta_banco}")

    # 4. Cria e persiste o banco vetorial
    banco_vetorial = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=pasta_banco
    )

    print("[*] SUCESSO: Banco Vetorial criado! O agente agora tem uma 'memória' pesquisável.")
    return banco_vetorial

if __name__ == "__main__":
    criar_banco_vetorial()