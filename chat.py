import streamlit as st
import sqlite3
import datetime

st.set_page_config(page_title="Chat Público SQL", page_icon="💬")
st.title("💬 Chat Público Persistente")

# Configuração/Conexão com o Banco de Dados SQLite
def inicializar_db():
    conn = sqlite3.connect("chat_publico.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            texto TEXT,
            hora TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_mensagem(usuario, texto, hora):
    conn = sqlite3.connect("chat_publico.db")
    c = conn.cursor()
    c.execute("INSERT INTO mensagens (usuario, texto, hora) VALUES (?, ?, ?)", (usuario, texto, hora))
    conn.commit()
    conn.close()

def apagar_mensagens():
    conn = sqlite3.connect("chat_publico.db")
    c = conn.cursor()
    c.execute("DELETE FROM mensagens WHERE 1=1")
    conn.commit()
    conn.close()
    buscar_mensagens()

def buscar_mensagens():
    conn = sqlite3.connect("chat_publico.db")
    c = conn.cursor()
    c.execute("SELECT usuario, texto, hora FROM mensagens ORDER BY id ASC")
    dados = c.fetchall()
    conn.close()
    return dados

# Inicializa o banco de dados
inicializar_db()
#@st.fragment(run_every=5)
# Fluxo de Usuário
if "nome_usuario" not in st.session_state:
    st.subheader("Escolha seu apelido para entrar:")
    nome = st.text_input("Apelido:")
    if st.button("Entrar no Chat"):
        if nome.strip():
            st.session_state.nome_usuario = nome.strip()
            st.rerun()
else:
    st.sidebar.markdown(f"Usuário: **{st.session_state.nome_usuario}**")
    if st.session_state.nome_usuario == 'Apiano':
        if st.sidebar.button("Apagar Mensagens ❌​"):
            apagar_mensagens()
        
    if st.sidebar.button("Atualizar Mensagens 🔄"):
        st.rerun()

    # Renderiza mensagens do banco de dados
    mensagens = buscar_mensagens()
    for msg in mensagens:
        usuario, texto, hora = msg
        with st.chat_message("user"):
            st.markdown(f"**{usuario}** <small style='color: gray;'>({hora})</small>", unsafe_allow_html=True)
            st.markdown(texto)

    # Input de nova mensagem
    if prompt := st.chat_input("Envie uma mensagem para todos..."):
        hora_atual = datetime.datetime.now().strftime("%H:%M:%S")
        salvar_mensagem(st.session_state.nome_usuario, prompt, hora_atual)
        st.rerun()