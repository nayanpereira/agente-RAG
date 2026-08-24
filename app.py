import streamlit as st
from agente import iniciar_agente

# 1. Configuração inicial da página
st.set_page_config(page_title="Agente IA - Mercado Central", page_icon="🛒", layout="centered")

st.title("🛒 Agente Corporativo - Mercado Central 24h")
st.markdown("Bem-vindo! Faça sua pergunta sobre políticas, regulamentos ou DRE da empresa.")

# 2. Carregamento do Agente (usando cache do Streamlit para não recarregar a cada mensagem)
if "agente" not in st.session_state:
    with st.spinner("Inicializando motor de IA e carregando documentos..."):
        agente, retriever = iniciar_agente()
        st.session_state.agente = agente
        st.session_state.retriever = retriever
        st.session_state.mensagens = []

# 3. Exibição do histórico de mensagens na tela
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Se a mensagem for do agente e tiver fontes, exibe um expansor
        if "fontes" in msg and msg["fontes"]:
            with st.expander("🔍 Fontes Consultadas"):
                for fonte in msg["fontes"]:
                    st.write(fonte)

# 4. Campo de entrada para a pergunta do usuário
pergunta_usuario = st.chat_input("Ex: Como funciona o reembolso de despesas?")

if pergunta_usuario:
    # Mostra a pergunta do usuário na tela e salva no histórico
    with st.chat_message("user"):
        st.markdown(pergunta_usuario)
    st.session_state.mensagens.append({"role": "user", "content": pergunta_usuario})

    # Mostra a resposta do assistente
    with st.chat_message("assistant"):
        with st.spinner("Consultando a base de conhecimento..."):
            # Chama o LLM
            resposta = st.session_state.agente.invoke(pergunta_usuario)
            documentos = st.session_state.retriever.invoke(pergunta_usuario)
            
            # Imprime a resposta
            st.markdown(resposta)
            
            # Formata e exibe as fontes
            fontes_formatadas = []
            with st.expander("🔍 Fontes Consultadas"):
                for doc in documentos:
                    origem = doc.metadata.get('source', 'Desconhecida')
                    pagina = doc.metadata.get('page', 'N/A')
                    texto_fonte = f"- {origem} (Página {pagina})"
                    st.write(texto_fonte)
                    fontes_formatadas.append(texto_fonte)

    # Salva a resposta do assistente no histórico
    st.session_state.mensagens.append({
        "role": "assistant",
        "content": resposta,
        "fontes": fontes_formatadas
    })