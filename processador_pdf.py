import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def processar_base_conhecimento(diretorio_base="./documentos_base"):
    print(f"[*] Iniciando leitura unificada dos PDFs na pasta: {diretorio_base}")
    
    if not os.path.exists(diretorio_base):
        raise FileNotFoundError("[Erro] A pasta de documentos não foi encontrada.")

    # Extração padronizada de todos os PDFs
    loader = PyPDFDirectoryLoader(diretorio_base)
    documentos = loader.load()
    print(f"[*] {len(documentos)} páginas carregadas com sucesso.")

    # Chunking: Fatiamento preservando o contexto
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " "]
    )
    
    chunks = text_splitter.split_documents(documentos)
    print(f"[*] Base dividida em {len(chunks)} blocos vetoriais prontos para indexação.")
    
    # Validação visual do primeiro chunk
    if chunks:
        print("\n--- Validação do Primeiro Chunk ---")
        print(f"Conteúdo Inicial: {chunks[0].page_content[:200]}...")
        print("-----------------------------------")
        
    return chunks

if __name__ == "__main__":
    chunks_finais = processar_base_conhecimento()
