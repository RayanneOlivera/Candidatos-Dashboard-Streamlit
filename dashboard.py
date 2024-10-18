import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Consulta de Candidatos 2024", layout="wide")

csv_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
if csv_file is not None:
    df = pd.read_csv(csv_file, sep=';', encoding='latin1')
else:
    df = pd.read_csv('consulta_cand_2024_CE.csv', sep=';', encoding='latin1')

if 'nm_ue' not in st.session_state:
    st.session_state.nm_ue = None
if 'cargo' not in st.session_state:
    st.session_state.cargo = None

st.sidebar.title('Candidatos')

menu_opcao = st.sidebar.radio("Selecione a página:", ["main page", "page 2"])

if menu_opcao == "main page":
    st.sidebar.header("Filtros")
    nm_ue = st.sidebar.selectbox("Selecione uma Unidade Eleitoral (NM_UE)", [''] + list(df['NM_UE'].unique()), index=0)
    cargo = st.sidebar.selectbox("Selecione um Cargo (DS_CARGO)", [''] + list(df['DS_CARGO'].unique()), index=0)
    
    if st.sidebar.button('Limpar Filtros'):
        st.session_state.nm_ue = None
        st.session_state.cargo = None
        nm_ue = ''
        cargo = ''

    filtered_df = df
    if nm_ue:
        filtered_df = filtered_df[filtered_df['NM_UE'] == nm_ue]
    if cargo:
        filtered_df = filtered_df[filtered_df['DS_CARGO'] == cargo]

    st.title('Prévia dos dados')
    st.write(filtered_df.head())

    st.title('Distribuição do Grau de Instrução')
    fig, ax = plt.subplots()
    filtered_df['DS_GRAU_INSTRUCAO'].value_counts().plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title("Distribuição do Grau de Instrução")
    ax.set_xlabel("Grau de Instrução")
    ax.set_ylabel("Contagem")
    st.pyplot(fig)

    st.title('Relação entre Gênero e Grau de Instrução')
    fig, ax = plt.subplots()
    filtered_df.groupby('DS_GRAU_INSTRUCAO')['DS_GENERO'].value_counts().unstack().plot(kind='bar', stacked=True, ax=ax)
    ax.set_title("Relação entre Gênero e Grau de Instrução")
    ax.set_xlabel("Grau de Instrução")
    ax.set_ylabel("Número de Candidatos")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.title('Distribuição da Cor/Raça dos Candidatos')
    fig, ax = plt.subplots()
    filtered_df['DS_COR_RACA'].value_counts().plot(kind='pie', ax=ax, autopct='%4.1f%%', colors=['#4A90E2', '#003366', '#8CC7FF', '#D9ECFF'])
    ax.set_ylabel("")

    ax.set_title("Distribuição da Cor/Raça")
    st.pyplot(fig)

    st.title('Distribuição de Gênero dos Candidatos')
    fig, ax = plt.subplots()
    filtered_df['DS_GENERO'].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=['#4A90E2', '#003366'])
    ax.set_ylabel("")
    ax.set_title("Distribuição de Gênero")
    st.pyplot(fig)

elif menu_opcao == "page 2":
    st.title("Página 2 - Informações Adicionais")
    st.write("Conteúdo da página 2 pode ser adicionado aqui.")
